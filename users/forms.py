from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class StyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                    }
                )

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update(
                    {
                        "class": "form-select",
                    }
                )


class SignupForm(StyleForm, UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control input-pers",
            }
        )

        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control input-pers",
            }
        )
