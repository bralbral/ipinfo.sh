# IPinfo.sh

Get informations about an IP address.

## Description

A simple service for getting informations about an IP address.

This is the code that powers [ipinfo.sh](https://ipinfo.sh)

## Getting Started

### API usage examples

Getting your IP address:
```
$ curl ipinfo.sh
82.65.42.142
```

Getting 9.9.9.9 country:
```
$ curl ipinfo.sh/9.9.9.9/country
United States
```

Getting 9.9.9.9 hostname:
```
$ curl ipinfo.sh/9.9.9.9/hostname
dns9.quad9.net
```

Getting 1.1.1.1 open ports:
```
$ curl ipinfo.sh/1.1.1.1/ports
[53, 80, 443]
```

Getting all 9.9.9.9 informations, with pretty yaml format:
```
$ curl ipinfo.sh/9.9.9.9
asn: AS19281
city: Berkeley
country: United States
country_code: US
hostname: dns9.quad9.net
hostnames:
- dns9.quad9.net
ip: 9.9.9.9
ip_address: 9.9.9.9
isp: QUAD9-AS-1
latitude: 37.8767
longitude: -122.2676
ports:
- 53
- 443
```

Getting all your own infomations, in yaml then in json:
```
$ curl ipinfo.sh/all
asn: AS12322
city: null
country: France
country_code: FR
hostname: 82-65-42-142.subs.proxad.net
hostnames:
- 82-65-42-142.subs.proxad.net
ip: 82.65.42.142
ip_address: 82.65.42.142
isp: Free SAS
latitude: 48.8582
longitude: 2.3387
ports:
- 32400

$ curl ipinfo.sh/json
{"asn":"AS12322","city":null,"country":"France","country_code":"FR","hostname":"82-65-42-142.subs.proxad.net","hostnames":["82-65-42-142.subs.proxad.net"],"ip":"82.65.42.142","ip_address":"82.65.42.142","isp":"Free SAS","latitude":48.8582,"longitude":2.3387,"ports":[32400]}
```

Getting exposed services and potentials vulnerabilities:
```
$ curl ipinfo.sh/153.122.112.234/cpes
0: cpe:/a:php:php:7.0.2
1: cpe:/a:openbsd:openssh:5.3
2: cpe:/a:jquery:jquery
3: cpe:/a:apache:http_server

$ curl ipinfo.sh/153.122.112.234/vulns
0: CVE-2013-7456
1: CVE-2016-7128
2: CVE-2016-4540
3: CVE-2011-5000
4: CVE-2018-10549
5: CVE-2016-10712
...
```

And you can find more examples in the website [ipinfo.sh](https://ipinfo.sh)

### Dependencies

ipinfo require local geoip databases (.mmdb), located by default in /var/lib/GeoIP.

I recommend using [geoipupdate](https://github.com/maxmind/geoipupdate) with a free key.

#### Docker

 - docker
 - docker-compose
 - geoipupdate

#### Source

 - python3
 - geoipupdate
 - geoip2>=4.5.0
 - Flask>=2.0.3
 - netaddr>=0.8.0
 - pyyaml>=6.0

### Installing

#### Docker
```
git clone https://git.rznet.fr/razian/geoipweb-py.git
cd geoipweb-py
vim docker-compose.yml
# edit port and geoip volume
docker-compose up -d
```

#### Source
```
git clone https://git.rznet.fr/razian/geoipweb-py.git
cd geoipweb-py
pip install --upgrade -r requirements.txt
python -m flask run --host=0.0.0.0 --port=8080
```

## Author

 - Tom Chivert [@razian](https://rznet.fr/)

The [github repo](https://github.com/tchivert/ipinfo.sh) is a mirror of [this repo](https://git.rznet.fr/razian/geoipweb-py).

## Acknowledgments

* [ifconfig.io](https://github.com/georgyo/ifconfig.io)
* [ifconfig.co](https://github.com/mpolden/echoip)
* [geoipupdate](https://github.com/maxmind/geoipupdate)
* [internetdb](https://internetdb.shodan.io/)
