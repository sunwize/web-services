#!/usr/bin/env python
# coding: utf-8

import requests 
import json
import html
import os 
import urllib
import xmltodict

from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, Markup, jsonify
from flask import jsonify
from flask_cors import CORS, cross_origin
from scipy import *

DEBUG = False
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'JHfdsjnbkKklmmgkjpobg'  
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=['GET', 'POST'])
def hello():
    return app.send_static_file('home.html')

@app.route("/hal/coauthors/<author>")
def hal_coo_authors(author):
    r = requests.get('http://api.archives-ouvertes.fr/search/?q=auth_t:'+author+'&wt=json')
    data = r.json()
    resp = []
    for i in range(len(data['response']['docs'])):
        x = data['response']['docs'][i]['label_s'].split('.',-1)
        d = dict()
        if len(x[0]) == 1:
            d["names"] = x[0] + '.' + x[1]
            d["source"] = x[2]
        else:
            d["names"] = x[0]
            d["source"] = x[1]
        resp.append(d)
    
    proper = []
    for entry in resp:
        names = entry["names"].split(',', -1)
        for name in names:
            if str(author).lower() in str(name).lower():
                continue
            d = dict()
            d["name"] = name
            d["source"] = entry["source"]
            proper.append(d)
    return jsonify(proper)

@app.route("/hal/sources/<author>")
def hal_sources(author):
    r = requests.get('http://api.archives-ouvertes.fr/search/?q=auth_t:'+author+'&wt=json')
    data = r.json()
    resp = []
    for i in range(len(data['response']['docs'])):
        x = data['response']['docs'][i]['uri_s']
        labels = data['response']['docs'][i]['label_s'].split('.',-1)
        d = dict()
        if len(labels[0]) == 1:
            d["title"] = labels[2]
        else:
            d["title"] = labels[1]
        d["url"] = x
        resp.append(d)
    return jsonify(resp)

@app.route("/arxiv/coauthors/<author>")
def arxiv_coo_authors(author):
    data = urllib.request.urlopen('http://export.arxiv.org/api/query?search_query=au:' + author).read()
    encoded = xmltodict.parse(data)
    resp = []
    for entry in encoded['feed']['entry']:
        for a in entry["author"]:
            if str(author).lower() in str(a).lower():
                continue
            d = dict()
            if type(a) is str:
                continue
            else:
                d["name"] = a["name"]
            d["source"] = entry["title"]
            resp.append(d)
    return jsonify(resp)

@app.route("/arxiv/sources/<author>")
def arxiv_sources(author):
    data = urllib.request.urlopen('http://export.arxiv.org/api/query?search_query=au:' + author).read()
    encoded = xmltodict.parse(data)
    resp = []
    for entry in encoded['feed']['entry']:
        d = dict()
        d["url"] = entry["id"]
        d["title"] = entry["title"]
        resp.append(d)
    return jsonify(resp)





