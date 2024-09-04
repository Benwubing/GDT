from rest_framework import serializers
from .models import CriteriaSet,Scheme,SchemeCriteria,SchemeGeneralBenefit,SchemeNumericBenefit

class SchemeCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchemeCriteria
        fields="__all__"

class CreateSchemeCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchemeCriteria
        fields=["criteria_field","criteria_field_type","criteria_operator","compare_value"]


class CriteriaSetSerializer(serializers.ModelSerializer):
    criterias = SchemeCriteriaSerializer(many=True)
    children = serializers.ListSerializer(child=serializers.DictField(), write_only=True, allow_empty=True, required=False)

    class Meta:
        model=CriteriaSet
        fields="__all__"

    def create(self,validated_data):
        children  = validated_data.pop('children',[])
        criteria_set = CriteriaSet.objects.create(**validated_data)

        #Create child criteria sets
        for child_data in children:
            child_serializer = CriteriaSetSerializer(data=child_data)
            if child_serializer.is_valid():
                child_serializer.save(parent=criteria_set)
            else:
                raise serializers.ValidationError(child_serializer.errors)
        
        criterias = validated_data.pop('criterias',[])
        for c in criterias:
            criteria_serializer = CreateSchemeCriteriaSerializer(data=c)
            if criteria_serializer.is_valid():
                criteria_serializer.save(criteria_set=criteria_set)
        return criteria_set

class SchemeGeneralBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeGeneralBenefit
        fields=(
            "name","description"
        )

class SchemeNumericBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeNumericBenefit
        fields=("name","amount")

class BasicSchemeSerializer(serializers.ModelSerializer):
    benefits = SchemeGeneralBenefitSerializer(many=True)
    num_benefits = SchemeNumericBenefitSerializer(many=True)

    class Meta:
        model=Scheme
        fields="__all__"

class FullSchemeSerializer(serializers.ModelSerializer):
    criteria_sets = CriteriaSetSerializer(many=True)
    benefits = SchemeGeneralBenefitSerializer(many=True)
    num_benefits = SchemeNumericBenefitSerializer(many=True)

    class Meta:
        model=Scheme
        fields="__all__"

class CreateSchemeSerializer(serializers.ModelSerializer):
    criteria_sets = serializers.ListSerializer(child=serializers.DictField(), write_only=True, allow_empty=True, required=False)
    benefits = SchemeGeneralBenefitSerializer(many=True)
    num_benefits = SchemeNumericBenefitSerializer(many=True)

    class Meta:
        model=Scheme
        fields=["name","criteria_sets","benefits","num_benefits"]

    def create(self,validated_data):
        scheme = Scheme.objects.create(**validated_data)

        criteria_sets_data = validated_data.pop('criteria_sets',[])
        benefits_data = validated_data.pop('benefits',[])
        num_benefits_data = validated_data.pop('num_benefits',[])

        # Create Criteria sets
        for criteria_set_data in criteria_sets_data:
            criteria_set_serializer = CriteriaSetSerializer(criteria_set_data)
            if criteria_set_serializer.is_valid():
                criteria_set_serializer.save(scheme=scheme)
            else:
                raise serializers.ValidationError(criteria_set_serializer.errors)
            
        # Create benefits
        for benefits_data in benefits_data:
            SchemeGeneralBenefit.objects.create(
                scheme=scheme,
                name=benefits_data.get("name"),
                description=benefits_data.get("description")
            )

        # Create num_benefits
        for benefits_data in num_benefits_data:
            SchemeNumericBenefit.objects.create(
                scheme=scheme,
                name=benefits_data.get("name"),
                amount=benefits_data.get("amount")
            )

        return scheme




    
