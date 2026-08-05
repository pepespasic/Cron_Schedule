#!/Library/Developer/CommandLineTools/usr/bin/python3
"""
Cron Schedule Visualizer
Displays cron schedules as a 2D array where:
- Columns represent hours (0-23)
- Rows represent minutes (0-59)
"""

import re
import csv
from datetime import datetime
from typing import List, Set, Tuple
import matplotlib.pyplot as plt
import numpy as np


class CronParser:
    """Parser for cron expressions."""

    @staticmethod
    def parse_field(field: str, min_val: int, max_val: int) -> Set[int]:
        """
        Parse a single cron field and return set of matching values.

        Args:
            field: Cron field string (e.g., "*/15", "1-5", "1,3,5", "*", "13-23,00-06")
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Set of integers matching the cron pattern
        """
        field = field.strip()
        result = set()

        # Handle asterisk (all values)
        if field == '*':
            return set(range(min_val, max_val + 1))

        # Handle list (must check before range because it may contain ranges)
        # e.g., "1,3,5" or "13-23,00-06"
        if ',' in field:
            for part in field.split(','):
                part = part.strip()
                # Recursively parse each part
                result.update(CronParser.parse_field(part, min_val, max_val))
            return result

        # Handle step values (e.g., */15 or 1-10/2 or 7-59/15)
        if '/' in field:
            base, step = field.split('/', 1)
            step = int(step)

            if base == '*':
                result = set(range(min_val, max_val + 1, step))
            elif '-' in base:
                start, end = map(int, base.split('-', 1))
                result = set(range(start, end + 1, step))
            else:
                result = set(range(int(base), max_val + 1, step))

            return result

        # Handle range (e.g., 1-10 or 00-06)
        if '-' in field:
            start, end = map(int, field.split('-', 1))
            return set(range(start, end + 1))

        # Handle single value
        num = int(field)
        if min_val <= num <= max_val:
            return {num}

        return result

    @staticmethod
    def parse_cron(cron_line: str, target_date: datetime) -> List[Tuple[int, int]]:
        """
        Parse a cron expression and return list of (minute, hour) tuples
        that match the target date.

        Args:
            cron_line: Cron expression (e.g., "*/15 * * * *")
            target_date: Date to check against

        Returns:
            List of (minute, hour) tuples that match
        """
        try:
            parts = cron_line.strip().split()

            if len(parts) < 5:
                return []

            minute_field, hour_field, day_field, month_field, weekday_field = parts[:5]

            # Skip invalid entries
            if 'None' in cron_line or not all(parts[:5]):
                return []

            # Check if date matches day/month/weekday criteria
            months = CronParser.parse_field(month_field, 1, 12)
            if target_date.month not in months:
                return []

            # Convert Python weekday (0=Monday) to cron weekday (0=Sunday)
            target_weekday = (target_date.weekday() + 1) % 7

            # Cron day/weekday matching logic:
            # - If both are *, always match
            # - If day is * and weekday is specific, match only if weekday matches
            # - If day is specific and weekday is *, match only if day matches
            # - If both are specific, match if either matches (OR logic)

            day_is_wildcard = day_field == '*'
            weekday_is_wildcard = weekday_field == '*'

            if day_is_wildcard and weekday_is_wildcard:
                # Both wildcards - always match
                pass
            elif day_is_wildcard and not weekday_is_wildcard:
                # Only check weekday
                weekdays = CronParser.parse_field(weekday_field, 0, 6)
                if target_weekday not in weekdays:
                    return []
            elif not day_is_wildcard and weekday_is_wildcard:
                # Only check day of month
                days = CronParser.parse_field(day_field, 1, 31)
                if target_date.day not in days:
                    return []
            else:
                # Both are specific - OR logic (either can match)
                days = CronParser.parse_field(day_field, 1, 31)
                weekdays = CronParser.parse_field(weekday_field, 0, 6)
                day_matches = target_date.day in days
                weekday_matches = target_weekday in weekdays
                if not (day_matches or weekday_matches):
                    return []

            # Parse minutes and hours
            minutes = CronParser.parse_field(minute_field, 0, 59)
            hours = CronParser.parse_field(hour_field, 0, 23)

            # Generate all combinations
            result = []
            for hour in sorted(hours):
                for minute in sorted(minutes):
                    result.append((minute, hour))

            return result
        except Exception:
            return []


class CronVisualizer:
    """Visualizes cron schedules as a 2D array."""

    def __init__(self):
        self.cron_schedules: List[str] = []

    def load_from_file(self, filename: str) -> int:
        """Load cron schedules from file."""
        try:
            with open(filename, 'r') as f:
                self.cron_schedules = [line.strip() for line in f if line.strip()]
            return len(self.cron_schedules)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return 0
        except Exception as e:
            print(f"Error loading file: {e}")
            return 0

    def generate_grid(self, target_date: datetime) -> List[List[int]]:
        """
        Generate a 2D grid where grid[minute][hour] = count of matching cron jobs.

        Returns:
            2D array: 60 rows (minutes) × 24 columns (hours)
        """
        # Initialize 60x24 grid with zeros
        grid = [[0 for _ in range(24)] for _ in range(60)]

        # Parse each cron schedule
        for cron_line in self.cron_schedules:
            matches = CronParser.parse_cron(cron_line, target_date)
            for minute, hour in matches:
                grid[minute][hour] += 1

        return grid

    def write_grid_to_file(self, grid: List[List[int]], target_date: datetime, filename: str):
        """Write the grid to a tab-delimited file without headers."""
        try:
            with open(filename, 'w') as f:
                for minute in range(60):
                    row_values = []
                    for hour in range(24):
                        row_values.append(str(grid[minute][hour]))
                    f.write('\t'.join(row_values) + '\n')
            print(f"Output written to: {filename}")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def display_grid(self, grid: List[List[int]], target_date: datetime):
        """Display the grid in a formatted way."""
        print(f"\nCron Schedule Visualization for {target_date.strftime('%Y-%m-%d')}")
        print(f"Total schedules loaded: {len(self.cron_schedules)}")

        # Find maximum value in grid to determine column width
        max_value = max(max(row) for row in grid)
        col_width = len(str(max_value)) + 1  # +1 for spacing

        # Calculate total width for separator
        header_width = 4 + (col_width * 24)  # "Min |" is 4 chars + 24 columns
        print("=" * header_width)

        # Header with hours
        print("Min |", end="")
        for hour in range(24):
            print(f"{hour:>{col_width}d}", end="")
        print()
        print("-" * header_width)

        # Print each minute row
        for minute in range(60):
            print(f"{minute:3d} |", end="")
            for hour in range(24):
                count = grid[minute][hour]
                if count > 0:
                    print(f"{count:>{col_width}d}", end="")
                else:
                    print(f"{'.':{col_width}}", end="")
            print()

    def get_statistics(self, grid: List[List[int]]) -> dict:
        """Get statistics about the schedule."""
        total_executions = sum(sum(row) for row in grid)
        max_concurrent = max(max(row) for row in grid)
        active_slots = sum(1 for row in grid for val in row if val > 0)

        return {
            'total_executions': total_executions,
            'max_concurrent': max_concurrent,
            'active_slots': active_slots,
            'total_slots': 60 * 24
        }

    def write_grid_to_csv(self, grid: List[List[int]], target_date: datetime, filename: str):
        """
        Write the grid to a CSV file (2D array without row/column headers).

        Args:
            grid: 2D array (60 rows × 24 columns)
            target_date: Date for filename
            filename: Output CSV filename
        """
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                for minute in range(60):
                    row_values = [grid[minute][hour] for hour in range(24)]
                    writer.writerow(row_values)
            print(f"CSV file written to: {filename}")
        except Exception as e:
            print(f"Error writing CSV file: {e}")

    def generate_heatmap(self, csv_filename: str, target_date: datetime, output_filename: str = None):
        """
        Generate a heatmap chart from CSV file using matplotlib.

        Args:
            csv_filename: Path to the CSV file containing execution data
            target_date: Date for chart title
            output_filename: Optional filename to save the chart (default: heatmap_YYYY-MM-DD.png)
        """
        try:
            # Read CSV file
            data = []
            with open(csv_filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append([int(val) for val in row])

            # Convert to numpy array
            grid_array = np.array(data)

            # Create figure and axis
            fig, ax = plt.subplots(figsize=(14, 10))

            # Create heatmap using 'RdYlGn_r' colormap (Red-Yellow-Green reversed)
            im = ax.imshow(grid_array, cmap='RdYlGn_r', aspect='auto', interpolation='nearest')

            # Set ticks and labels
            ax.set_xticks(np.arange(24))
            ax.set_yticks(np.arange(0, 60, 5))  # Show every 5 minutes
            ax.set_xticklabels(np.arange(24))
            ax.set_yticklabels(np.arange(0, 60, 5))

            # Labels and title
            ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
            ax.set_ylabel('Minute', fontsize=12, fontweight='bold')
            ax.set_title(f'Cron Job Execution Heatmap - {target_date.strftime("%Y-%m-%d")}',
                        fontsize=14, fontweight='bold', pad=20)

            # Add colorbar at the bottom
            cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.08, aspect=40)
            cbar.set_label('Number of Cron Jobs', fontsize=11, fontweight='bold')

            # Grid for better readability
            ax.set_xticks(np.arange(24) - 0.5, minor=True)
            ax.set_yticks(np.arange(60) - 0.5, minor=True)
            ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)

            # Add text annotations (numbers) in each cell
            # Only show numbers for non-zero values to avoid clutter
            for i in range(60):
                for j in range(24):
                    value = grid_array[i, j]
                    if value > 0:  # Only show non-zero values
                        # Choose text color based on value (white for dark cells, black for light cells)
                        text_color = 'white' if value > grid_array.max() / 2 else 'black'
                        text = ax.text(j, i, str(value),
                                     ha="center", va="center",
                                     color=text_color, fontsize=6, fontweight='bold')

            # Tight layout
            plt.tight_layout()

            # Save or show
            if output_filename is None:
                output_filename = f"heatmap_{target_date.strftime('%Y-%m-%d')}.png"

            plt.savefig(output_filename, dpi=300, bbox_inches='tight')
            print(f"Heatmap saved to: {output_filename}")

            # Also display the plot
            plt.show()

        except FileNotFoundError:
            print(f"Error: CSV file '{csv_filename}' not found.")
        except Exception as e:
            print(f"Error generating heatmap: {e}")


def main():
    """Main interactive loop."""
    visualizer = CronVisualizer()

    print("=" * 100)
    print("CRON SCHEDULE VISUALIZER")
    print("=" * 100)

    # Load cron schedules
    filename = input("Enter cron schedule filename (default: cron_schedule.txt): ").strip()
    if not filename:
        filename = "cron_schedule.txt"

    count = visualizer.load_from_file(filename)
    if count == 0:
        print("No schedules loaded. Exiting.")
        return

    print(f"Successfully loaded {count} cron schedules.")
    print("\nEnter a date to visualize the cron schedule.")
    print("Type 'x' or 'exit' to quit.\n")

    while True:
        # Get user input
        date_input = input("Enter date (YYYY-MM-DD) or 'today' [x/exit to quit]: ").strip()

        # Check for exit
        if date_input.lower() in ['x', 'exit']:
            print("Goodbye!")
            break

        # Parse date
        try:
            if date_input.lower() == 'today' or not date_input:
                target_date = datetime.now()
            else:
                target_date = datetime.strptime(date_input, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
            continue

        # Generate and display grid
        grid = visualizer.generate_grid(target_date)
        visualizer.display_grid(grid, target_date)

        # Write grid to tab-delimited file
        output_filename = f"cron_output_{target_date.strftime('%Y-%m-%d')}.txt"
        visualizer.write_grid_to_file(grid, target_date, output_filename)

        # Write grid to CSV file (without headers)
        csv_filename = f"execution_map_{target_date.strftime('%Y-%m-%d')}.csv"
        visualizer.write_grid_to_csv(grid, target_date, csv_filename)

        # Show statistics
        stats = visualizer.get_statistics(grid)
        print(f"\nStatistics:")
        print(f"  Total executions in day: {stats['total_executions']}")
        print(f"  Max concurrent jobs in any slot: {stats['max_concurrent']}")
        print(f"  Active time slots: {stats['active_slots']} / {stats['total_slots']}")
        print(f"  Coverage: {stats['active_slots'] / stats['total_slots'] * 100:.2f}%")
        print()

        # Ask user if they want to generate a heatmap
        generate_chart = input("Generate heatmap chart? (y/n) [default: y]: ").strip().lower()
        if generate_chart in ['', 'y', 'yes']:
            visualizer.generate_heatmap(csv_filename, target_date)
        print()


if __name__ == "__main__":
    main()
