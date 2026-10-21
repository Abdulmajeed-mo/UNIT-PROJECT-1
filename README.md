# Eldergrove: The Forgotten Forest

**The forest remembers. Will you escape?**

## Overview

Eldergrove: The Forgotten Forest is an interactive command-line adventure game built with Python. Players explore an ancient, mysterious forest, encounter strange characters, solve riddles, uncover forgotten secrets, and make choices that influence their journey and ultimate fate.

The game combines narrative exploration, puzzle-solving, and decision-making in a text-based experience.

## Features

- Interactive command-line gameplay.
- Story-driven exploration across nine main events.
- Four main puzzles to challenge the player.
- Choices and clues that influence the story's outcome.
- A journal for tracking discovered evidence.
- Multiple endings based on the player's progress and decisions.
- Save and resume gameplay.
- Modular Python code organized into packages and modules.

*Some features are planned for upcoming development and may not yet be implemented.*

## Technologies

- Python
- JSON for story data
- Rich for terminal formatting
- Questionary for interactive prompts
- Git and GitHub for version control

## User Stories

- As a player, I want to explore a mysterious forest so that I can uncover its secrets.
- As a player, I want to make meaningful choices so that my decisions affect the story.
- As a player, I want to solve riddles and puzzles to progress through the adventure.
- As a player, I want to collect clues and review them in a journal.
- As a player, I want to save my progress and resume the game later.
- As a player, I want multiple possible endings based on my actions.

## Getting Started

### Prerequisites

- Python 3.13 or a compatible Python version.
- pip.

### Installation

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd UNIT-PROJECT-1
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   **Windows PowerShell:**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

### Usage

Run the game from the project root:

```bash
python main.py
```

Follow the on-screen instructions to start a new game, explore the forest, and make your choices.

## Project Structure

```text
UNIT-PROJECT-1/
├── game/
│   ├── data/
│   │   └── story.json
│   ├── endings.py
│   ├── engine.py
│   ├── journal.py
│   ├── puzzles.py
│   ├── save_system.py
│   ├── story.py
│   └── __init__.py
├── ui/
│   ├── interface.py
│   └── __init__.py
├── saves/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Project Status

This project is being developed as part of the Unit 1 Python programming assessment. Features and documentation will be updated as development progresses.

## License

This project was created for educational purposes.
