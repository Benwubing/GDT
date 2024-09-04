from django.db import models
from applicants.models import Applicant,FamilyMember
from schemes.models import Scheme
from enum import Enum
# Create your models here.

class APPLICATION_STATUS(Enum):
    PENDING="PENDING"
    SUBMITTED="SUBMITTED"
    APPROVED="APPROVED"
    REJECTED="REJECTED"

class Application(models.Model):
    applicant = models.ForeignKey(Applicant,on_delete=models.CASCADE,related_name="applications")
    scheme = models.ForeignKey(Scheme,on_delete=models.CASCADE,related_name="applications")
    status = models.CharField(
        max_length=10, 
        choices=[(status.name, status.value) for status in APPLICATION_STATUS],
        default=APPLICATION_STATUS.SUBMITTED
    )
    class Meta:
        unique_together=("applicant","scheme")

    