from django import forms
from recommendations.models import Rule

class enteringForm(forms.ModelForm):
   class Meta:
       model = Rule
       labels = {
       "lhs": "Codes"
       }
       fields = ['lhs']
