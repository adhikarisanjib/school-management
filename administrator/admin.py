from django.contrib import admin

from administrator.models import (
    AcademicSession,
    Address,
    Assign,
    Class,
    Course,
    Department,
    Staff,
    Student,
    Subject,
    TimeSlot,
)

admin.site.register(AcademicSession)
admin.site.register(Address)
admin.site.register(Assign)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(TimeSlot)
