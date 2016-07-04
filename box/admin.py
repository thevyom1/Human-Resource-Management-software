from django.contrib import admin
from .models import Vehicle,Feedback,Employee_Gmail,Employee_Private,Employee_Public,Interviewee

admin.site.register(Vehicle)
admin.site.register(Employee_Gmail)
admin.site.register(Feedback)
admin.site.register(Interviewee)
admin.site.register(Employee_Private)
admin.site.register(Employee_Public)




# Register your models here.
