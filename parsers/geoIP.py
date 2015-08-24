import GeoIP


def push(ip):
    geoDB = GeoIP.open("GeoIPCity.dat", GeoIP.GEOIP_STANDARD)

    record = geoDB.record_by_addr(ip)

    return record
