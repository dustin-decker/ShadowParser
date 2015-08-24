import re
import json
import parsers.geoIP
import config


def parse(line):
    requestpattern = (r''
                      '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP address
                      )
    match = re.findall(requestpattern, line)
    if match:
        ip = match[0]
        geoinfo = getGeoInfo(match, ip)
        event = format(ip, geoinfo)
        return event
    else:
        pass


def getGeoInfo(match, ip):
    geoinfo = parsers.geoIP.push(ip)
    return geoinfo


def format(ip, geoinfo):
    host = config.load()
    if geoinfo:
        event = json.dumps(
            {
                "attackerLatitude": geoinfo['latitude'],
                "attackerLongitude": geoinfo['longitude'],
                "targetLongitude": host['targetLongitude'],
                "targetLatitude": host['targetLatitude'],
                "targetCountry": host['targetCountry'],
                "attackerCountry": geoinfo['country_name'],
                "signatureName": "LDAP Injection attempt",
                "attackerIP": ip,
                "targetIP": host['targetIP'],
                "hostHeader": "www.example.com"
            }
        )

        return event
    else:
        pass


if __name__ == '__main__':
    pass
