import re
import json
import parsers.geoIP
import config


def parse(ipregex, line, signature):
    match = re.findall(ipregex, line)
    if match:
        ip = match[0]
        geoinfo = getgeoinfo(ip)
        event = formatpayload(ip, geoinfo, signature)
        return event
    else:
        pass


def getgeoinfo(ip):
    geoinfo = parsers.geoIP.push(ip)
    return geoinfo


def formatpayload(ip, geoinfo, signature):
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
