import datetime

from django.db import models
import datetime
# Create your models here.


# class ReportModel(models.Model):
#     report_name = models.CharField(max_length=255)


class ReportVersionModel(models.Model):
    report_version_name = models.CharField(max_length=255)
    # report = models.ForeignKey(ReportModel, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    file = models.FileField(upload_to='documents/', max_length=100, blank=True)

    class Meta:
        managed = True
        db_table = str(AppConfig.name) + "_" + "cart"




