import importlib.util
import os

# Load the module containing vowel_counter
module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'script', 'NLP-Hangman-Game.py')
spec = importlib.util.spec_from_file_location("hangman", module_path)
hangman = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hangman)

vowel_counter = hangman.vowel_counter


def test_vowel_counter_simple():
    assert vowel_counter('hangman') == 2


def test_vowel_counter_uppercase():
    assert vowel_counter('EDUCATION') == 5


def test_vowel_counter_no_vowels():
    assert vowel_counter('rhythms') == 0
