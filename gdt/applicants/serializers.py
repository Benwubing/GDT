from rest_framework import serializers
from .models import Applicant,EMPLOYMENT,GENDER,FamilyMember
from datetime import date


#Used for GET/PATCH Applicant methods
class BasicApplicantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields=(
            "nric",
            "name",
            "employment_status",
            "gender",
            "date_of_birth",
            "marital_status",
            "education"
        )
    def update(self,instance,validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

#Used for POST Applicant methods
class SubApplicantSerializer(serializers.ModelSerializer):
    relation=serializers.CharField(max_length=25,write_only=True)
    
    class Meta:
        model = Applicant
        fields=(
            "nric",
            "name",
            "employment_status",
            "gender",
            "date_of_birth",
            "relation"
        )

    def validate_gender(self,value):
        if value not in GENDER._value2member_map_:
            raise serializers.ValidationError("Error saving gender")
        return value

    def validate_employment_status(self, value):
        if value not in EMPLOYMENT._value2member_map_:
            raise serializers.ValidationError("Invalid employment status")
        return value
        
    def validate_date_of_birth(self,value):
        if value >date.today():
            raise serializers.ValidationError("Date of birth cannot be later than current date")
        return value

class AddApplicantSerializer(serializers.ModelSerializer):
    household = SubApplicantSerializer(many=True)
    class Meta:
        model = Applicant
        fields=(
            "nric",
            "name",
            "employment_status",
            "gender",
            "date_of_birth",
            "household"
        )

    def create(self, validated_data):
        sub_applicants = validated_data.pop('household', [])
        main_applicant = Applicant.objects.create(**validated_data)

        # Create child Person objects with relationships
        for sub_applicant in sub_applicants:
            relation = sub_applicant.get('relation')
            s = Applicant.objects.create(
                nric=sub_applicant.get("nric"),
                name=sub_applicant.get("name"),
                employment_status=sub_applicant.get("employment_status"),
                gender=sub_applicant.get("gender"),
                date_of_birth=sub_applicant.get("date_of_birth")
            )
            FamilyMember.objects.create(
                main_applicant=main_applicant, 
                sub_applicant=s, 
                relation=relation
            )
        return main_applicant
    

        








