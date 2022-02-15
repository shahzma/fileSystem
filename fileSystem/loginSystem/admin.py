from django.contrib import admin
from .models import ReportModel, ReportUserModel
# Register your models here.

admin.site.register(ReportModel)
admin.site.register(ReportUserModel)