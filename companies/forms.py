from django import forms
from .models import Company
from users.forms import StyleForm


class CompanyForm(StyleForm):
    class Meta:
        model = Company
        exclude = ["user"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Write your company name"}),
            "cnpj": forms.TextInput(attrs={"placeholder": "Write your company CNPJ"}),
            "site": forms.URLInput(
                attrs={"placeholder": "Write your company site url"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "style": "width: 100%;border-radius: 8px;margin-bottom: 15px;",
                }
            ),
            "last_date_caption": forms.DateInput(attrs={"type": "date"}),
            "percentual_equity": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "internship": forms.RadioSelect(attrs={"class": "form-check-label"}),
            "value": forms.NumberInput(
                attrs={"placeholder": "Write your company value"}
            ),
        }
