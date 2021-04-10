from rest_framework import generics
from regguide.models import Subject,UserLogin
import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .forms import LoginForm
import random,string
from django.views.decorators.csrf import csrf_exempt

# class SubjectListCreateAPIView(generics.ListCreateAPIView):
#     # queryset = Subject.objects.filter(name_group_id=2)
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializers
url = ""
sessions = ""
mytoken = {}

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
        
    return JsonResponse({"url":"http://127.0.0.1:8000/api/login/"})

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
                global sessions,mytoken
                mytoken = {sessions : token}
                user.save()
            mytoken = {sessions : data.token}
            return redirect("http://127.0.0.1:8080/")

    return render(request,'login.html',{'form':LoginForm})

@csrf_exempt
def sessionTotoken(request):
    global mytoken
    if request.method == "POST":
        mydata = json.loads(request.body)
    return JsonResponse({"token":mytoken[sessions]})

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
        data1 = list(data.values())
        return JsonResponse({"id_user" : data1},safe=False)


