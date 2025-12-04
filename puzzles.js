// New Wheel of Fortune Puzzle System
class PuzzleManager {
    constructor() {
        this.puzzles = {
            "College Life": [
                { phrase: "WRITING FOR THE CAMPUS NEWSPAPER", words: 5, letters: 28, firstWordLetters: 7 },
                { phrase: "WALKING ACROSS CAMPUS", words: 3, letters: 19, firstWordLetters: 7 },
                { phrase: "UNIVERSITY BOOKSTORE", words: 2, letters: 19, firstWordLetters: 10 },
                { phrase: "STUDYING ABROAD", words: 2, letters: 14, firstWordLetters: 8 },
                { phrase: "STUDY-ABROAD PROGRAM", words: 2, letters: 18, firstWordLetters: 11 },
                { phrase: "STUDENT ORGANIZATIONS", words: 2, letters: 20, firstWordLetters: 7 },
                { phrase: "STUDENT GOVERNMENT", words: 2, letters: 17, firstWordLetters: 7 },
                { phrase: "STUDENT ACTIVITIES COMMITTEE", words: 3, letters: 26, firstWordLetters: 7 },
                { phrase: "SPENDING A SEMESTER ABROAD", words: 4, letters: 23, firstWordLetters: 8 },
                { phrase: "SORORITY RUSH", words: 2, letters: 12, firstWordLetters: 8 },
                { phrase: "PULLING AN ALL-NIGHTER", words: 3, letters: 19, firstWordLetters: 7 },
                { phrase: "PROFESSOR'S OFFICE HOURS", words: 3, letters: 21, firstWordLetters: 10 },
                { phrase: "PREREQUISITE CLASS", words: 2, letters: 17, firstWordLetters: 12 },
                { phrase: "PLEDGING A FRATERNITY", words: 3, letters: 19, firstWordLetters: 8 },
                { phrase: "PLAYING IN THE MARCHING BAND", words: 5, letters: 24, firstWordLetters: 7 },
                { phrase: "PHYSICS CLASS", words: 2, letters: 12, firstWordLetters: 7 },
                { phrase: "ON-CAMPUS ACTIVITIES", words: 2, letters: 18, firstWordLetters: 8 },
                { phrase: "NEW STUDENT ORIENTATION", words: 3, letters: 21, firstWordLetters: 3 },
                { phrase: "MOVING OFF CAMPUS", words: 3, letters: 15, firstWordLetters: 6 },
                { phrase: "MEDIEVAL & RENAISSANCE STUDIES", words: 3, letters: 26, firstWordLetters: 8 },
                { phrase: "MASTER'S DEGREE", words: 2, letters: 13, firstWordLetters: 7 },
                { phrase: "MAJORING IN SPANISH", words: 3, letters: 17, firstWordLetters: 8 },
                { phrase: "MAJORING IN ITALIAN", words: 3, letters: 17, firstWordLetters: 8 },
                { phrase: "MAJORING IN BUSINESS EDUCATION", words: 4, letters: 27, firstWordLetters: 8 },
                { phrase: "MAJORING IN BIOLOGY", words: 3, letters: 17, firstWordLetters: 8 },
                { phrase: "LATE-NIGHT STUDY SESSION", words: 3, letters: 21, firstWordLetters: 9 },
                { phrase: "LATE-NIGHT CRAM SESSIONS", words: 3, letters: 21, firstWordLetters: 9 },
                { phrase: "INTRAMURAL SPORTS", words: 2, letters: 16, firstWordLetters: 10 },
                { phrase: "INTRAMURAL ACTIVITIES", words: 2, letters: 20, firstWordLetters: 10 },
                { phrase: "GRADE POINT AVERAGE", words: 3, letters: 17, firstWordLetters: 5 },
                { phrase: "FRESHMAN ORIENTATION", words: 2, letters: 19, firstWordLetters: 8 },
                { phrase: "FINALS WEEK", words: 2, letters: 10, firstWordLetters: 6 },
                { phrase: "FALLING ASLEEP IN THE LIBRARY", words: 5, letters: 25, firstWordLetters: 7 },
                { phrase: "DECLARING A MAJOR", words: 3, letters: 15, firstWordLetters: 9 },
                { phrase: "CRAMMING FOR AN EXAM", words: 4, letters: 17, firstWordLetters: 8 },
                { phrase: "COURSE NUMBER", words: 2, letters: 12, firstWordLetters: 6 },
                { phrase: "COURSE CATALOG", words: 2, letters: 13, firstWordLetters: 6 },
                { phrase: "COPIES OF MY TRANSCRIPTS", words: 4, letters: 21, firstWordLetters: 6 },
                { phrase: "CHALLENGING CURRICULUM", words: 2, letters: 21, firstWordLetters: 11 },
                { phrase: "BUYING TEXTBOOKS", words: 2, letters: 15, firstWordLetters: 6 },
                { phrase: "BRINGING LAUNDRY HOME TO MOM AND DAD", words: 7, letters: 30, firstWordLetters: 8 },
                { phrase: "BEING GRANTED A SCHOLARSHIP", words: 4, letters: 24, firstWordLetters: 5 },
                { phrase: "ALL-NIGHT CRAM SESSION", words: 3, letters: 19, firstWordLetters: 8 },
                { phrase: "ACADEMIC SCHOLARSHIP", words: 2, letters: 19, firstWordLetters: 8 }
            ],
            "On The Map": [
                { phrase: "UNIVERSAL CITY CALIFORNIA", words: 3, letters: 23, firstWordLetters: 9 },
                { phrase: "TWIN FALLS IDAHO", words: 3, letters: 14, firstWordLetters: 4 },
                { phrase: "TURKS & CAICOS ISLANDS", words: 3, letters: 18, firstWordLetters: 5 },
                { phrase: "TSWALU KALAHARI RESERVE", words: 3, letters: 21, firstWordLetters: 6 },
                { phrase: "TROPIC OF CAPRICORN", words: 3, letters: 17, firstWordLetters: 6 },
                { phrase: "TRENTON NEW JERSEY", words: 3, letters: 16, firstWordLetters: 7 },
                { phrase: "TORONTO ONTARIO CANADA", words: 3, letters: 20, firstWordLetters: 7 },
                { phrase: "TIN SHUI WAI", words: 3, letters: 10, firstWordLetters: 3 },
                { phrase: "THON BURI DISTRICT", words: 3, letters: 16, firstWordLetters: 4 },
                { phrase: "THE YUKON RIVER", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE WEST INDIES", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE VERDE RIVER", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE VENICE LAGOON", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE UNITED KINGDOM", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE THAMES RIVER", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE SWISS ALPS", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE SOUTHERN OCEAN", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE SOUTH POLE", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE SOUTH PACIFIC", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE SEA-TO-SKY HIGHWAY", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE SARONIC GULF", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE SALTON SEA", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE ROUGE RIVER", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE ROCKY MOUNTAINS", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE RIVER THAMES", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE RIVER SHANNON", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE RIO GRANDE", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE RHONE VALLEY", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE PLAKA DISTRICT", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE PLAINS STATES", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE PACIFIC OCEAN", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE PACIFIC NORTHWEST", words: 3, letters: 19, firstWordLetters: 3 },
                { phrase: "THE OZARK MOUNTAINS", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE NORWEGIAN SEA", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE NORTHERN ROCKIES", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE NORTHERN OCEAN", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE NORTH POLE", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE NILE RIVER", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE NEGEV DESERT", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE MISSOURI RIVER", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE MEDITERRANEAN SEA", words: 3, letters: 19, firstWordLetters: 3 },
                { phrase: "THE MAINE COAST", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE LAKE DISTRICT", words: 3, letters: 15, firstWordLetters: 3 },
                { phrase: "THE KONA COAST", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE JARI RIVER", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE ITALIAN RIVIERA", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE IONIAN ISLANDS", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE INDIAN OCEAN", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE HUDSON RIVER", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE HUDSON BAY", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE HIGH VALLEY", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE HAWAIIAN ISLANDS", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE HAFNARFJALL MOUNTAIN", words: 3, letters: 22, firstWordLetters: 3 },
                { phrase: "THE GULF COAST", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE GREEK ISLES", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE GREEK ARCHIPELAGO", words: 3, letters: 19, firstWordLetters: 3 },
                { phrase: "THE GREAT PLAINS", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE GREAT LAKES", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE GREAT BASIN", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE GRAND VALLEY", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE GRAND STRAND", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE GRAND STAIRCASE", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE GOBI DESERT", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE GARDEN DISTRICT", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE GANGES RIVER", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE GALAPAGOS ISLANDS", words: 3, letters: 19, firstWordLetters: 3 },
                { phrase: "THE GALAPAGOS ISLAND", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE FRENCH RIVIERA", words: 3, letters: 16, firstWordLetters: 3 },
                { phrase: "THE FRENCH ALPS", words: 3, letters: 13, firstWordLetters: 3 },
                { phrase: "THE FLORIDA PANHANDLE", words: 3, letters: 19, firstWordLetters: 3 },
                { phrase: "THE FLORIDA KEYS", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE FIVE FREEWAY", words: 3, letters: 14, firstWordLetters: 3 },
                { phrase: "THE FAST LANE", words: 3, letters: 11, firstWordLetters: 3 },
                { phrase: "THE FALKLAND ISLANDS", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE ENGLISH CHANNEL", words: 3, letters: 17, firstWordLetters: 3 },
                { phrase: "THE EASTERN SEABOARD", words: 3, letters: 18, firstWordLetters: 3 },
                { phrase: "THE EAST RIVER", words: 3, letters: 12, firstWordLetters: 3 },
                { phrase: "THE DON RIVER", words: 3, letters: 11, firstWordLetters: 3 }
            ],
            "Fictional Character": [
                { phrase: "DAMSEL IN DISTRESS", words: 3, letters: 16, firstWordLetters: 6 },
                { phrase: "DAISY BUCHANAN", words: 2, letters: 13, firstWordLetters: 5 },
                { phrase: "DWIGHT K. SCHRUTE", words: 3, letters: 14, firstWordLetters: 6 }
            ]
        };
    }

    // Get all available categories
    getCategories() {
        return Object.keys(this.puzzles);
    }

    // Get all puzzles from a specific category
    getPuzzlesByCategory(category) {
        return this.puzzles[category] || [];
    }

    // Get a random puzzle from all categories
    getRandomPuzzle() {
        const categories = this.getCategories();
        const randomCategory = categories[Math.floor(Math.random() * categories.length)];
        const categoryPuzzles = this.puzzles[randomCategory];
        const randomPuzzle = categoryPuzzles[Math.floor(Math.random() * categoryPuzzles.length)];
        
        return {
            ...randomPuzzle,
            category: randomCategory
        };
    }

    // Get a random puzzle from a specific category
    getRandomPuzzleFromCategory(category) {
        const categoryPuzzles = this.puzzles[category];
        if (!categoryPuzzles || categoryPuzzles.length === 0) {
            return null;
        }
        
        const randomPuzzle = categoryPuzzles[Math.floor(Math.random() * categoryPuzzles.length)];
        return {
            ...randomPuzzle,
            category: category
        };
    }

    // Add a new puzzle to a category
    addPuzzle(category, phrase, words, letters, firstWordLetters) {
        if (!this.puzzles[category]) {
            this.puzzles[category] = [];
        }
        
        this.puzzles[category].push({
            phrase: phrase.toUpperCase(),
            words: words,
            letters: letters,
            firstWordLetters: firstWordLetters
        });
    }

    // Add a new category
    addCategory(categoryName) {
        if (!this.puzzles[categoryName]) {
            this.puzzles[categoryName] = [];
        }
    }

    // Get total number of puzzles
    getTotalPuzzleCount() {
        return Object.values(this.puzzles).reduce((total, categoryPuzzles) => total + categoryPuzzles.length, 0);
    }

    // Get puzzle count by category
    getCategoryPuzzleCount(category) {
        return this.puzzles[category] ? this.puzzles[category].length : 0;
    }

    // Bulk add puzzles from an array
    addPuzzlesFromArray(category, puzzleArray) {
        if (!this.puzzles[category]) {
            this.puzzles[category] = [];
        }
        
        puzzleArray.forEach(puzzle => {
            this.puzzles[category].push({
                phrase: puzzle.phrase.toUpperCase(),
                words: puzzle.words,
                letters: puzzle.letters,
                firstWordLetters: puzzle.firstWordLetters
            });
        });
    }

    // Get all puzzle data (useful for debugging or exporting)
    getAllPuzzles() {
        return this.puzzles;
    }

    // Search puzzles by phrase (partial match)
    searchPuzzles(searchTerm) {
        const results = [];
        const searchUpper = searchTerm.toUpperCase();
        
        Object.keys(this.puzzles).forEach(category => {
            this.puzzles[category].forEach(puzzle => {
                if (puzzle.phrase.includes(searchUpper)) {
                    results.push({
                        ...puzzle,
                        category: category
                    });
                }
            });
        });
        
        return results;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PuzzleManager;
}