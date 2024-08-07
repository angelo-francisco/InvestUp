from .modelChoices import (
    existence_time_choices,
    internship_choices,
    area_choices,
    target_audience_choices,
)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    existence_time = models.CharField(
        max_length=2, choices=existence_time_choices, default="-6"
    )
    description = models.TextField()
    last_date_capture = models.DateField()
    percentual_equity = models.IntegerField()
    internship = models.CharField(max_length=4, choices=internship_choices, default="I")
    area = models.CharField(max_length=3, choices=area_choices)
    target_audience = models.CharField(
        max_length=20, choices=target_audience_choices, default="BTC"
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    pitch = models.FileField(upload_to="pitches")
    logo = models.FileField(upload_to="logos")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} | {self.name}"

    @property
    def get_status(self):
        status = mark_safe('<span class="badge bg-success">Capting</span>')
        actual_date = timezone.now().date()

        if actual_date > self.last_date_capture:
            status = mark_safe('<span class="badge bg-primary">Closed Capture</span>')

        return status

    @property
    def get_valuation(self):
        valuation = (self.value * 100) / self.percentual_equity
        return round(valuation, 2)


class AttachDocument(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    document = models.FileField(upload_to="documents")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | {self.company}"



class Metrics(models.Model): ...