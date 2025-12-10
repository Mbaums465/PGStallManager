# Project Gorgon Sales Viewer

A GUI application for analyzing Player Shop Log files from Project Gorgon. View your stall sales grouped by buyer, item, or time period with filtering and sorting options.

## Requirements

- Windows OS
- Python 3.10 or higher (with `pythonw.exe` in PATH)
- No additional packages required (uses standard library only)

## Files

| File | Description |
|------|-------------|
| `PGStallManager_prod.py` | Main Python GUI application |
| `StallMe_prod.bat` | Windows launcher script (runs without console window) |

## Installation

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
2. Place both files in the same folder
3. Double-click `StallMe_prod.bat` to launch

## Usage

### Launching
Double-click `StallMe_prod.bat` to start the application without a console window.

### Configuration Options

- **Folder**: Path to your Player Shop Log files  
  Default: `%USERPROFILE%\AppData\LocalLow\Elder Game\Project Gorgon\Books`

- **Group By**: How to aggregate sales data
  - Buyer, Item, Year, Month, Week, or Day

- **Buyer Filter**: Show only sales to a specific buyer (exact match)

- **Item Filter**: Show only sales of items containing the filter text
  - Check "Exact" for exact item name matching

- **Start/End Date**: Filter sales within a date range (MM/DD/YYYY format)

- **Top N Results**: Limit output to top N results (0 = no limit)

- **Sort By**: Sort results by Group, TotalSold, TotalEarned, or AvgPrice

### Output Columns

| Column | Description |
|--------|-------------|
| Group | The grouping value (buyer name, item name, or date) |
| TotalSold | Total quantity of items sold |
| TotalEarned | Total councils earned |
| AvgPrice | Average price per item |

Click any column header to sort by that column.

## Features

- Automatic detection of latest log file per day
- Resizable window with expandable results table
- Click column headers to sort results
- Running total of all earnings displayed at bottom
- No external dependencies

## Troubleshooting

**"Python is not installed or not in PATH"**  
Install Python from python.org and ensure "Add Python to PATH" is checked during installation.

**"pythonw.exe not found"**  
Your Python installation may be incomplete. Reinstall Python with default options.

**No files found**  
Verify the folder path points to your Project Gorgon Books folder and that PlayerShopLog files exist within the date range.
