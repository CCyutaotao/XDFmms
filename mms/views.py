# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.conf import	settings
from django.http import	StreamingHttpResponse
from django.contrib.auth import authenticate, login, logout	
from django.db.models import Count, Sum, Min, F

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer 

from rest_framework import permissions, status
from rest_framework import generics 

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

from datetime import datetime, date, timedelta	

from mms.serializers import *
from mms.models import *

 

class CampusListView(generics.ListAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusListSerializer
    permission_classes = (
    )

    def list(self, request):
	try:
		if request.user.duty == u'店长助理' or request.user.duty == u'店长':
			queryset = Campus.objects.get(id = request.user.campusid)
		elif request.user.duty == u'部门经理':
			queryset = Campus.objects.filter(id__in = UserList.objects.filter(leaderid = request.user.id).values_list('campusid', flat=True))
		else :
			queryset = Campus.objects.all()
	except Exception, e:
	
		queryset = Campus.objects.all()
	serializer = CampusListSerializer(queryset, many=True)
	for i in range(0, queryset.count()):
		a = serializer.data[i]
		if UserList.objects.filter(status=1).filter(campusid = a['id']).filter(duty__iexact=u'店长').exists():
			leader = UserList.objects.get(campusid = a['id'], duty__iexact=u'店长')
			a['leaderid'] = leader.id
			a['leadername'] = leader.fullname
			
		else: 
			a['leaderid'] = ''
			a['leadername'] = ''
	return Response(serializer.data) 
		

class CampusCreateView(generics.CreateAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusListSerializer
    permission_classes = (
    	permissions.IsAdminUser,
    )


class UserLoginView(APIView):
    """
    登陆接口     
    """
    queryset = UserList.objects.all()
    serializer_class = AuthTokenSerializer
    permission_classes=()
    def post(self, request, *args, **kwargs):
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                if UserList.objects.get(id=user.id).status == 0:
                        return Response({'detail':'Ask the manager to confirm your identity '})
                login(request,user)
                token, created = Token.objects.get_or_create(user=user)
                duty = user.duty
                return Response({'userid':user.id, 'username':user.username, 'token': token.key,'duty':duty})  

class DirectorListView(generics.ListAPIView):
    queryset = UserList.objects.filter(duty=u'部门经理')
    serializer_class = DirectorListSerializer
    permission_classes = (
    ) 

class UserCreateView(APIView):
    """
    注册接口
    """
    queryset = UserList.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes =  (
    )
    def post(self, request, *args, **kwargs):
            if len(UserList.objects.filter(username=request.data['username']))!=0:
                    return Response({'detail':'username exist'}, status=status.HTTP_200_OK)
            try:     
                    user = UserList()
                    user.username = request.data['username']
                    user.set_password(request.data['password'])
                    user.fullname = request.data['fullname']
                    user.sex = request.data['sex']
                    user.email = request.data.get('email','2@qq.com')
                    user.phone = request.data.get('phone','')
		    user.duty = request.data['duty']
                    user.campusid = Campus.objects.get(id=request.data['campusid'])
		    if user.duty == u'店长':
			if UserList.objects.filter(campusid = user.campusid, duty = u'店长', status=1):
                        	return Response({"detail":u"campus manager exists."}, status=status.HTTP_400_BAD_REQUEST)
			user.leaderid = UserList.objects.get(id = float(request.data['leaderid']))
		    else :
                    	user.leaderid = UserList.objects.get(id = float(request.data['leaderid']))
                    user.is_active = True
                    user.is_staff = False
                    user.save()
                    return Response({'detail':"Success"}, status=status.HTTP_200_OK)
            except Exception,e:
                    print e
                    return Response({'detail':'Failed'}, status=status.HTTP_400_BAD_REQUEST)   



class UserStatusCheckListView(generics.ListAPIView):
    """
    返回 所有待审核的新注册用户  权限用户专用
    """

    serializer_class = UserListSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )

    def list(self, request):
            queryset = UserList.objects.filter(status = 0).filter(leaderid = request.user)
            serializer = UserListSerializer(queryset, many = True)
            return Response(serializer.data)

class UserInfoUpdateView(generics.UpdateAPIView):
    """
    待审核用户状态更新  允许登陆客户端
    """
    queryset = UserList.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )



class UserPasswordUpdate(APIView):

    """
    密码更改
    """
    def post(self, request, *args, **kwargs):
            oldpwd = request.data['opwd']
            newpwd = request.data['npwd']
            user = authenticate(username = request.user.username, password = oldpwd)
            if not user :
                    return Response({"detail": u"旧密码错误"}, status = status.HTTP_406_NOT_ACCEPTABLE)
            else : 
                    user.set_password(newpwd)
 	     	    user.save()
                    return Response({"detail": u"修改密码成功"}, status = status.HTTP_200_OK)




class UserDeleteView(generics.DestroyAPIView):
    """
    审核未通过用户删除 权限用户专用
    """
    queryset = UserList.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response({"detail":"success"}, status=status.HTTP_200_OK)




class UserInfoView(generics.ListAPIView):

    """
    用户本人信息查看  限用户本人 
    """
    queryset =  UserList.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )
    def list(self, request):
            queryset = UserList.objects.filter(id = request.user.id)
            serializer = UserListSerializer(queryset, many =True)
            return Response(serializer.data)



class UserForLeaderListView(generics.ListAPIView):
    queryset =  UserList.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )
    def list(self, request):
	    if request.user.duty == u'部门经理':
		L1 = UserList.objects.filter(status=1).filter(leaderid__in = UserList.objects.filter(leaderid = request.user.id).values_list('id', flat=True)).values_list('id', flat=True)
		L2 = UserList.objects.filter(status=1).filter(leaderid = request.user.id).values_list('id', flat=True)
		queryset = UserList.objects.filter(status=1).filter(id__in = L1 | L2 )
	    elif request.user.duty == u'店长':
            	queryset = UserList.objects.filter(status=1).filter(leaderid = request.user.id)
	    elif request.user.duty == u'店长助理':
		queryset = UserList.objects.filter(status=1).filter(id = request.user.id)
	    else:
		queryset = UserList.objects.filter(status=1).exclude(id__in = [1L,6L,27L,36L])

            serializer = UserListSerializer(queryset, many =True)
            return Response(serializer.data)



class StudentInfoListView(generics.ListAPIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    def list(self, request):
            queryset = StudentInfoCollect.objects.filter(recorderid = request.user.id)
            serializer = StudentInfoListSerializer(queryset, many =True)
            return Response(serializer.data)



class StudentDetailListView(generics.RetrieveAPIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )


class StudentInfoCollectView(generics.CreateAPIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(recorderid = self.request.user, campusid = self.request.user.campusid)


class StudentInfoUpdateView(generics.UpdateAPIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('id', )



class StudentInfoDeleteView(generics.DestroyAPIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )




class PersonalSeasonPlanListView(generics.ListAPIView):
    serializer_class = SeasonPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
 
    def list(self, request):
        queryset = Season.objects.filter(recorderid = request.user.id)
        serializer = SeasonPlanListSerializer(queryset, many =True)
        return Response(serializer.data)

class SeasonPlanForLeaderListView(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('recorderid',)    

class PersonalSeasonPlanCreateView(generics.CreateAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(recorderid = self.request.user)



class PersonalMonthPlanListView(generics.ListAPIView):
    queryset = Month.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = MonthPlanListSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('seasonid', 'recorderid')

class PersonalMonthPlanCreateView(generics.CreateAPIView):
    queryset = Month.objects.all()
    serializer_class = MonthPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(recorderid = self.request.user)

class PersonalWeekPlanListView(generics.ListAPIView):
    queryset = Week.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = WeekPlanListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('monthid', 'recorderid')



class PersonalWeekPlanCreateView(generics.CreateAPIView):
    queryset = Week.objects.all()
    serializer_class = WeekPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(recorderid = self.request.user)

class PersonalDayPlanListView(generics.ListAPIView): 
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def list(self, serializer):
	weekid = 0
	for item in self.request.GET.items():
		if item[0] == 'weekid':
			weekid = item[1]
	queryset = Day.objects.filter(weekid = weekid)
	serializer = DayPlanListSerializer(queryset, many=True)
	for i in range(0, queryset.count()):
		a = serializer.data[i]
		try:
			completionlist=Task.objects.filter(dayid = int(a['id'])).values_list('completion', flat=True)
			a['avgcompletion'] = sum(completionlist)/len(completionlist)
		except Exception, e:
			a['avgcompletion'] = 0 
	return Response(serializer.data)

class PersonalDayPlanCreateView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
	today = date.today().strftime('%Y/%m/%d')
	try :
		day = Day.objects.get(dayintroduction=today, plan=u'无', recorderid=request.user)
		return Response({'today':day.dayintroduction, 'dayid':day.id, 'weekid':day.weekid_id})
	except Exception, e:
		day, created = Day.objects.get_or_create(dayintroduction=today, plan=u'无', weekid=Week.objects.get(id=request.data['weekid']) ,recorderid=request.user)
		return Response({'today':day.dayintroduction, 'dayid':day.id, 'weekid':day.weekid_id})	

class DayPlanScoreUpdateView(generics.UpdateAPIView):
     queryset = Day.objects.all()
     serializer_class = DayPlanListSerializer
     permission_classes = (
	permissions.IsAuthenticated,
     )

class PersonalTaskPlanListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskPlanListSerializer 
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('dayid', 'recorderid')


class PersonalTaskPlanCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(recorderid = self.request.user)


class PersonalTaskPlanUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskPlanListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    


class FeedBackListView(generics.ListAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def list(self, serializer):
        queryset = FeedBack.objects.filter(campusid = self.request.user.campusid)
        serializer = FeedBackListSerializer(queryset, many=True)
        return Response(serializer.data)


class FeedBackFilterView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, serializer):
        days = 30
        campuslist = []
	problem = ''
        for item in Campus.objects.all().values_list('id', flat=True):
                campuslist.append(int(item))
	if self.request.user.duty == u'店长':
		campuslist = [self.request.user.campusid,]
        for item in self.request.GET.items():
            if item[0] == 'days':
                days = item[1]
            if item[0] == 'campus':
                campuslist = item[1].split(',')
	    if item[0] == 'problem':
                problem = item[1]
	if problem:
		queryset = FeedBack.objects.filter(campusid__in = campuslist).filter(problem = problem).filter(recordtime__gte = (date.today()-timedelta(int(days))))
	else:
       	 	queryset = FeedBack.objects.filter(campusid__in = campuslist).filter(recordtime__gte = (date.today()-timedelta(int(days))))
        serializer = FeedBackListSerializer(queryset, many=True)
        return Response(serializer.data)



class FeedBackCreateView(generics.CreateAPIView):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackListSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    def perform_create(self, serializer):
	print self.request.user
        serializer.save(recorderid = self.request.user, campusid = self.request.user.campusid)

class StudentInfoCount(APIView):
    queryset = StudentInfoCollect.objects.all()
    serializer_class = StudentInfoDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, serializer):
        days = 30
	campuslist = []
	for item in Campus.objects.all().values_list('id', flat=True):
		campuslist.append(int(item))	
        for item in self.request.GET.items():
            if item[0] == 'days':
                days = item[1]
            if item[0] == 'campus':
                campuslist = item[1].split(',')
	if self.request.user.duty == u'店长':
		campuslist = [self.request.user.campusid,]
	if self.request.user.duty == u'部门经理':
		campuslist = UserList.objects.filter(leaderid = self.request.user.id).values_list('campusid', flat=True)
        queryset = StudentInfoCollect.objects.filter(campusid__in = campuslist).filter(recordtime__gte = (date.today()-timedelta(int(days))))  
	
	querysetcount = queryset.order_by('campusid','recorderid').values('recorderid','recorderid__fullname', 'recorderid__campusid__campusname').annotate(collectcount=Count('recorderid')).annotate(sumregist=Sum('registornot')).annotate(sumintroduction=Sum('introducenumber')).annotate(mindate=Min('recordtime'))
        
	return Response(querysetcount)


from folder.excelwrite import student,count
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse

def file_iterator(filepath, chunk_size = 512):
    with open(filepath, 'rb') as f:
            while True:
                    c = f.read(chunk_size)
                    if c:
                            yield c
                    else:
                            break
@api_view(['get',])
def excelout(request):
    days = 30
    recorderid = 0
    for item in request.GET.items():
        if item[0] == 'days':
            days = item[1]
        if item[0] == 'recorderid':
            recorderid = item[1]
    queryset = StudentInfoCollect.objects.filter(recorderid = recorderid).filter(recordtime__gte = (date.today()-timedelta(int(days))))
    serializer = StudentInfoDetailSerializer(queryset, many=True) 
    filepath = student(serializer.data)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filepath.split('/')[-1])
    return response

@api_view(['get',])
def countexcelout(request):
    days = 30
    recorderid = 0
    for item in request.GET.items():
        if item[0] == 'days':
            days = item[1]
        if item[0] == 'recorderid':
            recorderid = item[1]
    queryset = StudentInfoCollect.objects.filter(recorderid = recorderid).filter(recordtime__gte = (date.today()-timedelta(int(days))))
    serializer = StudentInfoDetailSerializer(queryset, many=True)
    filepath = count(serializer.data)
    response = StreamingHttpResponse(file_iterator(filepath))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filepath.split('/')[-1])
    return response


