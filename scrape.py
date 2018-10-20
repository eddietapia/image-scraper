# Import the necessary packages
from requests import exceptions
import argparse
import requests
import cv2
import os
 
# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())


# Set your Microsoft Cognitive Services API key along with (1) the
# maximum number of results for a given search and (2) the group size
# for results (maximum of 50 per request)
# TODO: insert your Microsoft API key here. For more info, go to the tutorial link at the top of this README
API_KEY = "YOUR_API_KEY_GOES_HERE"
MAX_RESULTS = 1000
GROUP_SIZE = 50
 
# Set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# When attempting to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = set([IOError, FileNotFoundError,exceptions.RequestException, exceptions.HTTPError,exceptions.ConnectionError, exceptions.Timeout])

# Store the search term in a convenience variable then set the headers and search parameters
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}
 
# Make the search
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()
 
# Grab the results from the search, including the total number of estimated results 
# returned by the Bing API
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults,
	term))
 
# Initialize the total number of images downloaded thus far
total = 0

# Loop over the estimated number of results in `GROUP_SIZE` groups
for offset in range(0, estNumResults, GROUP_SIZE):
    # Update the search parameters using the current offset, then make the request to fetch the results
    print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
    
    # Loop over the results
    for v in results["value"]:
        # try to download the image
        try:
            # Make a request to download the image
            print("[INFO] fetching: {}".format(v["contentUrl"]))
            r = requests.get(v["contentUrl"], timeout=30)
 
            # Build the path to the output image
            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            p = os.path.sep.join([args["output"], "{}{}".format(str(total).zfill(8), ext)])
 
            # Write the image to disk
            f = open(p, "wb")
            f.write(r.content)
            f.close()
 
        # Catch any errors that would not unable us to download the image
        except Exception as e:
            # Check to see if our exception is in our list of exceptions to check for
            if type(e) in EXCEPTIONS:
                print("[INFO] skipping: {}".format(v["contentUrl"]))
                continue
                
        # Try to load the image from disk
        image = cv2.imread(p)
 
        # If the image is `None` then we could not properly load the image from disk (so it should be ignored)
        if image is None:
            print("[INFO] deleting: {}".format(p))
            os.remove(p)
            continue
 
        # Update the counter
        total += 1

