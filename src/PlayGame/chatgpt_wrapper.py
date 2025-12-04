"""
ChatGPT Wrapper for Enhanced Commentary Generation
Provides AI-powered commentary generation as an alternative to template-based responses
"""

from openai import OpenAI
import os
import json
import time
from typing import Dict, List, Optional, Any
import random

class ChatGPTWrapper:
    """Wrapper class for ChatGPT API integration"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.use_ai = False
        self.client = None
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_ai = True
                print("🤖 ChatGPT integration enabled!")
            except Exception as e:
                print(f"⚠️  OpenAI client initialization failed: {e}")
                print("   Using template-based responses.")
        else:
            print("⚠️  No OpenAI API key found. Using template-based responses.")
            print("   Set OPENAI_API_KEY environment variable to enable AI commentary.")
    
    def generate_pat_sajak_commentary(self, action: Dict, player_name: str) -> str:
        """Generate Pat Sajak style commentary using ChatGPT or templates"""
        
        if not self.use_ai:
            return self._generate_template_pat_commentary(action, player_name)
        
        try:
            prompt = self._create_pat_sajak_prompt(action, player_name)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_pat_sajak_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            commentary = response.choices[0].message.content.strip()
            return commentary
            
        except Exception as e:
            print(f"⚠️  ChatGPT error: {e}. Falling back to templates.")
            return self._generate_template_pat_commentary(action, player_name)
    
    def generate_player_commentary(self, personality: Any, action: Dict) -> str:
        """Generate player commentary based on personality using ChatGPT or templates"""
        
        if not self.use_ai:
            return self._generate_template_player_commentary(personality, action)
        
        try:
            prompt = self._create_player_commentary_prompt(personality, action)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_player_commentary_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=80,
                temperature=0.9
            )
            
            commentary = response.choices[0].message.content.strip()
            return commentary
            
        except Exception as e:
            print(f"⚠️  ChatGPT error: {e}. Falling back to templates.")
            return self._generate_template_player_commentary(personality, action)
    
    def generate_victory_speech(self, personality: Any, final_winnings: int, actions: List[Dict]) -> List[str]:
        """Generate Pat Sajak victory speech using ChatGPT or templates"""
        
        if not self.use_ai:
            return self._generate_template_victory_speech(personality, final_winnings, actions)
        
        try:
            prompt = self._create_victory_speech_prompt(personality, final_winnings, actions)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_victory_speech_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            speech = response.choices[0].message.content.strip()
            return speech.split('\n')
            
        except Exception as e:
            print(f"⚠️  ChatGPT error: {e}. Falling back to templates.")
            return self._generate_template_victory_speech(personality, final_winnings, actions)
    
    def _get_pat_sajak_system_prompt(self) -> str:
        """System prompt for Pat Sajak commentary generation"""
        return """You are Pat Sajak, the legendary host of Wheel of Fortune. You are known for:
- Warm, encouraging commentary
- Quick wit and gentle humor
- Professional but friendly demeanor
- Enthusiasm for the game and contestants
- Classic game show host phrases
- Keeping the energy positive and exciting

Generate commentary that sounds exactly like Pat Sajak would say it on the show. Keep it brief (1-2 sentences), enthusiastic, and appropriate for family television. Use his characteristic speaking style and phrases."""
    
    def _get_player_commentary_system_prompt(self) -> str:
        """System prompt for player commentary generation"""
        return """You are a Wheel of Fortune contestant with a specific personality. Generate commentary that reflects your unique traits and speaking style. Keep it brief (1-2 sentences), authentic to your character, and appropriate for the game show setting. Show your personality through your word choice and enthusiasm level."""
    
    def _get_victory_speech_system_prompt(self) -> str:
        """System prompt for victory speech generation"""
        return """You are Pat Sajak giving a congratulatory victory speech to a Wheel of Fortune winner. Create a 5-6 line speech that:
- Congratulates the winner warmly
- Mentions their winnings
- References specific actions they took during the game
- Acknowledges their personality or playing style
- Ends with classic Pat Sajak warmth and professionalism

Make it sound exactly like Pat Sajak's genuine congratulatory speeches from the show."""
    
    def _create_pat_sajak_prompt(self, action: Dict, player_name: str) -> str:
        """Create prompt for Pat Sajak commentary"""
        
        action_type = action.get('type', 'unknown')
        details = action.get('details', '')
        
        prompt = f"The contestant {player_name} just performed this action in Wheel of Fortune: {action_type}. "
        prompt += f"Details: {details}. "
        prompt += "Generate Pat Sajak's commentary for this moment."
        
        return prompt
    
    def _create_player_commentary_prompt(self, personality: Any, action: Dict) -> str:
        """Create prompt for player commentary"""
        
        traits = ", ".join(personality.traits[:3])
        mannerisms = personality.mannerisms[0] if personality.mannerisms else "speaks normally"
        action_details = action.get('details', '')
        
        prompt = f"You are a Wheel of Fortune contestant with these personality traits: {traits}. "
        prompt += f"Your speaking style: {mannerisms}. "
        prompt += f"Something just happened in the game: {action_details}. "
        prompt += "Give a brief comment about what just happened, staying in character."
        
        return prompt
    
    def _create_victory_speech_prompt(self, personality: Any, final_winnings: int, actions: List[Dict]) -> str:
        """Create prompt for victory speech"""
        
        player_name = personality.name
        traits = ", ".join(personality.traits[:3])
        
        # Summarize key actions
        action_summary = []
        for action in actions[-3:]:  # Last 3 actions
            action_summary.append(f"{action['type']}: {action['details']}")
        
        prompt = f"Generate Pat Sajak's victory speech for {player_name} who just won ${final_winnings}. "
        prompt += f"The winner's personality: {traits}. "
        prompt += f"Key actions they took: {'; '.join(action_summary)}. "
        prompt += "Make it 5-6 lines, warm and congratulatory in Pat's style."
        
        return prompt
    
    def _generate_template_pat_commentary(self, action: Dict, player_name: str) -> str:
        """Fallback template-based Pat Sajak commentary"""
        
        templates = {
            'spin': [
                f"And {player_name} gives the wheel a spin! Let's see what fortune has in store...",
                f"Here comes {player_name} with a confident spin of the wheel!",
                f"The wheel is spinning for {player_name}... and it's slowing down..."
            ],
            'guess_consonant': [
                f"'{action.get('details', '').split('letter:')[1].split(',')[0].strip() if 'letter:' in action.get('details', '') else 'X'}' says {player_name}! Let's see if it's up there...",
                f"{player_name} calls out a consonant - let's see if it pays off!",
                f"A confident guess from {player_name}!"
            ],
            'buy_vowel': [
                f"{player_name} decides to buy a vowel for $250!",
                f"Smart strategy from {player_name}, buying that vowel!",
                f"{player_name} invests in a vowel - let's see if it's there!"
            ],
            'bankrupt': [
                f"Oh no! {player_name} hits BANKRUPT! That's the way it goes sometimes!",
                f"BANKRUPT for {player_name}! The wheel can be cruel, folks!",
                f"Ouch! {player_name} loses it all to BANKRUPT!"
            ],
            'lose_turn': [
                f"Lose a Turn for {player_name}! Sometimes the wheel has other plans!",
                f"{player_name} hits Lose a Turn - that's the way the wheel spins!",
                f"The wheel says 'not this time' to {player_name}!"
            ]
        }
        
        action_type = action.get('type', 'spin')
        template_list = templates.get(action_type, templates['spin'])
        return random.choice(template_list)
    
    def _generate_template_player_commentary(self, personality: Any, action: Dict) -> str:
        """Fallback template-based player commentary"""
        
        base_comments = [
            "That was intense!",
            "What a moment!",
            "This game is exciting!",
            "I love this game!",
            "The suspense is killing me!"
        ]
        
        comment = random.choice(base_comments)
        
        # Add personality flair
        if "Optimistic" in personality.traits:
            comment = f"I'm feeling great about this! {comment}"
        elif "Nervous" in personality.traits:
            comment = f"Oh my goodness! {comment}"
        elif "Confident" in personality.traits:
            comment = f"I've got this! {comment}"
        
        return comment
    
    def _generate_template_victory_speech(self, personality: Any, final_winnings: int, actions: List[Dict]) -> List[str]:
        """Fallback template-based victory speech"""
        
        speech_lines = [
            f"Congratulations, {personality.name}! What an incredible game!",
            f"You've won ${final_winnings} and shown us some fantastic gameplay!",
            "From those confident spins to those strategic letter choices,",
            "you've demonstrated what it takes to be a champion!",
            f"Your {personality.reaction_style.lower()} really made this game special!",
            "Thanks for playing Wheel of Fortune, and congratulations once again!"
        ]
        
        return speech_lines

# Test function
def test_chatgpt_wrapper():
    """Test the ChatGPT wrapper functionality"""
    
    wrapper = ChatGPTWrapper()
    
    # Test action
    test_action = {
        'type': 'guess_consonant',
        'details': 'letter: R, count: 2, correct',
        'player': 1
    }
    
    # Test Pat commentary
    commentary = wrapper.generate_pat_sajak_commentary(test_action, "Amazing Player 1")
    print(f"Pat Commentary: {commentary}")
    
    # Mock personality for testing
    class MockPersonality:
        def __init__(self):
            self.name = "Test Player"
            self.traits = ["Optimistic", "Confident", "Enthusiastic"]
            self.mannerisms = ["Uses lots of exclamation points"]
            self.reaction_style = "Explosive celebrations"
    
    mock_personality = MockPersonality()
    
    # Test player commentary
    player_comment = wrapper.generate_player_commentary(mock_personality, test_action)
    print(f"Player Commentary: {player_comment}")
    
    # Test victory speech
    victory_speech = wrapper.generate_victory_speech(mock_personality, 5000, [test_action])
    print("Victory Speech:")
    for line in victory_speech:
        print(f"  {line}")

if __name__ == "__main__":
    test_chatgpt_wrapper()