#!/usr/bin/env python
#import required modules
from sys import argv
import random
try:#python 3
    import urllib.request as req
    from urllib.error import URLError, HTTPError
    three = True
except ImportError:#python 2
    import urllib2 as req
    three = False

def loadWordList(wordlist_file):#load pages to check from dictionary
    with open(wordlist_file) as wlf:
        content = wlf.readlines()
    for i in range(len(content)):
        content[i] = content[i].strip("\n")
    return content

def main(domain, strict=False, save = True, visible=True, wordlist_file="admin_login.txt"):
    print("working... press ctrl+c at any point to abort...")
    resp_codes = {403 : "request forbidden", 401 : "authentication required"}#HTTP response codes
    found = []#list to hold the results we find
    if domain.startswith("www."):#correct domain name for urllib
        domain = "http://" + domain[4:]
    print("loading wordlist...")
    attempts = loadWordList(wordlist_file)
    print("crawling...")
    #custom header to avoid being blocked by the website
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT {}; rv:{}.0) Gecko/20100101 Firefox/{}.0".format(random.randint(7,11),
                                                                                                        random.randint(40,50),
                                                                                                        random.randint(35,50))}
    for link in attempts:#loop over every page in the wordlist file
        try:
            if domain.endswith("/"):
                site = domain + link
            else:
                site = domain + "/" + link

            if visible:#show links as they're being tested
                print("trying:", end=" ")

            panel_page = req.Request(site, headers=headers)
            
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
                    print("potential positive.. %s" % (resp_codes[c]))
                    if not strict:
                        found.append(site)

            except URLError:
                print("invalid link or no internet connection!")
                break
        except KeyboardInterrupt:#make sure we don't lose everything should the user get bored
            print()
            break

    if found:
        if save:#save results to a text file
            print("Saving results...")
            with open("admin_sniffer_results.txt", "a") as f:
                for link in found:
                    print(link, file=f)
                print("______________________________________________", file=f)

            print("results saved to admin_sniffer_results.txt...")

        print("found the following results: " + "  ".join(found))

    else:
        print("could not find any panel pages... Make sure you're connected to the internet \n or try a different wordlist")

if __name__ == "__main__":
    print("+++++++++++++++++++admin_panel_sniffer by MCoury+++++++++++++++++++")
    print("                should work with python 2 or 3")
    print("           Author not responsible for malicious use!")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    if argv[1].upper() in ("HELP", "H"):
        print("python admin_panel_sniffer.py domain strict save visible wordlist\n\ndomain: the target domain\nstrict: optional, default False.. if True, HTTP codes that correspond to forbidden or authentication required will be ignored\nsave: optional, default True.. if True results will be saved to a txt file\nvisible: optional, default True.. if True each link will be shown as it's being tested\nwordlist: optional, default included wordlist.. wordlist file to be used")

    else:
        defs = ["pad", "pad", "False", "True", "True", "admin_login.txt"]
        try:
            argv.extend(defs[len(argv):])
        except:
            pass
        target_domain = argv[1]
        mode = eval(argv[2])
        save = eval(argv[3])
        visible = eval(argv[4])
        wordlist = argv[5]
        main(target_domain, mode, save, visible, wordlist)
