from django.contrib import admin
from .models import Scheme,SchemeCriteria,SchemeGeneralBenefit,SchemeNumericBenefit,CriteriaSet

# Register your models here.

class SchemeCriteriaInline(admin.TabularInline):
    model=SchemeCriteria
    extra=0


class CriteriaSetAdmin(admin.ModelAdmin):
    inlines=[SchemeCriteriaInline]
    list_displays=('set_operator','parent','scheme')

class CriteriaSetInline(admin.TabularInline):
    model=CriteriaSet
    extra=0

class SchemeGeneralBenefitInline(admin.TabularInline):
    model=SchemeGeneralBenefit
    extra=0

class SchemeNumericBenefitInline(admin.TabularInline):
   model=SchemeNumericBenefit
   extra=0

class SchemeAdmin(admin.ModelAdmin):
    inlines =[CriteriaSetInline,SchemeGeneralBenefitInline,SchemeNumericBenefitInline]
    list_displays=('name')
    fields=['name']



admin.site.register(Scheme,SchemeAdmin)
admin.site.register(CriteriaSet,CriteriaSetAdmin)
