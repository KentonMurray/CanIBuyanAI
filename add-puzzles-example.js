// Example: How to add more puzzles to the Wheel of Fortune game
// This file shows how you can easily add new puzzles and categories

// To add puzzles, you can use this template:

/*
// Example of adding a new category with puzzles
const newMoviePuzzles = [
    { phrase: "THE GODFATHER", words: 2, letters: 11, firstWordLetters: 3 },
    { phrase: "STAR WARS", words: 2, letters: 8, firstWordLetters: 4 },
    { phrase: "JURASSIC PARK", words: 2, letters: 12, firstWordLetters: 8 }
];

// Add the new category and puzzles
game.puzzleManager.addCategory("Movie Titles");
game.puzzleManager.addPuzzlesFromArray("Movie Titles", newMoviePuzzles);

// Or add individual puzzles
game.puzzleManager.addPuzzle("Movie Titles", "THE MATRIX", 2, 9, 3);
*/

// Example of adding puzzles to existing categories:
/*
const moreCollegePuzzles = [
    { phrase: "GRADUATION CEREMONY", words: 2, letters: 18, firstWordLetters: 10 },
    { phrase: "STUDENT LOAN DEBT", words: 3, letters: 16, firstWordLetters: 7 },
    { phrase: "CAMPUS TOUR", words: 2, letters: 10, firstWordLetters: 6 }
];

game.puzzleManager.addPuzzlesFromArray("College Life", moreCollegePuzzles);
*/

// To use this in your game:
// 1. Include this file after puzzles.js and script-new.js in your HTML
// 2. Uncomment the code above and modify with your own puzzles
// 3. The game will automatically include your new puzzles in the random selection

// Helper function to calculate puzzle statistics
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

// Example usage:
// console.log(calculatePuzzleStats("Hello World")); 
// Output: { phrase: "HELLO WORLD", words: 2, letters: 10, firstWordLetters: 5 }

console.log("Puzzle addition example loaded. Check add-puzzles-example.js for instructions on adding more puzzles.");