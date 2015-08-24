import GeoIP


def push(ip):
    geoDB = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)
    # ip = '168.235.64.205'
    record = geoDB.record_by_addr(ip)

    return record
