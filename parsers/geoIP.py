import GeoIP


def push(ip):
    geoDB = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)
    record = geoDB.record_by_addr(ip)

    return record


if __name__ == '__main__':
    pass
