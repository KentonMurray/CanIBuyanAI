import random
import sys
import re


PUZZLES = [
    "GREEN TEA SMOOTHIE",
    "BREAKING THE ICE",
    "JUMPING TO CONCLUSIONS",
    "MAKING A DIFFERENCE",
    "HOLIDAY ROAD TRIP",
]

VOWELS = set("AEIOU")

USED_LINES = set()

def pat_say(text):
    text = text.strip()
    if text not in USED_LINES:
        USED_LINES.add(text)
        return text
    i = 2
    while True:
        alt = f"{text} [{i}]"
        if alt not in USED_LINES:
            USED_LINES.add(alt)
            return alt
        i += 1


# --------------------------------------------
# Helpers
# --------------------------------------------

def mask_puzzle(puzzle, guessed):
    return " ".join([c if c in guessed or c == " " else "_" for c in puzzle])

def valid_letter(x):
    return len(x) == 1 and x.isalpha()

def is_gibberish(text):
    if len(text) >= 5 and not re.search(r"[aeiouAEIOU]", text):
        return True
    if re.fullmatch(r"[a-z]{6,}", text.lower()):
        return True
    return False


# --------------------------------------------
# Opener Questions (non repeating)
# --------------------------------------------

OPENERS = [
    "If today had a soundtrack, what song would play during this moment? 🎵🤔",
    "What’s a tiny victory you had today? 🌟🙂",
    "If you could teleport anywhere right now for 15 minutes, where are you going? 🌍🌀",
    "What color matches your mood right now and why? 🎨😄",
    "What’s something random that made you smile today? 😊✨",
]

def get_opener():
    if OPENERS:
        q = random.choice(OPENERS)
        OPENERS.remove(q)
        return pat_say("Pat: " + q)
    return pat_say("Pat: Alright, random question mode unlocked. 😄🎡")


# --------------------------------------------
# NEW Conversation Engine
# --------------------------------------------

def classify_message(msg):
    msgl = msg.lower()
    return {
        "tired": any(w in msgl for w in ["tired", "sleep", "sleepy"]),
        "confused": any(w in msgl for w in ["dont know", "idk", "not sure"]),
        "short": len(msgl.split()) <= 2,
        "long": len(msgl.split()) >= 6,
        "food": any(w in msgl for w in ["food", "eat", "snack", "apple", "pizza"]),
        "music": any(w in msgl for w in ["song", "music", "rap", "rock", "hiphop", "eminem"]),
        "motivational": any(w in msgl for w in ["lose yourself", "focus", "grind", "motivate"]),
        "gibberish": is_gibberish(msgl),
    }


def conversational_pat(user_msg, name, memory):
    msg = user_msg.strip()
    memory.append(msg)
    tags = classify_message(msg)

    # ----------------------------------
    # Gibberish
    # ----------------------------------
    if tags["gibberish"]:
        return pat_say(f"Pat: '{msg}' feels like your brain hit shuffle. You good over there? 😄🌀")

    # ----------------------------------
    # Motivational song (Lose Yourself)
    # ----------------------------------
    if "lose yourself" in msg.lower() or tags["motivational"]:
        return pat_say(
            "Pat: Oh that’s a *big* energy pick. That’s ‘main character in act three’ level intensity. "
            "What part of today feels like a moment you have to lock in for? 🎤🔥"
        )

    # ----------------------------------
    # Confused replies
    # ----------------------------------
    if tags["confused"]:
        return pat_say(
            "Pat: Totally fair. Sometimes the vibe hits before the explanation does. "
            "If you had to guess, does it feel more like uncertainty or just not wanting to overthink it? 🤔✨"
        )

    # ----------------------------------
    # Very short replies (“huh”, “ok”, etc.)
    # ----------------------------------
    if tags["short"] and len(msg) <= 4:
        return pat_say(
            "Pat: That’s the universal ‘processing noise’. Love it. "
            "What part is tripping your brain up — the question or the day itself? 😆🧠"
        )

    # ----------------------------------
    # Food-related
    # ----------------------------------
    if tags["food"]:
        return pat_say(
            f"Pat: Jumping topics to food is honestly relatable. "
            f"Did something make you think of that, or did your stomach just file a request form? 🍎😄"
        )

    # ----------------------------------
    # Long thoughtful messages
    # ----------------------------------
    if tags["long"]:
        return pat_say(
            f"Pat: That actually tells me a lot about where your head’s at. "
            f"What part of that feels the most true for you right now? 😊🧠"
        )

    # ----------------------------------
    # Artistic conversational replies (default)
    # ----------------------------------

    # If we have memory, connect the dots
    if len(memory) >= 2:
        prev = memory[-2]
        return pat_say(
            f"Pat: Interesting shift from when you said '{prev}'. "
            f"What made your mind hop to '{msg}' next? 🤔🔗"
        )

    # Start-of-convo default
    return pat_say(
        f"Pat: Gotcha. That’s an interesting angle. "
        f"What’s the next thing that comes to mind when you think about that? 😄✨"
    )


# --------------------------------------------
# SIDE CHAT LOOP
# --------------------------------------------

def run_side_chat(name, guessed, puzzle_mask, winnings):
    memory = []

    print("\n============ SIDE CHAT: Pat Sajak ============\n")
    print(pat_say(f"Pat: Yo {name}! Quick breather from the wheel. You’re doing great. 🌟🎡"))
    print(get_opener())
    print()

    for i in range(5):
        user = input(f"You ({i+1}/5): ").strip()
        if user.upper() == "BYE":
            print(pat_say("Pat: Irish exit accepted. Respect. 👋😄"))
            print("\n============ END SIDE CHAT ============\n")
            return

        print(conversational_pat(user, name, memory))
        print()

    print(pat_say("Pat: Quick recap before we head back in. ⚡📝"))
    print(pat_say(f"Pat: Winnings so far: ${winnings} 💰"))
    print(pat_say(f"Pat: Letters guessed: {', '.join(sorted(guessed)) or 'None'} 🔡"))
    print(pat_say(f"Pat: Puzzle looks like: {puzzle_mask} 🧩"))
    print(pat_say("Pat: Alright superstar, back to the game. 🎉🔥"))
    print("\n============ END SIDE CHAT ============\n")


# --------------------------------------------
# MAIN GAME LOOP
# --------------------------------------------

def play_game():
    print("=== Wheel of Fortune: Conversational Pat Sajak Edition ===")
    name = input("Enter your name: ").strip() or "Player"

    print(f"\nWelcome {name}! Let’s play. Type 'BYE' anytime.\n")

    puzzle = random.choice(PUZZLES)
    guessed = set()
    winnings = 0

    while True:
        masked = mask_puzzle(puzzle, guessed)

        print("----------------------------------------")
        print("Puzzle:", masked)
        print("Winnings:", f"${winnings}")
        print("Guessed letters:", ", ".join(sorted(guessed)) or "None")
        print("----------------------------------------")

        action = input("Choose: (G)uess, (B)uy vowel, (S)olve, (P)ass, (Q)uit: ").upper().strip()

        if action in ["BYE", "Q"]:
            print("Pat: Peace out. This was fun. 👋😄")
            sys.exit(0)

        if action == "G":
            letter = input("Letter: ").upper().strip()
            if letter == "BYE":
                print("Pat: Bold exit. Respect. 👋😄")
                sys.exit(0)

            if not valid_letter(letter):
                print("Invalid.")
                continue

            if letter in guessed:
                print("Already guessed.")
                continue

            guessed.add(letter)

            if letter in puzzle:
                count = puzzle.count(letter)
                winnings += count * 100
                print(f"{count} found! +${count * 100}")
            else:
                print("No match.")

            if random.random() < 0.65:
                run_side_chat(name, guessed, mask_puzzle(puzzle, guessed), winnings)

        elif action == "B":
            letter = input("Vowel: ").upper().strip()
            if letter not in VOWELS:
                print("Not a vowel.")
                continue
            guessed.add(letter)
            print("Added.")

            if random.random() < 0.4:
                run_side_chat(name, guessed, mask_puzzle(puzzle, guessed), winnings)

        elif action == "S":
            attempt = input("Solution: ").upper().strip()
            if attempt == puzzle:
                print("\n🎉 Correct! 🎉")
                print("Final winnings:", winnings)
                return
            print("Nope.")

        elif action == "P":
            print("Spinning...")
            if random.random() < 0.5:
                print("Safe!")
            else:
                print("Neutral spin.")
            if random.random() < 0.5:
                run_side_chat(name, guessed, mask_puzzle(puzzle, guessed), winnings)

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    play_game()

