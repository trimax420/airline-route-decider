from django import forms
import pandas as pd
import numpy as np 

aircity_choice = pd.read_csv(r"dataset/todemand.csv")
aircity_choice = aircity_choice['CITY 2']
aircity_choice = np.array(aircity_choice)
aircity_choice = list(aircity_choice)
aircity_choice = list(zip(aircity_choice, aircity_choice))

city = pd.read_csv(r"dataset/data_new.csv")
city = city['city']
city = np.array(city)
city = list(city)
city = list(zip(city, city))

class routeForm(forms.Form):
    from_city = forms.ChoiceField(choices = aircity_choice)
    to_city   = forms.ChoiceField(choices = aircity_choice)

class cordForm(forms.Form):
    fromlat = forms.FloatField()
    fromlon = forms.FloatField()
    tolat   = forms.FloatField()
    tolon   = forms.FloatField()

class airportForm(forms.Form):
    aircity = forms.ChoiceField(choices = city)

class demandForm(forms.Form):
    pop = forms.FloatField()
    gdp = forms.FloatField()