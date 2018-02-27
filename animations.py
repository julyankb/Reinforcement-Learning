import time
from tkinter import *
import random
#import locale
#locale.setlocale(locale.LC_NUMERIC, 'C')

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
#with open('action_list.txt', 'r') as infile:
#	for line in infile:
#		actions = [int(a) for a in line.rstrip().split(' ')]
#		#actions = [int(a) for a in line.split(' ') if a.isnumeric() or a == '-1']
#		action_lists.append(actions)


boxsize=100

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


def animate(action_lists, envt='blocking_maze'):
	tk = Tk()
	d = boxsize
	canvas = Canvas(tk, width=9*boxsize, height=6*boxsize)
	canvas.config(bg='black')
	tk.title(envt)
	canvas.pack()


	lc = 'white'
	for i in range(6):
		canvas.create_line(0*d,i*d,9*d,i*d, fill=lc)

	for i in range(9):
		canvas.create_line(i*d,0*d,i*d,6*d, fill=lc)

	if envt == 'blocking_maze':
		wall = canvas.create_rectangle(0, 3*boxsize, 8*boxsize, 4*boxsize, fill='blue')
	elif envt == 'shortcut_maze':
		wall = canvas.create_rectangle(1*boxsize, 3*boxsize, 9*boxsize, 4*boxsize, fill='blue')
		
	start = canvas.create_rectangle(3*boxsize, 5*boxsize, 4*boxsize, 6*boxsize, fill='grey')
	S = canvas.create_text(3.5*boxsize, 5.5*boxsize, text="S", fill='white', font=('Courier',20))

	terminal = canvas.create_rectangle(8*boxsize, 0*boxsize, 9*boxsize, 1*boxsize, fill='green')
	G = canvas.create_text(8.5*boxsize, 0.5*boxsize, text="G", fill='white', font=('Courier',20))

	player = canvas.create_oval(6,6,36,36, fill="orange")
	for i in range(1*boxsize):
		canvas.move(player, 0, 5)
		tk.update()
	for i in range(1*boxsize):
		canvas.move(player, 3, 0)


	text = canvas.create_text(3.5*boxsize, 3.5*boxsize, text="Steps = 0", fill='white', font=('Courier',50))
	canvas.move(player, 0.5*boxsize, 0.5*boxsize)
	counter = 0
	for a_l in action_lists:
		for a in a_l:
			counter +=1	
			canvas.delete(text)
			text = canvas.create_text(3.5*boxsize, 3.5*boxsize, text="Steps = %s"%counter, fill='white', font=('Courier',50))
			mov = action_to_movement(a)
		
			if mov == 'Change envt':
				if envt == 'blocking_maze':
					canvas.delete(wall)
					wall = canvas.create_rectangle(boxsize, 3*boxsize, 9*boxsize, 4*boxsize, fill='blue')
					text = canvas.create_text(3.5*boxsize, 3.5*boxsize, text="Steps = %s"%counter, fill='white', font=('Courier',50))
					canvas.delete(player)
					player = canvas.create_oval(6,6,36,36, fill="orange")
					canvas.move(player, 0.5*boxsize, 0.5*boxsize)
					#for i in range(5*boxsize):
					#	canvas.move(player, 0, 1)
					#	tk.update()
					#for i in range(3*boxsize):
					#	canvas.move(player, 1, 0)
					#	tk.update()

					canvas.move(player, 0, 500)
					canvas.move(player, 300, 0)
					tk.update()

				elif envt == 'shortcut_maze':
					canvas.delete(wall)
					wall = canvas.create_rectangle(boxsize, 3*boxsize, 8*boxsize, 4*boxsize, fill='blue')
					text = canvas.create_text(3.5*boxsize, 3.5*boxsize, text="Steps = %s"%counter, fill='white', font=('Courier',50))
					canvas.delete(player)
					player = canvas.create_oval(6,6,36,36, fill="orange")
					canvas.move(player, 0.5*boxsize, 0.5*boxsize)
					#for i in range(5*boxsize):
					#	canvas.move(player, 0, 1)
					#	tk.update()
					#for i in range(3*boxsize):
					#	canvas.move(player, 1, 0)
					#	tk.update()

					canvas.move(player, 0, 500)
					canvas.move(player, 300, 0)
					tk.update()

			elif mov == 'End of episode':
				canvas.delete(player)
				player = canvas.create_oval(6,6,36,36, fill="orange")
				canvas.move(player, 0.5*boxsize, 0.5*boxsize)
				#for i in range(1*boxsize):
				canvas.move(player, 0, 500)
				canvas.move(player, 300, 0)
				tk.update()
			else:
				canvas.move(player, mov[0], mov[1])
				tk.update()
			
			time.sleep(0.01)
			
	tk.mainloop()
