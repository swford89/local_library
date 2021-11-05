import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(label="RENEWAL DATE", help_text="Enter a date between now and four weeks (default = three weeks).")

    def clean_renewal_date(self):
        # get the renewal date
        data = self.cleaned_data["renewal_date"]

        # make sure date isn't in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date -- renewal in past."))

        # make sure date is within 4 week range
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date -- renewal is more than four weeks ahead"))

        return data