from django.contrib import admin
from .models import Company, AttachDocument, Metrics, Notifications

admin.site.register([Company, AttachDocument, Metrics, Notifications])
