# strings/utils.py
import hashlib
from collections import Counter
import re

WORD_RE = re.compile(r"\S+")

def sha256_of(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def compute_properties(s: str) -> dict:
    if not isinstance(s, str):
        raise TypeError("value must be a string")
    length = len(s)
    lower = s.lower()
    is_palindrome = lower == lower[::-1]
    unique_characters = len(set(s))
    word_count = len(WORD_RE.findall(s))
    sha = sha256_of(s)
    character_frequency_map = dict(Counter(s))
    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha,
        "character_frequency_map": character_frequency_map
    }

# Simple natural-language parser for the required examples
def parse_nl_query(q: str) -> dict:
    if not isinstance(q, str) or not q.strip():
        raise ValueError("empty query")
    q = q.lower().strip()
    filters = {}

    # Palindrome
    if 'palind' in q:  # catches palindrome, palindromic
        filters['is_palindrome'] = True

    # single word / one word
    if 'single word' in q or 'single-word' in q or 'one word' in q:
        filters['word_count'] = 1

    # strings longer than N characters
    m = re.search(r'longer than (\d+)', q)
    if m:
        # example "longer than 10 characters" interpret as min_length = 11
        n = int(m.group(1))
        filters['min_length'] = n + 1

    # strings longer than N (without explicit 'characters')
    m = re.search(r'longer than (\d+)\b', q)
    if m:
        n = int(m.group(1))
        filters.setdefault('min_length', n + 1)

    # contain / containing letter X
    m = re.search(r'containing the letter (\w)', q)
    if m:
        filters['contains_character'] = m.group(1)
    m = re.search(r'contain the letter (\w)', q)
    if m:
        filters['contains_character'] = m.group(1)
    m = re.search(r'containing (\w)', q)
    if m and 'letter' in q:
        filters['contains_character'] = m.group(1)

    # heuristic: 'first vowel' -> 'a'
    if 'first vowel' in q:
        filters.setdefault('contains_character', 'a')

    if not filters:
        raise ValueError("Unable to parse natural language query")

    return filters
