import os, sys
import openai
import time
from bs4 import BeautifulSoup
import requests

# Set the OPENAI_API_KEY environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to the RTF file
if len(sys.argv) > 1:
    rtf_file = sys.argv[1]
else:
    rtf_file = "IMF/22 USC Chapter 7 IMF subscription information.rtf"

# Regular expression to match URLs in the RTF file
url_regex = 'HYPERLINK "(http[^"]*)"'

# Array to hold the URLs
urls = []

# Read the RTF file line by line
with open(rtf_file, 'r') as file:
    for line in file:
        # If the line matches the URL regex, extract the URL and add it to the array
        if 'HYPERLINK' in line:
            url = line.split('"')[1]
            urls.append(url)

# Filter the URLs to include only the Cornell URLs
cornell_urls = [url for url in urls if 'cornell' in url]

title_permutations=["#page_title", "#page-title"]
def extract_elements(html):
    soup = BeautifulSoup(html, 'html.parser')

    # these cornell pages are not identically coded.  we want to extract the page-title and then the remainder of the parent of page-title as two distinct things.

    #bitbang the id's in title_permutations
    for title_permutation in title_permutations:
        page_title_elem = soup.select_one(title_permutation)
        if page_title_elem:
            title_id = title_permutation
            break


    page_title = page_title_elem.text

    # find the parent of the title
    page_title_parent = page_title_elem.parent

    # find the title element in the parent
    page_title_element = page_title_parent.select_one(title_id)

    #page_title_element is element /n/ of /m/ elements in page_title_parent.  we want to append  element ( (n+1)..m ) .text +\n to tab_content
    tab_content_elements = page_title_element.find_next_siblings()

    #foreach them and append to tab_content
    tab_content = ''
    for element in tab_content_elements:
        tab_content += element.text + "\n"
    return page_title, tab_content


MODEL = "gpt-3.5-turbo"
# Loop through the Cornell URLs and generate responses
for url in cornell_urls:
    # Perform the CURL request and extract the elements
    response = requests.get(url)
    output = response.text
    # page_title, tab_content = extract_elements(output)
    # rewrite with error trapping and diagnostics to figure out where our parser fails its assumptions
    try:
        page_title, tab_content = extract_elements(output)
    except Exception as e:
        print(f"Error during request: {e}", file=sys.stderr)
        print(f"URL: {url}", file=sys.stderr)
        print(f"pres enter for output dump or ctrl-c", file=sys.stderr)
        input()
        print(f"Output: {output}", file=sys.stderr)
        exit(1)

    # Print the extracted elements
    print("Page Title:", page_title)
    print("Tab Content:", tab_content)

    prompt = "\n\nTitle: " + page_title + "\nContent: " + tab_content
    prompt = prompt[:10000]
    prompt1 = prompt[:prompt.rfind(' ')]

    # Make the API call
    while True:
        try:
            api_response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "user",
                     "content": prompt1 + "\n(skeptical and mildly jaded analogies and summaries follow, with any signficant timeline events or commonly referred counterparts)"},
                ],
                temperature=0.8,
            )
            # If the request is successful, the loop will break
            break
        except Exception as e:
            # If there's an error (like a 429 Too Many Requests error), print error to stderr and wait for 5 seconds before retrying
            print(f"Error during request: {e}", file=sys.stderr)
            print("Waiting for 5 seconds before retrying...", file=sys.stderr)
            time.sleep(5)

    print(api_response.choices[0].message.content.strip())
    print("----")
