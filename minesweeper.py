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
square_size = 20

def play():
	"""
	Performs one loop of the game, one move.
	:return: ``True`` if a move was made, or ``False`` if no move was possible.
	"""
	board, corner_coordinates = look()
	move = think(board)
	click(move, corner_coordinates)

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
	for x in range(0, board_screenshot.width / square_size):
		result.append([])
		for y in range(0, board_screenshot.height / square_size):
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
	print("crop() not implemented yet.")

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
	print("recognise() not implemented yet.")

def think(board):
	"""
	Decides on a move that would be the safest bet based on some state of the
	board.
	:param board: The current board state.
	:return: The coordinates of the move to make.
	"""
	print("think() not implemented yet.")

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