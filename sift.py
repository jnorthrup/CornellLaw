import os,sys
import openai
import subprocess
import time
from bs4 import BeautifulSoup
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to the RTF file
rtf_file = "22 USC Chapter 7 IMF subscription information.rtf"

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


def extract_elements(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_title = soup.select_one("#page_title").text
    tab_content = soup.select_one("#tab_default_1").text
    return page_title, tab_content


MODEL="gpt-3.5-turbo"
# Loop through the Cornell URLs and generate responses
for url in cornell_urls:
    # Perform the CURL request and extract the elements
    response = requests.get(url)
    output = response.text
    page_title, tab_content = extract_elements(output)

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
                    {"role": "user", "content": prompt1 +"\n(skeptical and mildly jaded analogies and summaries follow, with any signficant timeline events or commonly referred counterparts)"},
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
