from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.template.loader import get_template

from teacher_directory_user.forms import CreateUserForm,LoginForm,TeacherForm,SubjectForm,SchoolForm
from teacher_directory_user.models import School,Subject,Teacher
from teacher_directory.utils import get_object_or_none,listToString

import csv
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
    creation_form = CreateUserForm()
    login_form = LoginForm()
    subjects = Subject.objects.all()
    return render(request,'subjects.html',locals())

def teachers(request,*args,**kwargs):
    creation_form = CreateUserForm()
    login_form = LoginForm()
    school = get_object_or_404(School,slug=kwargs.get('slug'))
    teachers = Teacher.objects.all()
    return render(request,'teachers.html',locals())
    
def manage_teachers(request,*args,**kwargs):
    creation_form = CreateUserForm()
    login_form = LoginForm()
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
            
            return redirect(reverse('teachers',args=[school.slug]))
        else:
            data = {Key : listToString(value) for (Key, value) in dict(request.POST).items()}
            form = TeacherForm(initial=data)
            for i in eval(form.errors.as_json()):
                messages.error(request,eval(form.errors.as_json())[i][0]['message'])
            return render(request,'manage_teacher.html',locals())

    return render(request,'manage_teacher.html',locals())


def manage_subjects(request,*args,**kwargs):
    creation_form = CreateUserForm()
    login_form = LoginForm()

    subject = get_object_or_none(Subject,slug = kwargs.get('slug'))
    form = SubjectForm(instance=subject)

    if request.method == "POST":
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            subject_data = form.save()
            if subject:
                messages.success(request,f"{subject_data} updated successfully")
            else:
                messages.success(request,f"{subject_data} added successfully")
            
            return redirect('subjects')
        else:
            data = {Key : listToString(value) for (Key, value) in dict(request.POST).items()}
            form = SubjectForm(initial=data)
            for i in eval(form.errors.as_json()):
                messages.error(request,eval(form.errors.as_json())[i][0]['message'])
    return render(request,'manage_subject.html',locals())

def manage_school(request,*args,**kwargs):
    creation_form = CreateUserForm()
    login_form = LoginForm()

    school = get_object_or_none(School,slug = kwargs.get('slug'))
    form = SchoolForm(instance=school)

    if request.method == "POST":
        form = SchoolForm(request.POST,instance=school)
        if form.is_valid():
            school_data = form.save()
            if school:
                messages.success(request,f"{school_data} updated successfully")
            else:
                messages.success(request,f"{school_data} added successfully")
            
            return redirect('subjects')
        else:
            data = {Key : listToString(value) for (Key, value) in dict(request.POST).items()}
            form = SchoolForm(initial=data)
            for i in eval(form.errors.as_json()):
                messages.error(request,eval(form.errors.as_json())[i][0]['message'])
    return render(request,'manage_school.html',locals())

def view_teacher_info(request,*args,**kwargs):
    school = get_object_or_404(School,slug=kwargs.get('slug'))
    teacher = get_object_or_404(Teacher,slug=kwargs.get('teacher_slug'))
    return render(request,'teacher_view.html',locals())

def bulk_addition(request,*args,**kwargs):
    from PIL import Image
    import os
    school = get_object_or_404(School,slug=kwargs.get('slug'))
    fs=FileSystemStorage(location='temp/')
    if request.method == "POST":
        csv_file = request.FILES.get('get_csv')
        file_content = ContentFile(csv_file.read())
        file_name = fs.save("temp.csv",file_content)
        temp_file = fs.path(file_name)
        csv_file = open(temp_file, errors='ignore')
        reader = csv.reader(csv_file)
        next(reader)
        
        for i,row in enumerate(reader):
            (first_name,last_name,profile_pic,email,phone,room_number,subject) = row

            relative_path = None
            if profile_pic:
                path = settings.BASE_DIR/'static'/"img"/profile_pic
                if os.path.exists(path):
                    im = Image.open(path)
                    relative_path = f'profile/{profile_pic}.png'
                    filename = os.path.join(settings.MEDIA_ROOT,relative_path)
                    im.save(filename)

            try:
                if email:
                    teacher,is_create = Teacher.objects.get_or_create(
                        first_name = first_name,last_name = last_name,
                        email = email, phone = phone,number_room = room_number,
                        profile_pic = relative_path
                    )
                    school.teachers.add(teacher)
                    for i,subject in enumerate(subject.split(",")):
                        subject,is_create = Subject.objects.get_or_create(
                            name = subject
                        )
                        if i <= 5:
                            teacher.subject.add(subject)
                        else:
                            messages.error(request,f'Maximum limited,{subject} is ignored!')
                
            except Exception as e:
                messages.error(request,str(e)+f"for addition in {first_name} {last_name}")
                continue
        return redirect(reverse('teachers',args=[school.slug]))
    
def filter_teacher(request,*args,**kwargs):
    school = get_object_or_404(School,slug=kwargs.get('school_slug'))
    teachers = school.teachers.all()
    filter_by = request.GET.get('filter_by')
    if filter_by:
        teachers = teachers.filter(
            Q(last_name__istartswith=filter_by) |
            Q(subject__name__istartswith=filter_by) 
        ).distinct()
    template = get_template('teachers_list.html').render(locals())
    return JsonResponse({
        "template":template
    })