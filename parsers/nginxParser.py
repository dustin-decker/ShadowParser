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
        print(match)
        match = format(match)
        return match
    else:
        pass


def format(match):
    host = config.load()
    ip = match[0]
    geoinfo = parsers.geoIP.push(ip)

    match = json.dumps(
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

    return match


if __name__ == '__main__':
    pass
