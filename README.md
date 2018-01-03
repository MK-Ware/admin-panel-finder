# admin_panel_sniffer
A powerful admin login page finder in python.. Should work with both python 2 and 3.

# Features:
- Huge dictionary file, which of course can be changed to anything you want.
- Progress tracking, if connection drops and the script has to stop for one reason or another, it'll give you the links that it could find and a progress parameter that you can provide the next time you run the program so you don't have to start from the beginning again.
- User can specify the website page extension (.asp, .php etc) to narrow down the search options.
- Results can be saved to a text file for future reference, and the user may choose to silence the script so that it doesn't show every link as it tests it.
- Ability to pull robots.txt which sometimes might save you having to search the dictionary file as it often contains the link to the panel. The script attempts to parse robots.txt.
- self changing user-agent that (a) keeps changing itself so that you don't end up getting blocked and (b) mimics a browser's user-agent to further minimize the chance that you get locked outside.


# Use:
python admin_panel_sniffer.py --domain [target domain] --progress [index of the page the script reached last run] --page_extension [website language] --strict [True or False] --save [Save the results to a text file?] --verbose [print links as they're tested?] --wordlist [dictionary file to use] --robots [if True don't enter anything else except the domain name]

- domain is obvious.
- progress: the index of the page the script reached last run.. The script displays and saves this value in the results file after every run. 0 starts from the beginning.
- page_extension: whether the website uses html asp php... default value is a which checks everything...
- strict: whether or not you care about 403 and 401 responses.
- verbose: whether or not you want the script to show each link as it's being tested

or:<br />
- python admin_panel_sniffer.py --domain [target domain] --robots True to search in the robots.txt file that usually contains the admin panel

python admin_panel_sniffer.py h or help for more details.. or of course take a look at the source code ;)

PS: written for pure testing, author not responsible for misuse.
