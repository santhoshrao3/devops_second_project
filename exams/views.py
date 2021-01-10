from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Questions, Extendedusers, Quiz, Answers
import requests, json
from django.core.paginator import (Paginator,
EmptyPage, PageNotAnInteger)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from dateutil import parser
from django.contrib import messages


# Show Quiz View
@login_required(login_url="/accounts/login")
def show_quiz(request):
	user = Extendedusers.objects.get(user=request.user)
	# If the user is school, show its' quizes
	if user.is_school:
		data = Quiz.objects.filter(
			user_id=request.user.id).order_by('-pub_date')
		is_school = True
		page = request.GET.get('page', 1)
		# total elements allowed on one page
		total_page_count = 5
		quiz_list = paginate(request, page, data, total_page_count)
		return render(request, 'exams/show_quiz.html',{
		'is_school': is_school, 'data': quiz_list})
	# If user is student then show available schools
	else:
		# If a user is a student, show the list of schools
		is_school = False
		data = Extendedusers.objects.filter(
			is_school=True).order_by('school_name')
		page = request.GET.get('page', 1)
		# total elements allowed on one page
		total_page_count = 5
		school_list = paginate(request, page, data, total_page_count)
		return render(request, 'exams/show_schools.html',{
		'data': school_list})

# Make a new quiz entry in DB
@login_required(login_url="/accounts/login")
def create_quiz(request):
	if request.method == 'POST':
		quiz_title = request.POST.get('quiz_title')
		user = Extendedusers.objects.get(user=request.user.id)
		if user.is_school:
			quiz = Quiz.objects.create(quiz_title=quiz_title,
			user=user, pub_date=datetime.now())
			# call the API via get_questions method
			status = get_questions(request, quiz)
			if status:
				msg = 'Quiz Created successfully!'
				data = Quiz.objects.filter(
					user_id=request.user.id).order_by('-pub_date')
				# sends msg on redirect
				messages.success(request, msg)
				return redirect('show_quiz')
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
	data = Quiz.objects.filter(user_id=id).order_by('-pub_date')
	page = request.GET.get('page', 1)
	# total elements allowed on one page
	total_page_count = 5
	quiz_list = paginate(request, page, data, total_page_count)
	return render(request, 'exams/show_quiz.html',{'data': quiz_list})

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
	pub_date = request.GET.get('pub_date')
	date = parser.parse(pub_date)
	# pub_date = datetime.strptime(pub_date, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
	print('line 93: ', date)
	quiz = Quiz.objects.create(user_id=request.user.id,
	pub_date=date, start_time=timezone.datetime.now())
	return render(request, 'exams/begin_quiz.html', {'id':id,
	'date':quiz.pub_date})

# Load the quiz page and paginate
@login_required(login_url="/accounts/login")
def quiz(request):
	quiz_id = request.GET.get('id')
	questions = Questions.objects.filter(quiz_id=quiz_id)
	page = request.GET.get('page', 1)
	print('line 97: ', page)
	pub_date = request.GET.get('pub_date')
	print('line 109.............', pub_date)
	# total elements allowed on one page
	total_page_count = 1
	question = paginate(request, page, questions, total_page_count)
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
	'data': question, 'id':quiz_id,'is_submitted':is_submitted,
	'pub_date':pub_date})

# Paginate the questions
def paginate(request, page, questions, total_page_count):
	paginator = Paginator(questions, total_page_count)
	try:
		elements = paginator.page(page)
		return elements
	except PageNotAnInteger:
		elements = paginator.page(1)
		return elements
	except EmptyPage:
		elements = paginator.page(paginator.num_pages)
		return elements

'''
 Get the results on test end 
 and show the time taken in readble format.
 If a user has left the quiz in middle then the Quiz filter condition last()
 will allow us to fetch the rescent entery for start time.
'''
@login_required(login_url="/accounts/login")
def get_results(request):
	quiz_id = request.GET.get('quiz_id')
	pub_date = request.GET.get('pub_date')
	score = 0
	date = parser.parse(pub_date)
	quiz = Quiz.objects.filter(user=request.user.id, pub_date=date).last()
	total_time_taken = quiz_time_taken(quiz.start_time)
	questions = Questions.objects.filter(quiz_id=quiz_id)
	for que in questions:
		answer = Answers.objects.get(user_key_id=request.user.id,
		question_key=que.id)
		is_correct = check_answer(answer.user_answer, que.is_correct)
		if is_correct:
			score += 1
	return render(request, 'exams/results.html', {'score':score,
	'time_taken':total_time_taken})
			
# Check if the answer is correct
def check_answer(selected_option, cor_ans):
	if cor_ans == selected_option:
		return True
	else:
		return False

# Calculate total time taken to solve the quiz
def quiz_time_taken(start_time):
	now = datetime.now(timezone.utc)
	time_taken = now - start_time
	hours, remainder = divmod(time_taken.total_seconds(), 3600)
	minutes, seconds = divmod(remainder, 60)
	total_time_taken = str(hours) + ' Hrs ' + str(minutes) + ' Minutes'
	return total_time_taken