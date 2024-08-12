from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)
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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_with_same_username = User.objects.filter(username__iexact=username).exists()

        if user_with_same_username:
            raise forms.ValidationError("This username already exists")
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_with_same_email = User.objects.filter(email=email).exists()

        if user_with_same_email:
            raise forms.ValidationError("This email already exists")

        return email
    

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


class ProfileForm(StyleForm, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)

        for _, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.Input):
                field.widget.attrs.update(
                    {
                        "style": "width:230px;",
                    }
                )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
