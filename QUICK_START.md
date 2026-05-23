# Quick Start Guide

## Help System

Get help for any program using the professional help system:

```bash
./help.sh                    # Show all available programs
./help.sh <program_name>     # Show detailed help for specific program
./help.sh --help             # Show help system usage
```

### Examples:
```bash
./help.sh cron_schedule.py
./help.sh cron_visualizer.py
./help.sh convert.py
```

## Quick Commands

### 1. Validate Cron Schedules
```bash
python3 cron_schedule.py
```
Prompts for input file (default: cron_schedule.txt).
Shows validation statistics and invalid entries.

### 2. Generate Heatmap Visualization
```bash
./cron_visualizer.py
```
Interactive prompts guide you through visualization.

### 3. Convert to TSV Format
```bash
python3 convert.py
```
Press Enter for default, or specify custom input file.

### 4. Full Validation with Details
```bash
python3 cron_schedule_with_full_validation.py
```
Shows detailed error messages for debugging.

## Common Workflows

### Workflow 1: Validate Data
```bash
python3 cron_schedule.py
# Enter: [press Enter for default file]
# Review validation statistics
# Check for invalid entries
```

### Workflow 2: Create Visualization
```bash
./cron_visualizer.py
# Enter: [press Enter for default file]
# Date: 2025-10-22
# Heatmap: y
```

### Workflow 3: Export to Database
```bash
python3 convert.py
# Enter: [press Enter for default]
# Import cron_schedule.tsv into your database
```

## File Overview

| File | Purpose | Output |
|------|---------|--------|
| `cron_schedule.py` | Validate schedules | Console statistics |
| `cron_visualizer.py` | Create heatmaps | PNG, CSV, TXT files |
| `convert.py` | Export to TSV | TSV file with job names |
| `help.sh` | Get help | Help information |

## First Time Setup

### 1. Install Requirements
```bash
pip install --user matplotlib numpy
```

### 2. Make Scripts Executable
```bash
chmod +x help.sh
chmod +x cron_visualizer.py
```

### 3. Test Installation
```bash
./help.sh
python3 cron_schedule.py
```

## Getting More Help

- Use `./help.sh <program>` for detailed program help
- Check `README.md` for comprehensive documentation
- See `CHANGES.md` for implementation details
