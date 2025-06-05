
@echo off

rem Build the Hangman game into a standalone Windows executable.

pyinstaller --clean --onefile --add-data "gamedata;gamedata" script/NLP-Hangman-Game.py -n hangman-game

