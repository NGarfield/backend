from django.urls import path
from regguide.api.views import SubjectListCreateAPIView

urlpatterns = [
    path("subjects/",SubjectListCreateAPIView, name="subject-list"),
    
]