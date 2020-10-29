import re
from PartA import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
crawled_url = list()

#test for eric

returnLink = ""

maximumWordCount = 0

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    global returnLink
    global maximumWordCount
    # Implementation required.
    parsed = urlparse(url)
    links = list()
    print("extract links")
    print(url)
    print(is_valid(url),resp.status,url not in crawled_url)
    # 200 OK,201 Creat,202 Accepted
    if is_valid(url) and 200 <= resp.status <= 202 and url not in crawled_url:
        print("isvalid")
        crawled_url.append(url)
        # read the page and save all urls that haven't been crawled.
        html_doc = resp.raw_response.content
        # put the html_doc variable contents into a file along with parsed
        f = open("storeDocument.txt", "a")  # argument a is for "append", change to "w" if you want to write over file
        # write the url followed by the contents of the page
        f.write(parsed.geturl())
        #f.write(html_doc)
        #f.close()

        soup = BeautifulSoup(html_doc, 'html.parser')
        #this loop gets the maximum word count from all the url
        s = soup.get_text()
        f.write(s)
        f.close()

        tempWC = len(s)
        if tempWC > maximumWordCount:
            maximumWordCount = tempWC
            returnLink = url
        print("Max word:", maximumWordCount)
        print("Max word link:",returnLink)
        for p in soup.find_all('a'):
            relative_url = p.get('href')
            if relative_url not in crawled_url:
                links.append(relative_url)
    return links



def check_domain(url):
    valid_domain = ["ics.uci.edu/", "cs.uci.edu/",
                    "informatics.uci.edu/", "stat.uci.edu/"]
    print(url.netloc)
    try:
        netloc = url.netloc[5:] + "/"
    except:
        return False
    for i in valid_domain:
        if netloc in i:
            return True
    if netloc == "today.uci.edu/" and "/department/information_computer_sciences" in url.path:
        return True
    return False



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