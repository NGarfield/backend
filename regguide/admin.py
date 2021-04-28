from django.contrib import admin
from regguide.models import (Subject,
                            PreSubject,
                            Deparment,
                            Faculty,
                            Student,
                            TimetableSubject,
                            TestSubject,
                            Calender,
                            UserLogin,
                            ConditionJSON,
                            RegisterSubject,
                            CourseSubject,
                            DateSystem,
                            OptionSubject,
                            GroupSubject)

admin.site.register(Subject)
admin.site.register(PreSubject)
admin.site.register(Deparment)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(TimetableSubject)
admin.site.register(TestSubject)
admin.site.register(Calender)
admin.site.register(UserLogin)
admin.site.register(ConditionJSON)
admin.site.register(RegisterSubject)
admin.site.register(CourseSubject)
admin.site.register(DateSystem)
admin.site.register(OptionSubject)
admin.site.register(GroupSubject)
