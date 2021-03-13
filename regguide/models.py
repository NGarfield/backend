from django.db import models

class Subject(models.Model):
    id_subject = models.CharField(max_length=10)
    subjectName = models.CharField(max_length=70)
    belongTo = models.CharField(max_length = 50)
    credit = models.IntegerField()
    name_group = models.IntegerField()
    def __str__(self):
        return f"{self.id_subject} {self.subjectName}"
