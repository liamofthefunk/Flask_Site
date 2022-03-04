
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


    #### COORD LOC DATA
    coordinates = (lat,long)
    search = rg.search(coordinates)
    name = search[0]['name']
    cc = search[0]['cc']

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

    ###

    urlmap = "https://api.mapbox.com/styles/v1/liamofthefunk/cl0ce7ngt006314rr18ushz4r.html?title=false&access_token=pk.eyJ1IjoibGlhbW9mdGhlZnVuayIsImEiOiJjbDBjZTNpMGQwNWpyM2tzNHNveXBpdTFjIn0.uwFSwJCyYceGQdfkA-93tA&zoomwheel=false#3/"
    urlmaploc = urlmap + lat + "/" + long


    # ISS NUMBER
    reqppl = requests.get('http://api.open-notify.org/astros.json')
    ppl = json.loads(reqppl.content)
    pplitr = ppl['people']
    out = [x for x in pplitr if x['craft']=='ISS']

    return render_template('home.html', pplitr=pplitr, lat=lat, long=long, name=name, cont=cont, reg=reg, cap=cap, lang=lang, pop=pop, out=out, urlmaploc=urlmaploc)

if __name__ =='__main__':
    app.run(debug=True)
