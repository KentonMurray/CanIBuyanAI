"""
Interactive Host System for Wheel of Fortune
Adds Pat Sajak commentary and player personalities to the game
"""

import random
import json
import time
from typing import Dict, List, Tuple, Optional
import os
from chatgpt_wrapper import ChatGPTWrapper

class PlayerPersonality:
    """Represents a player's personality traits and speaking mannerisms"""
    
    def __init__(self, name: str, traits: List[str], mannerisms: List[str], 
                 catchphrases: List[str], reaction_style: str):
        self.name = name
        self.traits = traits
        self.mannerisms = mannerisms
        self.catchphrases = catchphrases
        self.reaction_style = reaction_style
        self.game_actions = []  # Track actions for victory speech

class InteractiveHost:
    """Main class for managing Pat Sajak commentary and player interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        self.interactive_mode = False
        self.game_action_count = 0
        self.player_personalities = {}
        self.current_players = []
        self.game_actions_log = []
        
        # Initialize ChatGPT wrapper
        self.chatgpt_wrapper = ChatGPTWrapper(api_key=self.api_key)
        
        # Initialize personality database
        self._init_personality_database()
    
    def _init_personality_database(self):
        """Initialize the database of personality traits and mannerisms"""
        
        self.personality_traits = [
            "Optimistic", "Cautious", "Aggressive", "Analytical", "Superstitious",
            "Confident", "Nervous", "Competitive", "Friendly", "Sarcastic",
            "Enthusiastic", "Methodical", "Impulsive", "Strategic", "Lucky",
            "Unlucky", "Chatty", "Quiet", "Dramatic", "Calm",
            "Perfectionist", "Risk-taker", "Team-player", "Loner", "Cheerful",
            "Grumpy", "Witty", "Serious", "Playful", "Focused",
            "Distracted", "Patient", "Impatient", "Humble", "Boastful",
            "Logical", "Intuitive", "Traditional", "Innovative", "Stubborn",
            "Flexible", "Energetic", "Laid-back", "Precise", "Spontaneous",
            "Observant", "Dreamy", "Practical", "Creative", "Realistic"
        ]
        
        self.speaking_mannerisms = [
            "Uses lots of exclamation points",
            "Speaks in short, clipped sentences",
            "Always says 'you know' between thoughts",
            "Uses sports metaphors constantly",
            "Speaks like a game show contestant",
            "Always rhymes when possible",
            "Uses old-fashioned expressions",
            "Speaks in questions",
            "Uses technical jargon",
            "Always mentions their hometown",
            "Uses food analogies",
            "Speaks like a motivational speaker",
            "Always counts things out loud",
            "Uses movie quotes",
            "Speaks in whispers",
            "Always mentions the weather",
            "Uses nautical terms",
            "Speaks like a news anchor",
            "Always apologizes",
            "Uses business buzzwords",
            "Speaks in alliterations",
            "Always mentions their family",
            "Uses musical references",
            "Speaks like a teacher",
            "Always gives advice",
            "Uses animal comparisons",
            "Speaks in metaphors",
            "Always mentions time",
            "Uses color descriptions",
            "Speaks like a comedian",
            "Always asks for confirmation",
            "Uses travel references",
            "Speaks in superlatives",
            "Always mentions luck",
            "Uses cooking terms",
            "Speaks like a detective",
            "Always makes predictions",
            "Uses gardening analogies",
            "Speaks in opposites",
            "Always mentions money",
            "Uses space references",
            "Speaks like a philosopher",
            "Always gives compliments",
            "Uses book references",
            "Speaks in patterns of three",
            "Always mentions their job",
            "Uses car analogies",
            "Speaks like a coach",
            "Always uses hand gestures (mentioned)",
            "Uses historical references"
        ]
        
        self.catchphrases = [
            "Let's spin to win!", "Feeling lucky today!", "This is my moment!",
            "Come on, big money!", "I've got a good feeling!", "Time to take a chance!",
            "Let's solve this puzzle!", "Wheel of Fortune, here I come!", "Lucky letters, don't fail me now!",
            "I'm on fire today!", "This is it, this is my shot!", "Consonants are my friends!",
            "Vowels, vowels everywhere!", "Pat, I'm ready to play!", "Vanna, show me the letters!",
            "Big money, no whammies!", "I can taste victory!", "The wheel is calling my name!",
            "Letters, letters, give me letters!", "Fortune favors the bold!", "I'm feeling the magic!",
            "This puzzle is mine!", "Luck be a lady tonight!", "I've studied for this moment!",
            "The stars are aligned!", "Victory is within reach!", "I can see the solution!",
            "Time to make my mark!", "This is my lucky day!", "The wheel knows my name!",
            "I'm channeling my inner champion!", "Success is just a spin away!", "I was born for this!",
            "The puzzle gods are smiling!", "I've got the golden touch!", "This is destiny calling!",
            "I'm in the zone now!", "The letters are speaking to me!", "Fortune cookie wisdom guides me!",
            "I'm riding the wave of luck!", "This is my time to shine!", "The wheel is my friend!",
            "I can feel the win coming!", "Lady Luck is on my side!", "The puzzle is calling my name!",
            "I'm ready to make history!", "This is what dreams are made of!", "The stars have aligned!",
            "I'm channeling champion energy!", "Victory tastes so sweet!", "The wheel of destiny spins!",
            "I'm living my best life!", "This is pure magic!", "The universe wants me to win!"
        ]
        
        self.reaction_styles = [
            "Explosive celebrations", "Quiet confidence", "Nervous energy", 
            "Cool and collected", "Dramatic flair", "Humble gratitude",
            "Competitive fire", "Philosophical acceptance", "Childlike wonder",
            "Professional composure", "Emotional rollercoaster", "Zen-like calm"
        ]
    
    def enable_interactive_mode(self):
        """Enable interactive host mode and generate player personalities"""
        self.interactive_mode = True
        self.game_action_count = 0
        self.game_actions_log = []
        
        # Generate two random personalities
        self.player_personalities = {
            1: self._generate_random_personality("Player 1"),
            2: self._generate_random_personality("Player 2")
        }
        
        print("\n🎪 INTERACTIVE HOST MODE ACTIVATED! 🎪")
        print("Pat Sajak and our contestants are ready to entertain!")
        print(f"\nMeet our contestants:")
        print(f"🎭 {self.player_personalities[1].name}: {', '.join(self.player_personalities[1].traits[:3])}")
        print(f"🎭 {self.player_personalities[2].name}: {', '.join(self.player_personalities[2].traits[:3])}")
        print()
    
    def disable_interactive_mode(self):
        """Disable interactive host mode"""
        self.interactive_mode = False
        print("Interactive Host Mode disabled.")
    
    def _generate_random_personality(self, base_name: str) -> PlayerPersonality:
        """Generate a random personality for a player"""
        
        # Select random traits
        selected_traits = random.sample(self.personality_traits, 5)
        selected_mannerisms = random.sample(self.speaking_mannerisms, 3)
        selected_catchphrases = random.sample(self.catchphrases, 4)
        selected_reaction_style = random.choice(self.reaction_styles)
        
        # Generate a unique name based on traits
        name_prefixes = ["Amazing", "Incredible", "Fantastic", "Wonderful", "Spectacular", 
                        "Marvelous", "Brilliant", "Dazzling", "Magnificent", "Outstanding"]
        name_suffixes = ["from California", "from Texas", "from New York", "from Florida", 
                        "the Teacher", "the Engineer", "the Artist", "the Chef", "the Nurse", "the Student"]
        
        unique_name = f"{random.choice(name_prefixes)} {base_name} {random.choice(name_suffixes)}"
        
        return PlayerPersonality(
            name=unique_name,
            traits=selected_traits,
            mannerisms=selected_mannerisms,
            catchphrases=selected_catchphrases,
            reaction_style=selected_reaction_style
        )
    
    def log_game_action(self, action_type: str, player_num: int, details: str):
        """Log a game action for commentary purposes"""
        if not self.interactive_mode:
            return
            
        self.game_action_count += 1
        action = {
            'count': self.game_action_count,
            'type': action_type,
            'player': player_num,
            'details': details,
            'timestamp': time.time()
        }
        self.game_actions_log.append(action)
        
        # Add to player's personal action log for victory speech
        if player_num in self.player_personalities:
            self.player_personalities[player_num].game_actions.append(action)
        
        # Trigger commentary based on action count
        self._trigger_commentary(action)
    
    def _trigger_commentary(self, action: Dict):
        """Trigger appropriate commentary based on game action count"""
        action_count = action['count']
        
        if action_count % 3 in [1, 2]:  # 1st and 2nd actions
            self._generate_pat_sajak_commentary(action)
        elif action_count % 3 == 0:  # 3rd action
            self._handle_third_action_commentary(action)
    
    def _generate_pat_sajak_commentary(self, action: Dict):
        """Generate Pat Sajak style commentary using ChatGPT or templates"""
        
        # Get player name
        player_name = "the contestant"
        if action['player'] in self.player_personalities:
            player_name = self.player_personalities[action['player']].name
        
        # Generate commentary using ChatGPT wrapper
        commentary = self.chatgpt_wrapper.generate_pat_sajak_commentary(action, player_name)
        
        print(f"\n🎙️ Pat Sajak: {commentary}")
        time.sleep(1)
    

    
    def _handle_third_action_commentary(self, action: Dict):
        """Handle commentary for every third game action"""
        
        # Randomly select who provides commentary
        commentators = ['user', 'player1', 'player2']
        selected = random.choice(commentators)
        
        if selected == 'user':
            self._prompt_user_commentary(action)
        elif selected == 'player1' and 1 in self.player_personalities:
            self._generate_player_commentary(1, action)
        elif selected == 'player2' and 2 in self.player_personalities:
            self._generate_player_commentary(2, action)
        else:
            # Fallback to user if selected player doesn't exist
            self._prompt_user_commentary(action)
    
    def _prompt_user_commentary(self, action: Dict):
        """Prompt user for commentary"""
        print(f"\n🎤 Your turn to comment! What do you think about what just happened?")
        print(f"(Action: {action['details']})")
        print("Enter your commentary (up to 2 lines):")
        
        line1 = input("Line 1: ").strip()
        line2 = input("Line 2 (optional): ").strip()
        
        user_commentary = line1
        if line2:
            user_commentary += f" {line2}"
        
        if user_commentary:
            print(f"\n🎤 You: {user_commentary}")
            
            # Pat responds to user commentary
            pat_responses = [
                "Great observation!",
                "You're absolutely right!",
                "That's exactly what I was thinking!",
                "Couldn't have said it better myself!",
                "You know this game well!",
                "That's the spirit!",
                "You're really paying attention!",
                "Excellent point!",
                "I like your thinking!",
                "You've got a good eye for the game!"
            ]
            
            pat_response = random.choice(pat_responses)
            print(f"🎙️ Pat Sajak: {pat_response}")
            time.sleep(1)
    
    def _generate_player_commentary(self, player_num: int, action: Dict):
        """Generate commentary from a specific player using ChatGPT or templates"""
        
        if player_num not in self.player_personalities:
            return
        
        personality = self.player_personalities[player_num]
        
        # Generate commentary using ChatGPT wrapper
        commentary = self.chatgpt_wrapper.generate_player_commentary(personality, action)
        
        print(f"\n🎭 {personality.name}: {commentary}")
        
        # Pat responds to player commentary
        pat_responses = [
            f"Thanks for that insight, {personality.name.split()[1]}!",
            f"Well said, {personality.name.split()[1]}!",
            f"I appreciate your perspective, {personality.name.split()[1]}!",
            f"That's the competitive spirit, {personality.name.split()[1]}!",
            f"You're keeping us entertained, {personality.name.split()[1]}!",
            f"Great commentary, {personality.name.split()[1]}!"
        ]
        
        pat_response = random.choice(pat_responses)
        print(f"🎙️ Pat Sajak: {pat_response}")
        time.sleep(1)
    

    
    def generate_victory_speech(self, winning_player: int, final_winnings: int):
        """Generate Pat Sajak's congratulatory victory speech using ChatGPT or templates"""
        
        if not self.interactive_mode or winning_player not in self.player_personalities:
            return
        
        personality = self.player_personalities[winning_player]
        actions = personality.game_actions
        
        print(f"\n🏆 VICTORY SPEECH 🏆")
        
        # Generate victory speech using ChatGPT wrapper
        speech_lines = self.chatgpt_wrapper.generate_victory_speech(personality, final_winnings, actions)
        
        print(f"🎙️ Pat Sajak:")
        for line in speech_lines:
            if line.strip():  # Only print non-empty lines
                print(f"{line}")
                time.sleep(0.5)
        
        # Player's victory reaction
        victory_reactions = [
            f"This is amazing! {random.choice(personality.catchphrases)}",
            f"I can't believe it! Thank you, Pat!",
            f"This is the best day ever! {random.choice(personality.catchphrases)}",
            f"Dreams do come true! Thank you so much!",
            f"I'm speechless! This is incredible!"
        ]
        
        reaction = random.choice(victory_reactions)
        print(f"🎭 {personality.name}: {reaction}")
        time.sleep(2)

# Example usage and testing functions
def test_interactive_host():
    """Test function for the interactive host system"""
    host = InteractiveHost()
    host.enable_interactive_mode()
    
    # Simulate some game actions
    host.log_game_action('spin', 1, 'spun wheel, landed on $600')
    host.log_game_action('guess_consonant', 1, 'letter: R, count: 2, correct')
    host.log_game_action('spin', 2, 'spun wheel, landed on $500')
    host.log_game_action('guess_consonant', 2, 'letter: S, count: 1, correct')
    host.log_game_action('buy_vowel', 1, 'letter: E, count: 3, correct')
    host.log_game_action('spin', 2, 'spun wheel, landed on BANKRUPT')
    
    # Test victory speech
    host.generate_victory_speech(1, 2500)

if __name__ == "__main__":
    test_interactive_host()