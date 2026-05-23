#!/bin/bash
# Professional Help System for Cron Schedule Tools
# Usage: ./help.sh <program_name>

# Color codes for better readability
BOLD='\033[1m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
RED='\033[1;31m'
NC='\033[0m' # No Color

# Function to display header
display_header() {
    echo -e "${BOLD}${BLUE}"
    echo "================================================================================"
    echo "  CRON SCHEDULE TOOLKIT - HELP SYSTEM"
    echo "================================================================================"
    echo -e "${NC}"
}

# Function to display usage
display_usage() {
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  ./help.sh <program_name>"
    echo ""
    echo -e "${YELLOW}AVAILABLE PROGRAMS:${NC}"
    echo "  - cron_schedule.py"
    echo "  - cron_visualizer.py"
    echo "  - cron_schedule_with_full_validation.py"
    echo "  - convert.py"
    echo "  - test_comparison.py"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  ./help.sh cron_schedule.py"
    echo "  ./help.sh convert.py"
    echo ""
}

# Function to display help for cron_schedule.py
help_cron_schedule() {
    echo -e "${BOLD}${GREEN}PROGRAM: cron_schedule.py${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}DESCRIPTION:${NC}"
    echo "  Main validation script that validates all cron schedule entries and provides"
    echo "  comprehensive statistics about data quality."
    echo ""
    echo -e "${CYAN}FEATURES:${NC}"
    echo "  ✓ Validates all 5 cron fields (minute, hour, day_of_month, month, day_of_week)"
    echo "  ✓ Supports day_of_week values 0-7 (where 0 and 7 both represent Sunday)"
    echo "  ✓ Parses complex cron expressions (wildcards, ranges, lists, steps)"
    echo "  ✓ Tracks validation statistics with detailed breakdown"
    echo "  ✓ Displays invalid entries with reasons"
    echo "  ✓ Shows unique minute/hour combinations sorted by frequency"
    echo ""
    echo -e "${CYAN}USAGE:${NC}"
    echo "  python3 cron_schedule.py"
    echo ""
    echo -e "${CYAN}INTERACTIVE PROMPT:${NC}"
    echo "  Enter cron schedule filename (default: cron_schedule.txt):"
    echo "  - Press Enter to use default (cron_schedule.txt)"
    echo "  - Or type custom filename (e.g., cron_schedule_4k.txt)"
    echo ""
    echo -e "${CYAN}INPUT:${NC}"
    echo "  Any text file with one cron schedule per line"
    echo ""
    echo -e "${CYAN}OUTPUT:${NC}"
    echo "  - Validation statistics (total, valid, invalid by type)"
    echo "  - Success rate percentage"
    echo "  - Top 50 minute/hour combinations with counts"
    echo "  - Details of invalid entries (if any)"
    echo ""
    echo -e "${CYAN}EXAMPLE:${NC}"
    echo "  $ python3 cron_schedule.py"
    echo "  Enter cron schedule filename: [press Enter for default]"
    echo "  Using default: cron_schedule.txt"
    echo "  ✓ Successfully loaded 32567 cron schedules"
    echo ""
    echo -e "${CYAN}EXAMPLE OUTPUT:${NC}"
    echo "  CRON VALIDATION STATISTICS"
    echo "  Total entries processed:        1510"
    echo "  Valid entries:                  1510"
    echo "  Invalid entries (field count):  0"
    echo "  Invalid entries (pattern):      0"
    echo "  Invalid entries (range):        0"
    echo "  Validation success rate:        100.00%"
    echo ""
    echo -e "${CYAN}CRON SYNTAX SUPPORTED:${NC}"
    echo "  *         - Every value"
    echo "  */n       - Step values (e.g., */15 = every 15 minutes)"
    echo "  n         - Single value"
    echo "  n-m       - Range (e.g., 1-5)"
    echo "  n-m/x     - Range with step (e.g., 1-10/2)"
    echo "  n,m,p     - List (e.g., 1,3,5)"
    echo "  Mixed     - Combined (e.g., 1-5,10,15-20)"
    echo ""
}

# Function to display help for cron_visualizer.py
help_cron_visualizer() {
    echo -e "${BOLD}${GREEN}PROGRAM: cron_visualizer.py${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}DESCRIPTION:${NC}"
    echo "  Interactive tool that creates visual heatmap charts showing when cron jobs"
    echo "  execute on a specific date. Generates 60×24 grids (minutes × hours)."
    echo ""
    echo -e "${CYAN}FEATURES:${NC}"
    echo "  ✓ Date-based interactive visualization"
    echo "  ✓ Beautiful matplotlib heatmaps with 'RdYlGn_r' colormap"
    echo "  ✓ Numbers displayed in each cell"
    echo "  ✓ Exports to multiple formats (TXT, CSV, PNG)"
    echo "  ✓ High-quality PNG heatmaps (300 DPI)"
    echo "  ✓ Statistics: total executions, max concurrent jobs, coverage"
    echo ""
    echo -e "${CYAN}USAGE:${NC}"
    echo "  ./cron_visualizer.py"
    echo "  OR"
    echo "  python3 cron_visualizer.py"
    echo ""
    echo -e "${CYAN}INTERACTIVE PROMPTS:${NC}"
    echo "  1. Enter cron schedule filename (default: cron_schedule.txt)"
    echo "  2. Enter date (YYYY-MM-DD) or 'today'"
    echo "  3. Generate heatmap? (y/n)"
    echo "  4. Type 'x' or 'exit' to quit"
    echo ""
    echo -e "${CYAN}OUTPUT FILES:${NC}"
    echo "  - cron_output_YYYY-MM-DD.txt        Tab-delimited grid"
    echo "  - execution_map_YYYY-MM-DD.csv      CSV format (no headers)"
    echo "  - heatmap_YYYY-MM-DD.png            Beautiful visualization"
    echo ""
    echo -e "${CYAN}EXAMPLE:${NC}"
    echo "  $ ./cron_visualizer.py"
    echo "  Enter cron schedule filename: [press Enter for default]"
    echo "  Enter date: 2025-10-22"
    echo "  Generate heatmap? y"
    echo ""
    echo -e "${CYAN}REQUIREMENTS:${NC}"
    echo "  pip install matplotlib numpy"
    echo ""
}

# Function to display help for cron_schedule_with_full_validation.py
help_cron_schedule_with_full_validation() {
    echo -e "${BOLD}${GREEN}PROGRAM: cron_schedule_with_full_validation.py${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}DESCRIPTION:${NC}"
    echo "  Enhanced validation script with detailed error messages and comprehensive"
    echo "  validation functions. Alternative approach to cron_schedule.py."
    echo ""
    echo -e "${CYAN}FEATURES:${NC}"
    echo "  ✓ Function-based validation approach"
    echo "  ✓ Detailed error messages for each invalid entry"
    echo "  ✓ Extracts and validates minute/hour pairs"
    echo "  ✓ Shows sample invalid entries with reasons"
    echo "  ✓ Validation success rate calculation"
    echo ""
    echo -e "${CYAN}USAGE:${NC}"
    echo "  python3 cron_schedule_with_full_validation.py"
    echo ""
    echo -e "${CYAN}INPUT:${NC}"
    echo "  Reads from: cron_schedule.txt (hardcoded in script)"
    echo ""
    echo -e "${CYAN}OUTPUT:${NC}"
    echo "  - Validation statistics with detailed breakdown"
    echo "  - Sample invalid entries (first 10) with error descriptions"
    echo "  - Sample valid minute/hour pairs (first 20)"
    echo "  - Total counts and success rate"
    echo ""
    echo -e "${CYAN}KEY DIFFERENCES FROM cron_schedule.py:${NC}"
    echo "  - More verbose error messages"
    echo "  - Shows actual error reasons for each invalid entry"
    echo "  - Function-based architecture (easier to extend)"
    echo "  - Better for debugging data quality issues"
    echo ""
}

# Function to display help for convert.py
help_convert() {
    echo -e "${BOLD}${GREEN}PROGRAM: convert.py${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}DESCRIPTION:${NC}"
    echo "  Converts cron schedule text files to TSV (Tab-Separated Values) format with"
    echo "  unique job names. Creates a structured format suitable for databases and"
    echo "  spreadsheet applications."
    echo ""
    echo -e "${CYAN}FEATURES:${NC}"
    echo "  ✓ Interactive filename prompt with default option"
    echo "  ✓ Generates unique job names (job00001, job00002, etc.)"
    echo "  ✓ Tab-delimited output format"
    echo "  ✓ Automatic output filename generation"
    echo "  ✓ File existence validation"
    echo "  ✓ Preview of first 10 rows"
    echo "  ✓ Detailed step-by-step explanations"
    echo ""
    echo -e "${CYAN}USAGE:${NC}"
    echo "  python3 convert.py"
    echo ""
    echo -e "${CYAN}INTERACTIVE PROMPT:${NC}"
    echo "  Enter input filename (default: cron_schedule.txt): "
    echo "  - Press Enter to use default (cron_schedule.txt)"
    echo "  - Or type custom filename (e.g., cron_schedule_4k.txt)"
    echo ""
    echo -e "${CYAN}INPUT:${NC}"
    echo "  Any text file with one cron schedule per line"
    echo ""
    echo -e "${CYAN}OUTPUT:${NC}"
    echo "  TSV file with two columns:"
    echo "  - job_name: Unique identifier (job00001, job00002, ...)"
    echo "  - cron_schedule: The cron expression"
    echo ""
    echo -e "${CYAN}OUTPUT FILENAME:${NC}"
    echo "  Automatically generated based on input:"
    echo "  - cron_schedule.txt     → cron_schedule.tsv"
    echo "  - cron_schedule_4k.txt  → cron_schedule_4k.tsv"
    echo "  - my_file.txt           → my_file.tsv"
    echo ""
    echo -e "${CYAN}EXAMPLE:${NC}"
    echo "  $ python3 convert.py"
    echo "  Enter input filename (default: cron_schedule.txt): cron_schedule_4k.txt"
    echo "  Output will be saved to: cron_schedule_4k.tsv"
    echo ""
    echo -e "${CYAN}OUTPUT FORMAT:${NC}"
    echo "  job_name    cron_schedule"
    echo "  job00001    */15 * * * 1-5"
    echo "  job00002    */15 0-6 * * *"
    echo "  job00003    */15 3-20 * * 1-5"
    echo "  ..."
    echo ""
}

# Function to display help for test_comparison.py
help_test_comparison() {
    echo -e "${BOLD}${GREEN}PROGRAM: test_comparison.py${NC}"
    echo "================================================================================"
    echo ""
    echo -e "${CYAN}DESCRIPTION:${NC}"
    echo "  Testing utility for comparing validation approaches and debugging cron"
    echo "  schedule parsing logic."
    echo ""
    echo -e "${CYAN}FEATURES:${NC}"
    echo "  ✓ Compares different validation methods"
    echo "  ✓ Tests edge cases and corner scenarios"
    echo "  ✓ Useful for development and debugging"
    echo ""
    echo -e "${CYAN}USAGE:${NC}"
    echo "  python3 test_comparison.py"
    echo ""
    echo -e "${CYAN}PURPOSE:${NC}"
    echo "  Development and testing tool - not typically used in production."
    echo ""
}

# Function to display all programs summary
display_all_programs() {
    display_header
    echo -e "${BOLD}AVAILABLE PROGRAMS:${NC}"
    echo ""

    echo -e "${GREEN}1. cron_schedule.py${NC}"
    echo "   Main validation script with comprehensive statistics"
    echo ""

    echo -e "${GREEN}2. cron_visualizer.py${NC}"
    echo "   Interactive heatmap generator with matplotlib charts"
    echo ""

    echo -e "${GREEN}3. cron_schedule_with_full_validation.py${NC}"
    echo "   Enhanced validator with detailed error messages"
    echo ""

    echo -e "${GREEN}4. convert.py${NC}"
    echo "   Convert cron schedules to TSV format with job names"
    echo ""

    echo -e "${GREEN}5. test_comparison.py${NC}"
    echo "   Testing and comparison utility"
    echo ""

    echo "================================================================================"
    echo ""
    echo -e "${YELLOW}For detailed help on a specific program:${NC}"
    echo "  ./help.sh <program_name>"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./help.sh cron_schedule.py"
    echo "  ./help.sh convert.py"
    echo ""
}

# Main script logic
main() {
    # Check if argument provided
    if [ $# -eq 0 ]; then
        display_all_programs
        exit 0
    fi

    program_name="$1"

    # Route to appropriate help function
    case "$program_name" in
        cron_schedule.py)
            display_header
            help_cron_schedule
            ;;
        cron_visualizer.py)
            display_header
            help_cron_visualizer
            ;;
        cron_schedule_with_full_validation.py)
            display_header
            help_cron_schedule_with_full_validation
            ;;
        convert.py)
            display_header
            help_convert
            ;;
        test_comparison.py)
            display_header
            help_test_comparison
            ;;
        --help|-h|help)
            display_all_programs
            ;;
        *)
            display_header
            echo -e "${RED}ERROR: Unknown program '${program_name}'${NC}"
            echo ""
            display_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
