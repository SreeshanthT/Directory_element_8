from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from teacher_directory_user.models import Teacher,School,Subject

class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm,self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
                'placeholder':self.fields[name].label,
            })

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm,self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
                'placeholder':self.fields[name].label,
            })
    username = forms.CharField(label='Username',max_length=150)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)


class TeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm,self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
                'placeholder':self.fields[name].label,
            })

    class Meta:
        model = Teacher
        fields = ['first_name','last_name','profile_pic',
            'email','phone','number_room','number','subject','taught'
        ]

    def clean_subject(self):
        cleaned_data = super().clean()
        if cleaned_data.get('subject').count() > 5:
            raise forms.ValidationError('You have to choose 5 subjects for each teachers')

class SchoolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchoolForm,self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
                'placeholder':self.fields[name].label,
            })
    class Meta:
        model = School
        fields = ['name']

class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectForm,self).__init__(*args, **kwargs)

        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control',
                'placeholder':self.fields[name].label,
            })
    class Meta:
        model = Subject
        fields = ['name']