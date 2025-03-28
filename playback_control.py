from requests import post, get, put
from dotenv import load_dotenv
from backend_token_generation import refresh_access_token, get_token
import base64
import json
import os
# import the libraries

load_dotenv()	# load the environment variables

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URL")
auth_code = os.getenv("AUTH_CODE")
refresh_token = os.getenv("REFRESH_TOKEN")
# fetch the environment variables

# Returns the authorization headers
def get_auth_header(token):
	return {"Authorization": "Bearer " + token}

# Play Music
def play_music(token):
	url = "https://api.spotify.com/v1/me/player/play"	# base url
	headers = get_auth_header(token)	# fetch the headers

	result = put(url, headers = headers)	# send the request
	print(result, "Playing Music")	# print the result of the request


def pause_music(token):
	url = "https://api.spotify.com/v1/me/player/pause"	# base url
	headers = get_auth_header(token)	# fetch the headers

	result = put(url, headers = headers)	# send the request
	print(result, "Pausing Music")	# print the result of the request


def next_music(token):
	url = "https://api.spotify.com/v1/me/player/next"	# base url
	headers = get_auth_header(token)	# fetch the headers

	result = post(url, headers = headers)	# send the request
	print(result, "Next Music")	# print the result of the request

def prev_music(token):
	url = "https://api.spotify.com/v1/me/player/previous"
	headers = get_auth_header(token)

	result = post(url, headers = headers)
	print(result, "Previous Music")

def set_music_volume(token):
	url = "https://api.spotify.com/v1/me/player/volume"
	volume = int(input("ENter the volume: "))
	if 0 <= volume <= 100:
		volume_query = f"?volume_percent={volume}"
	else:
		print("Invalid Volume Option")
		return None
	query_url = url + volume_query
	headers = get_auth_header(token)
	result = put(query_url, headers = headers)
	print(result, f"Volume set to {volume}")


def enable_disable_repeat(token, state_type):
	state = ['off', 'track']
	state_type = int(input("Enter the state(1/0): "))
	if state == 0 or state == 1:
		url = f"https://api.spotify.com/v1/me/player/repeat?state={state[state_type]}"
	else:
		print("Invalid state option!")
		return None
	headers = get_auth_header(token)
	result = put(url, headers = headers)
	print(result, f"Repeat state set to: {state[state_type]}")

def get_playback_state(token):
	url = "https://api.spotify.com/v1/me/player"
	headers = get_auth_header(token)
	result = get(url, headers = headers)
	json_result = result.json()
	# return [json_result['device']['id'], json_result['device']['name'], json_result['item']['name']]
	return json_result

def pause_play_music(token):
	playback_state = get_playback_state(token)
	play_state = playback_state['is_playing']
	if play_state == False:
		play_music(token)
		return True
	elif play_state == True:
		pause_music(token)
		return False


def start():
	n = 1

	access_token = refresh_access_token(refresh_token)
	print(access_token)

	print(get_playback_state(access_token))

	while(n != 0):
		try:
			n = int(input("Enter your option: "))
		except ValueError:
			print("Invalid Option!")
			continue

		if n == 0:
			pass
		elif n == 1:
			play_music(access_token)
		elif n == 2:
			pause_music(access_token)
		elif n == 3:
			next_music(access_token)
		elif n == 4:
			prev_music(access_token)
		elif n == 5:
			set_music_volume(access_token)
		elif n == 6:
			enable_disable_repeat(access_token)
		else:
			print("Invalid option!")