from django.urls import path,include
from teacher_directory_user.views import home,sign_up,login_page,\
    logout_page,subjects,teachers,manage_teachers

urlpatterns = [
    path('',home,name='home'),
    path('sign-up',sign_up,name='sign-up'),
    path('login',login_page,name='login'),
    path('logout',logout_page,name='logout'),

    path('subjects/',subjects,name='subjects'),
    path('teachers-in-<str:slug>/',include([
        path('',teachers,name='teachers'),
        path('manage-<str:teacher_slug>',manage_teachers,name='manage-teacher'),
    ]))

]