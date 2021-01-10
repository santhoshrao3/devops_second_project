from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
from .models import Extendedusers
from exams.models import Quiz, Questions


# Signup method
def signup(request, cli):
	if request.method == 'POST':
		user = Extendedusers()
		email_validation = user.email_validate(request.POST.get('email'))
		if email_validation:
			email = request.POST.get('email')
			username = request.POST.get('username')
			password1 = request.POST.get('password1')
			password2 = request.POST.get('password2')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			school_name = request.POST.get('school_name')
			if username and email and password1 == password2:
				try:
					user = User.objects.get(username=username)
					# User already registered
					error = 'User already exists!'
					return render(request, 'accounts/signup.html', {
						'error': error, 'client': cli})
				except User.DoesNotExist:
					# register user
					user = User.objects.create_user(username, 
					password=password1)
					if cli == 'student':
						user_details = Extendedusers(first_name = first_name,
						last_name = last_name,email = email,user=user)
						user_details.save()
					elif (cli == 'school' and school_name):
						user_details = Extendedusers(email = email,
						user=user,school_name=school_name,is_school=True)
						user_details.save()
					# Login user
					auth.login(request, user)
					return redirect('show_quiz')
		else:
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