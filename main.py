
from distutils.log import debug

from flask import render_template, request
from website import create_app

import requests
import json

import reverse_geocoder as rg

import pprint

pp = pprint.PrettyPrinter(indent=4)

app = create_app()
@app.route('/', methods=['GET'])
def map():

    # ISS LAT LONG
    req = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(req.content)

    ###
    for k,latv in data['iss_position'].items():
        if k == 'latitude':
            lat=latv

    for k,longv in data['iss_position'].items():
        if k == 'longitude':
            long=longv

    # ###
    # try:
    #     g = geocoder.osm([lat, long], method='reverse')
    #     city = g.json['country'] # Prints Edmonton
    #     print(city)
    # except KeyError:
    #     pass        
    # except TypeError:
    #     pass        
    # ###

    #### COORD LOC DATA
    coordinates = (lat,long)
    search = rg.search(coordinates)
    name = search[0]['name']
    admin1 = search[0]['admin1']
    cc = search[0]['cc']

    ####

    ###
    url = 'https://restcountries.com/v3.1/alpha?codes='
    urlpls = url+cc
    reqcode = requests.get(urlpls)    
    code = json.loads(reqcode.content)


    cont = code[0]['name']['official']
    reg = code[0]['region']
    cap = code[0]['capital']
    lang = code[0]['languages']
    pop = code[0]['population']
    print(cont)
    print(reg)
    print(cap)
    print(lang)
    print(pop)
    ###




    # ISS NUMBER
    reqppl = requests.get('http://api.open-notify.org/astros.json')
    ppl = json.loads(reqppl.content)


    pplitr = ppl['people']

    #return render_template('home.html', data=data, pplitr=pplitr, ppl=ppl)
    return render_template('home.html', data=data, pplitr=pplitr, ppl=ppl, lat=lat, long=long, name=name, admin1=admin1, cc=cc, code=code)


if __name__ =='__main__':
    app.run(debug=True)