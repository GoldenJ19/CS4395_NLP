"""

Names: Justin Hardy, Benji Frenkel
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""

import requests
from bs4 import BeautifulSoup
import re as regex
import os
import pickle

# Define global variables
root_url = "https://upswingpoker.com/when-to-c-bet-everything/"
output_folder = "output"
output_file_name = "linktext"


def scrape_text(url):
    """
    Scrapes text from a given url

    :param url: URL to scrape text
    :return: Raw text from URL
    """
    # Specify header
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    # Make request & build soup
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # paragraphs
    text = ""
    for p in soup.select('p'):
        text += " " + p.get_text()

    # header 1s
    for h in soup.select('h1'):
        text += " " + h.get_text()

    # header 2s
    for h in soup.select('h2'):
        text += " " + h.get_text()

    # header 3s
    for h in soup.select('h3'):
        text += " " + h.get_text()

    return text


def validate_link(link, strings):
    """
    Checks if a given link doesn't contain the blacklisted words given.

    :param link: Link to validate
    :param strings: Strings to check for; the blacklist
    :return: Boolean True/False if it doesn't contain strings given
    """
    for s in strings:
        if link.__contains__(s):
            return False
    return True


def get_relevant_urls(url):
    """
    Returns 15 relevant URLS found on the given page.

    :param url: URL to grab relevant URLs from
    :return: List of 15 relevant URLs found on the page
    """
    # Specify header
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    # Make request
    page = requests.get(url, headers=headers)
    print(page)

    # Make soup
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract main wrapper
    results = soup.findAll('div', {'fl-module fl-module-fl-post-content fl-node-60e731bdb223c'})

    # Get links
    links = []
    # Adjust this regex value (particularly the 8 values) if using a different URL
    pattern = regex.compile(".*" + root_url[(root_url.index("/")+2):(root_url[8:].index("/")+8)] + "/.+")
    filter_out = ["shop", "f-a-q", "contact-us", "about-us", "blog", "category", "author",
                  "terms-and-conditions", "privacy-policy", "sitemap"]  # adjust this filter for other examples
    for post in results:
        # Filter for links
        for link in post.findAllNext('a'):
            # Break if we've surpassed 15 entries
            if len(links) == 15:
                break

            # Convert link to string format
            link_str = str(link.get('href'))

            # Add links that are related to the site, but stay on topic
            if pattern.match(link_str) and validate_link(link_str, filter_out) and not link_str == root_url:
                links.insert(len(links), link.get('href'))
                # DEBUG: Print links we inserted
                # print(link.get('href'))

    return links


def main():
    """
    Scrapes the website defined by program globals for relevant links, and scrapes those relevant links for text
    to be used for NLP in the accompanying program for this assignment.

    :return: exit code (0 = success, 1 = error)
    """
    # Get global
    global root_url

    scrape_text(root_url)

    # Get relevant URLS
    print("Scraping root URL (" + root_url + ") for relevant URL links...")
    relevant_urls = get_relevant_urls(root_url)
    print("Finished scraping root URL.")

    print("Links:", relevant_urls, "\n")

    # Get text from relevant url pages, store into list
    print("Scraping relevant URLs...")
    relevant_texts = []
    for r_url in relevant_urls:
        # Scrape individual URL
        text = scrape_text(r_url)
        relevant_texts.insert(len(relevant_texts), text)
    print("Finished scraping relevant URLS.")

    # Pickle each text to a file.
    global output_folder, output_file_name
    for i in range(len(relevant_texts)):
        # Pickle text
        pickle.dump(relevant_texts[i], open(os.path.join(output_folder, output_file_name + str((i+1)) + ".p"), "wb"))

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
