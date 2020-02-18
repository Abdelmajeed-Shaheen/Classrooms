from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Classroom , Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm
from django.contrib.auth import login, authenticate, logout

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	student = Student.objects.filter(classroom=classroom).order_by('name','-exam_grade')
	context = {
		"classroom": classroom,
		"students":student
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_authenticated:
		user_obj = request.user
		form = ClassroomForm()
		if request.method == "POST":
			form = ClassroomForm(request.POST, request.FILES or None)
			if form.is_valid():
				class_obj=form.save(commit=False)
				class_obj.teacher=user_obj
				class_obj.save()
				messages.success(request, "Successfully Created!")
				return redirect('classroom-list')
			print (form.errors)
		context = {
		"form": form,
		}
		return render(request, 'create_classroom.html', context)
	else:
		return redirect('signin')


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		form = ClassroomForm(instance=classroom)
		if request.method == "POST":
			form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('classroom-list')
			print (form.errors)
		context = {
		"form": form,
		"classroom": classroom,
		}
		return render(request, 'update_classroom.html', context)
	else:
		return redirect('signin')

def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id = classroom_id)
	if request.user == classroom.teacher:
		Classroom.objects.get(id=classroom_id).delete()
		messages.success(request, "Successfully Deleted!")
		return redirect('classroom-list')
	else:
		return redirect('signin')


def student_create(request, classroom_id):
	classroom = Classroom.objects.get(id = classroom_id)
	if request.user == classroom.teacher:
		form = StudentForm()
		if request.method == "POST":
			form = StudentForm(request.POST, request.FILES)
			if form.is_valid():
				student_obj=form.save(commit=False)
				student_obj.classroom=classroom
				student_obj.save()
				messages.success(request, "Successfully Created!")
				return redirect('classroom-detail',classroom_id)
		context = {
		"form": form,
		"classroom":classroom
		}
		return render(request, 'studentcreate.html', context)
	else:
		return redirect('signin')


def student_update(request, student_id , classroom_id):
	classroom = Classroom.objects.get(id = classroom_id)
	student = Student.objects.get(id=student_id)
	if request.user == classroom.teacher:
		form = StudentForm(instance=student)
		if request.method == "POST":
			form = StudentForm(request.POST, request.FILES , instance=student)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('classroom-list')
		context = {
		"form": form,
		"classroom": classroom,
		"student":student
		}
		return render(request, 'studentupdate.html', context)
	else:
		return redirect('signin')

def student_delete(request, student_id , classroom_id):
	classroom = Classroom.objects.get(id = classroom_id)
	if request.user == classroom.teacher:
		Student.objects.get(id=student_id).delete()
		messages.success(request, "Successfully Deleted!")
		return redirect('classroom-list')
	else:
		return redirect('signin')



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")
