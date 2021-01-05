from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Questions, Extendedusers, Quiz
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

def quiz(request, id):
	questions = Questions.objects.filter(quiz_id=id)
	page = request.GET.get('page', 1)

	paginator = Paginator(questions, 1)
	try:
		question = paginator.page(page)
	except PageNotAnInteger:
		question = paginator.page(1)
	except EmptyPage:
		question = paginator.page(paginator.num_pages)

	return render(request, 'exams/quiz.html', { 'data': question })
	
	
	# options = []
	# for data in data:
	# 	options.append(data.option1, data.option2, data.option3,
	# 	data.is_correct)
	