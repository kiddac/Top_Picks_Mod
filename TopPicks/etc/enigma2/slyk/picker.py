from PIL import Image
from datetime import datetime

import io
import json
import random
import sys

logo_source_folder = "/etc/enigma2/slyk/channel_logos_dark/"

pythonVer = 2
if sys.version_info.major == 3:
    pythonVer = 3

if pythonVer == 2:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen


def create_background(background):
    mask = Image.open('/etc/enigma2/slyk/images/mask.png').convert('RGBA')
    try:
        mask = mask.resize((backgroundsize[0], backgroundsize[1]), Image.Resampling.LANCZOS)
    except:
        mask = mask.resize((backgroundsize[0], backgroundsize[1]), Image.ANTIALIAS)
    plainbg = Image.open(skin_folder + image_folder + "background.jpg").convert('RGBA')
    try:
        background = background.resize((backgroundsize[0], backgroundsize[1]), Image.Resampling.LANCZOS)
    except:
        background = background.resize((backgroundsize[0], backgroundsize[1]), Image.ANTIALIAS)
    backgroundw, backgroundh = background.size
    plainsizew, plainsizeh = plainbg.size
    plainbg.paste(background, (plainsizew - backgroundw, 0), mask)
    plainbg = plainbg.convert('RGB')
    plainbg.save(skin_folder + image_folder + "hero.jpg", quality=85)


def download_image(url):
    try:
        fd = urlopen(url)
    except:
        if 'background' in url:
            url = url.replace('background', '16-9')
        if 'cover' in url:
            url = url.replace('cover', '16-9')
        if '16-9' in url:
            url = url.replace('16-9', 'cover')

        try:
            fd = urlopen(url)
        except:
            im = ""
            return im

    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    im = im.convert('RGB')
    return im


def crop_image(im, width, height):
    ratio = float(im.size[0]) // im.size[1]

    if width // height < ratio:
        crop_width = int(height * ratio)
        crop_height = height
    elif width // height > ratio:
        crop_width = width
        crop_height = int(width // ratio)
    else:
        crop_width = width
        crop_height = height

    size = crop_width, crop_height
    tl_w = (crop_width - width) // 2
    tl_h = (crop_height - height) // 2
    br_w = crop_width - ((crop_width - width) // 2)
    br_h = crop_height - ((crop_height - height) // 2)

    area = (tl_w, tl_h, br_w, br_h)
    try:
        im = im.resize((size), Image.Resampling.LANCZOS).crop(area)
        im = im.resize((width, height), Image.Resampling.LANCZOS)
    except:
        im = im.resize((size), Image.ANTIALIAS).crop(area)
        im = im.resize((width, height), Image.ANTIALIAS)

    return im


def add_logo(im, channel, logo_height):

    posx = 0
    posy = 0

    if skin_size == 1080:
        padding = 4
    else:
        padding = 2

    try:
        logo = Image.open(logo_source_folder + channel + '.png').convert('RGBA')
    except:
        logo = Image.open(logo_source_folder + 'blank.png').convert('RGBA')

    hpercent = (logo_height / float(logo.size[1]))
    wsize = int((float(logo.size[0]) * float(hpercent)))
    try:
        logo = logo.resize((wsize, logo_height), Image.Resampling.LANCZOS)
    except:
        logo = logo.resize((wsize, logo_height), Image.ANTIALIAS)

    img_w, img_h = im.size
    logo_w, logo_h = logo.size

    if logo_halign == "left":
        posx = 0 + padding

    if logo_halign == "right":
        posx = img_w - logo_w - padding

    if logo_halign == "center":
        posx = ((img_w - logo_w) // 2)

    if logo_valign == "top":
        posy = 0 + padding

    if logo_valign == "bottom":
        posy = img_h - logo_h - padding

    im.paste(logo, (posx, posy), logo)

    return im


with open('/etc/enigma2/settings', 'r') as settingsfile:
    for skin in settingsfile:
        if 'config.skin.primary_skin=' in skin:
            skin = skin.replace("config.skin.primary_skin=", "").replace("/skin.xml", "")
            sys.stderr.write(skin + "\n")
            sys.stderr.write("Processing...Please Wait.\n")
            break

try:
    with open('/etc/enigma2/slyk/image_awk_scrape.json') as json_data:
        tfile = json.load(json_data)
except:
    sys.stderr.write("Please run skyscraper.sh before running the picker script.\n")
    sys.exit()

if skin.strip() == "slyk-onyx-1080":
    skin_size = 1080
    number_of_images = 10

    portrait_size = [202, 270]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7]

    landscape_size = [407, 241]
    landscape_pics = [8, 9, 10]

    background = False
    backgroundsize = []

    logos = True
    logo_height = 18
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    skin_folder = "/usr/share/enigma2/slyk-onyx-1080/"
    image_folder = "whatson-gfx/"
    image_prefix = "whatson"

elif skin.strip() == "slyk-onyx-720":
    skin_size = 720
    number_of_images = 10

    portrait_size = [134, 180]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7]

    landscape_size = [270, 161]
    landscape_pics = [8, 9, 10]

    background = False
    backgroundsize = []

    logos = True
    logo_height = 12
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    skin_folder = "/usr/share/enigma2/slyk-onyx-720/"
    image_folder = "whatson-gfx/"
    image_prefix = "whatson"

elif skin.strip() == "slyk-1080-r19":
    skin_size = 1080
    number_of_images = 12

    portrait_size = [246, 328]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    landscape_size = []
    landscape_pics = []

    background = True
    backgroundsize = [1280, 720]

    logos = True
    logo_height = 21
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    skin_folder = "/usr/share/enigma2/slyk-1080-r19/"
    image_folder = "toppicks/screens2/"
    image_prefix = "toppicks"

elif skin.strip() == "slyk-720-r19":
    skin_size = 720
    number_of_images = 12

    portrait_size = [164, 219]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    landscape_size = []
    landscape_pics = []

    background = True
    backgroundsize = [853, 480]

    logos = True
    logo_height = 14
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    skin_folder = "/usr/share/enigma2/slyk-720-r19/"
    image_folder = "toppicks/screens2/"
    image_prefix = "toppicks"

elif skin.strip() == "slyk-q-1080":
    skin_size = 1080
    number_of_images = 10

    portrait_size = [240, 320]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    landscape_size = []
    landscape_pics = []

    background = True
    backgroundsize = [1280, 720]

    logos = True
    logo_height = 21
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    skin_folder = "/usr/share/enigma2/slyk-q-1080/"
    image_folder = "q-toppicks/"
    image_prefix = "toppicks"

elif skin.strip() == "slyk-q-720":
    skin_size = 720
    number_of_images = 10

    portrait_size = [160, 213]
    portrait_pics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    landscape_size = []
    landscape_pics = []

    background = True
    backgroundsize = [853, 480]

    logos = True
    logo_height = 14
    logo_valign = "top"
    logo_halign = "center"
    picons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    skin_folder = "/usr/share/enigma2/slyk-q-720/"
    image_folder = "q-toppicks/"
    image_prefix = "toppicks"

elif skin.strip() == "vskin-1080" or skin.strip() == "vskin-bolt-1080" or skin.strip() == "vskin-red-1080":
    skin_size = 1080
    number_of_images = 4

    portrait_size = []
    portrait_pics = []

    landscape_size = [252, 189]
    landscape_pics = [1, 2, 3, 4]

    background = False
    backgroundsize = []

    logos = False
    logo_height = 21
    logo_valign = "top"
    logo_halign = "center"
    picons = []

    skin_folder = "/usr/share/enigma2/"
    image_folder = "vskin-gfx/"
    image_prefix = "whatson"

elif skin.strip() == "vskin-720" or skin.strip() == "vskin-bolt-720" or skin.strip() == "vskin-red-720":
    skin_size = 720
    number_of_images = 4

    portrait_size = []
    portrait_pics = []

    landscape_size = [168, 126]
    landscape_pics = [1, 2, 3, 4]

    background = False
    backgroundsize = []

    logos = False
    logo_height = 14
    logo_valign = "top"
    logo_halign = "center"
    picons = []

    skin_folder = "/usr/share/enigma2/"
    image_folder = "vskin-gfx/"
    image_prefix = "whatson"


now = datetime.now().timestamp()
filename = '/etc/enigma2/slyk/shortlist.json'

if tfile == []:
    sys.stderr.write("No Valid Scrapes. Please run /usr/script.skyscraper.sh first. \n")
    sys.exit()

x = 0
shortlist = []
for entry in tfile:
    if (int(tfile[x]['Start']) + int(tfile[x]['Duration']) < int(now)) or (int(tfile[x]['Start']) > (int(now) + (2 * 3600))):
        x += 1
        continue
    else:
        shortlist.append(entry)
    x += 1


with open(filename, 'w') as f:
    json.dump(shortlist, f)

pick = random.sample(range(0, len(shortlist) - 1), len(shortlist) - 1)
selectedlist = []
y = 0
for x in range(1, number_of_images + 1):

    if x == 1 and background:
        invalid = True
        while invalid:

            if y >= (len(shortlist) - 1):
                break

            url = shortlist[pick[y]]['Background']
            # sys.stderr.write(str(y) + " " + shortlist[pick[y]]['Title'] + " " + url + "\n")
            try:
                im = download_image(url)
                im.verify()
                create_background(im)
                invalid = False

            except Exception as e:
                print(e)
                y += 1
                if y > (len(shortlist) - 1):
                    break

    if portrait_pics != [] and x in portrait_pics:
        invalid = True
        while invalid:

            if y >= (len(shortlist) - 1):
                break

            if str(shortlist[pick[y]]['Title']) in selectedlist:
                y += 1
                if y >= (len(shortlist) - 1):
                    break
                else:
                    continue

            url = shortlist[pick[y]]['Cover'].replace('500', str(portrait_size[1] * 2))
            # sys.stderr.write(str(y) + " " + shortlist[pick[y]]['Title'] + " " + url + "\n")
            width = portrait_size[0]
            height = portrait_size[1]

            try:
                im = download_image(url)
                im.verify()
                im = crop_image(im, width, height)
                channel = shortlist[pick[y]]['Channel']
                if logos and x in picons:
                    im = add_logo(im, channel, logo_height)
                im.save(skin_folder + image_folder + image_prefix + str(x) + ".jpg", quality=100)
                invalid = False
                selectedlist.append(str(shortlist[pick[y]]['Title']))

            except Exception as e:
                print(e)
                y += 1
                if y >= (len(shortlist) - 1):
                    break

        y += 1
        if y > len(shortlist) - 1:
            break

    if landscape_pics != [] and x in landscape_pics:
        invalid = True
        while invalid:

            if y >= (len(shortlist) - 1):
                break

            if str(shortlist[pick[y]]['Title']) in selectedlist:
                y += 1
                if y >= (len(shortlist) - 1):
                    break
                else:
                    continue

            url = shortlist[pick[y]]['16_9'].replace('500', str(landscape_size[0] * 2))
            # sys.stderr.write(str(y) + " " + shortlist[pick[y]]['Title'] + " " + url + "\n")
            width = landscape_size[0]

            height = landscape_size[1]
            try:
                im = download_image(url)
                im.verify()
                im = crop_image(im, width, height)
                channel = shortlist[pick[y]]['Channel']
                if logos:
                    im = add_logo(im, channel, logo_height)
                im.save(skin_folder + image_folder + image_prefix + str(x) + ".jpg", quality=100)
                invalid = False
                selectedlist.append(shortlist[pick[y]]['Title'])

            except Exception as e:
                print(e)
                invalid = True
                y += 1
                if y >= (len(shortlist) - 1):
                    break

        y += 1
