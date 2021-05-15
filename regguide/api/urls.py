from django.urls import path
from regguide.api.views import (SubjectListCreateAPIView,login,ssoAPI,sessionTotoken,
                                validateToken,getUser,getInfoStudent,getCalender,getCourseStudent,
                                getConditionSubject,getGuide,getOptionSubject,getStudyResults,
                                getTestSubject,getTableSubject)

urlpatterns = [
    path("subjects/",SubjectListCreateAPIView, name="subject-list"),
    path("login/",login, name="login"),
    path("ssoapi/",ssoAPI, name="ssoAPI"),
    path("sessiontotoken/",sessionTotoken, name="sessionTotoken"),
    path("validatetoken/",validateToken, name="validateToken"),
    path("getuser/",getUser, name="getUser"),
    path("getinfostudent/",getInfoStudent, name="getInfoStudent"),
    path("getcalender/",getCalender, name="getCalender"),
    path("getcoursestudent/",getCourseStudent, name="getCourseStudent"),
    path("getconditionsubject/",getConditionSubject, name="getConditionSubject"),
    path("getguide/",getGuide, name="getGuide"),
    path("getoptionsubject/",getOptionSubject, name="getOptionSubject"),
    path("getstudyresults/",getStudyResults, name="getStudyResults"),
    path("gettestsubject/",getTestSubject, name="getTestSubject"),
    path("gettablesubject/",getTableSubject, name="getTableSubject"),

]