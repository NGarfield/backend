from rest_framework import generics
from regguide.models import (Subject,UserLogin,Student,Faculty,Deparment
                            ,Calender,PreSubject,CourseSubject,RegisterSubject,
                            PreSubject)
import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .forms import LoginForm
import random,string,datetime
from django.views.decorators.csrf import csrf_exempt

# class SubjectListCreateAPIView(generics.ListCreateAPIView):
#     # queryset = Subject.objects.filter(name_group_id=2)
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializers
url = ""
mytoken = {}
sessions = ""
session = ""

def SubjectListCreateAPIView(request):
    if request.method=="GET":
        queryset = Subject.objects.all()
        print(queryset)
        data3 = list(queryset.values())
        return JsonResponse( data3, safe=False)

@csrf_exempt
def ssoAPI(request):
    if request.method == "GET":
        global sessions
        url = request.GET['url']
        sessions = request.GET['session']
        
    return JsonResponse({"url":"http://127.0.0.1:8000/api/login/?session=" + sessions})

@csrf_exempt
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        data  = UserLogin.objects.filter(username=username).first()
        if(data and data.username==username and data.password==password):
            if(data.token == ""):
                token = random_char(50)
                user = UserLogin(username = data.username,
                                password = data.password,
                                token = token)
                global session,mytoken
                
                mytoken[request.session['session']] = token
                user.save()
            
            else:
                print(request.session['session']+"555")
                mytoken[request.session['session']] = data.token

            return redirect("http://127.0.0.1:8080/")
    
    if request.method=="GET":
        request.session['session'] = request.GET['session']
        print(request.session['session'])
        mytoken.update({request.session['session'] : ""})
        return render(request,'login.html',{'form':LoginForm})

@csrf_exempt
def sessionTotoken(request):
    global mytoken
    if request.method == "POST":
        mydata = json.loads(request.body)
    return JsonResponse({"token":mytoken.get(mydata['session'])})
    

def random_char(y):
    return ''.join(random.choice(string.ascii_letters+"0123456789") for x in range(50))

@csrf_exempt
def validateToken(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        data = UserLogin.objects.filter(token=mydata['token']).first()
        if(data):
            return JsonResponse({"state" : "200"})
        
        return JsonResponse({"state" : "402"})

@csrf_exempt
def getUser(requset):
    if requset.method == "POST":
        mydata = json.loads(requset.body)
        data =  UserLogin.objects.filter(token=mydata['token'])
        data_student = Student.objects.filter(id_student=data[0])
        data_student1 = data_student[0].student_name+" "+data_student[0].student_surname
        data1 = list(data.values())
        return JsonResponse({"id_user" : data1,"name" : data_student1},safe=False)

@csrf_exempt
def getInfoStudent(requset):
    if requset.method == "POST":
        mydata = json.loads(requset.body)
        data =  UserLogin.objects.filter(token=mydata['token'])
        data_student = Student.objects.filter(id_student=data[0])
        data_student1 = list(data_student.values())
        name_faculty = Faculty.objects.filter(faculty_id = data_student1[0]['faculty_id_id'])
        name_faculty1 = list(name_faculty.values())
        data_student1[0].update({"faculty" : name_faculty1[0]['faculty_name']})
        name_deparment = Deparment.objects.filter(deparment_id = data_student1[0]['deparment_id_id'])
        name_deparment1 = list(name_deparment.values())
        data_student1[0].update({"deparment" : name_deparment1[0]['deparment_name']})
        return JsonResponse({"student":data_student1},safe=False)

def getCalender(requset):
    if requset.method == "GET":
        timenow = datetime.datetime.now()
        time30d = datetime.datetime.now() + datetime.timedelta(days=150)
        data = Calender.objects.filter(end_date__range=(timenow,time30d))
        data_date = list(data.values())
        return JsonResponse({"date":data_date},safe=False)


@csrf_exempt
def getCourseStudent(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        data_allsubject = [{
          "key": 11,
          "text": "ปีการศึกษาปีที่ 1/1",
          "isGroup": "true",
        },
        {
          "key": 12,
          "text": "ปีการศึกษาปีที่ 1/2",
          "isGroup": "true",
        },
        {
          "key": 21,
          "text": "ปีการศึกษาปีที่ 2/1",
          "isGroup": "true",
        },
        {
          "key": 22,
          "text": "ปีการศึกษาปีที่ 2/2",
          "isGroup": "true",
        },
        {
          "key": 31,
          "text": "ปีการศึกษาปีที่ 3/1",
          "isGroup": "true",
        },
        {
          "key": 32,
          "text": "ปีการศึกษาปีที่ 3/2",
          "isGroup": "true",
        },
        {
          "key": 41,
          "text": "ปีการศึกษาปีที่ 4/1",
          "isGroup": "true",
        },
        {
          "key": 42,
          "text": "ปีการศึกษาปีที่ 4/2",
          "isGroup": "true",
        }]

        student = Student.objects.filter(id_student=userlogin.username).first()
        all_subject = CourseSubject.objects.filter(deparment=student.deparment_id)
        for a in all_subject:
            data_subject = {}
            key = Subject.objects.filter(id_subject=a.subject.id_subject).first()
            data_subject.update({"key" : key.id_subject})
            data_subject.update({"name" : key.subjectName})
            data_subject.update({"group" : a.group})
            register = RegisterSubject.objects.filter(student=student,subject=key).first()
            if(register):
                if register.grade == "f" or register.grade == "F" :
                    data_subject.update({"grade" : -1})
                
                else:
                    data_subject.update({"grade" : 1})

            else:
                data_subject.update({"grade" : 0})

            data_allsubject.append(data_subject)
        
        data_allsubject1 = list(data_allsubject)
        return JsonResponse({"nodeDataArray" : data_allsubject1},safe=False)

@csrf_exempt
def getConditionSubject(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        all_presubject = []
        student = Student.objects.filter(id_student=userlogin.username).first()
        all_subject = CourseSubject.objects.filter(deparment=student.deparment_id)
        for a in all_subject :
            con = PreSubject.objects.filter(condition=a.subject.id_subject)
            
            if con :
                for c in con :
                    pre = {}
                    pre.update({"from":a.subject.id_subject})
                    pre.update({"to":c.subject.id_subject})
                    all_presubject.append(pre)
        
        all_presubject1 = list(all_presubject)
        return JsonResponse({"linkDataArray":all_presubject1},safe=False)