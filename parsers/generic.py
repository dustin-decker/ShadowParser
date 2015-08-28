import re
import json
import parsers.geoIP
import config


def parse(ip, line):
    match = re.findall(ip, line)
    if match:
        ip = match[0]
        geoinfo = getGeoInfo(ip)
        event = format(ip, geoinfo)
        return event
    else:
        pass


def getGeoInfo(ip):
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
                "signatureName": "not yet implemented",
                "attackerIP": ip,
                "targetIP": host['targetIP'],
                "hostHeader": "www.example.com"
            }
        )

        return event
    else:
        pass
