import time
from tkinter import *
import random

action_lists = []
'''
Must be a list of actions.
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
INACTION = -1
END OF EPISODE = -2 
CHANGE OF ENVT = -3
'''

boxsize=75
Y = 9
X = 13

def action_to_movement(action):
	stepsize = boxsize
	if action == 0:
		return (0, -stepsize)
	if action == 1:
		return (0, stepsize)
	if action == 2:
		return (-stepsize, 0)
	if action == 3:
		return (stepsize, 0)
	if action == -1:
		return (0,0)
	if action == -2:
		return 'End of episode'	
	if action == -3:
		return 'Change envt'


def animate(action_lists):
	tk = Tk()
	d = boxsize
	
	bgc = 'black'
	lc = 'white'

	canvas = Canvas(tk, width=X*boxsize, height=Y*boxsize)
	canvas.config(bg=bgc)
	#tk.title(envt)
	canvas.pack()

	border_top = canvas.create_rectangle(0,0*boxsize, X*boxsize, 1*boxsize, fill='grey')
	border_bottom = canvas.create_rectangle(0,(Y-1)*boxsize, X*boxsize, Y*boxsize, fill='grey')
	border_left = canvas.create_rectangle(0,0*boxsize, 1*boxsize, Y*boxsize, fill='grey')
	border_right = canvas.create_rectangle((X-1)*boxsize,0*boxsize, X*boxsize, Y*boxsize, fill='grey')
	
	horizontal_lines = Y - 1
	for i in range(horizontal_lines + 1):
		canvas.create_line(0*d,i*d, X*d,i*d, fill=lc)

	vertical_lines = X - 1
	for i in range(vertical_lines + 1):
		canvas.create_line(i*d, 0*d,i*d, Y*d, fill=lc)


	# x1,y1, x2,y2 (starting from top left corner)
	
	vertical_wall = canvas.create_rectangle(6*boxsize, 2*boxsize, 7*boxsize, 7*boxsize, fill='blue')
	top_horizontal_wall = canvas.create_rectangle(6*boxsize, 2*boxsize, 9*boxsize, 3*boxsize, fill='blue')
	bottom_horizontal_wall = canvas.create_rectangle(6*boxsize, 6*boxsize, 9*boxsize, 7*boxsize, fill='blue')
	
	terminal = canvas.create_rectangle(3*boxsize, 3*boxsize, 4*boxsize, 4*boxsize, fill='green')
	
	for i in range(0,X):
		for j in range(0,Y):
			T = canvas.create_text((i+0.5)*boxsize, (j+0.5)*boxsize, text="%s,%s"%(j,i), fill='white', font=('Courier',10))
			
	
	
	tk.mainloop()


if __name__ == "__main__":
	# Start position
	animate([])
