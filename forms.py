from django import forms
from models import RecycleType

class AddressForm(forms.Form):
	choices = ((row.name, row.name) for row in RecycleType.objects.all().order_by('name'))
	address = forms.CharField(label=u'Address', max_length=100)
	type = forms.ChoiceField(label=u'Material', choices=choices)
	
class RecyclerSuggestionForm(forms.Form):
	author_name = forms.CharField(label=u'Your name*', max_length=100)
	author_email = forms.EmailField(label=u'Your email*', max_length=75)
	name = forms.CharField(label=u'Name of drop-off point*', max_length=100)
	address = forms.CharField(label=u'Address of drop-off point (street, city, state, ZIP)*', max_length=100)
	comment = forms.CharField(label=u'Description of drop-off point (which materials are accepted here)*', max_length=1000, widget=forms.Textarea)
	hours = forms.CharField(label=u'Hours of operation of drop-off point', max_length=100)
	hours.required = False
	phone = forms.CharField(label=u'Phone number of drop-off point', max_length=100)
	phone.required = False
	website = forms.URLField(label=u'Website of drop-off point', max_length=100)
	website.required = False
	source = forms.CharField(label=u'Source for your information (URL)', max_length=100)
	source.required = False

class RecycleTypeSuggestionForm(forms.Form):
	author_name = forms.CharField(label=u'Your name*', max_length=100)
	author_email = forms.EmailField(label=u'Your email*', max_length=75)
	name = forms.CharField(label=u'Name of material type (ex: batteries, clothing, etc.)*', max_length=100)
	desc = forms.CharField(label=u'Description of material type (ex: why it should be recycled, which locations accept it, etc.)*', max_length=1000, widget=forms.Textarea)
	source = forms.CharField(label=u'Source for your information (URL)', max_length=100)
	source.required = False

class DatasetSuggestionForm(forms.Form):
	author_name = forms.CharField(label=u'Your name*', max_length=100)
	author_email = forms.EmailField(label=u'Your email*', max_length=75)
	website = forms.URLField(label=u'Website of dataset (URL)*', max_length=100)
	comment = forms.CharField(label=u'Description of dataset (what kind of information does it contain)*', max_length=1000, widget=forms.Textarea)