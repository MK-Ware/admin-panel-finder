#!/usr/bin/env python
#import required modules
from sys import argv
from datetime import datetime as dt
import sys
import random
try:#python 3
    import urllib.request as req
    from urllib.error import URLError, HTTPError
    three = True
except ImportError:#python 2
    import urllib2 as req
    three = False

#custom header to avoid being blocked by the website
custom_headers = {"User-Agent" : "Mozilla/5.0 (Windows NT {}; rv:{}.0) Gecko/20100101 Firefox/{}.0".format(random.randint(7,11),
                                                                                                           random.randint(40,50),
                                                                                                           random.randint(35,50))}

def adjustDomainName(domain):#correct domain name for urllib
    if domain.startswith("www."):
        domain = "http://" + domain[4:]
    if domain.endswith("/"):
        domain = domain[:-1]
    return domain

def loadWordList(wordlist_file):#load pages to check from dictionary
    try:
        with open(wordlist_file) as wlf:
            content = wlf.readlines()
        for i in range(len(content)):
            content[i] = content[i].strip("\n")
        return content
    except FileNotFoundError:
        sys.exit("Couldn't find wordlist file!")

def saveResults(file_name, found_pages, progress=0):
    now = dt.now()
    with open("admin_sniffer_results.txt", "a") as f:
        stamp = "%d-%d-%d %d: %d: %d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        print(stamp, file=f)
        for page in found_pages:
            print(page, file=f)
        print("total progress: %d\n______________________________________________" % progress, file=f)

def main(domain, progress=0, strict=False, save = True, visible=True, wordlist_file="admin_login.txt"):
    print("working... press ctrl+c at any point to abort...")
    resp_codes = {403 : "request forbidden", 401 : "authentication required"}#HTTP response codes
    found = []#list to hold the results we find
    domain = adjustDomainName(domain)#correct domain name for urllib

    print("loading wordlist...")
    attempts = loadWordList(wordlist_file)
    print("crawling...")
    
    for link in attempts[progress:]:#loop over every page in the wordlist file
        try:
            site = domain + "/" + link

            if visible:#show links as they're being tested
                print("trying:", end=" ")

            panel_page = req.Request(site, headers=custom_headers)
            
            try:
                resp = req.urlopen(site)#try visiting the page
                found.append(site)
                print("%s page valid!" % site)

            except HTTPError as e:#investigate the HTTPError we got
                if three:
                    c = e.getcode()
                else:
                    c = e.code()
                    
                if c == 404:
                    if visible:
                        print("%s not found..." % site)
                else:
                    print("%s potential positive.. %s" % (site, resp_codes[c]))
                    if not strict:
                        found.append(site)

            except URLError:
                print("invalid link or no internet connection!")
                break
            progress += 1
            
        except KeyboardInterrupt:#make sure we don't lose everything should the user get bored
            print()
            break

    if found:
        if save:#save results to a text file
            print("Saving results...")
            saveResults("admin_sniffer_results.txt", found)

            print("results saved to admin_sniffer_results.txt...")

        print("found the following results: " + "  ".join(found))

    else:
        print("could not find any panel pages... Make sure you're connected to the internet \n or try a different wordlist")

def getRobotsFile(domain):
    print("Attempting to get robots.txt file...")
    found = []
    domain = adjustDomainName(domain)#correct domain name for urllib
    
    robots_file = domain + "/robots.txt"
    try:
        data = req.urlopen(robots_file).read().decode("utf-8")
        for element in data.split("\n"):
            if element.startswith("Disallow:"):
                panel_page = domain + element[10:]
                print("Disallow rule found: %s" % (panel_page))
                found.append(panel_page)
        if found:
            print("admin panels found... Saving results to file...")
            saveResults("admin_sniffer_results.txt", found, 0)
            print("done...")
        else:
            print("could not find any panel pages in the robots file...")
    except:
        sys.exit("Could not retrieve robots.txt!")

if __name__ == "__main__":
    print("+++++++++++++++++++admin_panel_sniffer by MCoury+++++++++++++++++++")
    print("+                should work with python 2 or 3                   +")
    print("+           Author not responsible for malicious use!             +")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    if argv[1].upper() in ("HELP", "H"):
        print("python admin_panel_sniffer.py domain strict save visible wordlist\n\ndomain: the target domain\nstrict: optional, default False.. if True, HTTP codes that correspond to forbidden or authentication required will be ignored\nsave: optional, default True.. if True results will be saved to a txt file\nvisible: optional, default True.. if True each link will be shown as it's being tested\nwordlist: optional, default included wordlist.. wordlist file to be used")
        print("or:\npython admin_panel_sniffer.py domain robots to get the robots.txt file that usually contains the admin panel")

    elif len(argv) > 2 and argv[2].lower() in ("robots", "bots", "r"):
        getRobotsFile(argv[1])

    else:
        defs = ["pad", "pad", 0, "False", "True", "True", "admin_login.txt"]
        try:
            argv.extend(defs[len(argv):])
        except:
            pass
        target_domain = argv[1]
        prog = int(argv[2])
        mode = eval(argv[3])
        save = eval(argv[4])
        visible = eval(argv[5])
        wordlist = argv[6]
        main(target_domain, prog, mode, save, visible, wordlist)
