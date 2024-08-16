#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import random

directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gamedata')

def connlu_scanner(directory, max_length=20, rare_threshold=10):
    """
    Scans CoNLL-U files in the gamedata directory, loading sentences while applying several filters:
    sentences are limited by length, and those containing rare words are omitted.
    
    Args:
    - directory (str): The directory containing .conllu files to be processed.
    - max_length (int): Maximum allowed word count for sentences
    - rare_threshold (int): The threshold below which words are considered 'rare'.
    
    Returns:
    - list of list of tuples: A list where each element represents a sentence. Each sentence
      is itself a list of (word, POS tag) tuples, filtered according to the specified criteria.
    """
    word_counts = {}  # To hold the count of each word across all sentences.
    all_sentences = []  # Temporary storage for all sentences, prior to filtering for rare words.

    # First pass through the files: count word occurrences and collect sentences.
    for filename in os.listdir(directory):
        if filename.endswith(".conllu"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                current_sentence = []  # Holds the current sentence being read from the file.
                for line in file:
                    if line.strip() == "":  # Empty line signifies end of a sentence in CoNLL-U format.
                        # Check if the sentence's length is within the specified bounds before adding.
                        if 5 <= len(current_sentence) <= max_length:
                            all_sentences.append(current_sentence)
                            # Count occurrences of each word in the current sentence.
                            for word, _ in current_sentence:
                                word_counts[word.lower()] = word_counts.get(word.lower(), 0) + 1
                        current_sentence = []  # Reset for the next sentence.
                    elif not line.startswith('#'):  # Ignore comment lines.
                        parts = line.split('\t')  # CoNLL-U fields are separated by tabs.
                        if len(parts) > 3:
                            # Normalize word to lowercase to ensure consistent counting and add it to the current sentence.
                            token, pos_tag = parts[1].lower(), parts[3]
                            current_sentence.append((token, pos_tag))
                # After file end, check and add the last sentence if it wasn't followed by a newline.
                if 5 <= len(current_sentence) <= max_length:
                    all_sentences.append(current_sentence)
                    for word, _ in current_sentence:
                        word_counts[word.lower()] = word_counts.get(word.lower(), 0) + 1

    # Second pass: Filter out sentences containing rare words.
    filtered_sentences = [sentence for sentence in all_sentences
                          if not any(word_counts[word.lower()] < rare_threshold for word, _ in sentence)]

    return filtered_sentences


def sentence_processor(sentences, min_length=5, max_length=20, rare_threshold=10):
    """
    Process the sentences to apply several filters: convert all words to lowercase, 
    remove sentences shorter than 5 or longer than 20, and exclude sentences 
    containing rare words.

    Args:
    - sentences (list of list of str): The input list where each element is a sentence represented 
      as a list of words (tokens).
    - min_length (int): The minimum acceptable sentence length. Sentences with fewer words 
      than this will be excluded.
    - max_length (int): The maximum acceptable sentence length. Sentences with more words 
      than this will be excluded.
    - rare_threshold (int): The minimum frequency a word must have across all sentences 
      to not be considered rare. Sentences containing words that appear less frequently than 
      this threshold will be excluded.

    Returns:
    - list of list of str: A filtered list of sentences after applying all the specified criteria. 
      Each sentence is represented as a list of lowercase words (tokens).
    """
    # Convert to lowercase and filter by sentence length
    sentences = [[token.lower() for token in sentence] for sentence in sentences if min_length <= len(sentence) <= max_length]
    
    # Count word occurrences
    word_counts = {}
    for sentence in sentences:
        for token in sentence:
            word_counts[token] = word_counts.get(token, 0) + 1
    
    # Identify rare words
    rare_words = {word for word, count in word_counts.items() if count < rare_threshold}
    
    # Remove sentences containing rare words
    filtered_sentences = []
    for sentence in sentences:
        if not any(token in rare_words for token in sentence):
            filtered_sentences.append(sentence)
    
    return filtered_sentences


def vowel_counter(word):
    """
    Count the number of vowels in a word, which will be used as a hint for the user.
    """
    # Define the vowels to look for.
    vowels = 'aeiouAEIOU'
    # Count vowels, iterating through each character in the word.
    return sum(1 for char in word if char in vowels)

def hint_generator(word, pos_tag):
    """
    Generate a set of hints for a given word, leveraging its length, POS tag, and the number of vowels.
    """
    # Create a list of hints based on the word and POS tag.
    hints = [
        f"Hint 1: It's a {pos_tag.lower()} with {len(word)} letters.",
        f"Hint 2: It starts with {word[0]} and ends with {word[-1]}.",
        f"Hint 3: It has {vowel_counter(word)} vowels."  # Count the vowels in the word for hint 3.
    ]
    return hints

def play_the_game(sentences):
    """
    Initialize the game using the processed sentences.
    """
    if not sentences:
        print("No sentences available to play the game.")
        return
    
    # Randomly choose a sentence from the list of processed sentences.
    sentence_with_pos = random.choice(sentences)
    # Unzip the sentence into two lists: one for words and one for POS tags.
    sentence, pos_tags = zip(*sentence_with_pos)
    # Create a display sentence with underscores for words and keeping punctuation and numerals.
    display_sentence = ['_'*len(word) if word.isalpha() else word for word in sentence]
    
    # Introduction to the game.
    print("Welcome to the sentence guessing game! Your challenge is to guess the words and complete the sentence.")
    print("Ready to play?")
    # Display the sentence with words as underscores and other characters as is.
    print("The sentence has {} words. What's the first one?".format(len(sentence)))
    print(' '.join(display_sentence))
    
    score = 0  # Initialize the player's score.
    
    # Loop through each word in the sentence.
    for index, (word, pos_tag) in enumerate(sentence_with_pos):
        if not word.isalpha():  # If the word is not alphabetic, such as punctuation, skip it.
            display_sentence[index] = word  # Directly reveal punctuation and numerals.
            continue
        
        # Generate the hints for the word.
        hints = hint_generator(word, pos_tag)
        attempts = 4  # Set the number of attempts for guessing the word.
        used_hints = 0  # Keep track of hints used.
        
        # Word guessing loop.
        while attempts > 0:
            guess = input(f"Your guess: ").lower().strip()  # Get the user's guess.
            normalized_word = word.lower().strip()  # Normalize the word for comparison.
            
            if guess == "?":
                # Provide hints when the user asks for them.
                if used_hints < len(hints):
                    print(hints[used_hints])
                    used_hints += 1  # Increment the used hints.
                else:
                    print("No more hints available.")
                continue
            
            if guess == normalized_word:  # Check if the guess is correct.
                print("Great! What's the next word?")
                # Update the display sentence with the correctly guessed word.
                display_sentence[index] = word
                print(' '.join(display_sentence))
                # Update the score based on hints used. No hints mean a full score for the word.
                score += 30 - (used_hints * 5)
                break  # Move to the next word.
            else:
                attempts -= 1  # Decrement the number of attempts left.
                print(f"Wrong! Try another word or ask for a hint. {attempts} attempts left.")
                
        if attempts == 0:
            # Reveal the correct word if the user fails to guess it within the allowed attempts.
            print(f"The correct word was '{word}'.")
            display_sentence[index] = word  # Update the display sentence.
            print(' '.join(display_sentence))
            score -= 10  # Apply penalty to the score for failing to guess the word.

    # Conclude the game with the final score.
    print(f"Congratulations! Your final score is {score}.")

# Load the sentences from the gamedatafiles.
sentences = connlu_scanner(directory_path)
# Start the game with loaded sentences.
play_the_game(sentences)


# In[ ]:




