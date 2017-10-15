from django.contrib import admin

# Register your models here.

from mms.models import *

admin.site.register(UserList)
admin.site.register(Campus)
admin.site.register(StudentInfoCollect)
