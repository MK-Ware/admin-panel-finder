# admin_panel_sniffer
A powerful admin login page finder in python.. Should work with both python 2 and 3.

# Use:
python admin_panel_sniffer.py domain strict save visible wordlist

domain is obvious.

progress: the index of the page the script reached last run.. The script displays and saves this value in the results file after every run. 0 starts from the beginning

page_extension: whether the website uses html asp php... default value is a which checks everything...

strict: whether or not you care about 403 and 401 responses

visible: whether or not you want the script to show each link as it's being tested

or:
python admin_panel_sniffer.py domain robots to search in the robots.txt file that usually contains the admin panel
______________________________________________________________________________________________________
python admin_panel_sniffer.py h or help for more details.. or of course take a look at the source code ;)

PS: written for pure testing
