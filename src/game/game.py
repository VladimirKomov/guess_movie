from src.database.database_connection import DatabaseConnection
from src.database.database_manager import GetData

import tkinter as tk
from tkinter import messagebox

class Game:
    # creating a game
    def __init__(self, user, points):
        self.user = user
        self.points = points
        # getting a random movie for the game
        self.film = GetData.get_random_movie() 


