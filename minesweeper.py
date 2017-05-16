#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
	print("look() not implemented yet.")

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
	print("click() not implemented yet.")

if __name__ == "__main__":
	while play():
		pass