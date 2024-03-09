# -*- coding: utf-8 -*-

import json
import sys
import os

import datetime

today = datetime.date.today().strftime('%Y%m%d')
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')

pythonVer = 2
if sys.version_info.major == 3:
    pythonVer = 3

if pythonVer == 2:
    print("python 2")
    from urllib2 import urlopen, Request
else:
    from urllib.request import urlopen, Request

try:
    os.chmod("/usr/script/skyscraper.sh", 0o0755)
    os.chmod("/usr/script/skypicker.sh", 0o0755)
except Exception as e:
    print(e)


# png references
movies = {
    "1409": "sky-cinema",  # "sky-cinema-premiere"
    "4033": "sky-cinema",  # "sky-cinema-middle-earth"
    "1815": "sky-cinema",  # "sky-cinema-british-icons" # sky-cinema-greats
    "1199": "sky-cinema",  # "sky-cinema-animation"
    "1808": "sky-cinema",  # "sky-cinema-family"
    "1001": "sky-cinema",  # "sky-cinema-action"
    "4062": "sky-cinema",  # "sky-cinema-thriller"
    "4016": "sky-cinema",  # "sky-cinema-drama"
    "4017": "sky-cinema",  # "sky-cinema-scfi-hor"
    "4019": "sky-cinema"   # "sky-cinema-comedy"
}

entertainment = {
    "1276": "sky-showcase",
    "2201": "sky-witness",
    "1412": "sky-atlantic",
    "1402": "sky-max",
    "1177": "sky-comedy",
    "1752": "sky-arts",
    "2505": "sky-sci-fi",
    "1831": "sky-mix",
    "2510": "comedy-central",
    "1813": "comedy-xtra"
}

documentaries = {
    "1127": "sky-documentaries",
    "1875": "sky-history",
    "1879": "sky-history2",
    "2401": "discovery",
    "2407": "disc-history",
    "2406": "disc-science",
    "2409": "disc-turbo",
    "1065": "blaze",
    "2305": "yesterday",
    "1806": "national-geographic"
}

crime = {
    "1448": "crime-inv",
    "2207": "sky-crime",
    "2413": "id",
    "2303": "alibi",
    "3352": "true-crime",
    "3617": "true-crime-x"
}

nature = {
    "1194": "sky-nature",
    "2402": "animal-planet",
    "1847": "nat-geo-wild",
    "2302": "eden"
}

kids = {
    "5601": "cartoon-network",
    "5609": "boomerang",
    "1846": "nickelodeon",
    "1849": "nicktoons",
    "1857": "nick-jr",
    "2020": "cbbc",
    "2019": "cbeebies",
    "1147": "sky-kids",
    "1371": "cartoonito",
    "3750": "pop"
}


choice = [movies, entertainment, documentaries]

allchannels = {key:val for d in choice for key,val in d.items()}


urls = []

# max 10 channels per url call
# comment out channel groups you do not need

urls.append({'channel': 'Movies', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/1409,4033,1815,1199,1808,1001,4019,4062,4016,4017'})
urls.append({'channel': 'Movies', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/1409,4033,1815,1199,1808,1001,4019,4062,4016,4017'})

urls.append({'channel': 'Entertainment', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/1276,2201,1412,1402,1177,1752,2505,1831,2510,1813'})
urls.append({'channel': 'Entertainment', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/1276,2201,1412,1402,1177,1752,2505,1831,2510,1813'})

urls.append({'channel': 'Documentaries', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/1127,1875,1879,2401,2407,2406,2409,1065,2305,1806'})
urls.append({'channel': 'Documentaries', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/1127,1875,1879,2401,2407,2406,2409,1065,2305,1806'})

# urls.append({'channel': 'Crime', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/1448,2207,2413,2303,3352,3617'})
# urls.append({'channel': 'Crime', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/1448,2207,2413,2303,3352,3617'})

# urls.append({'channel': 'Nature', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/1194,2402,1847,2302'})
# urls.append({'channel': 'Nature', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/1194,2402,1847,2302'})

# urls.append({'channel': 'Kids', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(today) + '/5601,5609,1846,1849,1857,2020,2019,1147,1371,3750'})
# urls.append({'channel': 'Kids', 'url': 'https://awk.epgsky.com/hawk/linear/schedule/' + str(tomorrow) + '/5601,5609,1846,1849,1857,2020,2019,1147,1371,3750'})

hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}


def scraper():
    tilelist = []
    tilevalues = {}
    tilevalues = {}
    response = ""

    for url in urls:
        sys.stderr.write("Scraping :" + url['channel'] + "\n")
        req = Request(url['url'], headers=hdr)

        try:
            response = urlopen(req)
        except Exception as e:
            print(e)
            response = ""

        if response:
            initialdata = json.load(response)

            if 'schedule' in initialdata:

                for channel in initialdata["schedule"]:

                    sid = str(channel["sid"])
                    if sid and "events" in channel:

                        for event in channel["events"]:

                            e_uuid = ''
                            e_title = ''
                            e_channel = ''
                            e_cover = ''
                            e_background = ''
                            e_16_9 = ''
                            e_start = 0
                            e_duration = 0

                            try:
                                e_start = str(event["st"])
                                e_duration = str(event["d"])
                                e_uuid = str(event["programmeuuid"])
                                e_title = str(event["t"])
                            except:
                                pass

                            if e_uuid and e_start and e_duration:
                                e_channel = allchannels[sid]
                                e_cover = "https://images.metadata.sky.com/pd-image/" + e_uuid + "/cover/500"
                                e_background = "https://images.metadata.sky.com/pd-image/" + e_uuid + "/background/1280"
                                e_16_9 = "https://images.metadata.sky.com/pd-image/" + e_uuid + "/16-9/500"

                                tilevalues['UUID'] = str(e_uuid)
                                tilevalues['Title'] = str(e_title)
                                tilevalues['Channel'] = str(e_channel)
                                tilevalues['Background'] = str(e_background)
                                tilevalues['16_9'] = str(e_16_9)
                                tilevalues['Cover'] = str(e_cover)
                                tilevalues['Start'] = str(e_start)
                                tilevalues['Duration'] = str(e_duration)

                                tilelist.append(tilevalues.copy())

        else:
            print("**** no response ***")

    filename = '/etc/enigma2/slyk/image_awk_scrape.json'
    with open(filename, 'w') as f:
        json.dump(tilelist, f)


scraper()
