import GeoIP


def push(ip):
    geodb = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)
    record = geodb.record_by_addr(ip)

    return record


if __name__ == '__main__':
    pass
