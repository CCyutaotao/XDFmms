# -*- coding:utf-8 -*-
from rest_framework import serializers	

from mms.models import	*






class CampusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(required=True, max_length=1024)
    password = serializers.CharField(required=True, max_length=1024)
    token = serializers.UUIDField()
    class Meta:
        model = UserList
        fields = ('id', 'username', 'password', 'token')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=True)

    class Meta:
        model = UserList
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
   leadername = serializers.ReadOnlyField(source='leaderid.fullname')
   campusname = serializers.ReadOnlyField(source='campusid.campusname')	
    
   class Meta:
        model = UserList
        exclude = ('password', )


class DirectorListSerializer(serializers.ModelSerializer):
   class Meta:
	model = UserList
	fields = ('id','fullname')	

class StudentInfoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentInfoCollect
        fields = ('id', 'studentname', 'schoolname', 'grade', 'phone', 'infosource', 'registornot', 'advice')


class StudentInfoDetailSerializer(serializers.ModelSerializer):
   recordername = serializers.ReadOnlyField(source='recorderid.fullname')
   campusname = serializers.ReadOnlyField(source='campusid.campusname')
   class Meta:
        model = StudentInfoCollect
        fields = '__all__' 




class SeasonPlanListSerializer(serializers.ModelSerializer):
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')
    class Meta:
        model = Season
        exclude = ('recorderid',)


class MonthPlanListSerializer(serializers.ModelSerializer):
    seasonintroduction = serializers.ReadOnlyField(source = 'seasonid.seasonintroduction')
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')

    class Meta:
        model = Month
	exclude = ('recorderid',)

class WeekPlanListSerializer(serializers.ModelSerializer):
    monthintroduction = serializers.ReadOnlyField(source = 'monthid.monthintroduction')
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')
    class Meta:
        model = Week
	exclude = ('recorderid',)

class DayPlanListSerializer(serializers.ModelSerializer):
    weekintroduction = serializers.ReadOnlyField(source = 'weekid.weekintroduction')
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')
    class Meta:
        model = Day
        exclude = ('recorderid',)

class TaskPlanListSerializer(serializers.ModelSerializer):
    dayintroduction = serializers.ReadOnlyField(source = 'dayid.dayintroduction')
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')
    class Meta:
        model = Task
	exclude = ('recorderid',)

class FeedBackListSerializer(serializers.ModelSerializer):
    recordername = serializers.ReadOnlyField(source = 'recorderid.fullname')
    campusname = serializers.ReadOnlyField(source = 'campusid.campusname')

    class Meta:
        model = FeedBack
        fields = ('id','parentname','phone','studentid','problem','detail','recordername','campusname') 
