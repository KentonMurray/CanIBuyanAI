#!/usr/bin/env python3
"""
Free AI Wrapper - Uses local AI models instead of paid APIs
No API key required, completely free!
"""

import random
import re
from typing import Dict, Any, Optional

class FreeAIWrapper:
    """
    Free AI wrapper that uses local models and enhanced templates
    No API keys, no payments, no accounts needed!
    """
    
    def __init__(self):
        self.use_local_ai = False
        self.model = None
        self.tokenizer = None
        
        # Try to initialize local AI models
        self._try_initialize_local_ai()
        
        # Enhanced template system with more variety
        self._initialize_enhanced_templates()
        
        print("🆓 FREE AI MODE ACTIVATED!")
        if self.use_local_ai:
            print("   Using local AI models for dynamic commentary")
        else:
            print("   Using enhanced template system (still awesome!)")
    
    def _try_initialize_local_ai(self):
        """Try to initialize free local AI models"""
        try:
            # Try to import and use Hugging Face transformers (free!)
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            
            print("🤖 Loading free local AI model...")
            
            # Use a small, fast model that works well for text generation
            model_name = "microsoft/DialoGPT-small"  # Free conversational model
            
            # Initialize the model
            self.model = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                max_length=100,
                do_sample=True,
                temperature=0.8,
                pad_token_id=50256
            )
            
            self.use_local_ai = True
            print(f"✅ Local AI model loaded: {model_name}")
            
        except ImportError:
            print("📦 Hugging Face transformers not installed")
            print("   Install with: pip install transformers torch")
            print("   Using enhanced templates instead (still great!)")
        except Exception as e:
            print(f"⚠️  Could not load local AI: {e}")
            print("   Using enhanced templates instead")
    
    def _initialize_enhanced_templates(self):
        """Initialize enhanced template system with more variety"""
        
        # Pat Sajak commentary templates with more variety
        self.pat_templates = {
            'spin': [
                "And {player} gives the wheel a spin! Let's see what fortune has in store...",
                "Here comes {player} with a confident spin of the wheel!",
                "The wheel is spinning for {player}... and it's slowing down...",
                "{player} steps up to the wheel with determination!",
                "A big spin from {player}! Where will it land?",
                "The wheel is in motion thanks to {player}!",
                "{player} puts some muscle into that spin!",
                "Round and round it goes for {player}!",
                "What a spin from {player}! The suspense is building!",
                "The wheel spins as {player} hopes for the best!"
            ],
            'guess_consonant': [
                "'{letter}' says {player}! Let's see if it's up there...",
                "A confident guess from {player}! Is '{letter}' on the board?",
                "{player} calls out '{letter}' - will it pay off?",
                "'{letter}' is the choice from {player}!",
                "Let's see if '{letter}' is hiding in this puzzle, {player}!",
                "{player} goes with '{letter}' - a solid choice!",
                "The letter '{letter}' from {player} - fingers crossed!",
                "'{letter}' says {player} with conviction!",
                "{player} picks '{letter}' - let's light up the board!",
                "A strategic '{letter}' from {player}!"
            ],
            'buy_vowel': [
                "{player} invests in a vowel - let's see if it's there!",
                "Smart move, {player}! Buying that '{letter}' could open things up!",
                "{player} spends $250 on '{letter}' - will it pay off?",
                "A vowel purchase from {player}! '{letter}' is the choice!",
                "{player} goes shopping for '{letter}'!",
                "'{letter}' for $250, {player}! Let's see what happens!",
                "{player} invests in '{letter}' - a calculated risk!",
                "Vowel time! {player} buys '{letter}'!",
                "{player} thinks '{letter}' might be the key!",
                "A strategic vowel buy from {player}!"
            ],
            'bankrupt': [
                "Oh no! {player} hits BANKRUPT! That's the way it goes sometimes!",
                "BANKRUPT! Sorry {player}, that's the risk of the wheel!",
                "The wheel can be cruel! BANKRUPT for {player}!",
                "Ouch! {player} loses it all to BANKRUPT!",
                "That's the game! BANKRUPT takes {player}'s earnings!",
                "The dreaded BANKRUPT! Tough break, {player}!",
                "BANKRUPT strikes {player}! Back to zero!",
                "Oh my! {player} hits the BANKRUPT wedge!",
                "The wheel shows no mercy! BANKRUPT for {player}!",
                "That's a heartbreaker! BANKRUPT, {player}!"
            ],
            'lose_turn': [
                "Lose a Turn! Sorry {player}, that's how the wheel rolls!",
                "{player} hits Lose a Turn - better luck next time!",
                "The wheel says 'Lose a Turn' to {player}!",
                "Tough break! {player} loses their turn!",
                "Lose a Turn for {player} - that's the game!",
                "The wheel takes away {player}'s turn!",
                "{player} gets Lose a Turn - onto the next player!",
                "No luck this time, {player}! Lose a Turn!",
                "The wheel decides {player} loses this turn!",
                "Lose a Turn strikes {player}!"
            ],
            'correct_guess': [
                "Yes! {count} {letter}'s on the board! Nice work, {player}!",
                "There {are} {count} {letter}'s! Great guess, {player}!",
                "Excellent! {count} {letter}'s light up the board for {player}!",
                "Perfect! {player} finds {count} {letter}'s!",
                "Beautiful! {count} {letter}'s for {player}!",
                "Outstanding! {player} reveals {count} {letter}'s!",
                "Fantastic guess! {count} {letter}'s, {player}!",
                "Well done! {player} uncovers {count} {letter}'s!",
                "Brilliant! {count} {letter}'s appear for {player}!",
                "Superb! {player} hits {count} {letter}'s!"
            ],
            'wrong_guess': [
                "Sorry {player}, no {letter}'s in this puzzle!",
                "Ooh, sorry! No {letter}'s up there, {player}!",
                "Not this time, {player}! No {letter}'s on the board!",
                "Sorry {player}, the {letter} isn't there!",
                "No luck with {letter}, {player}!",
                "The {letter} doesn't appear, {player}!",
                "Sorry, no {letter}'s in the puzzle, {player}!",
                "The board says no to {letter}, {player}!",
                "Not today, {player}! No {letter}'s!",
                "The {letter} isn't hiding in this puzzle, {player}!"
            ]
        }
        
        # Enhanced player response templates
        self.player_responses = {
            'optimistic': [
                "I've got a good feeling about this!",
                "This is going to be great!",
                "I can feel the luck coming!",
                "Everything's looking up!",
                "This is my moment!"
            ],
            'cautious': [
                "Let me think about this carefully...",
                "I need to be strategic here.",
                "Better safe than sorry!",
                "I'll play it safe this time.",
                "Let me consider my options."
            ],
            'aggressive': [
                "I'm going for it!",
                "Time to take some risks!",
                "Let's make something happen!",
                "I'm feeling bold today!",
                "Go big or go home!"
            ],
            'confident': [
                "I know I can do this!",
                "This is right in my wheelhouse!",
                "I've got this figured out!",
                "Confidence is key!",
                "I'm ready for anything!"
            ],
            'nervous': [
                "Oh boy, here goes nothing...",
                "I hope this works out...",
                "This is making me nervous!",
                "Fingers crossed!",
                "I'm a little worried about this..."
            ]
        }
        
        # Pat Sajak responses to player commentary
        self.pat_responses = [
            "Excellent point!",
            "I couldn't agree more!",
            "You know this game well!",
            "That's the spirit!",
            "Absolutely right!",
            "Well said!",
            "I like your thinking!",
            "You've got it figured out!",
            "That's what I'm talking about!",
            "Couldn't have said it better myself!",
            "You're really into this game!",
            "Great observation!",
            "That's the way to look at it!",
            "You understand the strategy!",
            "I love the enthusiasm!"
        ]
    
    def generate_pat_sajak_commentary(self, action: Dict[str, Any], player_name: str) -> str:
        """Generate Pat Sajak commentary for a game action"""
        
        if self.use_local_ai:
            return self._generate_ai_commentary(action, player_name)
        else:
            return self._generate_template_commentary(action, player_name)
    
    def _generate_ai_commentary(self, action: Dict[str, Any], player_name: str) -> str:
        """Generate commentary using local AI model"""
        try:
            action_type = action.get('type', 'unknown')
            details = action.get('details', '')
            
            # Create a prompt for the AI
            prompt = f"Pat Sajak commenting on Wheel of Fortune: {player_name} just {action_type}"
            if details:
                prompt += f" and {details}"
            prompt += ". Pat says:"
            
            # Generate response
            response = self.model(prompt, max_length=len(prompt) + 30, num_return_sequences=1)
            generated_text = response[0]['generated_text']
            
            # Extract just the new part
            commentary = generated_text[len(prompt):].strip()
            
            # Clean up the response
            commentary = re.sub(r'["\n]', '', commentary)
            commentary = commentary.split('.')[0] + '.'
            
            return commentary if commentary else self._generate_template_commentary(action, player_name)
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_template_commentary(action, player_name)
    
    def _generate_template_commentary(self, action: Dict[str, Any], player_name: str) -> str:
        """Generate commentary using enhanced templates"""
        
        action_type = action.get('type', 'spin')
        details = action.get('details', '')
        
        # Get appropriate template
        templates = self.pat_templates.get(action_type, self.pat_templates['spin'])
        template = random.choice(templates)
        
        # Prepare format parameters
        format_params = {'player': player_name}
        
        # Parse details string to extract letter and count information
        if details:
            # Extract letter from details like "letter: A, count: 2"
            import re
            letter_match = re.search(r'letter:\s*([A-Z])', details)
            if letter_match:
                format_params['letter'] = letter_match.group(1)
            
            count_match = re.search(r'count:\s*(\d+)', details)
            if count_match:
                count = int(count_match.group(1))
                format_params['count'] = count
                format_params['are'] = "are" if count != 1 else "is"
        
        # Handle specific details from action dict (legacy support)
        if 'letter' in action:
            format_params['letter'] = action['letter']
        
        if 'count' in action:
            count = action['count']
            format_params['count'] = count
            format_params['are'] = "are" if count != 1 else "is"
        
        # Only format with available parameters
        try:
            commentary = template.format(**format_params)
        except KeyError as e:
            # If template has missing parameters, use a safe fallback
            missing_key = str(e).strip("'")
            safe_template = template
            
            if missing_key == 'letter':
                safe_template = safe_template.replace('{letter}', 'that letter')
            if missing_key == 'count':
                safe_template = safe_template.replace('{count}', 'some')
            if missing_key == 'are':
                safe_template = safe_template.replace('{are}', 'are')
                
            commentary = safe_template.format(**{k: v for k, v in format_params.items() if k != missing_key})
        
        return commentary
    
    def generate_player_commentary(self, action: Dict[str, Any], player_personality: Dict[str, Any]) -> str:
        """Generate player commentary based on personality"""
        
        # Get personality traits
        traits = player_personality.get('traits', ['optimistic'])
        primary_trait = traits[0].lower()
        
        # Get appropriate responses
        responses = self.player_responses.get(primary_trait, self.player_responses['optimistic'])
        
        # Add some variety based on action
        action_type = action.get('type', '')
        if action_type == 'bankrupt':
            responses = ["Oh no!", "That's rough!", "Better luck next time!", "The wheel can be cruel!"]
        elif action_type == 'correct_guess':
            responses = ["Yes! I knew it!", "That's what I'm talking about!", "Perfect!", "I'm on fire!"]
        
        return random.choice(responses)
    
    def generate_pat_response(self, player_commentary: str) -> str:
        """Generate Pat Sajak response to player commentary"""
        return random.choice(self.pat_responses)
    
    def generate_victory_speech(self, winner_name: str, winnings: int, actions_taken: list) -> str:
        """Generate victory speech from Pat Sajak"""
        
        # Victory speech templates
        openings = [
            f"Congratulations, {winner_name}! What an incredible game!",
            f"Outstanding performance, {winner_name}!",
            f"Well done, {winner_name}! You've earned this victory!",
            f"Fantastic job, {winner_name}! What a game!"
        ]
        
        winnings_lines = [
            f"You've won ${winnings} and shown us some fantastic gameplay!",
            f"${winnings} is your total, and you've earned every penny!",
            f"You're taking home ${winnings} with style!",
            f"${winnings} and a great performance - well deserved!"
        ]
        
        action_lines = [
            "From those confident spins to those strategic letter choices,",
            "Your gameplay from start to finish was impressive,",
            "The way you handled every challenge,",
            "Your strategy and determination throughout,"
        ]
        
        personality_lines = [
            "you've demonstrated what it takes to be a champion!",
            "you've shown us real Wheel of Fortune mastery!",
            "you've proven you belong on this stage!",
            "you've made this game truly special!"
        ]
        
        closings = [
            f"Thanks for playing Wheel of Fortune, and congratulations once again!",
            f"It's been a pleasure having you on the show, {winner_name}!",
            f"You're a true champion, {winner_name}!",
            f"Well played, {winner_name}! Enjoy your winnings!"
        ]
        
        # Build the speech
        speech_parts = [
            random.choice(openings),
            random.choice(winnings_lines),
            random.choice(action_lines),
            random.choice(personality_lines),
            random.choice(closings)
        ]
        
        return '\n'.join(speech_parts)

# Test the free AI wrapper
if __name__ == "__main__":
    print("🆓 Testing Free AI Wrapper")
    print("=" * 40)
    
    wrapper = FreeAIWrapper()
    
    # Test commentary
    test_action = {
        'type': 'spin',
        'details': 'spun wheel, landed on $600'
    }
    
    commentary = wrapper.generate_pat_sajak_commentary(test_action, "Test Player")
    print(f"📝 Commentary: {commentary}")
    
    # Test player response
    test_personality = {
        'traits': ['optimistic', 'confident'],
        'name': 'Amazing Player 1'
    }
    
    player_response = wrapper.generate_player_commentary(test_action, test_personality)
    print(f"🎭 Player: {player_response}")
    
    pat_response = wrapper.generate_pat_response(player_response)
    print(f"🎙️ Pat: {pat_response}")
    
    print("\n✅ Free AI Wrapper is working!")