from django.urls import path,include
from teacher_directory_user.views import home,sign_up,login_page,\
    logout_page,subjects,teachers,manage_teachers,bulk_addition,\
        manage_subjects,manage_school,view_teacher_info,filter_teacher

urlpatterns = [
    
    path('',home,name='home'),
    path('sign-up',sign_up,name='sign-up'),
    path('login',login_page,name='login'),
    path('logout',logout_page,name='logout'),

    path('subjects/',include([
        path('',subjects,name='subjects'),
        path('manage-<str:slug>',manage_subjects,name='manage-subjects'),
    ])),
    path('teachers-in-<str:slug>/',include([
        path('',teachers,name='teachers'),
        path('manage-<str:teacher_slug>',manage_teachers,name='manage-teacher'),
        path('u-can/view-the-info-of-<str:teacher_slug>',view_teacher_info,name='view-teacher'),
        path('bulk-addition',bulk_addition,name='bulk-addition'),
    ])),
    path('school/manage-<str:slug>',manage_school,name="manage-school"),

    path('filter-teachers-of-<str:school_slug>',filter_teacher,name='filter-teachers')


]