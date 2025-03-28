from requests import post, get, put
from dotenv import load_dotenv
import base64
import json
import os

load_dotenv()	# load environment variables


# get the environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URL")
auth_code = os.getenv("AUTH_CODE")
refresh_token = os.getenv("REFRESH_TOKEN")


def get_token(auth_code):
	"""Fetches the token and takes the parameter authorization codes"""
	url = "https://accounts.spotify.com/api/token"

	data = {
		"grant_type" : "authorization_code",
		"code" : auth_code,
		"redirect_uri" : redirect_url,
		"client_id" : client_id,
		"client_secret" : client_secret
	}

	result = post(url, data = data).json()
	return result

def refresh_access_token(refresh_token):
	"""Fetches the new access token and takes the parameter refresh token"""
	url = "https://accounts.spotify.com/api/token"

	data = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
		"client_id": client_id,
		"client_secret": client_secret
	}

	result = post(url, data = data).json()
	access_token = result['access_token']
	return access_token
