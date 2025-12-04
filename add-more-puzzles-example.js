// Example: How to add more puzzles to the game
// 
// To add new puzzles, you can either:
// 1. Edit puzzles.js directly and add them to the appropriate category array
// 2. Use the helper functions (addPuzzle or addPuzzles) in your game code
//
// Here are examples of both methods:

// Method 1: Direct editing in puzzles.js
// Just add new objects to the category arrays like this:
// { phrase: "YOUR PUZZLE PHRASE", words: 3, letters: 15, firstWordLetters: 4 }

// Method 2: Using helper functions (in your game initialization code)
// Example usage:

/*
// Initialize puzzle manager
const puzzleManager = new PuzzleManager();

// Add a single puzzle
puzzleManager.addPuzzle("College Life", "DORMITORY ROOM", 2, 13, 9);

// Add multiple puzzles at once
const newPuzzles = [
    { phrase: "SPRING BREAK TRIP", words: 3, letters: 15, firstWordLetters: 6 },
    { phrase: "GRADUATION CEREMONY", words: 2, letters: 18, firstWordLetters: 10 },
    { phrase: "CAMPUS BOOKSTORE", words: 2, letters: 15, firstWordLetters: 6 }
];
puzzleManager.addPuzzles("College Life", newPuzzles);

// Create a new category
puzzleManager.addPuzzle("Food & Drink", "CHOCOLATE CHIP COOKIES", 3, 20, 9);
*/

// Tips for creating puzzles:
// 1. Count words carefully (spaces separate words, hyphens don't)
// 2. Count total letters (excluding spaces and punctuation)
// 3. Count letters in first word only
// 4. Use ALL CAPS for phrases
// 5. Common categories: "College Life", "On The Map", "Fictional Character", 
//    "Food & Drink", "Movie Title", "Song Title", "Famous People", etc.

// Example puzzle breakdowns:
// "CHOCOLATE CHIP COOKIES" = 3 words, 20 letters, 9 first word letters
// "SPRING BREAK TRIP" = 3 words, 15 letters, 6 first word letters  
// "NEW YORK CITY" = 3 words, 11 letters, 3 first word letters