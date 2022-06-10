#!/usr/bin/python3

import geoip2.database
import socket, requests, random, yaml, os
from os import environ
from netaddr import *
from flask import Flask, render_template, request

app = Flask(__name__)
cli = ["curl", "HTTPie", "httpie-go", "Wget", "fetch libfetch", "Go", "Go-http-client", "ddclient", "Mikrotik", "xh"]
netinfos = ["ip", "ports", "cpes", "hostnames", "tags", "vulns"]
colors = [ '#2488bf', '#d84d3d', '#f39700', '#4caf50' ]

def to_yaml(value):
  return (yaml.dump(value, default_flow_style=False))
app.jinja_env.filters['to_yaml'] = to_yaml

def get_name(host):
  if environ.get('GEOIPNAME') is not None:
    return (environ.get('GEOIPNAME'))
  return (host)

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
    name = ip
  return (name)

#
# Get host's IP
#
def getip(ip):
  if any(c.isalpha() for c in ip) and '.' in ip:
    try:
      ip = socket.gethostbyname(ip)
    except:
      ip = 0
  return (ip)

#
# Get request headers
#
def gethead(request, ip):
  if request.headers.getlist('X-Forwarded-For'):
    ip = request.headers.getlist('X-Forwarded-For')[0]
  elif request.headers.get('CF-Connecting-IP'):
    ip = request.headers.get('CF-Connecting-IP')
  else:
    ip = request.remote_addr
  if request.headers.get("X-Forwarded-For"):
    forwarded = request.headers.get("X-Forwarded-For").split(',')[0]
  else:
    forwarded = "None, there is no forwarded IP"
  head = {
    "ip_address": ip,
    "remote_host": gethost(ip),
    "port": request.environ.get('REMOTE_PORT'),
    "user-agent": request.headers.get("User-Agent"),
    "mime_type": request.headers.get("Accept"),
    "language": request.headers.get("Accept-Language"),
    "encoding": request.headers.get("Accept-Encoding"),
    "method": request.method,
    "cache-control": request.headers.get("Cache-Control"),
    "x-forwarded-for": forwarded.split(',')[0],
    "x-forwarded-proto": request.headers.get("X-Forwarded-Proto")
  }
  return (head)

#
# Location GeoIP database informations querry
#
def getcity(ip):
  geoipath = "/var/lib/GeoIP"
  try:
    with geoip2.database.Reader(geoipath + '/GeoLite2-City.mmdb') as city_reader:
      city_res = city_reader.city(ip)
  except:
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
    return (0)
  return (asn_res)

#
# Network informations querry
#
def getnet(ip):
  try:
    network = requests.get(f"https://internetdb.shodan.io/{ip}").json()
    network = dict([(k.lower(),v) for k,v in network.items() if len(v)>0])
    if "detail" in network:
      del network["detail"]
  except:
    return(0)
  return (network)

#
# GeoIP informations put in a dict
#
def getgeo(ip):
  infos = {
    "ip_address": ip
  }
  infos.update({"hostname": gethost(ip)})

  city_res = getcity(ip)
  if city_res:
    infos.update({
        "country": city_res.country.name,
        "country_code": city_res.country.iso_code,
        "city": city_res.city.name,
        "latitude": city_res.location.latitude,
        "longitude": city_res.location.longitude
    })
  else:
    return (0)

  asn_res = getasn(ip)
  if asn_res:
    infos.update({
      "isp": asn_res.autonomous_system_organization,
      "asn": f"AS{asn_res.autonomous_system_number}"
    })
  else:
    return (0)

  return (infos)

#
# Return a single info
#
def getself(request, info):
  ip = request.headers.get('X-Client-Ip')
  info = info.lower()
  infos = gethead(request, ip)
  if (infos := getgeo(ip)) == 0:
    infos = {"Error": f"No location data about {ip}"}
  if info in netinfos:
    infos.update(getnet(ip))

  if info == "all":
    return (to_yaml(infos))
  if info == "json":
    return (infos)

  if not info in infos and info != "all":
    return (f"No data about {info} for {ip}\n")

  if isinstance(infos[info], list):
    conv = { i : infos[info][i] for i in range(0, len(infos[info]) ) }
    infos[info] = conv
    return (to_yaml(infos[info]))

  return (infos[info] + '\n')

####################
### FLASK ROUTES ###
####################

#
# Specific info path
#
@app.route('/<ip>/<info>')
def getspec(ip, info):
  ip = getip(ip)
  if IPAddress(ip).is_private():
    return(f"{ip} is a private IP\n")

  info = info.lower()
  if (infos := getgeo(ip)) == 0:
    infos = {"Error": f"No location data about {ip}"}
  if info in netinfos:
    infos.update(getnet(ip))

  if info == "all":
    return (to_yaml(infos))
  if info == "json":
    return (infos)

  if not info in infos:
    return (f"No data about {info} for {ip}\n")

  if isinstance(infos[info], list):
    conv = { i : infos[info][i] for i in range(0, len(infos[info]) ) }
    infos[info] = conv
    return (to_yaml(infos[info]))

  return (infos[info] + '\n')

#
# IP path
#
@app.route('/<ip>')
def getinfo(ip):
  ip = getip(ip)
  if any(c.isalpha() for c in ip):
    return (getself(request, ip))
  if ip == 0:
    return (f"Host unavailable\n")
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")

  if (infos := getgeo(ip)) == 0:
    infos = {"Error": f"No location data about {ip}"}
  network = getnet(ip)

  if any(x in request.headers.get('User-Agent') for x in cli):
    infos.update(network)
    return (to_yaml(infos))
  else:
    title = get_name(request.headers.get("host"))
    return (render_template('template.html',
            hostname=request.headers.get("host"),
            title=title,
            ip=request.headers.get('X-Client-Ip'),
            infos=infos,
            network=network,
            color=random.choice(colors)))

#
# Json path
#
@app.route('/<ip>/json')
def getinfojson(ip):
  ip = getip(ip)
  if ip == 0:
    return (f"Host unavailable\n")
  if IPAddress(ip).is_private():
    return (f"{ip} is a private IP\n")

  if (infos := getgeo(ip)) == 0:
    infos = {"Error": f"No location data about {ip}"}
  infos.update(getnet(ip))

  return (infos)

#
# Root path
#
@app.route('/')
def self():
  if request.headers.getlist('X-Forwarded-For'):
    ip = request.headers.getlist('X-Forwarded-For')[0]
  elif request.headers.get('CF-Connecting-IP'):
    ip = request.headers.get('CF-Connecting-IP')
  else:
    ip = request.remote_addr
  if any(x in request.headers.get('User-Agent') for x in cli):
    return (str(ip) + '\n')
  head = gethead(request, ip)
  if (infos := getgeo(ip)) == 0:
    infos = {"Error": f"No location data about {ip}"}
  network = getnet(ip)
  title = get_name(request.headers.get("host"))
  return (render_template('template.html',
          hostname=request.headers.get("host"),
          title=title,
          ip=ip,
          head=head,
          infos=infos,
          network=network,
          color=random.choice(colors)))

#
# Favicon
#
@app.route('/favicon.ico')
def favicon():
  return ("Not found"), 404
