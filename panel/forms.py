from django import forms
from django.core.validators import RegexValidator


class CreateSiteForm(forms.Form):
    profile_url = forms.CharField(
        label="Your Linkedin profile URL",
        validators=[
            RegexValidator(
                regex=r"https://www.linkedin.com/in/.+/?",
                message="Invalid Linkedin profile URL",
            )
        ],
        max_length=256,
    )
