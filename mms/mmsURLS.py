from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from mms import views




urlpatterns = format_suffix_patterns([
	url(r'campus/list/$', views.CampusListView.as_view()),
	url(r'campus/create/$', views.CampusCreateView.as_view()),
	url(r'director/list/$', views.DirectorListView.as_view()),
	url(r'users/login/$', views.UserLoginView.as_view()),
	url(r'users/create/$', views.UserCreateView.as_view()),
	url(r'users/userstatus/list/$', views.UserStatusCheckListView.as_view()),
	url(r'users/userinfo/update/(?P<pk>[0-9]+)/$', views.UserInfoUpdateView.as_view()),
	url(r'users/password/update/$',views.UserPasswordUpdate.as_view()),
	url(r'users/userinfo/list/$', views.UserInfoView.as_view()),
	url(r'users/delete/(?P<pk>[0-9]+)/$', views.UserDeleteView.as_view()),
	url(r'leader/userinfo/list/$', views.UserForLeaderListView.as_view()),
	url(r'student/create/$', views.StudentInfoCollectView.as_view()),
	url(r'student/list/$', views.StudentInfoListView.as_view()),
	url(r'student/detail/(?P<pk>[0-9]+)/$', views.StudentDetailListView.as_view()),
	url(r'student/update/(?P<pk>[0-9]+)/$', views.StudentInfoUpdateView.as_view()),
        url(r'student/delete/(?P<pk>[0-9]+)/$', views.StudentInfoDeleteView.as_view()),
	url(r'student/count/list/$',views.StudentInfoCount.as_view()),
        url(r'leader/season/list/$', views.SeasonPlanForLeaderListView.as_view()),
	url(r'staff/season/list/$', views.PersonalSeasonPlanListView.as_view()),
        url(r'staff/month/list/$', views.PersonalMonthPlanListView.as_view()),
        url(r'staff/week/list/$', views.PersonalWeekPlanListView.as_view()), 
        url(r'staff/day/list/$', views.PersonalDayPlanListView.as_view()),      
        url(r'staff/task/list/$', views.PersonalTaskPlanListView.as_view()),
        url(r'staff/season/create/$', views.PersonalSeasonPlanCreateView.as_view()),
        url(r'staff/month/create/$', views.PersonalMonthPlanCreateView.as_view()),
        url(r'staff/week/create/$', views.PersonalWeekPlanCreateView.as_view()), 
        url(r'staff/day/create/$', views.PersonalDayPlanCreateView.as_view()),      
        url(r'staff/day/score/update/(?P<pk>[0-9]+)/$', views.DayPlanScoreUpdateView.as_view()),
	url(r'staff/task/create/$', views.PersonalTaskPlanCreateView.as_view()),
	url(r'staff/task/update/(?P<pk>[0-9]+)/$', views.PersonalTaskPlanUpdateView.as_view()),
	url(r'feedback/list/$', views.FeedBackListView.as_view()),
	url(r'feedback/filter/list/$', views.FeedBackFilterView.as_view()),
        url(r'feedback/create/$', views.FeedBackCreateView.as_view()),
	url(r'excel/student/$', views.excelout),
	url(r'excel/leader/$', views.countexcelout),

])
