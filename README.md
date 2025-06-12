# WAL25 – Würfelwurf for Science

This Python script allows users to manually input the outcomes of 500 dice rolls for experimental or statistical purposes, saving each entry immediately to a CSV file. It includes live audio feedback and correction capabilities.

## Features

- Prompts for dice proportion label at startup (e.g., `60:40`).
- Creates a CSV file named `diceroll_{proportions}.csv`.
- For each roll:
  - Displays the current throw number.
  - Accepts only `A` (for big) or `B` (for small) as valid inputs.
  - Plays a distinct audio file (`A.m4a` or `B.m4a`) upon input.
  - Automatically saves the input with a timestamp into the CSV.
- Allows correction:
  - Press `ESC` to undo the previous entry.
- Can be exited anytime by pressing `X` (saves progress and exits cleanly).
- Automatically saves entries into a CSV file in a `data` folder next to the script.
- Finishes after 500 entries with a "Progress finished" message.

## Usage

1. **Prepare audio files**  
   Place `A.m4a` and `B.m4a` sound files in the same directory as the script (not inside `data/`).

2. **Run the script**  
   Use the terminal (not an IDE) to run the program:
   ```bash
   python3 csv_writer.py
   ```

3. **Follow the prompts**  
   - Enter the dice proportions (used in the filename).
   - For each throw, press:
     - `A` → for "big"
     - `B` → for "small"
     - `ESC` → to undo the last entry  
     - `X` → to exit the program at any time

> ⚠️ Note: This program must be run in a real terminal (TTY). It does not work properly in IDE consoles like PyCharm due to raw input requirements.
