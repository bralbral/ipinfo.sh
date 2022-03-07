#!/usr/bin/python3

import geoip2.database
import socket, requests, random
from netaddr import *
from flask import Flask, render_template, request

app = Flask(__name__)
cli = ["curl", "HTTPie", "httpie-go", "Wget", "fetch libfetch", "Go", "Go-http-client", "ddclient", "Mikrotik", "xh"]

#############################
### INFORMATIONS QUERRIES ###
#############################

#
# Get IP's host
#

def gethost(ip):
  try:
    name = socket.getnameinfo((ip, 0), 0)[0]
  except:
    print(f"Hostname resolution failure for {ip}")
    name = "Unknown"
  return (name)

#
# Location GeoIP database informations querry
#

def getcity(ip):
  geoipath = "/var/lib/GeoIP"
  try:
    with geoip2.database.Reader(geoipath + '/GeoLite2-City.mmdb') as city_reader:
      city_res = city_reader.city(ip)
  except:
    print(f"No data about {ip}")
    return (0)
  return (city_res)

#
# ASN GeoIP database informations querry
#

def getasn(ip):
  geoipath = "/var/lib/GeoIP"
  try:
    with geoip2.database.Reader(geoipath + '/GeoLite2-ASN.mmdb') as asn_reader:
      asn_res = asn_reader.asn(ip)
  except:
    print(f"No data about {ip}")
    return (0)
  return (asn_res)

#
# Network informations querry
#

def getnet(ip):
  try:
    network = requests.get(f"https://internetdb.shodan.io/{ip}").json()
    network = dict([(k.capitalize(),v) for k,v in network.items() if len(v)>0])
  except:
    print(f"No net data about {ip}")
    network = "No net data about {ip}"
  return (network)

#
# GeoIP informations put in a dict
#

def getgeo(ip):
  infos = {
    "IP Address": ip
  }
  infos.update({"Hostname": gethost(ip)})

  city_res = getcity(ip)
  if city_res:
    infos.update({
        "Country": city_res.country.name,
        "Country Code": city_res.country.iso_code,
        "City": city_res.city.name,
        "Latitude": city_res.location.latitude,
        "Longitude": city_res.location.longitude
    })
  else:
    return (f"No location data about {ip}")

  asn_res = getasn(ip)
  if asn_res:
    infos.update({
      "ISP": asn_res.autonomous_system_organization,
      "ASN": f"AS{asn_res.autonomous_system_number}"
    })
  else:
    return (f"No ISP data about {ip}")

  return (infos)

####################
### FLASK ROUTES ###
####################

#
# Specific info path
#

@app.route('/<ip>/<info>')
def getspec(ip, info):
  if IPAddress(ip).is_private():
    return(f"{ip} is a private IP\n")

  infos = getgeo(ip)
  infos.update(getnet(ip))

  if len(info) == 3:
    info = info.upper()
  elif info == "cc" or info == "countryiso":
    info = "Country Code"
  else:
    info = info.capitalize()

  if not info in infos:
    return (f"No data about {info} for {ip}")

  if isinstance(infos[info], list):
    conv = { i : infos[info][i] for i in range(0, len(infos[info]) ) }
    infos[info] = conv

  return (infos[info] + '\n')

#
# Json path
#

@app.route('/<ip>/json')
def getinfojson(ip):
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")

  infos = getgeo(ip)
  infos.update(getnet(ip))

  return (infos)

#
# IP path
#

@app.route('/<ip>')
def getinfo(ip):
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")

  infos = getgeo(ip)
  network = getnet(ip)
  colors = [ '#2488bf', '#d84d3d', '#f39700', '#4caf50' ]

  if any(x in request.headers.get('User-Agent') for x in cli):
    infos.update(network)
    return (infos), 404
  else:
    return (render_template('template.html', ip=ip, infos=infos, network=network, color=random.choice(colors)))

#
# Root path
#

@app.route('/')
@app.route('/self')
def self():
  ip = request.environ.get('HTTP_X_FORWARDED_FOR').split(',')
  if any(x in request.headers.get('User-Agent') for x in cli):
    return (ip[0] + '\n'), 404
  else:
    return (getinfo(ip[0]))
