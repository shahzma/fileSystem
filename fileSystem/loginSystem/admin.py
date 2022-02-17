from django.contrib import admin
from .models import ReportModel, ReportUserModel, ReportVersionModel
# Register your models here.

admin.site.register(ReportModel)
admin.site.register(ReportUserModel)
admin.site.register(ReportVersionModel)