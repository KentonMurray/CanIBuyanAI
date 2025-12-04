# Wheel of Fortune - New Puzzle System

## Overview
The game now uses a new, self-contained puzzle system that doesn't rely on external CSV files or backend services. All puzzles are stored directly in JavaScript for better performance and easier management.

## Current Puzzle Categories

### College Life (44 puzzles)
Examples:
- WRITING FOR THE CAMPUS NEWSPAPER
- STUDYING ABROAD
- FINALS WEEK
- ACADEMIC SCHOLARSHIP

### On The Map (82 puzzles)
Examples:
- THE PACIFIC OCEAN
- UNIVERSAL CITY CALIFORNIA
- THE ROCKY MOUNTAINS
- TORONTO ONTARIO CANADA

### Fictional Character (3 puzzles)
Examples:
- DAMSEL IN DISTRESS
- DAISY BUCHANAN
- DWIGHT K. SCHRUTE

## How It Works

1. **PuzzleManager Class**: Manages all puzzles and provides methods for selection and management
2. **Random Selection**: The game randomly selects puzzles from all categories
3. **Category Display**: Each puzzle shows its category along with the puzzle board
4. **Easy Addition**: New puzzles can be easily added using provided methods

## Adding New Puzzles

### Method 1: Individual Puzzle Addition
```javascript
// Add a single puzzle to an existing category
game.puzzleManager.addPuzzle("College Life", "SPRING BREAK", 2, 11, 6);

// Add a single puzzle to a new category
game.puzzleManager.addCategory("Food & Drink");
game.puzzleManager.addPuzzle("Food & Drink", "PIZZA PARTY", 2, 10, 5);
```

### Method 2: Bulk Addition
```javascript
// Add multiple puzzles at once
const newPuzzles = [
    { phrase: "GRADUATION DAY", words: 2, letters: 13, firstWordLetters: 10 },
    { phrase: "SUMMER VACATION", words: 2, letters: 14, firstWordLetters: 6 }
];

game.puzzleManager.addPuzzlesFromArray("College Life", newPuzzles);
```

### Method 3: Using the Helper Function
```javascript
// Use the helper function to calculate stats automatically
function calculatePuzzleStats(phrase) {
    const words = phrase.split(' ').length;
    const letters = phrase.replace(/\s/g, '').length;
    const firstWordLetters = phrase.split(' ')[0].length;
    
    return {
        phrase: phrase.toUpperCase(),
        words: words,
        letters: letters,
        firstWordLetters: firstWordLetters
    };
}

// Example usage
const newPuzzle = calculatePuzzleStats("Hello World");
game.puzzleManager.addPuzzle("Greetings", newPuzzle.phrase, newPuzzle.words, newPuzzle.letters, newPuzzle.firstWordLetters);
```

## File Structure

- `puzzles.js` - Contains the PuzzleManager class and all puzzle data
- `script-new.js` - Main game logic (updated to use new puzzle system)
- `wheel-of-fortune-new.html` - Main game HTML (includes puzzles.js)
- `add-puzzles-example.js` - Example file showing how to add more puzzles
- `test-puzzles.html` - Test page to verify puzzle system functionality

## Features

- **129 total puzzles** across 3 categories
- **Random selection** from all puzzles
- **Category display** with each puzzle
- **Easy expansion** - add new puzzles and categories
- **Search functionality** - find puzzles by partial phrase match
- **Statistics tracking** - get counts by category or total
- **No external dependencies** - all puzzles stored locally

## Testing

Open `test-puzzles.html` in a browser to verify the puzzle system is working correctly. It will show:
- Total puzzle count
- Available categories
- Random puzzle examples
- Category-specific examples

## Console Logging

When the game loads, check the browser console to see puzzle system statistics:
```
Puzzle System Loaded:
- Total puzzles: 129
- Categories: College Life, On The Map, Fictional Character
  - College Life: 44 puzzles
  - On The Map: 82 puzzles
  - Fictional Character: 3 puzzles
```

## Migration Notes

The new system completely replaces the old CSV-based backend system. The game no longer needs:
- Backend server for puzzle loading
- CSV files in the data directory
- Network requests for puzzle data

All puzzles are now loaded instantly from JavaScript, making the game faster and more reliable.