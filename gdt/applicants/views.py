from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Applicant
from .serializers import AddApplicantSerializer,BasicApplicantsSerializer
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


# Create your views here.

class ApplicantView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        applicants = Applicant.objects.all()
        serializer = BasicApplicantsSerializer(applicants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = AddApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,nric=None):
        if nric is None:
            return Response({"error":"NRIC required."}, status=status.HTTP_400_BAD_REQUEST)
        applicant = get_object_or_404(Applicant,nric=nric)
        serializer = BasicApplicantsSerializer(applicant,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.update(applicant, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateApplicantView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def patch(self,request):
        serializer = AddApplicantSerializer(data=request.data)
        print(serializer.is_valid())
        serializer.update()

