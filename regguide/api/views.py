from rest_framework import generics
from regguide.models import Subject
import json
from django.http import HttpResponse,JsonResponse

# class SubjectListCreateAPIView(generics.ListCreateAPIView):
#     # queryset = Subject.objects.filter(name_group_id=2)
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializers

def SubjectListCreateAPIView(request):
    if request.method=="GET":
        queryset = Subject.objects.all()
        print(queryset)
        data3 = list(queryset.values())
        return JsonResponse( data3, safe=False)
