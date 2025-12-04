# 🎪 Interactive Host System for Wheel of Fortune

A ChatGPT-powered commentary system that adds Pat Sajak commentary and player personalities to the Wheel of Fortune game, bringing the excitement of the TV show to your terminal!

## ✨ Features

### 🎙️ Pat Sajak Commentary
- **Authentic Commentary**: Pat Sajak-style commentary for every 1st and 2nd game action
- **Dynamic Responses**: Context-aware commentary based on game events (spins, guesses, bankrupts, etc.)
- **ChatGPT Integration**: Uses OpenAI's API for natural, varied commentary (with template fallback)

### 🎭 Player Personalities
- **50+ Personality Traits**: Optimistic, Cautious, Aggressive, Analytical, Superstitious, and many more
- **Unique Speaking Styles**: Each player gets 3 random mannerisms from 50+ options
- **Personal Catchphrases**: 4 unique catchphrases per player from a pool of 50+
- **Reaction Styles**: 12 different celebration/reaction styles

### 🎤 Interactive Commentary System
- **3rd Action Rule**: Every 3rd game action triggers special commentary
- **Random Selection**: Randomly chooses between User, Player 1, or Player 2 for commentary
- **User Participation**: Prompts you to provide up to 2 lines of commentary
- **AI Player Responses**: Personality-driven commentary from virtual contestants

### 🏆 Victory Speeches
- **5-6 Line Speeches**: Comprehensive congratulatory speeches from Pat Sajak
- **Action References**: Mentions specific actions the winner took during the game
- **Personality Integration**: Acknowledges the winner's playing style and personality
- **Player Reactions**: Winners respond with personality-appropriate celebrations

## 🚀 Quick Start

### Installation
```bash
cd /workspace/project/CanIBuyanAI
pip install -r requirements.txt
```

### Basic Usage
```bash
cd src/PlayGame

# Play with commentary (default)
python3 play_with_commentary.py

# Play with specific player types and commentary
python3 play_with_commentary.py human smart conservative

# Play without commentary
python3 play_with_commentary.py --no-commentary

# Run the demo
python3 demo_commentary.py
```

### With ChatGPT Integration
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run with AI-powered commentary
python3 play_with_commentary.py
```

## 🎮 Player Types

Choose from these AI strategies:
- **human**: Interactive human player
- **smart**: Advanced AI with optimal decision-making
- **conservative**: Cautious AI strategy
- **aggressive**: Bold, risk-taking AI
- **morse**: Uses Morse code letter frequency
- **oxford**: Uses Oxford dictionary frequency
- **trigram**: Uses trigram/bigram analysis

## 🎪 Commentary System Details

### Action Tracking
The system tracks these game actions:
- **Spins**: Wheel spins and their results
- **Letter Guesses**: Consonant guesses with success/failure
- **Vowel Purchases**: Vowel buying decisions
- **Special Events**: Bankrupt, Lose a Turn
- **Solve Attempts**: Puzzle solving attempts

### Commentary Triggers
- **Actions 1 & 2**: Pat Sajak provides commentary
- **Action 3**: Random selection for commentary:
  - **User**: You're prompted to comment (up to 2 lines)
  - **Player 1/2**: AI generates personality-based commentary
- **Pattern Repeats**: Every 3rd action continues the cycle

### Example Commentary Flow
```
Action 1: Player spins wheel
🎙️ Pat Sajak: "And Amazing Player 1 gives the wheel a spin!"

Action 2: Player guesses 'R'
🎙️ Pat Sajak: "'R' says Amazing Player 1! Let's see if it's up there..."

Action 3: Player buys vowel 'E'
🎤 Your turn to comment! What do you think about what just happened?
Line 1: Great strategy buying that vowel!
Line 2: Those E's could really open up the puzzle!
🎤 You: Great strategy buying that vowel! Those E's could really open up the puzzle!
🎙️ Pat Sajak: Excellent observation!
```

## 🤖 ChatGPT Integration

### Setup
1. Get an OpenAI API key from https://platform.openai.com/
2. Set the environment variable: `export OPENAI_API_KEY="your-key"`
3. Run the game - ChatGPT integration will be automatically enabled

### Features
- **Natural Commentary**: AI-generated Pat Sajak commentary
- **Personality-Driven Responses**: Player commentary based on their traits
- **Dynamic Victory Speeches**: Personalized congratulatory speeches
- **Fallback System**: Uses templates if API is unavailable

### API Usage
- **Model**: GPT-3.5-turbo (configurable)
- **Token Limits**: 
  - Commentary: 100 tokens
  - Player responses: 80 tokens  
  - Victory speeches: 200 tokens
- **Temperature**: Varied for different response types (0.7-0.9)

## 📁 File Structure

```
src/PlayGame/
├── interactive_host.py          # Main interactive host system
├── chatgpt_wrapper.py          # ChatGPT API integration
├── play_with_commentary.py     # Enhanced game with commentary
├── demo_commentary.py          # Demo script
└── play_random_puzzle.py       # Original game (unchanged)
```

## 🎭 Personality System

### Traits (50 options)
Optimistic, Cautious, Aggressive, Analytical, Superstitious, Confident, Nervous, Competitive, Friendly, Sarcastic, Enthusiastic, Methodical, Impulsive, Strategic, Lucky, Unlucky, Chatty, Quiet, Dramatic, Calm, Perfectionist, Risk-taker, Team-player, Loner, Cheerful, Grumpy, Witty, Serious, Playful, Focused, Distracted, Patient, Impatient, Humble, Boastful, Logical, Intuitive, Traditional, Innovative, Stubborn, Flexible, Energetic, Laid-back, Precise, Spontaneous, Observant, Dreamy, Practical, Creative, Realistic

### Speaking Mannerisms (50+ options)
- Uses lots of exclamation points
- Speaks in short, clipped sentences  
- Always says 'you know' between thoughts
- Uses sports metaphors constantly
- Speaks like a game show contestant
- Always rhymes when possible
- Uses old-fashioned expressions
- And 40+ more unique styles...

### Catchphrases (50+ options)
- "Let's spin to win!"
- "Feeling lucky today!"
- "Come on, big money!"
- "I've got a good feeling!"
- "Time to take a chance!"
- And 45+ more exciting phrases...

## 🔧 Customization

### Adding New Personalities
Edit `interactive_host.py` and add to these lists:
- `self.personality_traits`
- `self.speaking_mannerisms` 
- `self.catchphrases`
- `self.reaction_styles`

### Modifying Commentary
Edit `chatgpt_wrapper.py` to customize:
- System prompts for different commentary types
- Template fallbacks
- API parameters (model, temperature, tokens)

### Changing Commentary Frequency
Modify the trigger logic in `_trigger_commentary()` in `interactive_host.py`:
```python
if action_count % 3 in [1, 2]:  # Pat Sajak commentary
if action_count % 3 == 0:       # Interactive commentary
```

## 🎯 Implementation Details

### Pseudo Code Implementation
Your original pseudo code has been fully implemented:

✅ **Interactive Host Mode Toggle**: `enable_interactive_mode()` / `disable_interactive_mode()`

✅ **Random Personality Generation**: 2 players get random traits from 30-50 options

✅ **Commentary Timing**: 
- 1st & 2nd actions → Pat Sajak commentary
- 3rd action → Random selection (User/Player1/Player2)

✅ **User Commentary Prompts**: Up to 2 lines of user input

✅ **Player Commentary**: AI-generated based on personality traits

✅ **Victory Speeches**: 5-6 line congratulatory speeches mentioning game actions

### Technical Architecture
- **Modular Design**: Separate classes for host, wrapper, and personalities
- **Error Handling**: Graceful fallbacks when API is unavailable
- **Template System**: Rich template library for offline operation
- **Action Logging**: Comprehensive tracking of all game events
- **State Management**: Persistent game state and player information

## 🎪 Example Session

```
🎪 INTERACTIVE HOST MODE ACTIVATED! 🎪
Pat Sajak and our contestants are ready to entertain!

Meet our contestants:
🎭 Amazing Player 1 the Engineer: Optimistic, Methodical, Confident
🎭 Incredible Player 2 from Texas: Aggressive, Dramatic, Superstitious

Welcome to Wheel of Fortune
You are playing a game of type: Phrase
The clue is: Common Saying

_ _ _ _ _   _ _ _ _ _   _ _ _ _ _

It is player 0's turn
This player is: human

1: Spin, 2: Buy Vowel, 3: Solve .... 1

🎙️ Pat Sajak: Here comes our contestant with a confident spin of the wheel!

Wheel is spinning ....
It landed on ....
.... 600 dollars

Name a consonant .... R

🎙️ Pat Sajak: 'R' says our contestant! Let's see if it's up there...

Yes! 2 R's on the board!
```

## 🚀 Future Enhancements

Potential improvements:
- **Voice Integration**: Text-to-speech for Pat Sajak commentary
- **Visual Elements**: ASCII art for contestants and reactions  
- **Tournament Mode**: Multi-game tournaments with persistent personalities
- **Custom Personalities**: User-defined personality creation
- **Difficulty Levels**: Personality complexity based on game difficulty
- **Statistics Tracking**: Player performance and personality effectiveness

## 🤝 Contributing

To add new features:
1. Fork the repository
2. Create a feature branch
3. Add your enhancements to the appropriate modules
4. Test with both ChatGPT and template modes
5. Submit a pull request

## 📝 License

This project extends the original CanIBuyanAI Wheel of Fortune solver with interactive commentary features.

---

🎪 **Enjoy the show!** The Interactive Host System brings the excitement and personality of Wheel of Fortune right to your terminal. Spin that wheel and let Pat Sajak guide you to victory! 🎪