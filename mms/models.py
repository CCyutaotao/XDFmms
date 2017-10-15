# -*-  coding:utf-8 -*- 
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class Campus(models.Model):
	campusname = models.CharField(max_length=100, unique=True)
	campusintroduction = models.CharField(max_length=200, blank=True)
	extra = models.TextField(blank=True)
	

	def __unicode__(self):
		return self.campusname


class UserList(AbstractUser):
	DUTY_CHOICES = (
                (u'店长助理',u'店长助理'),
                (u'店长',u'店长'),
                (u'部门经理',u'部门经理'),
                (u'部门总监',u'部门总监'),
                (u'市场总监',u'市场总监'),
    )
	SEX_CHOICES =(
                ('男','男'),
                ('女','女'),
    )

	status  = models.BooleanField(default=False)
	fullname = models.CharField(max_length=20, blank=False)
	sex = models.CharField(max_length=5, choices=SEX_CHOICES, blank=True)
	phone = models.CharField(max_length=11, blank=True)
	leaderid = models.ForeignKey('self', editable=True, blank=True, null=True ,on_delete = models.CASCADE)
	campusid = models.ForeignKey(Campus, editable=True, blank=True, null=True ,on_delete = models.CASCADE)
	duty = models.CharField(max_length=20, choices=DUTY_CHOICES)	

	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.fullname


class StudentInfoCollect(models.Model):
	studentname = models.CharField(max_length=20, blank=True)
	schoolname = models.CharField(max_length=50, blank=True)
	grade = models.CharField(max_length=50, blank=True)
	phone = models.CharField(max_length=11, blank=True) 
	infosource = models.CharField(max_length=100,db_index=True,blank=True) 
	registornot = models.IntegerField(default=0)
	firstfollow = models.CharField(max_length=500, blank=True)
	secondfollow = models.CharField(max_length=200, blank=True)
	thirdfollow = models.CharField(max_length=200, blank=True)
	introduceornot = models.BooleanField(default=False)
	introducenumber = models.IntegerField(default=0)
	classcoreid =  models.CharField(max_length=20, blank=True)
	anotherchoiceornot = models.CharField(max_length=20, blank=True)
	chinese = models.CharField(max_length=200,default=u'')
	math = models.CharField(max_length=200,default=u'')
	english = models.CharField(max_length=200,default=u'')
	extra = models.CharField(max_length=200,blank=True)
	campusid = models.ForeignKey(Campus, editable=True, blank=True, null=True, on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList, editable=False, on_delete=models.CASCADE)
	recordtime = models.DateTimeField(auto_now_add=True)
	lastupdatetime = models.DateTimeField(auto_now=True)	
	advice = models.CharField(max_length=200, blank=True)
	schoolclassid = models.CharField(max_length=100, blank=True)	

	infosourceintroduction = models.CharField(max_length=200,default='')
	wechatornot = models.IntegerField(default=0)
	visitornot = models.IntegerField(default=0)
	registtime = models.DateTimeField(blank=True)
	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.id



class Season(models.Model):
	seasonintroduction = models.CharField(max_length=300)
	plan = models.CharField(max_length=500)
	advice = models.CharField(max_length=200, blank=True)

	recorderid = models.ForeignKey(UserList, on_delete= models.CASCADE)

	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.seasonintroduction


class Month(models.Model):
	monthintroduction = models.CharField(max_length=300)
	plan = models.CharField(max_length=500)
	advice = models.CharField(max_length=200,blank=True)
	
	seasonid = models.ForeignKey(Season, on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.monthintroduction




class Week(models.Model):
	weekintroduction = models.CharField(max_length=300)
	plan = models.CharField(max_length=500)
	advice = models.CharField(max_length=200, blank=True)

	monthid = models.ForeignKey(Month, on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList, on_delete=models.CASCADE)



	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.weekintroduction




class Day(models.Model):
	dayintroduction = models.CharField(max_length=300)
	plan = models.CharField(max_length=500)
	advice = models.CharField(max_length=200, blank=True)

	weekid = models.ForeignKey(Week,  on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList,  on_delete=models.CASCADE)
	score = models.IntegerField(default=0)

	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.dayintroduction


class Task(models.Model):
	taskintroduction = models.CharField(max_length=300)
	completion = models.IntegerField(default=0)
	reason = models.CharField(max_length=200, blank=True)
	plan = models.CharField(max_length=500)
	advice = models.CharField(max_length=200, blank=True)

	dayid = models.ForeignKey(Day,  on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList,  on_delete=models.CASCADE)


	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.taskintroduction



class FeedBack(models.Model):
	parentname = models.CharField(max_length=20)
	studentid = models.CharField(max_length=20)
	phone = models.CharField(max_length=11)

	campusid = models.ForeignKey(Campus, on_delete=models.CASCADE)
	recorderid = models.ForeignKey(UserList, on_delete=models.CASCADE)
	problem = models.CharField(max_length=200, blank=True)
	detail = models.CharField(max_length=200, blank=True)
 	recordtime = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.id


