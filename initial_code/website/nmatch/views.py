from django.shortcuts import render
from django.template import RequestContext, loader
from django import forms
from django.utils.safestring import mark_safe

from pull_scores import *

ALL_TRACTS = 802
'''
All values are floats, the number of stores in a census tract


Childcare services (including eaerly learnign programs and Children service facilities)
'amen_child_early_learning", "amen_child_child_biz"

Youth Centers
amen_child_youth_centers

Library
amen_gen_LIBRARYNAME 

Senior centers
amen_senior_senior_centers

Commercial businsses
amen_gen_commerical_biz

Farmer's markets
amen_gen_farmers_markets

Restaurants and bars
amen_adult_restaurant_bar

Event spaces, performing arts venues, etc.
amen_adult_entertainment_biz 
'''


# Q = "What income range are you targeting?" #find widget for range
Q_1 = "Is housing type important? What type?"
Q_2 = "Target rent for area around business?"
Q_3 = "What age are your target customers?"
Q_4 = "What special amenities do you want nearby?" 

Q_5 = "How do you get around?"
Q_6 = "How would you rank these categories?"


CHOICES_1 = [("housing_HOU1DET_by_housing_HOUTOT", 'Detached house'), 
			("housing_HOU1ATT_by_housing_HOUTOT", 'Attached house (townhouse)'), 
			("housing_HOUSMALLAPT_by_housing_HOUTOT", 'Small apartment building (1-9 units)'),
	 		("housing_HOUBIGAPT_by_housing_HOUTOT", 'Big apartment building (10+)')]

CHOICES_3 = [("age_AGE09_by_age_AGEPOP", "Children (ages 0-9)"), 
			("age_AGE1019_by_age_AGEPOP", "Tweens to teens (ages 10-19)"), 
			("age_AGE2034_by_age_AGEPOP", "Ages 20-34"),
	 		("age_AGE3549_by_age_AGEPOP", "Ages 35-49"), 
	 		("age_AGE5064_by_age_AGEPOP", "Ages 50-64"), 
	 		("age_AGE65_by_age_AGEPOP", "Ages 65 years+")]
CHOICES_4 = [("amen_child", "Stuff to do with my kids"), 
			("amen_adult", "Places to socialize and go with friends"), 
	 		("amen_senior", "Things to do with other retirees")]
CHOICES_5 = [("trans_WALKSCORE", "Walk"), ("trans_trans_by_geo_sq_mileage", "Public transportation"), ("trans_drive", "Drive")]
CHOICES_6 = [("housing", "Housing type"),
			("house_cost", "Housing cost"), 
			("neighbor", "My neighbors"), 	
			("amen", "Special amenitites"),
			("amen_gen", "Everyday amenities"), 
			("trans", "Transportation"),
			("crime", "Neighborhood safety")]




class PreferenceForm(forms.Form):
	housing = forms.ChoiceField(
				label=Q_1,
				choices=CHOICES_1,
				widget=forms.RadioSelect,
				required=True)
	house_cost = forms.IntegerField(
				label=Q_2,
				widget=forms.NumberInput,
				min_value=1,
				max_value=1000000,
				required=True)	
	age = forms.ChoiceField(
				label=Q_3,
				choices=CHOICES_3,
				widget=forms.RadioSelect,
				required=True,
				error_messages = {'required': 'You skipped this one!'} )
	amenities = forms.ChoiceField(
				label=Q_4,
				choices=CHOICES_4,
				widget=forms.RadioSelect,
				required=True)
	trans = forms.ChoiceField(
				label=Q_5,
				choices=CHOICES_5,
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
	args ={}
	c['error'] = None

	if request.method == 'GET':
		#create a form instance and populate it with data from the request
		form = PreferenceForm(request.GET)
		#check whether it's valid
		if form.is_valid():
			#add form data to an args dictionary 
			h_type = form.cleaned_data['housing']
			if h_type:
				args['housing'] = h_type
			
			h_cost = form.cleaned_data['house_cost']
			if h_cost:
				args['house_cost'] = h_cost

			neigh = form.cleaned_data['age']
			if neigh:
				args['age'] = neigh

			amen = form.cleaned_data['amenities']
			if amen:
				args['amenities'] = amen

			trans = form.cleaned_data['trans']
			if trans:
				args['trans'] = trans
			
			

			#add args to c dictionary
			c['args'] = args
			
			#get matching tracts and make javascript string
			if c['args'] is not None:
				#gets list of matching tracts
				tracts = go(args, 5)
				c['tracts'] = tracts
				java_str = get_string(tracts)
				c['java_str'] = java_str
				return render(request, 'nmatch/map_only.html', c)

		else:
			form = PreferenceForm()

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

	