from rest_framework import generics
from regguide.models import (Subject, UserLogin, Student, Faculty, Deparment, Calender, PreSubject, CourseSubject, RegisterSubject,
                             PreSubject,ConditionJSON,DateSystem,GroupSubject,OptionSubject,TestSubject,TimetableSubject)
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import LoginForm
import random
import string
import datetime
from django.views.decorators.csrf import csrf_exempt

# class SubjectListCreateAPIView(generics.ListCreateAPIView):
#     # queryset = Subject.objects.filter(name_group_id=2)
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializers
url = ""
mytoken = {}
sessions = ""
session = ""
date = DateSystem.objects.all().first()

def SubjectListCreateAPIView(request):
    if request.method == "GET":
        queryset = Subject.objects.all()
        print(queryset)
        data3 = list(queryset.values())
        return JsonResponse({'subject':data3}, safe=False)


@csrf_exempt
def ssoAPI(request):
    if request.method == "GET":
        global sessions
        url = request.GET['url']
        sessions = request.GET['session']

    return JsonResponse({"url": "http://127.0.0.1:8000/api/login/?session=" + sessions})


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        data = UserLogin.objects.filter(username=username).first()
        if(data and data.username == username and data.password == password):
            if(data.token == ""):
                token = random_char(50)
                user = UserLogin(username=data.username,
                                 password=data.password,
                                 token=token)
                global session, mytoken

                mytoken[request.session['session']] = token
                user.save()

            else:
                print(request.session['session']+"555")
                mytoken[request.session['session']] = data.token

            return redirect("http://127.0.0.1:8080/")
        else:
            return render(request, 'login.html', {'form': LoginForm})

    if request.method == "GET":
        request.session['session'] = request.GET['session']
        print(request.session['session'])
        mytoken.update({request.session['session']: ""})
        return render(request, 'login.html', {'form': LoginForm})


@csrf_exempt
def sessionTotoken(request):
    global mytoken
    if request.method == "POST":
        mydata = json.loads(request.body)
    return JsonResponse({"token": mytoken.get(mydata['session'])})


def random_char(y):
    return ''.join(random.choice(string.ascii_letters+"0123456789") for x in range(50))


@csrf_exempt
def validateToken(request):
    if request.method == "POST":
        mydata = json.loads(request.body)
        data = UserLogin.objects.filter(token=mydata['token']).first()
        if(data):
            return JsonResponse({"state": "200"})

        return JsonResponse({"state": "402"})


@csrf_exempt
def getUser(requset):
    if requset.method == "POST":
        mydata = json.loads(requset.body)
        data = UserLogin.objects.filter(token=mydata['token'])
        data_student = Student.objects.filter(id_student=data[0])
        data_student2 = Student.objects.filter(id_student=data[0]).first()
        data_student1 = data_student[0].student_name + " "+data_student[0].student_surname
        data1 = list(data.values())
        return JsonResponse({"id_user": data1, "name": data_student1 , "choose" : data_student2.deparment_id.deparment_name}, safe=False)


@csrf_exempt
def getInfoStudent(requset):
    if requset.method == "POST":
        mydata = json.loads(requset.body)
        data = UserLogin.objects.filter(token=mydata['token'])
        data_student = Student.objects.filter(id_student=data[0])
        data_student1 = list(data_student.values())
        name_faculty = Faculty.objects.filter(
            faculty_id=data_student1[0]['faculty_id_id'])
        name_faculty1 = list(name_faculty.values())
        data_student1[0].update({"faculty": name_faculty1[0]['faculty_name']})
        name_deparment = Deparment.objects.filter(
            deparment_id=data_student1[0]['deparment_id_id'])
        name_deparment1 = list(name_deparment.values())
        data_student1[0].update(
            {"deparment": name_deparment1[0]['deparment_name']})
        return JsonResponse({"student": data_student1}, safe=False)


def getCalender(requset):
    if requset.method == "GET":
        timenow = datetime.datetime.now()
        time30d = datetime.datetime.now() + datetime.timedelta(days=150)
        data = Calender.objects.filter(end_date__range=(timenow, time30d)).order_by('start_date')
        arDate = []
        i = 0
        for d in data:
            arDate.append({"id":i,"title":d.title,"start_date":d.start_date,"end_date":d.end_date})
            i += 1
        data_date = list(arDate)
        return JsonResponse({"date": data_date}, safe=False)

@csrf_exempt
def getStudyResults(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        all_regissubject = []
        student = Student.objects.filter(id_student=userlogin.username).first()
        dateSystem = DateSystem.objects.all().first()
        entryYear = student.yaer_of_entry
        currentTerm = dateSystem.system_term
        boo = False

        while entryYear <= dateSystem.system_yaer:
            for i in range(3):
                if (i+1) > currentTerm and dateSystem.system_yaer <= entryYear:
                    boo = True
                    break
                regis = RegisterSubject.objects.filter(student=student,yaer=entryYear,term=i+1)
                sub = []
                if regis:
                    for re in regis:
                        sub.append({'id':re.subject.id_subject,'name':re.subject.subjectName,'credit':re.subject.credit,'grade':re.grade})
                    all_regissubject.append({'year':entryYear,'term':i+1,'id_subject':sub})
        
            if boo :
                break
            entryYear += 1
        all_regissubject1 = list(all_regissubject)
        return JsonResponse({'subject':all_regissubject1}, safe=False)


@csrf_exempt
def getTableSubject(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        student = Student.objects.filter(id_student=userlogin.username).first()
        dateSystem = DateSystem.objects.get(id_date=2)
        regis = RegisterSubject.objects.filter(student=student,yaer=dateSystem.system_yaer,term=dateSystem.system_term)
        allSub = [] 
        for re in regis :
            test = TimetableSubject.objects.filter(subject=re.subject)
            for te in test:
                starttime = te.start_date
                endtime = te.end_date
                stoptime = dateSystem.end_date
                while starttime < stoptime :
                    allSub.append({"title" : te.subject.subjectName ,"start":starttime,"end":endtime,"description":te.room})
                    starttime += datetime.timedelta(days=7)
                    endtime += datetime.timedelta(days=7)
        allS = list(allSub)
        return JsonResponse({'subject' : allS},safe=False)



@csrf_exempt
def getTestSubject(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        student = Student.objects.filter(id_student=userlogin.username).first()
        dateSystem = DateSystem.objects.get(id_date=2)
        dateyear = dateSystem.system_yaer
        allSub = [] 
        boo = False
        while dateyear >= student.yaer_of_entry:
            term = 3
            while term > 0 :
                
                regis = RegisterSubject.objects.filter(student=student,yaer=dateyear,term=term)
                if regis:
                    print (dateyear)
                    print (term)
                
                    for re in regis:
                        sub = TestSubject.objects.filter(subject=re.subject)
                        for s in sub:
                            allSub.append({"title" : s.subject.subjectName ,"start":s.start_date,"end":s.end_date,"description":s.room})
                    boo = True
                    break
                else:
                    term -= 1

            if boo :
                break
            dateyear -= 1
        allS = list(allSub)
        return JsonResponse({'subject' : allS},safe=False)
        


@csrf_exempt
def getCourseStudent(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        choose = tokenjson['choose']
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
        all_subject = CourseSubject.objects.filter(
            deparment=student.deparment_id,choose=choose)
        for a in all_subject:
            data_subject = {}
            key = Subject.objects.filter(
                id_subject=a.subject.id_subject).first()
            data_subject.update({"key": key.id_subject})
            data_subject.update({"name": key.subjectName})
            data_subject.update({"group": a.group})
            register = RegisterSubject.objects.filter(
                student=student, subject=key)

            if(len(register)>1):
                boo = True
                for re in register:
                    if (re.grade != "f" and  re.grade !="F" and re.grade !="-" and 
                    re.grade !="W" and re.grade !="w" and re.grade != "i" and re.grade != "I") :
                        data_subject.update({"grade": 1})
                        boo = False
                        break

                    elif re.grade == "-" or re.grade =="i" or re.grade == "I":
                        data_subject.update({"grade": -2})
                        boo = False
                        break
                        
                
                if boo :
                    data_subject.update({"grade": -1})
                

            elif(register):
                if register[0].grade == "f" or register[0].grade == "F" or register[0].grade == "w" or register[0].grade == "W":
                    data_subject.update({"grade": -1})

                elif register[0].grade == "-" or register[0].grade == "i" or register[0].grade == "I":
                    data_subject.update({"grade": -2})

                else:
                    data_subject.update({"grade": 1})

            else:
                data_subject.update({"grade": 0})

            data_allsubject.append(data_subject)

        data_allsubject1 = list(data_allsubject)
        return JsonResponse({"nodeDataArray": data_allsubject1}, safe=False)



@csrf_exempt
def getConditionSubject(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        choose = tokenjson['choose']
        userlogin = UserLogin.objects.filter(token=token).first()
        all_presubject = []
        student = Student.objects.filter(id_student=userlogin.username).first()
        all_subject = CourseSubject.objects.filter(
            deparment=student.deparment_id,choose=choose)
        for a in all_subject:
            con = PreSubject.objects.filter(condition=a.subject.id_subject)

            if con:
                for c in con:
                    pre = {}
                    pre.update({"from": a.subject.id_subject})
                    pre.update({"to": c.subject.id_subject})
                    all_presubject.append(pre)

        all_presubject1 = list(all_presubject)
        return JsonResponse({"linkDataArray": all_presubject1}, safe=False)

@csrf_exempt
def getOptionSubject(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        userlogin = UserLogin.objects.filter(token=token).first()
        student = Student.objects.filter(id_student=userlogin.username).first()
        subject4 = OptionSubject.objects.filter(deparment=student.deparment_id)
        subject41 = []
        for s in subject4:
            subject41.append({'id':s.subject.id_subject,'name':s.subject.subjectName,'credit':s.subject.credit})
        subject41 = list(subject41)

        g1 = GroupSubject.objects.filter(name_group = "เสรี").first()
        subject1 = OptionSubject.objects.filter(group=g1)
        subject11 = []
        for s in subject1:
            subject11.append({'id':s.subject.id_subject,'name':s.subject.subjectName,'credit':s.subject.credit})
        subject11 = list(subject11)

        g2 = GroupSubject.objects.filter(name_group = "กำหนดโดยคณะวิทยาศาสตร์").first()
        subject2 = OptionSubject.objects.filter(group=g2)
        subject21 = []
        for s in subject2:
            subject21.append({'id':s.subject.id_subject,'name':s.subject.subjectName,'credit':s.subject.credit})
        subject21 = list(subject21)

        g3 = GroupSubject.objects.filter(name_group = "ศึกษาทั่วไป").first()
        subject3 = OptionSubject.objects.filter(group=g3)
        subject31 = []
        for s in subject3:
            subject31.append({'id':s.subject.id_subject,'name':s.subject.subjectName,'credit':s.subject.credit})
        subject31 = list(subject31)
        return JsonResponse({'free':subject11,'sci':subject21,'general':subject31,'maj':subject41}, safe=False)


@csrf_exempt
def getGuide(requset):
    if requset.method == "POST":
        tokenjson = json.loads(requset.body)
        token = tokenjson['token']
        choose = tokenjson['choose']
        nodeSubject = algorithm(token,choose)
        nodeSubject1 = list(nodeSubject)
        return JsonResponse({'nodeSubject':nodeSubject1}, safe=False)


def algorithm(token,choose):
    class Subject():

        def __init__(self, id_sub, name, weight, stet,
                    condition, year, term, credit, consub):
            self.id_sub = id_sub
            self.name = name
            self.weight = weight
            self.stet = stet
            self.condition = condition
            self.year = year
            self.term = term
            self.credit = credit
            self.consub = consub

        def __repr__(self):
            return '<{}: {} : {}>'.format(self.name, self.weight, self.id_sub)

        def __lt__(self, other):
            if not isinstance(other, Subject):
                return self > other
            return self.weight > other.weight


    allSub = []
    userlogin = UserLogin.objects.filter(token=token).first()
    student = Student.objects.filter(id_student=userlogin.username).first()
    con = ConditionJSON.objects.filter(deparment=student.deparment_id,choose=choose).first()
    inputCourseJSON = con.conditionJSON
    courseJSON = json.loads(inputCourseJSON)
    for s in courseJSON:
        if len(s["condition"]) > 0 and s["condition"][0] == "*":
            consub = s["consub"]
        else:
            consub = []
        allSub.append(Subject(s["id"], s["name"], s["weight"], "notpass", s["condition"], s["year"], [
                    s["team1"], s["team2"], s["team3"]], s["credit"], consub))

    
    dateSystem = DateSystem.objects.all().first()
    currentYear = dateSystem.system_yaer - student.yaer_of_entry + 1
    currentTerm = dateSystem.system_term
    RegisSub = RegisterSubject.objects.filter(student=student)
    groupYaer = []
    groupTerm = []
    JSONPass = []
    arrRegis = []

    


    for r in RegisSub:
        if r.grade != "f" and r.grade != "F" and r.grade != "W" and r.grade != "w" and r.grade != "U":
            if r.grade == "-" or r.grade == "I" or r.grade == "i":
                if r.yaer < dateSystem.system_yaer:
                    JSONPass.append({"id":r.subject.id_subject})

                elif r.yaer == dateSystem.system_yaer and r.term < dateSystem.system_term:
                    JSONPass.append({"id":r.subject.id_subject})
            else:
                JSONPass.append({"id":r.subject.id_subject})
        

    for i in JSONPass:
        for j in allSub:
            if i["id"] == j.id_sub:
                j.stet = "pass"


    class TermRegister():
        def __init__(self):
            self.term = 0
            self.year = 0
            self.subject = []
            self.credit = 0

        def __repr__(self):
            return '<{} : {} : {} : {}>'.format(self.year, self.term, self.subject, self.credit)


    
    notPassed = []
    passed = []
    for i in allSub:
        if i.stet == "pass":
            passed.append(i)

        else:
            notPassed.append(i)

    boolBrake = False
    # boolBrake1 = True
    for i in range(currentYear):
        # register1 = RegisterSubject.objects.filter(student=student, yaer=student.yaer_of_entry + i)
        # if register1:
        if i+1 == currentYear and len(notPassed)<1:
            reSub1 = RegisterSubject.objects.filter(student=student, yaer=student.yaer_of_entry + i, term=1)
            reSub2 = RegisterSubject.objects.filter(student=student, yaer=student.yaer_of_entry + i, term=1)
            reSub3 = RegisterSubject.objects.filter(student=student, yaer=student.yaer_of_entry + i, term=1)
            
            if reSub1 or reSub2 or reSub3:
                groupYaer.append({'key' : i+1 , 'isGroup' : 'true' ,'text' : 'ปีการศึกษาปีที่ '+str(i+1) , 'horiz': 'true'})
        
        else:
            groupYaer.append({'key' : i+1 , 'isGroup' : 'true' ,'text' : 'ปีการศึกษาปีที่ '+str(i+1) , 'horiz': 'true'})
            # boolBrake1 = False
        for y in range(3):
            if i+1 == currentYear and y+1 == currentTerm:
                boolBrake = True
                break

            register = RegisterSubject.objects.filter(student=student, yaer=student.yaer_of_entry + i, term=y+1)
            # print("**************")
            # print(student.yaer_of_entry + i)
            # print(y+1)
            if register:
                # print("----------------")
                # print(student.yaer_of_entry + i)
                # print(y+1)
                groupTerm.append({ 'key':str(i+1)+''+str(y+1), 'isGroup': 'true', 'text': "เทอม"+str(y+1), 'group': str(i+1) })
                
                for re in register:
                    if re.grade != 'f' and re.grade != 'F' and re.grade != 'W'and re.grade != 'w'and re.grade != 'i'and re.grade != 'I'and re.grade != '-':
                        arrRegis.append({'text':re.subject.id_subject+' '+re.subject.subjectName,'group':str(i+1)+''+str(y+1),'check':1})
                    
                    elif re.grade == 'i' or re.grade == 'I' or re.grade == '-':
                        arrRegis.append({'text':re.subject.id_subject+' '+re.subject.subjectName,'group':str(i+1)+''+str(y+1),'check':-2}) 
            
                    
                    else:
                        arrRegis.append({'text':re.subject.id_subject+' '+re.subject.subjectName,'group':str(i+1)+''+str(y+1),'check':-1})
            
                    
        
        if boolBrake:
            break


    notPassed.sort()

    countYear = currentYear
    kkk = 0
    countTerm = 1
    boolBrake = False
    while countYear <= 8:
        print(notPassed)
        if len(notPassed) == 0:
            break

        if kkk == 0:
            countTerm = currentTerm
            kkk += 1
        else:
            countTerm = 1

        while countTerm <= 3:

            if len(notPassed) == 0:
                break


            termRegister = TermRegister()
            termRegister.year = countYear
            termRegister.term = countTerm

            notPassed2 = notPassed.copy()

            for x in notPassed2:

                if termRegister.credit + x.credit >= 22:
                    break

                con = True

                if len(x.condition) > 0:
                    if x.condition[0] == "*":
                        countSubNotPass = len(x.consub)-1
                        for i in x.consub:
                            for j in notPassed2:
                                if i == j.id_sub:
                                    countSubNotPass -= 1

                        if int(x.consub[0]) > countSubNotPass:
                            con = False
                            continue

                    for i in notPassed2:
                        for j in x.condition:
                            if j == i.id_sub:
                                con = False

                if ((x.year <= countYear and
                        bool(x.term[countTerm-1]) and con) or (len(x.condition) > 0 and x.condition[0] == "*" and con and bool(x.term[countTerm-1]))):
                    termRegister.subject.append(x)
                    termRegister.credit += x.credit
                    passed.append(x)
                    notPassed.remove(x)

            
            if termRegister.credit != 0:
                for re in termRegister.subject:
                    if len(re.condition)>0 and re.condition[0] == "#":
                        arrRegis.append({'text':re.id_sub+' '+re.name,'group':str(countYear)+''+str(countTerm),'check':2})
                    
                    else:
                        arrRegis.append({'text':re.id_sub+' '+re.name,'group':str(countYear)+''+str(countTerm),'check':0})
                

                groupTerm.append({ 'key':str(countYear)+''+str(countTerm), 'isGroup': 'true', 'text': "เทอม"+str(countTerm), 'group': countYear })
                print(termRegister)
            
            countTerm += 1
        if boolBrake :
            groupYaer.append({'key': countYear, 'isGroup': 'true', 'text': "ปีการศึกษาปีที่ "+str(countYear), 'horiz': 'true'})

        boolBrake = True    
        countYear += 1
    # print("***************************")    
    # print(groupYaer)
    # print("***************************")    
    # print(groupTerm)
    # print("***************************")    
    # print(arrRegis)
    return groupYaer+groupTerm+arrRegis
    
    

