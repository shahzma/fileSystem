from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from. serializers import UserSerializer, ReportVersionSerializer, ReportSerializer, ReportUserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from . import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
from . base_functions import get_token
import requests
import json

# Create your views here.




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReportLCView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportSerializer
    queryset = models.ReportModel.objects


class ReportVersionLCView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportVersionSerializer
    queryset = models.ReportVersionModel.objects

    def get_queryset(self):
        query_params = self.request.query_params
        # change to report name
        report_name = query_params['report_name']
        report_id = models.ReportModel.objects.filter(report_name=report_name).first()
        # report_version_name = query_params["report_version_name"]
        return self.queryset.filter(report=report_id)


    def create(self, request, *args, **kwargs):
        report_name = self.request.data['report']
        report_version_name = self.request.data['report_version_name']+'.xlsx'
        file = self.request.data['file']
        token2 = get_token()
        headers2 = {'Authorization': 'Bearer {}'.format(token2['access_token'])}
        RESOURCE_URL = 'https://graph.microsoft.com/'
        API_VERSION = 'v1.0'
        onedrive_destination = '{}/{}/me/drive/root:/UploadFiles'.format(RESOURCE_URL, API_VERSION)
        r = requests.put(onedrive_destination + "/" + report_version_name + ":/content", data=file, headers=headers2)
        print('link=', r.json())
        self.request.data['link'] = r.json()['@microsoft.graph.downloadUrl']
        print('data=', self.request.data)
        report_id = models.ReportModel.objects.filter(report_name=report_name).first()
        user_queryset = models.ReportUserModel.objects.filter(report=report_id)
        user_list = [x.user for x in user_queryset]
        user_email_list = []
        for i in user_list:
            user_model_queryset = User.objects.filter(username=i).first()
            user_email_list = user_email_list+[user_model_queryset.email]
        print(user_email_list)
        subject = 'Redseer files'
        message = f'New Files available'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['shahzmaalif@gmail.com']+user_email_list
        send_mail(subject, message, email_from, recipient_list)
        return super(ReportVersionLCView, self).create(request, *args, **kwargs)


class ReportVersionRUDView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportVersionSerializer
    queryset = models.ReportVersionModel.objects
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        print(self.request.data)
        file = False
        report_version_name = False
        if 'file' in self.request.data.keys():
            file = self.request.data['file']
        if 'report_version_name' in self.request.data.keys():
            report_version_name = self.request.data['report_version_name'] + '.xlsx'
        if file and report_version_name:
            token2 = get_token()
            headers2 = {'Authorization': 'Bearer {}'.format(token2['access_token'])}
            RESOURCE_URL = 'https://graph.microsoft.com/'
            API_VERSION = 'v1.0'
            onedrive_destination = '{}/{}/me/drive/root:/UploadFiles'.format(RESOURCE_URL, API_VERSION)
            r = requests.put(onedrive_destination + "/" + report_version_name + ":/content", data=file, headers=headers2)
            print('link=', r.json())
            self.request.data['link'] = r.json()['@microsoft.graph.downloadUrl']
            print('data=', self.request.data)
        return super(ReportVersionRUDView, self).update(request, *args, **kwargs)


class ReportUserLCView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportUserSerializer
    queryset = models.ReportUserModel.objects

    def get_queryset(self):
        request = self.request
        user_id = request.user.id
        return self.queryset.filter(user=user_id)
