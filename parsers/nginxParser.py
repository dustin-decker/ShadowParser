import re
import json
import parsers.geoIP
import config

def parse(line):
    requestpattern = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP address
           '"GET\s(.+)\s\w+/.+"\s\d+\s'  # requested file
           '"(.+)"'  # user agent
           )
    match = re.findall(requestpattern, line)
    if match:
        match = format(match)
        return match
    else:
        pass

def format(match):
    target = config.load()
    ip = match[0]
    geoinfo = parsers.geoIP.push(ip)

    json.dump(
        {
        "attackerLatitude": geoinfo['latitude'],
        "attackerLongitude": geoinfo['longitude'],
        "targetLongitude": target['targetLongitude'],
        "targetLatitude": target['targetLatitude'],
        "targetCountry": target['targetCountry'],
        "attackerCountry": geoinfo['country_name'],
        "signatureName": "LDAP Injection attempt",
        "attackerIP": ip,
        "targetIP": target['targetIP'],
        "hostHeader": "www.example.com"
        }
    )


if __name__ == '__main__':
    pass