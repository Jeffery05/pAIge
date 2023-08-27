from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from page.themes import themes

from . import models


class CreateSiteForm(forms.Form):
    profile_url = forms.CharField(
        label="Your Linkedin profile URL",
        help_text="Must be a full Linkedin profile URL, including https://.",
        validators=[
            RegexValidator(
                regex=r"https://www.linkedin.com/in/.+/?",
                message="Invalid Linkedin profile URL",
            )
        ],
        max_length=256,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_url"].widget.attrs[
            "placeholder"
        ] = "https://www.linkedin.com/in/john-do"
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))


theme_choices = [
    (theme["theme_name"], theme["theme_name"]) for theme in themes.values()
]


class PortfolioForm(ModelForm):
    theme = forms.ChoiceField(choices=theme_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Save"))

    class Meta:
        model = models.Portfolio
        fields = ["theme"]
