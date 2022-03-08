# geoipweb

A simple service for getting informations about an IP address. This is the code that powers ipinfo.sh

## Usage

### API
```bash
$ curl ipinfo.sh
82.65.180.141

$ curl ipinfo.sh/1.1.1.1/country
Australia

$ curl ipinfo.sh/one.one.one.one/ip
1.1.1.1

$ curl ipinfo.sh/153.122.112.234
asn: AS131921
city: null
country: Japan
country_code: JP
cpes:
- cpe:/a:php:php:7.0.2
- cpe:/a:openbsd:openssh:5.3
- cpe:/a:jquery:jquery
- cpe:/a:apache:http_server
hostname: sub0000542438.hmk-temp.com
hostnames:
- sub0000542438.hmk-temp.com
ip: 153.122.112.234
ip_address: 153.122.112.234
isp: GMO GlobalSign Holdings K.K.
latitude: 35.6897
longitude: 139.6895
ports:
- 22
- 80
- 443
vulns:
- CVE-2013-7456
- CVE-2016-7128
- CVE-2016-4540
- CVE-2011-5000
```
More examples on the [website](https://ipinfo.sh).

## Install

Require local geoip databases (.mmdb).
Default path: /var/lib/GeoIP fetched by geoipmysql.

```
git clone https://git.rznet.fr/razian/geoipweb-py.git
vim docker-compose.yml
# edit port and geoip volume
docker-compose up -d
```
