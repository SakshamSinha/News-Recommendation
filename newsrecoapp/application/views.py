# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.db import transaction

from application import dbops
from application import forms
from application import models
from application.models import NewsModel

# Create your views here.

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class BrowseView(TemplateView):
	def get(request):
		Latest_news_list=NewsModel.objects.order_by('-title')[:10]
		staticPrefs = models.UserStaticPrefs.objects.get(profileof_user = request.user.id)
		return render(request, 'radhe.html', {'staticPrefs':staticPrefs, 'Latest_news_list': Latest_news_list})

class UserRegView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'userSignup.html', context=None)

	def return_data(request):
		#Add DB operations here
		dbops.UserOperations.register(request.POST['username'], request.POST['email'], request.POST['password'])
		return render(request, 'index.html', context=None)

	def signup(request):
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid() and request.POST['email'] != "":
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password1')
				email =  request.POST['email']

				#Also save to SQLite DB
				dbops.UserOperations.register(username, email, raw_password)

				is_admin = request.POST.get('admin')
				if is_admin is not None:
					user = User.objects.create_superuser(username=username, email=email, password=raw_password)
					userstaticprefs = models.UserStaticPrefs.objects.create(profileof_user=user)
					return redirect('../admin')

				newuser = form.save()
				userstaticprefs = models.UserStaticPrefs.objects.create(profileof_user=newuser)

				user = authenticate(username=username, password=raw_password)
				login(request, user)
				return redirect('../registration/success')
		else:
			form = UserCreationForm()
		return render(request, 'registration/signup.html', {'form': form})

	def success(request):
		return render(request, 'registration/success.html', context=None)

@login_required
@transaction.atomic
def update_profile(request):
	if request.method == 'POST':
		prefs_form = forms.UserStaticPrefsForm(request.POST)
		if prefs_form.is_valid():
			userstaticprefs = prefs_form.save(commit=False)
			userstaticprefs.profileof_user = request.user
			models.UserStaticPrefs.objects.filter(profileof_user = request.user.id).delete()
			userstaticprefs.save()
			return render(request, 'registration/success.html', context=None)
		else:
			messages.error(request, _('Please correct the error below.'))
	else:
		userPrefs = models.UserStaticPrefs.objects.filter(profileof_user = request.user.id).get()
		prefs_form = forms.UserStaticPrefsForm(initial={'economy': userPrefs.economy, 'politics' : userPrefs.politics, 'science' : userPrefs.science, 'arts' : userPrefs.arts, 'sports' : userPrefs.sports, 'misc' : userPrefs.misc})
	return render(request, 'profile.html', {
		'prefs_form': prefs_form
	})