from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from applicants.models import Applicant
from schemes.models import Scheme,SchemeCriteria
from .models import Application
from .serializers import ApplicationSerializer,CreateApplicationSerializer


# Create your views here.
class ApplicationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def get(self,request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CreateApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Successfully submitted application"}, status=status.HTTP_201_CREATED)
        return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

