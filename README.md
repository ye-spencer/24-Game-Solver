# 24 Game Solver

A comprehensive solution for analyzing and playing the mathematical card game *24*. This project includes both a statistical analysis tool to determine the solvability percentage of different card combinations and an automated bot that can play the game on 4nums.com.

## Overview

The 24 Game is a mathematical card game where players use four numbers and basic arithmetic operations (+, -, ×, ÷) to create an expression that equals 24. This project was originally created to settle a family dispute about the percentage of solvable hands, but has evolved into a complete analysis and automation solution.

## Features

### Statistical Analysis (`solver.py`)
- **Comprehensive Solvability Testing**: Analyzes all possible card combinations to determine solvability percentages
- **Multiple Testing Methods**:
  - **Combination Analysis**: Tests all 715 unique combinations (76.5% solvable)
  - **Permutation Analysis**: Tests all 10,000 possible hand orders (83.5% solvable)
  - **Deck Simulation**: Deals hands from shuffled 40-card decks (four copies of each number 1–10) to mirror actual gameplay (~85.7% solvable)
- **Solution Generation**: Finds and outputs mathematical expressions that equal 24
- **Configurable Parameters**: Adjustable number ranges, operations, and testing parameters

### Automated Bot (`bot.py`)
- **Web Automation**: Uses Selenium WebDriver to interact with 4nums.com
- **Computer Vision**: Implements OpenCV and Tesseract OCR to read numbers from canvas elements
- **Intelligent Solving**: Automatically calculates and executes solutions in real-time
- **Anti-Detection**: Variable timing and movement patterns to avoid bot detection
- **High-Score Capable**: Designed for competitive play and achieving high scores

## Installation

### Prerequisites
- Python 3.7+
- Chrome browser
- ChromeDriver (a Windows build is included in the `drivers/` directory; the bot currently targets Windows)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and available on your `PATH` (required by `pytesseract`)

### Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure ChromeDriver is compatible with your Chrome version

## Usage

### Running the Statistical Analysis

1. Open `solver.py` and uncomment the desired test method in the `main()` function:
   ```python
   # test_every_combination()  # Tests all unique combinations
   # test_all_hands()          # Tests all possible hand orders
   # test_sample()             # Simulates random game rounds
   ```

2. Run the analysis:
   ```bash
   python solver.py
   ```

### Running the Automated Bot

1. Start the bot:
   ```bash
   python bot.py
   ```

2. Wait for the browser window to load and click "Against the clock"

3. **Important**: Within 3 seconds, position your mouse slightly above and to the right of the canvas top corner (approximate positioning is sufficient)

4. The bot will automatically:
   - Read the numbers from the canvas using OCR
   - Calculate the optimal solution
   - Execute the moves to solve the puzzle

5. To stop the bot, slam the mouse into a corner of the screen to trigger PyAutoGUI's built-in fail-safe, or terminate the process from the terminal

> **⚠️ Important**: The bot requires supervision. The site's "coffee break" prompts appear randomly and must be dismissed manually to keep the bot running.

## Demo

Watch the bot in action! Here's a recording of the beginning of a run using `bot.py`:

[![24 Game Bot Demo](https://github.com/user-attachments/assets/a0a4b9a3-b67f-4758-8956-06d0e01cf65e)](https://github.com/user-attachments/assets/a0a4b9a3-b67f-4758-8956-06d0e01cf65e)

The demo shows the bot automatically:
- Reading numbers from the canvas using OCR
- Calculating solutions in real-time
- Executing moves with precise timing
- Handling the game interface seamlessly

## Technical Details

### Algorithm
The solver uses a brute-force approach with the following key components:
- **Permutation Generation**: Generates all possible orderings of the four numbers
- **Operation Enumeration**: Tests all possible combinations of arithmetic operations
- **Expression Evaluation**: Uses Python's `eval()` function with proper error handling
- **Floating-Point Precision**: Implements margin of error (0.00001) for floating-point comparisons

### Computer Vision Pipeline
1. **Canvas Capture**: Extracts canvas data using JavaScript injection
2. **Image Processing**: Converts to grayscale and applies binary thresholding
3. **OCR Recognition**: Uses Tesseract with PSM 7 configuration for optimal number recognition
4. **Coordinate Mapping**: Maps recognized numbers to their screen positions

### Automation Strategy
- **Mouse Movement**: Calculates pixel ratios for accurate positioning
- **Timing Variations**: Random delays to mimic human behavior
- **Error Handling**: Graceful handling of unsolvable puzzles and edge cases

## Results

The analysis reveals significant differences in solvability depending on the testing methodology:

| Method | Total Tests | Solvable | Percentage |
|--------|-------------|----------|------------|
| Unique Combinations | 715 | 547 | 76.5% |
| All Permutations | 10,000 | 8,350 | 83.5% |
| Deck Simulation | 100,000 | ~85,720 | ~85.7% |

Since the deck simulation most closely mirrors how hands are dealt in actual play, roughly **85%** of dealt hands are solvable in practice.

## Known Issues & Limitations

### Floating-Point Precision
Some solvable puzzles may be missed due to floating-point arithmetic errors or integer truncation issues.

### Bot Limitations
- **Coffee Break Detection**: Currently requires manual intervention for coffee breaks
- **Solution Button**: Does not automatically click the "never show solutions" button
- **Graceful Shutdown**: No built-in stop command; the bot must be stopped via PyAutoGUI's fail-safe or by terminating the process
- **Platform Support**: The bundled ChromeDriver (`chromedriver.exe`) targets Windows

## Future Improvements

### Planned Features
- [ ] Automatic coffee break detection and handling
- [ ] Automatic "never show solutions" button clicking
- [ ] Graceful program termination mechanism

## Dependencies

- `pytesseract==0.3.10` - OCR for number recognition
- `PyAutoGUI==0.9.54` - Mouse and keyboard automation
- `numpy==1.23.3` - Numerical computations
- `selenium==3.141.0` - Web browser automation
- `opencv-python==4.7.0.68` - Image processing
- `pillow==10.4.0` - Image manipulation

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to improve the project.

## Author

**Spencer Ye**
