# Linguistic Sentence Guessing Hangman Game and Data Exploration

This repository contains my final project for the "Basic Programming" course as part of my Master's in Linguistics. The project is divided into two parts:

# Part 1: Data Exploration

In the first part of the project, I conducted an analysis of the GUM corpus, accessible at https://github.com/amir-zeldes/gum/tree/master . The GUM corpus is a collection of various texts organized into separate genres. My focus was on the comparison between the fiction and news genres. I analyzed the corpus using various natural language processing techniques.
My tasks included:

    Frequency Analysis: Identifying and plottingthe 100 most frequent words in each genre.
    Rare Words Visualization: Creating word clouds for words that appeared less than 10 times.
    POS Tag Distribution: Analyzing and visualizing the distribution of Part-of-Speech (POS) tags.
    Sentence Length Distribution: Comparing the sentence length distribution across genres.
    Pronouns vs. Noun Phrases: Analyzing the distribution of pronouns compared to other noun phrases.
    Descriptive Statistics: Generating basic descriptive statistics for each genre.

The findings from this exploration and the code used for the analysis can be found in the "Data Exploration" file. This analysis provides an interesting view of how different genres of text can exhibit unique language patterns.

# Part 2: Sentence Guessing Game

In the second part, I implemented a text-based game inspired by the Hangman game, with a linguistic twist. Instead of guessing individual letters, players must guess words to complete a sentence. The game uses the fiction sub-corpus from the GUM dataset to generate sentences and provide hints.
Game Features:

    Random Sentence Selection: A sentence is randomly selected from a preprocessed subset of the corpus, ensuring appropriate sentence length and word frequency.
    Hints System: Players can ask for up to three hints per word:
        First hint: Provides the Part-of-Speech (POS) tag and the number of letters.
        Second hint: Reveals the first and last character of the word.
        Third hint: Reveals the number of vowels in the word.
    Scoring System: Players earn or lose points based on their performance, with different scores assigned for correct guesses with or without hints.
    Robust Input Handling: The game handles various edge cases, such as invalid inputs, repeated guesses, and unexpected user behavior.

How to Run:

To play the game, clone the repository to your local machine, locate the script folder using the cd command on your terminal and run the script. No additional python libraries are required.
Type ? to receive a hint. You can receive up to 3 hints per word.
You have 4 attempts to guess each word correctly.
Your score is based on correct guesses with penalties for wrong guesses and using hints.
