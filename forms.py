from django import forms
from models import RecycleType

class AddressForm(forms.Form):
	choices = ((row.name, row.name) for row in RecycleType.objects.all().order_by('name'))
	address = forms.CharField(label=u'Address', max_length=100)
	type = forms.ChoiceField(label=u'Material', choices=choices)