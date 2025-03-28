from tkinter import *	# Import tkinter library
from playback_control import *
from backend_token_generation import refresh_access_token, refresh_token
from PIL import Image, ImageTk
from requests import get
from io import BytesIO

# define application attributes
root_width = 300
root_height = 400
main_win_color = '#040424' # dark black blue

root = Tk()
root.geometry(f'{root_width}x{root_height}')
root.resizable(width = False, height = False)

token = refresh_access_token(refresh_token)

def pause_play():
	state = pause_play_music(token)
	if state:
		pause_play_button.config(text = "Pause")
	else:
		pause_play_button.config(text = "Play")

def next_track():
	next_music(token)
	photo = load_image()
	image_label.config(image = photo)
	

def prev_track():
	prev_music(token)
	photo = load_image()
	image_label.config(image = photo)

def get_current_data():
	data = get_playback_state(token)
	return data

frame = Frame(root, width = root_width, height = root_height, bg = main_win_color)
frame.pack_propagate(False)
frame.pack()
data = get_current_data()
playback_state = data['is_playing']
if playback_state:
	pause_play_button = Button(frame, text = "Pause", command = pause_play)
else:
	pause_play_button = Button(frame, text = "Play", command = pause_play)

def load_image():
	data = get_current_data()
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


pause_play_button.pack()
next_button = Button(frame, text = "Next", command = next_track)
next_button.pack(side = "right")
prev_button = Button(frame, text = "Previous", command = prev_track)
prev_button.pack(side = "left")
photo = load_image()
image_label = Label(frame, image = photo)
image_label.pack(side = 'bottom')
root.mainloop()