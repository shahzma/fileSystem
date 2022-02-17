import datetime

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import ReportVersionModel, ReportModel, ReportUserModel
from django.contrib.auth import authenticate
from rest_framework import exceptions
# from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']
        # extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportModel
        fields = '__all__'
        read_only_fields = ['id']


class ReportVersionSerializer(serializers.ModelSerializer):
    report = serializers.CharField(source='report.report_name')

    class Meta:
        model = ReportVersionModel
        fields = '__all__'
        read_only_fields = ['created_on', 'created_by']

    def create(self, validated_data):
        request = self.context.get("request")
        # user_data = validated_data.pop('user')
        #
        # # Find a user with that username
        # user = User.objects.get(username=user_data['username'])
        report = validated_data['report']
        report = ReportModel.objects.get(report_name=report['report_name'])
        validated_data['report'] = report
        if request:
            created_by = request.user.username
            validated_data['created_by'] = created_by
        else:
            validated_data['created_by'] = 'anon'
        return super(ReportVersionSerializer, self).create(validated_data)


class ReportUserSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    # report = serializers.StringRelatedField()

    class Meta:
        model = ReportUserModel
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super(ReportUserSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        rep['report'] = instance.report.report_name
        repver_queryset = ReportVersionModel.objects.filter(report=instance.report.id)
        date_list = [x.created_on for x in repver_queryset]
        rep['date'] = max(date_list)
        return rep

#convert to report version
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['salary', 'designation', 'picture']
#
# class EmployeeSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name',
#                 'last_name', 'profile', 'email',
#                 'is_staff', 'is_active', 'date_joined',
#                 'is_superuser']
#
# # compare to yours
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         username = data.get("username", "")
#         password = data.get("password", "")
#
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     data["user"] = user
#                 else:
#                     msg = "User is deactivated."
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = "Unable to login with given credentials."
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = "Must provide username and password both."
#             raise exceptions.ValidationError(msg)
#         return data
