#!/bin/sh
#

# Slyk Universal toppicks V7 (C) kiddac. 2024

python /etc/enigma2/slyk/scraper.py

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

if test -f /etc/enigma2/slyk/image_awk_scrape.json; then
    python /etc/enigma2/slyk/picker.py
fi
exit 0
