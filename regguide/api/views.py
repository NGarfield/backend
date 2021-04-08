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

def SubjectListCreateAPIView(request):
    if request.method=="GET":
        queryset = Subject.objects.all()
        print(queryset)
        data3 = list(queryset.values())
        return JsonResponse( data3, safe=False)

@csrf_exempt
def ssoAPI(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        url = mydata['url']
        request.session['session_key'] = mydata['session']
    return redirect("/api/login/")

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
                request.session[request.session['session_key']] = token
                user.save()
            return redirect(url)

    return render(request,'login.html',{'form':LoginForm})

@csrf_exempt
def sessionTotoken(request):
    if request.method == "POST":
        mydata = json.loads(request.body)

    return HttpResponse(request.session[mydata['session']])

def random_char(y):
    return ''.join(random.choice(string.ascii_letters+"0123456789") for x in range(50))