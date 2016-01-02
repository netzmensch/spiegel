# Spiegel
A simple tool, which downloads a youtube video and uploads it to your own channel.

## Requirements
Python 3

## Installation

### Credentials
Register your Youtube application under https://console.developers.google.com/ and create an API key and OAuth keys.
Also, in the creation page for the OAuth keys you need to authorize the redirect url
"https://developers.google.com/oauthplayground" for your project (the last form field).

Next, go to https://developers.google.com/oauthplayground/ and click on the settings button in the upper right. Check on
"Use your own OAuth credentials" and fill the form fields with your OAuthcredentials. After that, click on "close" and
choose "YouTube Data API v3" and then "https://www.googleapis.com/auth/youtube.upload" in the menu on the left side of
the page (Step 1). Submit the data with the button "Authorize APIs". When step 2 opens, click on 
"Exchange authorization code for tokens" and copy the "Refresh Token". This token is long living.

### Configuration
Open the file "config.py" and set your API token, OAuth credentials and the refresh token. 

### Setup
`pip install -r requirements.txt`

## Run
`spiegel.py https://www.youtube.com/watch?v=[VIDEO_HASH]`