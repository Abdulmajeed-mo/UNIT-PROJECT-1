# Eldergrove: The Forgotten Forest

**The forest remembers. Will you escape?**

## Overview

**Eldergrove: The Forgotten Forest** is an interactive, story-driven command-line adventure game developed using Python.

Players enter a mysterious ancient forest, explore hidden locations, solve randomized puzzles, collect evidence, and make decisions that shape their journey.

The game combines fantasy storytelling, mystery, exploration, and logical challenges, offering multiple possible endings based on the player's achievements.

This project was developed as part of the **Unit 1 Python Programming Assessment at Tuwaiq Academy**.

## Features

- **Bilingual Gameplay:** Arabic and English language support, with Arabic as the default language.
- **Interactive Exploration:** Three main regions containing 12 explorable locations, including optional areas.
- **Story-Driven Adventure:** Nine main story events featuring interactive decisions and mysterious encounters.
- **Randomized Puzzles:** Four puzzle stations with a total bank of 20 questions, including hints and retry options.
- **Explorer Journal:** Tracks collected evidence, solved puzzles, and discoveries.
- **Forest Memory System:** Previous decisions influence certain story interactions.
- **Scoring System:** Earn up to 1,000 points through puzzles, evidence, decisions, and secrets.
- **Multiple Endings:** Six possible endings divided into positive and negative outcomes.
- **Save and Resume:** Save progress and continue an adventure later.
- **Explorer Records:** The Hall of Lost Explorers records player names, scores, completion times, dates, and endings.
- **Modular Architecture:** Organized Python modules and JSON files for game logic, story content, and localization.

## Technologies

- **Python 3.13**
- **JSON** — Story content, puzzles, translations, saved progress, and explorer records.
- **arabic-reshaper** — Arabic text shaping for terminal output.
- **python-bidi** — Bidirectional text handling.
- **Git & GitHub** — Version control and project management.

### Additional Dependencies

- Rich
- Questionary

These libraries are included for planned terminal interface improvements.

## Game Structure

| Component | Description |
|---|---|
| Regions | 3 |
| Explorable Locations | 12 |
| Main Story Events | 9 |
| Puzzle Stations | 4 |
| Puzzle Questions | 20 |
| Possible Endings | 6 |
| Supported Languages | Arabic & English |
| Maximum Score | 1,000 |

## How to Play

1. Launch the game and select your preferred language.
2. Start a new adventure and enter your explorer name.
3. Explore available locations and unlock new paths.
4. Make decisions and interact with story events.
5. Solve puzzles to progress through the forest.
6. Collect evidence and review discoveries in your Journal.
7. Save your progress whenever needed.
8. Complete your journey and discover your final fate.

### In-Game Commands

| Command | Action |
|---|---|
| `N` | Move to the next region |
| `J` | Open the Explorer Journal |
| `S` | View your score |
| `T` | View your playtime |
| `V` | Save your adventure |
| `Q` | Return to the main menu |
| `1–4` | Select available locations |

## Getting Started

### Prerequisites

- Python 3.13 or a compatible version.
- pip
- Git (optional, for cloning the repository).

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Abdulmajeed-mo/UNIT-PROJECT-1.git
```

**2. Navigate to the project directory**

```bash
cd UNIT-PROJECT-1
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment**

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**5. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

### Run the Game

From the project root, execute:

```bash
python main.py
```

Follow the instructions displayed in the terminal to begin your adventure.

## Project Structure

```text
UNIT-PROJECT-1/
├── game/
│   ├── data/
│   │   ├── story.json
│   │   ├── story_ar.json
│   │   ├── puzzles.json
│   │   ├── puzzles_ar.json
│   │   ├── locations.json
│   │   ├── locations_ar.json
│   │   ├── endings.json
│   │   ├── endings_ar.json
│   │   ├── journal.json
│   │   ├── journal_ar.json
│   │   └── translations.json
│   ├── engine.py
│   ├── story.py
│   ├── puzzles.py
│   ├── exploration.py
│   ├── journal.py
│   ├── scoring.py
│   ├── explorers.py
│   ├── endings.py
│   ├── save_system.py
│   └── localization.py
├── ui/
│   ├── interface.py
│   ├── effects.py
│   └── audio.py
├── assets/
│   └── sounds/
├── saves/
├── records/
├── tests/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Scoring System

Players can earn points across four categories:

| Category | Maximum Points |
|---|---:|
| Puzzles | 400 |
| Evidence | 250 |
| Decisions | 200 |
| Secrets | 150 |
| **Total** | **1,000** |

The final score determines whether the player receives a randomly selected positive or negative ending.

## User Stories

- As a player, I want to explore a mysterious forest and uncover its hidden secrets.
- As a player, I want to make decisions that affect my adventure.
- As a player, I want to solve randomized puzzles and receive hints when needed.
- As a player, I want to collect evidence and review my discoveries.
- As a player, I want to experience the game in Arabic or English.
- As a player, I want to save my progress and continue later.
- As a player, I want my achievements and completion time recorded.
- As a player, I want different possible endings based on my progress.

## Project Status

**Core gameplay implemented — testing and enhancements in progress.**

The main adventure, exploration system, puzzles, scoring, Journal, save system, explorer records, localization, and multiple endings have been implemented.

### Planned Improvements

- Enhanced terminal visuals using Rich.
- Interactive keyboard-driven menus using Questionary.
- Fantasy-themed sound effects and atmospheric feedback.
- Further gameplay balancing and secret rewards.
- Additional localization and terminal display refinements.
- Automated testing and final gameplay polish.

## Educational Objectives

This project demonstrates practical application of fundamental Python concepts, including:

- Variables, data types, and conditional statements.
- Loops and functions.
- Lists, dictionaries, and sets.
- Modules and packages.
- JSON file handling.
- Exception handling.
- Object-oriented programming.
- Virtual environments and external libraries.
- Git and GitHub version control.

## License

This project was created for educational purposes as part of the Tuwaiq Academy Python Programming Assessment.