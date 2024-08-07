from django.contrib import admin
from .models import Company, AttachDocument

admin.site.register([Company, AttachDocument])
