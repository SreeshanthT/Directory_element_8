from django.db import models
from django_lifecycle import LifecycleModelMixin,hook,BEFORE_CREATE
from teacher_directory.utils import unique_slug_generator

# Create your models here.

class School(LifecycleModelMixin,models.Model):
    name = models.CharField(max_length=255)
    teachers = models.ManyToManyField('teacher_directory_user.Teacher',blank=True)
    slug = models.SlugField(max_length=255,blank=True)

    @hook(BEFORE_CREATE)
    def set_slug(self):
        self.slug = unique_slug_generator(self,self.name)
    def __str__(self) -> str:
        return str(self.name)


class Teacher(LifecycleModelMixin,models.Model):
    first_name = models.CharField("First Name",max_length=100)
    last_name = models.CharField("Last Name",max_length=100)
    profile_pic = models.FileField(upload_to = "profile",null=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=20)
    number_room = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    subject = models.ManyToManyField('teacher_directory_user.Subject',blank=True)
    taught = models.BooleanField(choices=(
        (True,'Yes'),
        (False,'No'),
    ),default=True)
    slug = models.SlugField(max_length=255,blank=True)

    @hook(BEFORE_CREATE)
    def set_slug(self):
        name = f"{self.first_name}-{self.last_name}"
        self.slug = unique_slug_generator(self,name)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    


class Subject(LifecycleModelMixin,models.Model):
    name = models.CharField("Subject",max_length=100)
    slug = models.SlugField(max_length=105,blank=True)
    @hook(BEFORE_CREATE)
    def set_slug(self):
        self.slug = unique_slug_generator(self,self.name)
    def __str__(self) -> str:
        return str(self.name)

