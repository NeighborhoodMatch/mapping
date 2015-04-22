from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from django.utils.safestring import mark_safe

from pull_scores import *

ALL_TRACTS = 802

class CAPP_Form(forms.Form):
	yes = forms.ChoiceField(
				label="Go to map?",
				choices=[("YES", "Gladly!")],
				widget=forms.RadioSelect,
				required=True)

def about(request):
	c = {}
	return render(request, 'nmatch/about.html', c)

def home(request):
	c = {}
	return render(request, 'nmatch/home.html', c)

def survey_CAPP(request):
	c = {}
	args = {}
	
	if request.method == 'GET':
		form = CAPP_Form(request.GET)
		if form.is_valid():
			to_map = form.cleaned_data['yes']
			if to_map:
				args['yes'] = to_map

			#add args to c dictionary
			c['args'] = args
			
			#get matching tracts and make javascript string
			if c['args'] is not None:
				#gets list of matching tracts
				tracts = go(ALL_TRACTS)
				c['tracts'] = tracts
				java_str = get_string(tracts)
				c['java_str'] = java_str
				return render(request, 'nmatch/map_only.html', c)
		else:
			form = CAPP_Form()
	c['form'] = form
	return render(request, 'nmatch/survey_CAPP.html', c)


#takes list of tracts and returns javascript string
def get_string(tracts):
	tract_list = list(str(c) for c in tracts)

	string_1 = "{ where: 'col0\x3e\x3e0 \x3d "
	string_2 = "',\
		polygonOptions: {\
		fillColor: '#0000FF',\
		fillOpacity: 1\
		}\
		}, "

	full_str = ''

	#displays only the first five tracts in ordered list
	for tract in tract_list:
		tract_string = string_1 + tract + string_2
		full_str = full_str + tract_string
	
	full_str = full_str[:-2]

	return full_str

	