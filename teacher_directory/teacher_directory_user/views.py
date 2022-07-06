from audioop import reverse
from gettext import install
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from teacher_directory_user.forms import CreateUserForm,LoginForm,TeacherForm
from teacher_directory_user.models import School,Subject,Teacher
from teacher_directory.utils import get_object_or_none
# Create your views here.

def home(request):
    creation_form = CreateUserForm()
    login_form = LoginForm()
    schools = School.objects.all()
    return render(request,'home.html',locals())

def sign_up(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Registration completed')
        else:
            for i in eval(form.errors.as_json()):
                messages.error(request,eval(form.errors.as_json())[i][0]['message'])
    return redirect(request.META.get('HTTP_REFERER'))

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'{user} login successfully')
        else:
            messages.error(request,'Oops! Account not exist')

    return redirect(request.META.get('HTTP_REFERER'))

def logout_page(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def subjects(request):
    subjects = Subject.objects.all()
    return render(request,'subjects.html',locals())

def teachers(request,*args,**kwargs):
    school = get_object_or_404(School,slug=kwargs.get('slug'))
    teachers = Teacher.objects.all()
    return render(request,'teachers.html',locals())
    
def manage_teachers(request,*args,**kwargs):
    school = get_object_or_404(School,slug=kwargs.get('slug'))
    teacher = get_object_or_none(Teacher,slug = kwargs.get('teacher_slug'))
    form = TeacherForm(instance=teacher)

    if request.method == "POST":
        form = TeacherForm(request.POST,request.FILES,instance=teacher)
        if form.is_valid():
            teacher_data = form.save()
            school.teachers.add(teacher_data)
            if teacher:
                messages.success(request,f"{teacher_data} updated successfully")
            else:
                messages.success(request,f"{teacher_data} added successfully")
            return redirect(reverse('teachers',args=[kwargs.get('slug')]))
        else:
            form = TeacherForm(initial=request.POST)
            return render(request,'manage_teacher.html',locals())

    return render(request,'manage_teacher.html',locals())