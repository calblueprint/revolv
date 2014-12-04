def get_solar_csv_url(csv_id, mode):
    """Gets request url to export csv for project with that id.
    Mode represents daily, monthly or annual values based on whether
    it is 1, 2, or 3 respectively."""

    url = "http://home.solarlog-web.net/sds/modul/SolarLogWeb/Statistik.php?logid=0&c="
    url += csv_id + "&mode=" + str(mode) + "&offset=0&flag=32&ex=csv"
    return url
