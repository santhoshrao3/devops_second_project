from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
from .models import Extendedusers
from exams.models import Quiz, Questions


# Show Quiz View
@login_required(login_url="/accounts/login")
def show_quiz(request):
	user = Extendedusers.objects.get(user=request.user)
	# If the user is school, show its' quizes
	if user.is_school:
		data = Quiz.objects.filter(
			user_id=request.user.id).order_by('-pub_date')
		is_school = True
		return render(request, 'accounts/show_quiz.html',{
		'is_school': is_school, 'data': data})
	else:
		# If a user is a student, show the list of schools
		is_school = False
		data = Extendedusers.objects.filter(is_school=True)
		return render(request, 'exams/show_schools.html',{
		'data': data})
	

# Signup method
def signup(request, cli):
	print('line 12', cli)
	if request.method == 'POST':
		user = Extendedusers()
		email_validation = user.email_validate(request.POST.get('email'))
		if email_validation:
			print('line 17', cli)
			email = request.POST.get('email')
			username = request.POST.get('username')
			password1 = request.POST.get('password1')
			password2 = request.POST.get('password2')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			print('line 24', cli)
			school_name = request.POST.get('school_name')
			print('line 26', cli)
			if username and email and password1 == password2:
				print('line 28', cli)
				try:
					user = User.objects.get(username=username)
					# User already registered
					error = 'User already exists!'
					return render(request, 'accounts/signup.html', {
						'error': error, 'client': cli})
				except User.DoesNotExist:
					print('line 34', cli)
					# register user
					user = User.objects.create_user(username, 
					password=password1)
					if cli == 'student':
						print('line 39', cli)
						user_details = Extendedusers(first_name = first_name,
						last_name = last_name,email = email,user=user)
						user_details.save()
					elif (cli == 'school' and school_name):
						print('line 44', cli)
						user_details = Extendedusers(email = email,
						user=user,school_name=school_name,is_school=True)
						user_details.save()
					# Login user
					auth.login(request, user)
					print('line 50', cli)
					return redirect('show_quiz')
		else:
			print('line 54', cli)
			error = 'Email already in use or not valid!'
			return render(request, 'accounts/signup.html', {
				'error': error, 'client': cli})
	else:
		return render(request, 'accounts/signup.html', {'client': cli})

# Login method
def login(request):
	if request.method == 'POST':
		user = auth.authenticate(username=request.POST.get('username'),
		password=request.POST.get('password'))
		if user is not None:
			auth.login(request, user)
			return redirect('show_quiz')
		else:
			error = 'Username or password is incorrect'
			return render(request, 'accounts/login.html', {
				'error': error})
	else:
		return render(request, 'accounts/login.html')

# Logout method
def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		return redirect('show_quiz')