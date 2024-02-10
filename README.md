# Top_Picks_Mod
Mod for Kiddac Skins to bring in cover art on the menu page

Install IPK

Use FTP client change the permissions of the 2 script files to 755

/usr/script/skyscraper.sh

/usr/script/skypicker.sh

Edit cron file so the scripts run at scheduled time

/etc/cron/crontabs/root

0 9 * * * /usr/script/skyscraper.sh 

*/10 * * * * /usr/script/skypicker.sh

Reboot gui
