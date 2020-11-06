import re
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup

crawled_url = set()
uniq_url = set()
subdomain = dict()
returnLink = ""

maximumWordCount = 0
bigBook = {}


def scraper(url, resp):
    """
    :param url: given url
    :param resp: response from the website
    :return:
    """
    global bigBook  # used for the word dictionary for frequencies

    links = extract_next_links(url, resp)  # all relative url put into links

    print("New test starts here")
    # print(subdomain.items())
    # count of all the subdomains (question #4)
    for i in sorted(subdomain.keys()):
        print(i, ":", subdomain[i])

    # for i, j in sorted(subdomain.items()):
    # print(i, ", ", len(j), ": ", j)
    print("Total number of unique urls: ", len(uniq_url))  # question #1 (how many unique url there is yuh)
    # print(uniq_url)
    print50(bigBook)  # prints top 50 most frequent words
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    """
    gets the link -lydia(2020)
    :param url:
    :param resp:
    :return:  all relative url put into links
    """
    global returnLink  # link with the most words
    global maximumWordCount
    global bigBook  # dictionary holding all the words/freq
    # Implementation required.
    parsed = urlparse(url)  # parsed holds the url
    links = list()
    print("---------------------------------")
    print("Current url:", url)
    # 200 OK,201 Create,202 Accepted
    if is_valid(url) and 200 <= resp.status <= 202 and url not in crawled_url:
        # url passes all tests and is valid
        crawled_url.add(url)

        # read the page and save all urls that haven't been crawled.
        html_doc = resp.raw_response.content
        # put the html_doc variable contents into a file along with parsed
        f = open("storeDocument.txt", "a")  # argument a is for "append", change to "w" if you want to write over file
        # f1 = open("icsurl.txt","a")
        # write the url followed by the contents of the page
        f.write(parsed.geturl())
        soup = BeautifulSoup(html_doc, 'html.parser')
        # this loop gets the maximum word count from all the url
        s = soup.get_text()
        f.write(s)
        f.close()

        # Saving for top 50 words
        wordList = simple_tokenize(s.split())
        bigBook = combineFreq(wordList, bigBook)
        # TODO Take this out(done)
        # print50(bigBook)
        # Largest Page
        tempWC = len(wordList)
        if tempWC > maximumWordCount:
            maximumWordCount = tempWC
            returnLink = url
        print("Max word:", maximumWordCount)
        print("Max word link:", returnLink)

        # suburl = url.replace(parsed.path, '')  # take out fragment
        if len(parsed.scheme) > 0:
            suburl = parsed.scheme + "://" + parsed.netloc
        else:
            suburl = parsed.netloc
        if parsed.fragment != '':
            t = url.replace("#" + parsed.fragment, '')
            uniq_url.add(t)
        else:
            uniq_url.add(url)
        # f1.write(parsed.netloc + "\n")

        print("Suburl:", suburl)
        # print(subdomain.keys(), "----------------------")
        # checks if domain is ics, then checks the suburl is not the main domain
        # netloc is the domain
        if ".ics.uci.edu" in parsed.netloc and parsed.netloc != "www.ics.uci.edu":
            if suburl not in subdomain.keys():
                subdomain[suburl] = 1
            else:
                subdomain[suburl] += 1
        for p in soup.find_all('a'):  # formatting (a means link)
            relative_url = p.get('href')
            # if parsed.netloc=="support.ics.uci.edu":
            # f1.write(relative_url)
            # check if relative url is valid then add to the set
            # if relative_url is not None and len(relative_url) > 1 and suburl in subdomain.keys():
            #     subdomain[suburl].add(urlparse(relative_url).netloc)
            # print("relative url:",relative_url)
            if relative_url not in crawled_url:
                # print("True:",relative_url)
                links.append(relative_url)
        # if suburl in subdomain.keys() and '' in subdomain[suburl]:
        #     subdomain[suburl].remove('')
        # f1.close()
    return links


def check_domain(url):
    """
    checks if domain is valid
    :param url:
    :return: yay or nay
    """
    valid_domain = ["ics.uci.edu/", "cs.uci.edu/",
                    "informatics.uci.edu/", "stat.uci.edu/"]
    # print(url.netloc)
    if len(url.netloc) <= 3:
        return False
    try:
        # test= url.netloc[5:]
        netloc = url.netloc + "/"
        if netloc.startswith("www."):
            netloc = netloc.strip("www.")
    except:
        return False

    if netloc == "wics.ics.uci.edu/" and "/events" in url.path.lower():
        return False
    if "/pdf" in url.path.lower():
        return False
    if netloc == "archive.ics.uci.edu":
        return False

    if netloc == "intranet.ics.uci.edu":
        return False

    if netloc == "hack.ics.uci.edu" and "gallery" in url.path:
        return False

    if netloc == "grape.ics.uci.edu":
        return False

    if netloc == "today.uci.edu/" and "/department/information_computer_sciences" in url.path:
        return True
    for i in valid_domain:
        if i in netloc:
            return True


def is_valid(url):
    try:
        parsed = urlparse(url)
        if not check_domain(parsed):
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
