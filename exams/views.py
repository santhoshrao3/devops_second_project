from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Questions, Extendedusers, Quiz, Answers
import requests, json, random
from django.core.paginator import (Paginator,
EmptyPage, PageNotAnInteger)


# Make a new quiz entry in DB
def create_quiz(request):
	print('quiz created')
	if request.method == 'POST':
		quiz_title = request.POST.get('quiz_title')
		print('line 13: ', request.user.id)
		user = Extendedusers.objects.get(user=request.user.id)
		print('line 15 : ', user)
		if user.is_school:
			quiz = Quiz.objects.create(quiz_title=quiz_title,
			user_school=user)
			print('quiz id ', quiz.id)
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
def get_questions(request, quiz):
	try:
		api_uri = str('https://opentdb.com/api.php?amount=10&type=multiple')
		api_data = requests.get(api_uri)
		api_data = api_data.content
		api_data = json.loads(api_data)
		print('line 41')
		for data in api_data['results']:
			question = data['question']
			correct_ans = data['correct_answer']
			print('line 44')
			quiz_obj = Quiz.objects.get(id=quiz.id)
			options = []
			i = 0
			print('line 49')
			for option in data['incorrect_answers']:
				print('line 51 ', option)
				options.append(option)
				i += 1
			print('line 50')
			Questions.objects.create(quiz=quiz_obj, question=question,
				is_correct=correct_ans, option1=options[0],
				option2=options[1], option3=options[2])
			print('line 54')
		return True
	except Exception as e:
		print('line 57', e)
		return False

# Show Quizes of a particular school
def school(request, id):
	data = Quiz.objects.filter(user_school_id=id)
	return render(request, 'accounts/show_quiz.html',{'data': data})

# TODO serve an AJAX POST request and save the ans in DB
def submit_answer(request):
	question_id = request.GET.get('que_id')
	print('line 74',question_id)
	user_ans = request.GET.get('selected_option')
	print('line 76',user_ans)
	user = Extendedusers.objects.get(user=request.user.id)
	question = Questions.objects.get(id=question_id)
	response = {}
	print('line 80',question)
	# breakpoint()
	try:
		Answers.objects.create(user_key=user, 
		question_key=question,user_answer=user_ans)
		response['status'] = True
		print('line 83')
	except Exception as e:
		response['status'] = False
		print(e)
	return JsonResponse(response)

# Get confirmation to begin quiz
def begin_quiz(request, id):
	return render(request, 'exams/begin_quiz.html', {'id':id})

# Load the quiz page and paginate
def quiz(request):
	quiz_id = request.GET.get('id')
	questions = Questions.objects.filter(quiz_id=quiz_id)
	page = request.GET.get('page', 1)
	print('line 97: ', page)
	# selected_option = request.GET.get('option')
	# print('line 76: ', selected_option)
	# score = request.GET.get('score')
	# print('score line 77: ', score)
	question = paginate(request, page, questions)
	# res = check_answer(selected_option, question)
	# if not score:
	# 	score = 0
	# print('line 84: ', res)

	# score = int(score) + 1
	# print('line 93: ', score)

	return render(request, 'exams/quiz.html', {'questions':questions,
	'data': question, 'id':quiz_id})

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

	# options = []
	# for data in data:
	# 	options.append(data.option1, data.option2, data.option3,
	# 	data.is_correct)

# Check if the answer is correct
def check_answer(selected_option, question):
	for data in question:
		if data.is_correct == selected_option:
			return True
		else:
			return False
