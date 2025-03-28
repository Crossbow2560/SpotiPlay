from tkinter import *
from playback_control import *
from backend_token_generation import refresh_access_token, refresh_token
from PIL import Image, ImageTk
from requests import get
from io import BytesIO
import time

window_width = 300
window_height = 400
window_color = '#040424'

root = Tk()
root.geometry(f"{window_width}x{window_height}")
root.resizable(width = 0, height = 0)

token = refresh_access_token(refresh_token)

def load_image(data):
	image_data = data['item']['album']['images']
	image_url = image_data[0]['url']
	image_width = image_data[0]['width']
	image_height = image_data[0]['height']
	
	image_response = get(image_url)
	image_bytes = BytesIO(image_response.content)
	image = Image.open(image_bytes)
	final_image = image.resize((int(image_width/2.5), int(image_height/2.5)))
	photo = ImageTk.PhotoImage(final_image)
	return photo

def next_track():
	global track_name_label, image_label, data
	next_music(token)
	time.sleep(1)
	data = get_playback_state(token)
	name = data['item']['name']
	track_name_label.config(text = name)

def prev_track():
	global track_name_label, image_label, data
	prev_music(token)
	time.sleep(1)
	data = get_playback_state(token)
	name = data['item']['name']
	track_name_label.config(text = name)


# Start Creating the UI

# Retrieve the assets
def getImages():
	global play_image, pause_image, next_image, prev_image
	image = Image.open("./assets/play.png")
	resized_image = image.resize((50, 50))
	play_image = ImageTk.PhotoImage(resized_image)
	image = Image.open("./assets/pause.png")
	resized_image = image.resize((50, 50))
	pause_image = ImageTk.PhotoImage(resized_image)
	image = Image.open("./assets/next.png")
	resized_image = image.resize((50, 50))
	next_image = ImageTk.PhotoImage(resized_image)
	image = Image.open("./assets/prev.png")
	resized_image = image.resize((50, 50))
	prev_image = ImageTk.PhotoImage(resized_image)

getImages()

def pause_play():
	state = pause_play_music(token)
	if state:
		pauseplay_button.config(image = pause_image)
	else:
		pauseplay_button.config(image = play_image)

def startApplication():
	global root, main_win_frame, pauseplay_button, next_button, prev_button, track_name_label
	main_win_frame = Frame(root, width = window_width, height = window_height, bg = window_color)
	main_win_frame.pack_propagate(False)
	data = get_playback_state(token)
	playback_state = data['is_playing']
	track_name = data['item']['name']
	if playback_state:
		pauseplay_button = Button(main_win_frame, image = pause_image, relief = 'flat', bg = window_color, activebackground = window_color, highlightthickness = 0, borderwidth = 0, command = pause_play)
	else:
		pauseplay_button = Button(main_win_frame, image = play_image, relief = 'flat', bg = window_color, activebackground = window_color,  highlightthickness = 0, borderwidth = 0, command = pause_play)

	next_button = Button(main_win_frame, image = next_image, relief = 'flat', bg = window_color, activebackground = window_color, highlightthickness = 0, borderwidth = 0, command = next_track)
	prev_button = Button(main_win_frame, image = prev_image, relief = 'flat', bg = window_color, activebackground = window_color, highlightthickness = 0, borderwidth = 0, command = prev_track)
	track_name_label = Label(main_win_frame, text = track_name, bg = window_color, fg = 'white', font = 'Roboto 12 bold')
	photo = load_image(data)
	image_label = Label(main_win_frame, image = photo)
	main_win_frame.place(x = 0, y = 0)
	pauseplay_button.place(x = 125, y = 325)
	next_button.place(x = 200, y = 325)
	prev_button.place(x = 50, y = 325)
	image_label.place(x = 20, y = 30)
	track_name_label.place(x = 15, y = 290)

startApplication()
root.mainloop()