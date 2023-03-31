from django.shortcuts import render
from pandas import read_csv,DataFrame
from .forms import airportForm,cordForm,routeForm,demandForm
from sklearn import preprocessing
from sklearn.tree import DecisionTreeRegressor
import math
tree_model = DecisionTreeRegressor()

le = preprocessing.LabelEncoder()
routes = read_csv(r"dataset\routes.csv")
to_demand = read_csv(r"dataset\todemand.csv")
from_demand = read_csv(r"dataset\fromdemand.csv")
data = read_csv(r"dataset\data_new.csv")
data_routes = read_csv(r"dataset\routeswithdist.csv")

q1 = data_routes[['distance']].quantile(0.25).values
q3 = data_routes[['distance']].quantile(0.75).values

data['city'] = data['city'].str.upper()
X = data[['pop2023','GDP per city in crores']]
y = data[['airport_available']]
y = le.fit_transform(y)
y = DataFrame(y,columns=['airport available'])
tree_model.fit(X, y)


def home(request):
    if request.method == 'POST':
        form = routeForm(request.POST)
        if form.is_valid():
            from_city = form.cleaned_data['from_city']
            to_city = form.cleaned_data['to_city']

        if len(routes.loc[(routes['CITY 1'] == from_city) & (routes['CITY 2'] == to_city)]) == 1:
            result = "Route available"

        else:
            result = "Further analysis need to be done to see if a direct route is applicable or go through connecting flights"
        return render(request,"index.html",{'form':form,'result':result})
    else:
        form = routeForm()
        return render(request,"index.html",{'form':form})

def airport(request):
    if request.method == 'POST':
        form = airportForm(request.POST)
        if form.is_valid():
            aircity = form.cleaned_data['aircity']
            if data['airport_available'].loc[data['city'] == aircity].values[0] == True:
                result = "Airport available"
            else:
                result = "Let go for an further in-depth analysis for building an airport"

        return render(request,"airport.html",{'form':form,'result':result})
    else:
        form = airportForm()
        return render(request,"airport.html",{'form':form})
    
def demand(request):
    if request.method == 'POST':
        form = demandForm(request.POST)
        if form.is_valid():
            pop = form.cleaned_data['pop']
            gdp = form.cleaned_data['gdp']
            x = []
            y = []
            x.append(pop)
            y.append(gdp)
            d = {'pop2023': x, 'GDP per city in crores': y}
            result = tree_model.predict(DataFrame(d))
            if result[0] == 1:
                res = "Airport can be established"
            else:
                res = "The city does not have proper economy to population ratio for establishing an airport "
            return render(request,"demand.html",{'form':form,'result':res})
    else:
        form = demandForm()
        return render(request,"demand.html",{'form':form})
    
def distance(request):
    if request.method == 'POST':
        form = cordForm(request.POST)
        if form.is_valid():
            fromlat = form.cleaned_data['fromlat']
            fromlon = form.cleaned_data['fromlon']
            tolat = form.cleaned_data['tolat']
            tolon = form.cleaned_data['tolon']

            distance = math.acos((math.cos(math.radians(90-fromlat)) * math.cos(math.radians(90-tolat))) + (math.sin(math.radians(90-fromlat))*math.sin(math.radians(90-tolat))*math.cos(math.radians(fromlon-tolon)))) * 6371  
            if distance >= q3:
                result = "Opting for a connecting flight would be an efficient option"
            elif distance <= q1:
                result = "Opting for a land transport would be an effective option"
            else:
                result = "Direct route can be setup "
            return render(request,"distance.html",{'form':form,'result':result})

    else:
        form = cordForm()
        return render(request,"distance.html",{'form':form})