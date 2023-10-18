def district_URL_scrapper(Const):
    i = 1
    districts_URL = []
    URL_base = Const.URL
    districts = Const.electoral_district_number
    while i < districts:
        URL = URL_base + str(i)
        districts_URL.append(URL)
        i = i + 1
    return districts_URL