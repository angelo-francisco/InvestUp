from django.db import models
from companies.models import Company
from django.contrib.auth.models import User
from secrets import token_urlsafe

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
    proposal_token = models.CharField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.proposal_token:
            self.proposal_token = self.generate_unique_token()
        super().save(*args, **kwargs)

    def generate_unique_token(self):
        token = token_urlsafe(32)
        # Ensure the token is unique
        while InvestmentProposal.objects.filter(proposal_token=token).exists():
            token = token_urlsafe(32)
        return token

    @property
    def get_valuation(self):
        valuation = (float(self.value) * 100) / float(self.percentual)
        return round(valuation, 2)

    def __str__(self):
        return str(self.value)
