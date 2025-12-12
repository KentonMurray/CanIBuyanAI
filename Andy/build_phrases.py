#gets ngrams from google
#works but phrases are not usable for wheel of fortune

import os
import re
from google_ngram_downloader import readline_google_store
from itertools import islice

OUTPUT_FILE = "data/phrases.txt"
MIN_WORDS = 2
MAX_WORDS = 5
MAX_PHRASES = 20000  # limit how many phrases you extract (adjust as needed)

def clean_phrase(p: str) -> str:
    p = p.upper()
    p = re.sub(r"[^A-Z' ]+", " ", p)
    p = re.sub(r"\s+", " ", p).strip()
    if 3 <= len(p) <= 40:
        return p
    return None

def extract_phrases(ngram_len: int, limit: int):
    extracted = set()
    for filename, url, records in readline_google_store(ngram_len=ngram_len, lang='eng'):
        print(f"Processing {filename}")
        for rec in islice(records, limit):
            if rec.volume_count > 1000:
                print(rec.ngram, rec.volume_count)
                phrase = rec.ngram
                words = phrase.split()
                if MIN_WORDS <= len(words) <= MAX_WORDS:
                    cleaned = clean_phrase(phrase)
                    if cleaned:
                        extracted.add(cleaned)
                if len(extracted) >= MAX_PHRASES:
                    return extracted
    return extracted

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    phrases = set()
    for n in range(MIN_WORDS, MAX_WORDS + 1):
        print(f"Extracting {n}-grams …")
        ph = extract_phrases(ngram_len=n, limit=100000)
        phrases.update(ph)
        if len(phrases) >= MAX_PHRASES:
            break

    print(f"Total phrases collected: {len(phrases)}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for p in sorted(phrases):
            f.write(p + "\n")
    print(f"Wrote phrases to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()