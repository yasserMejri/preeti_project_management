# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def auth_login(request):

	error = None
	message = None

	if request.GET.get('thankyou') != None:
		message = "Thank you for your registeration !"

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		print username, password

		try:
			user = User.objects.get(username=username)
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('coordinator:home'))
			error = "Password Incorrect"
		except:
			error = "No registered user!"

	return render(request, 'auth/user-login.html', {
		'error': error, 
		'message': message
		})

@login_required
def auth_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('auth:login'))

def auth_register(request):
	error = None
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')

		try:
			user = User.objects.get(username=username)
			error = "User with same name already exists!"
		except:
			try:
				user = User.objects.get(email=email)
				error = "Email already used."
			except:
				error = None
		if error == None:
			user = User(
				username = username,
				email = email
				)
			user.save()
			user.set_password(password)
			user.save()
			return HttpResponseRedirect(reverse('auth:login') + '?thankyou')

	return render(request, 'auth/user-register.html', {
		'error': error
		})
	return HttpResponse('register')

@login_required
def auth_profile(request):
	error = None

	return render(request, 'auth/user-profile.html', {
		'user': request.user,
		'error': error
		})



@login_required
def auth_manage(request):

	error = ""

	if request.method == 'POST':
		print request.POST
		print request.POST.get('user-active')
		try:
			if request.POST.get('action') == 'register':
				user = User(
					username = request.POST.get('username'), 
					email = request.POST.get('email'), 
					is_active = True if request.POST.get('user-active') == 'on' else False
					)
				user.save()
				user.set_password(request.POST.get('pasword'))
				user.save()
			elif request.POST.get('action') == 'update':
				user = User.objects.get(id=int(request.POST.get('user-id')))
				user.username = request.POST.get('username')
				user.email = request.POST.get('email')
				user.is_active = True if request.POST.get('user-active') == 'on' else False
				user.save()
				user.set_password(request.POST.get('password'))
				user.save()
			elif request.POST.get('action') == 'delete':
				user = User.objects.get(id=int(request.POST.get('user-id')))
				user.delete()
		except:
			error = "Something Went Wrong!"

	users = User.objects.all()

	return render(request, 'auth/user-manage.html', {
		'user': request.user, 
		'users': users, 
		'error': error
		})

