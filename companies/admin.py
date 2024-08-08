from django.contrib import admin
from .models import Company, AttachDocument, Metrics

admin.site.register([Company, AttachDocument, Metrics])
