# 3041_assignment2

Maze solving with **BFS** and **A\***.

## Requirements

- Python **3.12+**

## How to run

This program supports **two input methods**:

1) Read maze from **stdin** (`--line` / `-l`)
2) Read maze from a **file** (`--file <path>` / `-f <path>`)

It also supports selecting an algorithm:

- `--algorithm BFS`
- `--algorithm A*(h=0)`
- `--algorithm A*` (default)

### Option A: paste input (recommended when submitting only .py/.md)

When using stdin mode and paste the maze directly:

PowerShell (Windows):

```powershell
python .\assignment2.py --line --algorithm A*
```

Then paste input in this format (see **Input format** below), and press `Ctrl+Z` then `Enter` to end input.

### Option B: run with an input file

If you do have an input file, you can run:

```powershell
# Run from the folder containing assignment2.py
python .\assignment2.py --file .\maze1.in --algorithm BFS

# Or provide an absolute path if the input file is elsewhere
python .\assignment2.py --file "C:\\path\\to\\maze.in" --algorithm A*
```

#### Important note about paths (for submission)

- Only `assignment2.py` and `README.md` are submitted.
- Input files (e.g., `maze1.in`) are **not** submitted, so during grading the input file will likely be in a **different path**.
- To avoid path issues, either:
	- use **stdin mode** (`--line`) and paste the test case, or
	- place the input file in the **same directory** as `assignment2.py` and run with `--file .\\your_maze.in`, or
	- pass the input file’s **absolute path**.

## Input format

The maze format is:

1) First line: `n m` (rows and columns)
2) Next `n` lines: a grid of `m` characters

Characters:

- `#` wall (blocked)
- `S` start
- `T` target
- any other non-`#` character is treated as free space

Example:

```text
5 7
#######
#S..#T#
#.#...#
#...#.#
#######
```

## Output

The program prints one line like:

```text
[A*] 
	Path Exist: Yes
	Length: 255872
	Expanded States: 2002999
	Time: 13530.6192 ms
```

- `path_exist`: whether a path from `S` to `T` exists
- `length`: path length in steps (`-1` means no path)
- `expanded_states`: number of expanded/visited states
- `elapsed_time`: runtime in milliseconds
