This scans links to cornell. edu and writes a openai chatgpt blurb about each

#to install the requirements
pip install -r requirements.txt

# Api key

the script is using `openai.api_key = os.getenv("OPENAI_API_KEY")`
so you need to set that in your environment variables.

# to run the script

python sift.py input.rtf |tee output.md

# no warranty express or implied, nor even where LICENSE file specifies otherwise, nuh-uh, 
# there is still no contract here 