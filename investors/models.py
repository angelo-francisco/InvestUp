from django.db import models
from companies.models import Company
from django.contrib.auth.models import User


status_choices = (
    ("AS", "Awaiting signature"),
    ("PE", "Proposal sent"),
    ("PA", "Proposal accepted"),
    ("PR", "Proposal rejected"),
)


class InvestmentProposal(models.Model):
    value = models.DecimalField(max_digits=9, decimal_places=2)
    percentual = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    investor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=status_choices, default="AS")
    selfie = models.FileField(upload_to="selfies", null=True, blank=True)
    rg = models.FileField(upload_to="rgs", null=True, blank=True)

    @property
    def get_valuation(self):
        valuation = (float(self.value) * 100) / float(self.percentual)
        return round(valuation, 2)

    def __str__(self):
        return str(self.value)
