#!/bin/bash
# Build the Hangman game into a standalone executable.
# This script should be run on the operating system for which you want the executable.
pyinstaller --clean --onefile --add-data "gamedata:gamedata" script/NLP-Hangman-Game.py -n hangman-game
