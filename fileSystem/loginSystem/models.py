from django.db import models
from .apps import LoginsystemConfig as AppConfig
import uuid
from django.contrib.auth.models import User


class ReportModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    report_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "Report"

    def __str__(self):
        return self.report_name


class ReportVersionModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    report_version_name = models.CharField(max_length=255)
    report = models.ForeignKey(ReportModel, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # file = models.FileField(upload_to='/RedSeerFiles', storage=gd_storage)
    # file = models.FileField(upload_to='message/%Y/%m/%d/', max_length=100, blank=True)
    link = models.TextField(default='http://127.0.0.1:8000/media/message/2022/02/25/Insurance_9OQCmFU.xlsx')

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
