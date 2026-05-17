# Cron Schedule Validator & Visualizer

A comprehensive Python toolkit for validating, analyzing, and visualizing cron schedules with beautiful heatmap charts.

## Features

### 1. **Cron Schedule Validator** (`cron_schedule.py`)
- ✅ Validates all 5 cron fields (minute, hour, day_of_month, month, day_of_week)
- ✅ Parses complex cron expressions (wildcards, ranges, lists, steps)
- ✅ Supports day_of_week values 0-7 (where 0 and 7 both represent Sunday)
- ✅ Detailed validation statistics with breakdown by failure type
- ✅ Identifies and tracks invalid entries
- ✅ Displays unique minute/hour combinations with counts
- ✅ **100% validation success rate** on cleaned data

### 2. **Cron Visualizer** (`cron_visualizer.py`)
- 📊 Interactive date-based visualization
- 📈 Generates 60×24 heatmap grid (minutes × hours)
- 🎨 Beautiful matplotlib heatmaps with 'RdYlGn_r' colormap
- 🔢 Numbers displayed in each cell
- 📁 Exports to multiple formats:
  - Tab-delimited text files
  - CSV files (pure 2D arrays)
  - High-quality PNG heatmaps (300 DPI)
- 📉 Statistics: total executions, max concurrent jobs, coverage

### 3. **Full Validation Script** (`cron_schedule_with_full_validation.py`)
- Enhanced validation with detailed error messages
- Function-based validation approach
- Extracts and validates minute/hour pairs
- Shows sample invalid entries with reasons

## Requirements

```bash
pip install matplotlib numpy
```

Or for user installation:
```bash
pip install --user matplotlib numpy
```

## Usage

### Validate Cron Schedules

```bash
python3 cron_schedule.py
```

**Output:**
- Validation statistics (total, valid, invalid by type)
- Success rate percentage
- Top 50 minute/hour combinations sorted by frequency
- Details of any invalid entries

### Generate Heatmap Visualizations

```bash
./cron_visualizer.py
```

**Interactive prompts:**
1. Enter filename (default: `cron_schedule.txt`)
2. Enter date (YYYY-MM-DD) or 'today'
3. Choose to generate heatmap (y/n)

**Generated files:**
- `cron_output_YYYY-MM-DD.txt` - Tab-delimited grid
- `execution_map_YYYY-MM-DD.csv` - CSV format (no headers)
- `heatmap_YYYY-MM-DD.png` - Beautiful visualization

### Run Full Validation

```bash
python3 cron_schedule_with_full_validation.py
```

## Project Structure

```
.
├── cron_schedule.py                      # Main validation script
├── cron_visualizer.py                    # Heatmap generator
├── cron_schedule_with_full_validation.py # Alternative validator
├── test_comparison.py                    # Testing utilities
├── cron_schedule_4k.txt                  # Sample data (4000 entries)
├── test_small.txt                        # Small test file
├── test_specific_days.txt                # Specific test cases
├── CHANGES.md                            # Enhancement documentation
├── VALIDATION_IMPROVEMENTS.md            # Validation features guide
├── REVIEW_AND_SUGGESTIONS.md             # Code review
├── HOW_TO_FIX.md                         # Troubleshooting guide
└── README.md                             # This file
```

## Cron Syntax Supported

### Patterns
- `*` - Every value
- `*/n` - Step values (e.g., `*/15` = every 15 minutes)
- `n` - Single value
- `n-m` - Range (e.g., `1-5` = 1,2,3,4,5)
- `n-m/x` - Range with step (e.g., `1-10/2` = 1,3,5,7,9)
- `n,m,p` - List (e.g., `1,3,5`)
- Mixed: `1-5,10,15-20`

### Fields
1. **Minute** (0-59)
2. **Hour** (0-23)
3. **Day of Month** (1-31)
4. **Month** (1-12)
5. **Day of Week** (0-7, where 0=Sunday, 7=Sunday)

## Examples

### Example 1: Validation Statistics
```
================================================================================
CRON VALIDATION STATISTICS
================================================================================
Total entries processed:        1510
Valid entries:                  1510
Invalid entries (field count):  0
Invalid entries (pattern):      0
Invalid entries (range):        0
Validation success rate:        100.00%
================================================================================
```

### Example 2: Heatmap Output
![Sample Heatmap](docs/sample_heatmap.png)

The heatmap shows:
- **Red cells**: High activity (many jobs scheduled)
- **Yellow cells**: Medium activity
- **Green cells**: Low activity
- **Numbers in cells**: Exact count of concurrent jobs

### Example 3: Common Schedule Patterns
```
Minute     Hour       Count
0          0          18        ← 18 jobs at midnight
0          6          15        ← 15 jobs at 6 AM
*/15       *          4         ← 4 jobs every 15 minutes
```

## Key Improvements

### From Original Implementation

| Feature | Before | After |
|---------|--------|-------|
| **Field Validation** | Last 3 fields only | All 5 fields |
| **Day of Week** | 0-6 only | 0-7 (accepts Sunday as 0 or 7) |
| **Statistics** | None | Detailed breakdown |
| **Output** | Simple list | Formatted tables + charts |
| **Invalid Tracking** | None | Captures and displays all invalid entries |
| **Visualization** | Text only | Beautiful heatmap charts |

## Insights from Analysis

Using this tool on 32,567 cron schedules revealed:
- **Peak scheduling times**: Midnight, 6 AM, and hourly intervals
- **Most common patterns**: Every 15 minutes (`*/15 * * * *`)
- **100% time coverage**: Jobs scheduled for every minute of every hour
- **4+ million executions** per day on analyzed system

## Documentation

- **[CHANGES.md](CHANGES.md)** - Detailed enhancement documentation
- **[VALIDATION_IMPROVEMENTS.md](VALIDATION_IMPROVEMENTS.md)** - Validation features
- **[HOW_TO_FIX.md](HOW_TO_FIX.md)** - Troubleshooting guide
- **[REVIEW_AND_SUGGESTIONS.md](REVIEW_AND_SUGGESTIONS.md)** - Code review

## Contributing

Feel free to open issues or submit pull requests for:
- Additional validation rules
- New visualization options
- Performance improvements
- Bug fixes

## License

This project is open source and available for educational and commercial use.

## Author

Created with assistance from Claude Code (Anthropic).
