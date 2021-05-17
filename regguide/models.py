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
    total_credit = models.IntegerField(null=True)
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
    level_education = models.CharField(max_length=50,blank=True)
    name_education = models.CharField(max_length=100,blank=True)
    email = models.CharField(max_length=100,blank=True)
    campus = models.CharField(max_length=100,blank=True)
    yaer_of_entry = models.IntegerField(blank=True, null=True)
    term_of_entry = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_student} {self.student_name}"

class TimetableSubject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    room = models.CharField(max_length=50,blank=True)
    term = models.IntegerField(null=True)
    yaer = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.subject}"
    

class TestSubject(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    midterm = models.BooleanField(blank=True)
    finalterm = models.BooleanField(blank=True)
    room = models.CharField(max_length=50,blank=True)
    term = models.IntegerField(null=True)
    yaer = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.subject} {self.term} {self.yaer}"

class Calender(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    def __str__(self):
        return self.title

class ConditionJSON(models.Model):
    deparment = models.ForeignKey(Deparment, on_delete=models.CASCADE)
    conditionJSON = models.TextField(default="")
    choose = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.deparment}"
    
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
    grade = models.CharField(max_length=2)
    yaer = models.IntegerField(null=True)
    term = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.student} {self.subject} {self.yaer} {self.term}"

class CourseSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    deparment = models.ForeignKey(Deparment, on_delete=models.CASCADE)
    group = models.IntegerField()
    def __str__(self):
        return f"{self.subject}"

class DateSystem(models.Model):
    id_date = models.CharField(max_length=1,primary_key=True)
    system_yaer = models.IntegerField()
    system_term = models.IntegerField()
    end_date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.system_yaer} {self.system_term}"

class GroupSubject(models.Model):
    name_group = models.CharField(max_length=200)
    credit = models.IntegerField()
    deparment = models.ForeignKey(Deparment, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name_group} {self.deparment}"

class OptionSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupSubject, on_delete=models.CASCADE)
    deparment = models.ForeignKey(Deparment,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.subject} {self.group} {self.deparment}"

class AllImage(models.Model):
    page = models.IntegerField()
    image = models.TextField()
    def __str__(self):
        return f"{self.page} {self.image}"
