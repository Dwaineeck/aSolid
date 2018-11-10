from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def current_user(request):
	return User.objects.get(id = request.session['user_id'])
def home(request):
	return render(request, 'aSolid_app/home.html')
def log(request):
	return render(request, 'aSolid_app/login.html')
def registration(request):
	return render(request, 'aSolid_app/registration.html')

def login(request):
	if request.method != 'POST':
		return redirect('/log')
	#find user
	user = User.objects.filter(email = request.POST.get('email')).first()
	#Check user credentials
	#add them to session and log in or add error message and route to home page
	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/jobs')
	else: 
		messages.add_message(request, messages.INFO, 'Invalid Email or Password.', extra_tags="login")
		return redirect('/log')
	return redirect('/jobs')

def register(request):
	check = User.objects.validateUser(request.POST)
	if request.method != 'POST':
		return redirect('/registration')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/registration')
	hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
	#create user
	user = User.objects.create(
		first_name = request.POST.get('first_name'),
		last_name = request.POST.get('last_name'),
		email = request.POST.get('email'),	
		password = hashed_pw,
	)
	# add user to session, logging them in
	request.session['user_id'] = user.id
	#route to jobs page
	return redirect('/jobs')



def logout(request):
	request.session.clear()
	return redirect('/')

def edit(request, id):
	job = Job.objects.get(id=id)
	context = {
		'job': job,
	}
	return render(request, 'aSolid_app/edit.html', context)

def jobs(request):
	user = current_user(request)

	context = {
		'user': user,
		'jobs': Job.objects.exclude(add = user),
		'add': user.add.all()
	}

	return render(request, 'aSolid_app/jobs.html', context)

def update(request, id):
	check = Job.objects.validateJobUpdate(request.POST)
	if request.method != 'POST':
		return redirect(f'/users/{id}/edit')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect(f'/users/{id}/edit')
	job = Job.objects.get(id=id)
	job.job = request.POST['job']
	job.description = request.POST['description']
	job.location = request.POST['location']
	job.save()
	return redirect('/jobs')

def create(request):
	if request.method != 'POST':
		return redirect('/')
	##adds item to jobs
	check = Job.objects.validateJob(request.POST)
	if request.method != 'POST':
		return redirect('/jobs')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/jobs')
	if check[0] == True:

		job = Job.objects.create(
			description = request.POST.get('description'),
			poster = current_user(request),
			job = request.POST.get('job'),
			location = request.POST.get('location'),
			)

		return redirect('/jobs')
	return redirect('/jobs')

def add_add(request, id):

	user = current_user(request)
	add = Job.objects.get(id=id)

	user.add.add(add)

	return redirect('/jobs')

def remove_add(request, id):

	user = current_user(request)
	add = Job.objects.get(id=id)

	user.add.remove(add)

	return redirect('/jobs')

def show_user(request, id):
	context = {
		'job': Job.objects.get(id=id),
	}
	return render(request, 'aSolid_app/user.html', context)

def destroy(request, id):
	Job.objects.get(id=id).delete()
	return redirect('/jobs')