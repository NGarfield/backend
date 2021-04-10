from django.urls import path
from regguide.api.views import (SubjectListCreateAPIView,login,ssoAPI,sessionTotoken,
                                validateToken,getUser,)

urlpatterns = [
    path("subjects/",SubjectListCreateAPIView, name="subject-list"),
    path("login/",login, name="login"),
    path("ssoapi/",ssoAPI, name="ssoAPI"),
    path("sessiontotoken/",sessionTotoken, name="sessionTotoken"),
    path("validatetoken/",validateToken, name="validateToken"),
    path("getuser/",getUser, name="getUser"),

    
]