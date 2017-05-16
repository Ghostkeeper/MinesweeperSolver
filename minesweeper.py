#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This little script plays the game of Minesweeper for you.

It only works on a very particular version of Minesweeper called Mines.exe on
Windows.
"""

import pyautogui
import pyscreenshot

#Data about this Minesweeper game.
number_of_mines = 35 #Total number of mines in the game.
square_size = 20 #Size of one cell of the game, in pixels.
window_recognise_kernel = [ #A number of pixel colours that are hopefully unique to the Minesweeper game window by which to locate the window. Must be rectangular.
	[ #First row of pixels.
		[233, 219, 216], #R, G, B.
		[243, 152, 150],
		[221, 203, 200],
		[184, 187, 183],
		[152, 183, 146]
	],
	[ #Second row of pixels.
		[236, 209, 206],
		[224, 81, 79],
		[198, 176, 171],
		[193, 192, 192],
		[131, 179, 126]
	]
]
window_recognise_offset = [27, 73] #The offset of the upper-left corner of the game board relative to the window_recognise_kernel, in pixels.
width_recognise_kernel = [ #Horizontal kernel to find the width of the board. This is searched for halfway through the height of the first cell.
	[255, 255, 255],
	[255, 255, 255],
	[255, 255, 255]
]
height_recognise_kernel = [ #Vertical kernel to find the height of the board. This is searched for halfway through the width of the first cell.
	[255, 255, 255],
	[255, 255, 255],
	[255, 255, 255]
]
sample_coordinates = { #For each number, where to sample relative to the cell's top-left corner.
	-1: [10, 10],
	0:  [11, 10],
	1:  [11, 10],
	2:  [10, 11],
	3:  [10, 9],
	4:  [12, 10],
	5:  [10, 9],
	6:  [10, 9],
	7:  [10, 10],
	8:  [10, 10]
}
sample_colours = { #For each number, the expected colour to find in the sample coordinates.
	-1: [240, 240, 240],
	0:  [228, 228, 228],
	1:  [0, 0, 255],
	2:  [0, 127, 0],
	3:  [251, 0, 0],
	4:  [0, 0, 127],
	5:  [127, 0, 0],
	6:  [0, 127, 127],
	7:  [0, 0, 0],
	8:  [127, 127, 127]
}

def play():
	"""
	Performs one loop of the game, one move.
	:return: ``True`` if a move was made, or ``False`` if no move was possible.
	"""
	board, corner_coordinates = look()
	move = think(board)
	if move[0] < 0 or move[1] < 0: #No move found.
		return False
	click(move, corner_coordinates)
	return True

def look():
	"""
	Takes a screenshot and converts that into an easy representation of the
	current state of the board.
	:return: A 2D grid indicating the number of mines around each tile. The
	number -1 indicates that the number is unknown.
	"""
	screenshot = pyscreenshot.grab()
	board_screenshot, corner_coordinates = crop(screenshot)
	result = []
	for x in range(0, int(board_screenshot.width / square_size)):
		result.append([])
		for y in range(0, int(board_screenshot.height / square_size)):
			result[x].append(recognise(board_screenshot, x, y))
	return result, corner_coordinates

def crop(screenshot):
	"""
	Crops a full-screen screenshot to just the part that has the game board on
	it.
	:param screenshot: A full-screen screenshot with the Minesweeper board
	somewhere on it.
	:return: A cropped screenshot that just has the Minesweeper board.
	"""
	kernel_height = len(window_recognise_kernel)
	if kernel_height <= 0:
		raise Exception("Kernel to recognise window is not filled.")
	kernel_width = len(window_recognise_kernel[0])

	#Search for the kernel on the screenshot.
	for x in range(0, screenshot.width - kernel_width): #Kernel position.
		for y in range(0, screenshot.height - kernel_height):
			for sample_x in range(0, kernel_width): #Sample in kernel window.
				for sample_y in range(0, kernel_height):
					kernel_pixel = window_recognise_kernel[sample_y][sample_x]
					r, g, b = screenshot.getpixel((x + sample_x, y + sample_y))
					if r != kernel_pixel[0] or g != kernel_pixel[1] or b != kernel_pixel[2]:
						break #Continue with the next kernel position.
				else:
					continue
				break
			else: #No breaking out because of wrong pixels after whole kernel. We found our match!
				x += window_recognise_offset[0]
				y += window_recognise_offset[1]
				print("Found board at position (" + str(x) + "," + str(y) + ")!")
				#Find the width.
				for x2 in range(x, screenshot.width - len(width_recognise_kernel)):
					for sample_x in range(0, len(width_recognise_kernel)):
						kernel_pixel = width_recognise_kernel[sample_x]
						r, g, b = screenshot.getpixel((x2 + sample_x, y + square_size / 2))
						if r != kernel_pixel[0] or g != kernel_pixel[1] or b != kernel_pixel[2]:
							break #Continue with the next kernel position.
					else: #Didn't break, so we have our match.
						board_right = x2
						break
				else:
					raise Exception("Couldn't find the width of the board.")
				for y2 in range(y, screenshot.height - len(height_recognise_kernel)):
					for sample_y in range(0, len(height_recognise_kernel)):
						kernel_pixel = height_recognise_kernel[sample_y]
						r, g, b = screenshot.getpixel((x + square_size / 2, y2 + sample_y))
						if r != kernel_pixel[0] or g != kernel_pixel[1] or b != kernel_pixel[2]:
							break #Continue with the next kernel position.
					else: #Didn't break, so we have our match.
						board_bottom = y2
						break
				else:
					raise Exception("Couldn't find the height of the board.")
				cropped = screenshot.crop((x, y, board_right, board_bottom))
				return cropped, [x, y]
	raise Exception("Couldn't find the game window.")

def recognise(screenshot, x, y):
	"""
	Recognises the current state of a cell in Minesweeper and returns that state
	as a number.

	The number indicates the number of mines around the cell. A number of -1
	indicates that it's unknown.
	:param screenshot: A screenshot of the board.
	:param x: The x-coordinate of the cell to recognise.
	:param y: The y-coordinate of the cell to recognise.
	:return: The number of mines around the cell, or -1 if it's unknown.
	"""
	for number, coordinates in sample_coordinates.items():
		r, g, b = screenshot.getpixel((x * square_size + coordinates[0], y * square_size + coordinates[1]))
		colour = sample_colours[number]
		if r == colour[0] and g == colour[1] and b == colour[2]:
			return number
	raise Exception("Didn't recognise the colour at position (" + str(x) + "," + str(y) + ").")

def think(board):
	"""
	Decides on a move that would be the safest bet based on some state of the
	board.
	:param board: The current board state.
	:return: The coordinates of the move to make.
	"""
	best_chance = 1
	best_x = -1
	best_y = -1
	for x in range(len(board)):
		for y in range(len(board)):
			if board[x][y] != -1: #Known cell.
				continue
			this_chance = chance(x, y, board)
			if this_chance < best_chance:
				best_x = x
				best_y = y
				best_chance = this_chance
	return [best_x, best_y]

def chance(x, y, board):
	"""
	Determine the chance of a cell on the board having a mine.
	:param x: The X-coordinate of the cell to determine the chance for.
	:param y: The Y-coordinate of the cell to determine the chance for.
	:param board: The current state of the board, as far as is known.
	:return: A number between 0 and 1 that indicates the chance of this cell
	having a mine.
	"""
	if board[x][y] != -1: #Known cell.
		return 0
	print("chance() is not yet implemented.")

def click(move, corner_coordinates):
	"""
	Clicks on a square in the game, communicating the actual move to the game.
	:param move: The cell (in game cells from the top-left) to click on.
	:param corner_coordinates: The pixel coordinate of the top-left corner of
	the board on the screen.
	"""
	x = corner_coordinates[0] + move[0] * square_size + square_size / 2 #Click the middle of the button.
	y = corner_coordinates[1] + move[1] * square_size + square_size / 2
	pyautogui.moveTo(x, y)
	pyautogui.click()

if __name__ == "__main__":
	while play():
		pass