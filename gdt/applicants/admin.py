from django.contrib import admin
from .models import Applicant,FamilyMember

# Register your models here.
class ApplicantAdmin(admin.ModelAdmin):
    list_displays = ('nric','name','employment_status','gender','date_of_birth','education','marital_status')
    fields =['nric','name','employment_status','gender','date_of_birth','education','marital_status']

class FamilyMemberAdmin(admin.ModelAdmin):
    list_displays=('main_applicant','sub_applicant','relation')

admin.site.register(Applicant,ApplicantAdmin)
admin.site.register(FamilyMember,FamilyMemberAdmin)