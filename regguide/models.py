from django.db import models

class Subject(models.Model):
    id_subject = models.CharField(max_length=6,primary_key=True)
    subjectName = models.CharField(max_length=70)
    credit = models.IntegerField()

    def __str__(self):
        return f"{self.id_subject} {self.subjectName}"

class PreSubject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    condition = models.CharField(max_length=6,blank=True)
    def __str__(self):
        return f"{self.subject} {self.condition}"

class Deparment(models.Model):
    deparment_id = models.CharField(max_length=10,primary_key=True)
    deparment_name = models.CharField(max_length=50)
    def __str__(self):
        return self.deparment_name
    

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=3,primary_key=True)
    faculty_name = models.CharField(max_length=100)
    def __str__(self):
        return self.faculty_name


class Student(models.Model):
    id_student = models.CharField(max_length=10,primary_key=True)
    student_name = models.CharField(max_length=60)
    student_surname = models.CharField(max_length=60)
    citizen_id = models.CharField(max_length=13)
    birthday = models.DateField()
    gpax = models.FloatField()
    credit = models.IntegerField()
    faculty_id = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    deparment_id = models.ForeignKey(Deparment, on_delete=models.CASCADE)
    image_student = models.TextField() 

    def __str__(self):
        return f"{self.id_student} {self.student_name}"

class TimetableSubject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    def __str__(self):
        return self.subject
    

class TestSubject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    midterm = models.BooleanField(blank=True)
    finalterm = models.BooleanField(blank=True)
    def __str__(self):
        return self.subject

class Calender(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    def __str__(self):
        return self.title

class ConditionJSON(models.Model):
    deparment = models.ForeignKey(Deparment, on_delete=models.CASCADE)
    conditionJSON = models.TextField(default="")
    def __str__(self):
        return self.deparment
    
class UserLogin(models.Model):
    username = models.CharField(max_length=10,primary_key=True)
    password = models.CharField(max_length=20)
    token = models.CharField(max_length=50,blank=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.username

class RegisterSubject(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)
    def __str__(self):
        return f"{self.student} {self.subject}"


