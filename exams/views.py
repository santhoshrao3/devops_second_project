from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Questions, Extendedusers, Quiz, Answers
import requests, json, random
from django.core.paginator import (Paginator,
EmptyPage, PageNotAnInteger)
from django.contrib.auth.decorators import login_required


# Make a new quiz entry in DB
@login_required(login_url="/accounts/login")
def create_quiz(request):
	if request.method == 'POST':
		quiz_title = request.POST.get('quiz_title')
		user = Extendedusers.objects.get(user=request.user.id)
		if user.is_school:
			quiz = Quiz.objects.create(quiz_title=quiz_title,
			user_school=user)
			# call the API via get_questions method
			status = get_questions(request, quiz)
			if status:
				return render(request, 'accounts/show_quiz.html', 
				{'is_school': True})
			else:
				error = 'Something went wrong. Please try again later.'
				return render(request, 'exams/create_quiz.html',
				{'error':error})
		else:
			return HttpResponse('Insufficient Previleges.')
	else:
		return render(request, 'exams/create_quiz.html')

# Call the API to fetch questions
@login_required(login_url="/accounts/login")
def get_questions(request, quiz):
	try:
		api_uri = str('https://opentdb.com/api.php?amount=10&type=multiple')
		api_data = requests.get(api_uri)
		api_data = api_data.content
		api_data = json.loads(api_data)
		for data in api_data['results']:
			question = data['question']
			correct_ans = data['correct_answer']
			quiz_obj = Quiz.objects.get(id=quiz.id)
			options = []
			i = 0
			for option in data['incorrect_answers']:
				options.append(option)
				i += 1
			Questions.objects.create(quiz=quiz_obj, question=question,
				is_correct=correct_ans, option1=options[0],
				option2=options[1], option3=options[2])
		return True
	except Exception as e:
		return False

# Show Quizes of a particular school
@login_required(login_url="/accounts/login")
def school(request, id):
	data = Quiz.objects.filter(user_school_id=id)
	return render(request, 'accounts/show_quiz.html',{'data': data})

# TODO serve an AJAX POST request and save the ans in DB
@login_required(login_url="/accounts/login")
def submit_answer(request):
	question_id = request.GET.get('que_id')
	user_ans = request.GET.get('selected_option')
	user = Extendedusers.objects.get(user=request.user.id)
	response = {}
	try:
		answer = Answers.objects.get(user_key=user, 
		question_key=question_id, is_submitted=True)
		answer.user_answer = user_ans
		answer.save()
		response['status'] = True
	except Exception as e:
		Answers.objects.create(user_key=user, question_key=question_id,
		user_answer=user_ans, is_submitted=True)
		response['status'] = False
	return HttpResponse(json.dumps(response))

# Get confirmation to begin quiz
@login_required(login_url="/accounts/login")
def begin_quiz(request, id):
	return render(request, 'exams/begin_quiz.html', {'id':id})

# Load the quiz page and paginate
@login_required(login_url="/accounts/login")
def quiz(request):
	quiz_id = request.GET.get('id')
	questions = Questions.objects.filter(quiz_id=quiz_id)
	page = request.GET.get('page', 1)
	print('line 97: ', page)
	question = paginate(request, page, questions)
	for i in question:
		que_id = i.id
	answers = Answers.objects.filter(user_key_id=request.user.id,
	question_key=que_id).last()

	try:
		if answers.is_submitted:
			is_submitted = True
	except Exception as e:
		is_submitted = False

	return render(request, 'exams/quiz.html', {'questions':questions,
	'data': question, 'id':quiz_id,'is_submitted':is_submitted})

# Paginate the questions
def paginate(request, page, questions):
	paginator = Paginator(questions, 1)
	try:
		question = paginator.page(page)
		return question
	except PageNotAnInteger:
		question = paginator.page(1)
		return question
	except EmptyPage:
		question = paginator.page(paginator.num_pages)
		return question

# Get the results on test end
@login_required(login_url="/accounts/login")
def get_results(request):
	quiz_id = request.GET.get('quiz_id')
	score = 0
	questions = Questions.objects.filter(quiz_id=quiz_id)
	for que in questions:
		answer = Answers.objects.get(user_key_id=request.user.id,
		question_key=que.id)
		is_correct = check_answer(answer.user_answer, que.is_correct)
		if is_correct:
			score += 1
	return render(request, 'exams/results.html', {'score':score})
	
			
# Check if the answer is correct
def check_answer(selected_option, cor_ans):
	if cor_ans == selected_option:
		return True
	else:
		return False
