from django.db import models
from enum import Enum
import uuid
import json

# Create your models here.

class EMPLOYMENT(Enum):
    EMPLOYED="EMPLOYED"
    UNEMPLOYED="UNEMPLOYED"

class GENDER(Enum):
    MALE = "MALE"
    FEMALE="FEMALE"
    UNSPECIFIED="UNSPECIFIED"

class MARITAL_STATUS(Enum):
    SINGLE= "SINGLE"
    MARRIED= "MARRIED"
    DIVORCED="DIVORCED"
    WIDOWED="WIDOWED"

class Applicant(models.Model):
    nric = models.CharField(max_length=9,primary_key=True)
    name = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    marital_status = models.CharField(
        max_length=10, 
        choices=[(status.name, status.value) for status in MARITAL_STATUS],
        default=MARITAL_STATUS.SINGLE
    )
    employment_status = models.CharField(
        max_length=10, 
        choices=[(status.name, status.value) for status in EMPLOYMENT],
        default=EMPLOYMENT.UNEMPLOYED
    )
    gender=models.CharField(
        max_length=11, 
        choices=[(status.name, status.value) for status in GENDER],
        default=GENDER.UNSPECIFIED
    )
    date_of_birth = models.DateField()
    household = models.ManyToManyField('self', through='FamilyMember', symmetrical=False, related_name='main_applicant')

    def to_dict(self):
        household=[]
        for h in self.household.all():
            household.append({
                 "nric":h.nric,
                "name":h.name,
                "employment_status":h.employment_status,
                "gender":h.gender,
                "date_of_birth":h.date_of_birth.strftime('%d/%m/%Y'),
                "education":h.education,
                "marital_status":h.marital_status,
            })
        return {
            "nric":self.nric,
            "name":self.name,
            "employment_status":self.employment_status,
            "gender":self.gender,
            "date_of_birth":self.date_of_birth.strftime('%d/%m/%Y'),
            "education":self.education,
            "marital_status":self.marital_status,
            "household":household
        }


class FamilyMember(models.Model):
    main_applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,related_name="sub_applicants")
    sub_applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,related_name="main_applicants")
    relation = models.CharField(max_length=100,blank=False,null=False)
    class Meta:
        unique_together = ('main_applicant', 'sub_applicant','relation')

