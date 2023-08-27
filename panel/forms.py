from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import RegexValidator


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
