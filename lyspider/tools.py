def get_link_from_json(line):
    url = "/line/t" + line['prop']
    if int(line['proType']) < 3:
        url += "j1p" + str(line['Id']) + "c0.html"
    else:
        url += "j" + line['proType'] + "p" + str(line['Id']) + "c" + line[
            'portCityId'] + ".html"
    return url
