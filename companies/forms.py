from django import forms
from .models import Company, AttachDocument
from users.forms import StyleForm
from django.utils import timezone


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
            "last_date_capture": forms.DateInput(attrs={"type": "date"}),
            "percentual_equity": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "internship": forms.RadioSelect(attrs={"class": "form-check-label"}),
            "value": forms.NumberInput(
                attrs={"placeholder": "Write your company value"}
            ),
        }

    def clean_area(self):
        area = self.cleaned_data.get("area", None)
        area_list = ("ED", "FT", "AT")

        if area not in area_list:
            raise forms.ValidationError("This value isnt'valid")

        return area

    def clean_target_audience(self):
        target_audience = self.cleaned_data.get("target_audience", None)
        target_audience_list = ("BTC", "B2B")

        if target_audience not in target_audience_list:
            raise forms.ValidationError("This value isnt'valid")

        return target_audience

    def clean_internship(self):
        internship = self.cleaned_data.get("internship", None)
        internship_list = ("I", "MVP", "MVPP", "E")

        if internship not in internship_list:
            raise forms.ValidationError("This value isnt'valid")

        return internship

    def clean_existence_time(self):
        existence_time = self.cleaned_data.get("existence_time", None)
        existence_time_list = ("+6", "-6", "+1", "+5")

        if existence_time not in existence_time_list:
            raise forms.ValidationError("This value isn't valid")

        return existence_time

    def clean_last_date_capture(self):
        last_date_capture = self.cleaned_data.get("last_date_capture", None)
        actual_date = timezone.now().date()

        if last_date_capture < actual_date:
            raise forms.ValidationError("Last Date Capture can't be in the past")

        return last_date_capture

    def clean_percentual_equity(self):
        percentual_equity = self.cleaned_data.get("percentual_equity", None)

        if not (0 <= percentual_equity <= 100):
            raise forms.ValidationError("It must be between 0 and 100")

        return percentual_equity

    def clean_pitch(self):
        pitch = self.cleaned_data.get("pitch", None)
        max_size = 100 * pow(1024, 2)
        allowed_types = ["application/pdf"]

        if not pitch:
            raise forms.ValidationError("Please, enter your company's pitch")

        if pitch.size > max_size:
            raise forms.ValidationError("Pitch file size must be under 100MB")

        if pitch.content_type not in allowed_types:
            raise forms.ValidationError("Only PDF files are allowed")

        return pitch

    def clean_logo(self):
        logo = self.cleaned_data.get("logo", None)
        max_size = 2 * pow(1024, 2)
        allowed_types = ["image/jpeg", "image/png"]

        if not logo:
            raise forms.ValidationError(
                "Please, enter your company's logo",
            )

        if logo.size > max_size:
            raise forms.ValidationError("Logo file size must be under 2MB")

        if logo.content_type not in allowed_types:
            raise forms.ValidationError("Supported types is only: JPEG and PNG")

        return logo


class AttachDocumentForm(StyleForm):
    class Meta:
        model = AttachDocument
        fields = ("title", "document")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Write the document name"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.company = kwargs.pop("company", None)

        super().__init__(*args, **kwargs)

    def clean_document(self):
        document = self.cleaned_data.get("document", None)
        max_size = 100 * pow(1024, 2)
        allowed_types = ["application/pdf"]

        if self.company.user != self.user:
            raise forms.ValidationError("Your not the company's owner")

        if not document:
            raise forms.ValidationError("Please, enter the document!")

        if document.size > max_size:
            raise forms.ValidationError("File size must be under 100MB")

        if document.content_type not in allowed_types:
            raise forms.ValidationError("Only PDF file is allow")

        return document
