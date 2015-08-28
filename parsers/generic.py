import re
import json
import parsers.geoIP
import config


def parse(ip, line, signature):
    match = re.findall(ip, line)
    if match:
        ip = match[0]
        geoinfo = getGeoInfo(ip)
        event = format(ip, geoinfo, signature)
        return event
    else:
        pass


def getGeoInfo(ip):
    geoinfo = parsers.geoIP.push(ip)
    return geoinfo


def format(ip, geoinfo, signature):
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
                "signatureName": signature,
                "attackerIP": ip,
                "targetIP": host['targetIP'],
                "hostHeader": "not yet implemented"
            }
        )

        return event
    else:
        pass


if __name__ == '__main__':
    pass
