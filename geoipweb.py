#!/usr/bin/python3

import geoip2.database
from netaddr import *
from flask import Flask, render_template

app = Flask(__name__)

def getcity(ip):
  geoipath = "/var/lib/GeoIP"
  try:
    with geoip2.database.Reader(geoipath + '/GeoLite2-City.mmdb') as city_reader:
      city_res  = city_reader.city(ip)
  except:
    print(f"No data about {ip}")
    return (0)
  return (city_res)

def getasn(ip):
  geoipath = "/var/lib/GeoIP"
  try:
    with geoip2.database.Reader(geoipath + '/GeoLite2-ASN.mmdb') as asn_reader:
      asn_res = asn_reader.asn(ip)
  except:
    print(f"No data about {ip}")
    return (0)
  return (asn_res)

@app.route('/<ip>/<info>')
def getspec(ip, info):
  if IPAddress(ip).is_private():
    return(f"{ip} is a private IP\n")
  city_res = getcity(ip)
  asn_res = getasn(ip)
  if city_res and info == "country":
    return (f"{city_res.country.name}\n")
  if city_res and info == "cc":
    return (f"{city_res.country.iso_code}\n")
  if city_res and info == "city":
    return (f"{city_res.city.name}\n")
  if city_res and (info == "coordinates" or info == "coords"):
    return (f"{city_res.location.latitude} {city_res.location.longitude}\n")
  if asn_res and info == "isp":
    return (f"{asn_res.autonomous_system_organization}\n")
  if asn_res and info == "asn":
    return (f"AS{asn_res.autonomous_system_number}\n")

@app.route('/<ip>/json')
def getinfojson(ip):
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")
  city_res = getcity(ip)
  if city_res != 1:
    lat = city_res.location.latitude
    lon = city_res.location.longitude
    country = city_res.country.name
    cc = city_res.country.iso_code
    city = city_res.city.name

  asn_res = getasn(ip)
  if asn_res != 1:
    isp = asn_res.autonomous_system_organization
    asn = asn_res.autonomous_system_number
  return {
    "ip": ip,
    "lat": lat,
    "lon": lon,
    "country": country,
    "cc": cc,
    "city": city,
    "isp": isp,
    "asn": asn,
  }

@app.route('/<ip>')
def getinfo(ip):
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")
  city_res = getcity(ip)
  if city_res != 1:
    lat = city_res.location.latitude
    lon = city_res.location.longitude
    country = city_res.country.name
    cc = city_res.country.iso_code
    city = city_res.city.name

  asn_res = getasn(ip)
  if asn_res != 1:
    isp = asn_res.autonomous_system_organization
    asn = asn_res.autonomous_system_number
  return (render_template('template.html', ip=ip, lat=lat, lon=lon, country=country, cc=cc, city=city, isp=isp, asn=asn))

@app.route('/')
def hello():
  return ("Hello, World!\n")
