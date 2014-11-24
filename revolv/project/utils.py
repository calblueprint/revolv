def get_solar_csv_url(csv_id, offset):
    url = "http://home.solarlog-web.net/sds/modul/SolarLogWeb/Statistik.php?logid=0&c="
    url += csv_id + "&mode=1&offset=" + str(offset) + "&flag=32&ex=csv"
    return url
