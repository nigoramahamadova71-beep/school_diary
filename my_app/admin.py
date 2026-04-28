from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Schedule)
admin.site.register(Users)
admin.site.register(Subjects)
admin.site.register(Grades)
admin.site.register(Attendance)
admin.site.register(Payment)