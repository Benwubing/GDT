from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Scheme
from .serializers import BasicSchemeSerializer,FullSchemeSerializer,CreateSchemeSerializer
from applicants.models import Applicant,FamilyMember
from applicants.serializers import BasicApplicantsSerializer
from django.core import serializers

# Create your views here.

class SchemeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        schemes = Scheme.objects.all()
        serializer=FullSchemeSerializer(schemes,many=True)
        return Response({"schemes":serializer.data}, status=status.HTTP_200_OK)
    
    # def post(self,request):
    #     serializer = CreateSchemeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED) 
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SchemeEligibilityView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        schemes = Scheme.objects.all()
        applicant_id = request.query_params.get('applicant')
        if not applicant_id:
            return Response({"error": "Applicant ID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            applicant = Applicant.objects.get(nric=applicant_id)
            applicant_json = applicant.to_dict()

            # Evaluate all schemes
            eligible_schemes=[]

            for scheme in schemes.iterator():
                if scheme.is_eligible(applicant_json):
                    eligible_schemes.append(BasicSchemeSerializer(scheme).data)

            return Response({"applicant":BasicApplicantsSerializer(applicant).data,"eligible_schemes":eligible_schemes}, status=status.HTTP_200_OK)
        except Applicant.DoesNotExist:
            return Response({"error": "Applicant does not exist"}, status=status.HTTP_404_NOT_FOUND)
        