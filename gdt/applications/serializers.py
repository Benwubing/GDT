from rest_framework import serializers
from .models import Application,APPLICATION_STATUS
from applicants.models import Applicant
from schemes.models import Scheme
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields="__all__"

class CreateApplicationSerializer(serializers.ModelSerializer):
    nric = serializers.CharField(max_length=9,write_only=True)
    scheme = serializers.CharField(max_length=200,write_only=True)

    class Meta:
        model=Application
        fields=["nric","scheme"]
        extra_kwargs = {
            'nric': {'write_only': True},
            'scheme': {'write_only': True}
        }
    

    def create(self,validated_data):
        applicant = Applicant.objects.get(nric=validated_data["nric"])
        scheme =Scheme.objects.get(name=validated_data["scheme"])

        if applicant and scheme:
            if scheme.is_eligible(applicant.to_dict()):
                try:
                    obj = Application.objects.create(applicant=applicant,scheme=scheme,status=APPLICATION_STATUS.SUBMITTED)
                    obj.save()
                    return obj
                except IntegrityError:
                    raise ValidationError("Application already submitted")
            else:
                raise ValidationError("Applicant is not eligible")
        else:
            raise ValidationError("Applicant or scheme not found")
        