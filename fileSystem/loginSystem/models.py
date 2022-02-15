from django.db import models
from .apps import LoginsystemConfig as AppConfig
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


class ReportModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    report_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "Report"

    def __str__(self):
        return self.report_name


class ReportVersionModel(models.Model):
    report_version_name = models.CharField(max_length=255)
    report = models.ForeignKey(ReportModel, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # file = models.FileField(upload_to='/RedSeerFiles', storage=gd_storage)
    file = models.FileField(upload_to='message/%Y/%m/%d/', max_length=100, blank=True)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "ReportVersion"

    def __str__(self):
        return self.report_version_name


class ReportUserModel(models.Model):
    report = models.ForeignKey(ReportModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "ReportUser"




# # convert to report version model
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     designation = models.CharField(max_length=20, null=False, blank=False)
#     salary = models.IntegerField(null=True, blank=True)
#     picture = models.ImageField(upload_to='pictures/%Y/%m/%d/', max_length=255, null=True, blank=True)
#
#     class Meta:
#         ordering = ('-salary',)
#
#     def __str__(self):
#         return "{0} - {1}".format(self.user.username, self.designation)
#
#
# class EmployeeManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(profile__designation="Employee")
#
#
# class Employee(User):
#     class Meta:
#         ordering = ("username",)
#         proxy = True
#
#     objects = EmployeeManager()
#
#     def full_name(self):
#         return self.first_name + " - " + self.last_name
#
#
# @receiver(post_save, sender=User)
# def user_is_created(sender, instance, created, **kwargs):
#     print(created)
#     if created:
#         Profile.objects.create(user=instance)
#     else:
#         instance.profile.save()
#
#
# from django.contrib.auth.models import User
#
#
# @property
# def full_name(self):
#     return "{} {}".format(self.first_name, self.last_name)
#
#
# User.add_to_class('full_name', full_name)