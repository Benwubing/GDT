from django.contrib import admin
from .models import Application

# Register your models here.
class ApplicationAdmin(admin.ModelAdmin):
    list_displays=("applicant","scheme","status")
    fields=["applicant","scheme","status"]


admin.site.register(Application,ApplicationAdmin)