from django.conf.urls import url
from . import views
app_name = 'box'
urlpatterns = [
    url(r'^(?P<employee_id>[0-9]+)/further/$',views.further, name='further'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<employee_gmail_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<employee_id>[0-9]+)/create_employee_private/$', views.create_employee_private, name='create_employee_private'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_employee_gmail/$', views.create_employee_gmail, name='create_employee_gmail'),
    url(r'^(?P<employee_id>[0-9]+)/scheduling/$', views.scheduling, name='scheduling'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/(?P<feedback_id>[0-9]+)/feedback/$', views.feedback, name='feedback'),
    url(r'^(?P<employee_id>[0-9]+)/interview_details/$', views.interview_details, name='interview_details'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/status/$', views.status, name='status'),
    url(r'^(?P<employee_id>[0-9]+)/update/$', views.update, name='update'),
    url(r'^(?P<employee_id>[0-9]+)/update_public/$', views.update_public, name='update_public'),
    url(r'^(?P<employee_id>[0-9]+)/update_private/$', views.update_private, name='update_private'),
    url(r'^(?P<employee_id>[0-9]+)/update_vehicle/$', views.update_vehicle, name='update_vehicle'),
    url(r'^(?P<employee_id>[0-9]+)/hr_all/$', views.hr_all, name='hr_all'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/hr_inter_all/$', views.hr_inter_all, name='hr_inter_all'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/(?P<feedback_id>[0-9]+)/inter_all/$', views.inter_all, name='inter_all'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/scheduling2/$', views.scheduling2, name='scheduling2'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/scheduling3/$', views.scheduling3, name='scheduling3'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/rescheduling1/$', views.rescheduling1, name='rescheduling1'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/rescheduling2/$', views.rescheduling2, name='rescheduling2'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/rescheduling3/$', views.rescheduling3, name='rescheduling3'),
    url(r'^(?P<employee_id>[0-9]+)/(?P<interviewee_id>[0-9]+)/rescheduling/$', views.rescheduling, name='rescheduling'),
]
