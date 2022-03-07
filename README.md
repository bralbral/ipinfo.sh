# geoipweb

A simple service for getting informations about an IP address. This is the code that powers rzip.fr

## Usage

### Webpage
https://rzip.fr/1.1.1.1

### API

```
$ curl rzip.fr/1.1.1.1/json
{"ASN":"AS13335","City":null,"Country":"Australia","Country Code":"AU","Hostname":"one.one.one.one","Hostnames":["one.one.one.one"],"IP Address":"1.1.1.1","ISP":"CLOUDFLARENET","Ip":"1.1.1.1","Latitude":-33.494,"Longitude":143.2104,"Ports":[53,80,443]}

$ curl rzip.fr/1.1.1.1/country
Australia

$ curl rzip.fr/1.1.1.1/ISP
CLOUDFLARENET

$ curl rzip.fr/1.1.1.1/ports
{"0":53,"1":80,"2":443}
```

Prettier json
```
curl -s rzip.fr/1.1.1.1/json | jq .
{
  "ASN": "AS13335",
  "City": null,
  "Country": "Australia",
  "Country Code": "AU",
  "Hostname": "one.one.one.one",
  "Hostnames": [
    "one.one.one.one"
  ],
  "IP Address": "1.1.1.1",
  "ISP": "CLOUDFLARENET",
  "Ip": "1.1.1.1",
  "Latitude": -33.494,
  "Longitude": 143.2104,
  "Ports": [
    53,
    80,
    443
  ]
}
```

## Install

Require local geoip databases (.mmdb).
Default path: /var/lib/GeoIP fetched by geoipmysql.

```
git clone https://git.rznet.fr/razian/geoipweb-py.git
vim docker-compose.yml
# edit port and geoip volume
docker-compose up -d
```
