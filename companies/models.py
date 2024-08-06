from django.db import models
from django.contrib.auth.models import User
from .modelChoices import *


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    existence_time = models.CharField(
        max_length=2, choices=existence_time_choices, default="-6"
    )
    description = models.TextField()
    last_date_caption = models.DateField()
    percentual_equity = models.IntegerField()
    internship = models.CharField(max_length=4, choices=internship_choices, default="I")
    area = models.CharField(max_length=3, choices=area_choices)
    target_audience = models.CharField(
        max_length=20, choices=target_audience_choices, default="BTC"
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    pitch = models.FileField(upload_to="pitches")
    logo = models.FileField(upload_to="videos")

    def __str__(self):
        return f"{self.user.username} | {self.name}"
