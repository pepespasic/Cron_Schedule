import re
import sys

# ── Cron entry refinement helpers ──────────────────────────────────────────────

def _strip_leading_zeros(s):
    """Remove leading zeros from a pure-numeric string ('05' → '5')."""
    return str(int(s)) if s.isdigit() else s


def _refine_segment(seg):
    """Apply leading-zero removal to one cron segment (no commas)."""
    seg = seg.strip()
    if seg == '*':
        return '*'
    if '/' in seg:
        base, step = seg.split('/', 1)
        step = _strip_leading_zeros(step)
        if base == '*':
            return f'*/{step}'
        if '-' in base:
            lo, hi = base.split('-', 1)
            return f'{_strip_leading_zeros(lo)}-{_strip_leading_zeros(hi)}/{step}'
        return f'{_strip_leading_zeros(base)}/{step}'
    if '-' in seg:
        lo, hi = seg.split('-', 1)
        return f'{_strip_leading_zeros(lo)}-{_strip_leading_zeros(hi)}'
    return _strip_leading_zeros(seg)


def _segment_sort_key(seg):
    """Numeric start value of a segment, used for ascending comma-list sort."""
    seg = seg.strip()
    if seg == '*' or seg.startswith('*/'):
        return 0
    if '-' in seg:
        return int(seg.split('-')[0])
    base = seg.split('/')[0] if '/' in seg else seg
    return int(base) if base.isdigit() else 0


_FULL_RANGES = {
    0: {'0-59'},        # minute
    1: {'0-23'},        # hour
    2: {'1-31'},        # day of month
    3: {'1-12'},        # month
    4: {'0-6', '1-7'},  # day of week
}


def _refine_field(field_str, field_idx):
    """
    Refine one cron field:
      1. Strip leading zeros from all numeric parts.
      2. Sort comma-separated segments ascending by start value.
      3. Replace full-range expressions with '*'.
    """
    field_str = field_str.strip()
    if field_str == '*':
        return '*'
    if ',' in field_str:
        segs = [_refine_segment(s) for s in field_str.split(',')]
        segs.sort(key=_segment_sort_key)
        result = ','.join(segs)
    else:
        result = _refine_segment(field_str)
    if result in _FULL_RANGES.get(field_idx, set()):
        return '*'
    return result


def refine_cron_entry(entry_str):
    """
    Refine a 5-field cron entry string by applying _refine_field to each field.
    Entries with fewer than 5 fields are returned unchanged.
    """
    parts = entry_str.split()
    if len(parts) < 5:
        return entry_str
    refined = [_refine_field(parts[i], i) for i in range(5)]
    return ' '.join(refined + parts[5:])

# ── End of refinement helpers ──────────────────────────────────────────────────

# Prompt user for input filename
print("=" * 80)
print("CRON SCHEDULE VALIDATOR")
print("=" * 80)
print()

user_input = input("Enter cron schedule filename (default: cron_schedule.txt): ").strip()

# Use default if user just presses Enter
if user_input == "":
    input_filename = "cron_schedule.txt"
    print(f"Using default: {input_filename}")
else:
    input_filename = user_input
    print(f"Using: {input_filename}")

print()

# Check if file exists
try:
    with open(input_filename, 'r') as f:
        cron_schedule = f.readlines()
    print(f"✓ Successfully loaded {len(cron_schedule)} cron schedules from '{input_filename}'")
    print()
except FileNotFoundError:
    print(f"ERROR: File '{input_filename}' not found!")
    print("Please make sure the file exists and try again.")
    sys.exit(1)

MAX_DAYS_IN_MONTH = 31
MAX_MONTH = 12
# Day of week: 0-6 (Sun-Sat) is standard, but many cron implementations also accept 7 for Sunday
MAX_DAYS_IN_WEEK = 7  # 0,7 = Sunday, 1 = Monday, ..., 6 = Saturday
MAX_MINUTES = 59
MAX_HOURS = 23


for i in range(len(cron_schedule)):
    cron_schedule[i] = cron_schedule[i].strip()

# ── Derive output filenames from input filename ────────────────────────────────
_base, _sep, _ext = input_filename.rpartition('.')
if _sep:
    refined_filename    = f"{_base}_refined.{_ext}"
    comparison_filename = f"{_base}_comparison.{_ext}"
else:
    refined_filename    = f"{input_filename}_refined"
    comparison_filename = f"{input_filename}_comparison"

# ── Refine entries and write output files ──────────────────────────────────────
comparison_rows = []
for i in range(len(cron_schedule)):
    original = cron_schedule[i]
    refined  = refine_cron_entry(original)
    cron_schedule[i] = refined
    if refined != original:
        comparison_rows.append((original, refined))

with open(refined_filename, 'w') as f:
    f.write('\n'.join(cron_schedule))
    if cron_schedule:
        f.write('\n')

with open(comparison_filename, 'w') as f:
    f.write('Original\tRefined\n')
    for orig, ref in comparison_rows:
        f.write(f'{orig}\t{ref}\n')

print(f"✓ {len(comparison_rows)} entries refined  → '{refined_filename}'")
print(f"✓ Comparison file saved ({len(comparison_rows)} changed rows) → '{comparison_filename}'")
print()

print("=" * 80)
print(f"COMPARISON PREVIEW — first 10 of {len(comparison_rows)} refined entries")
print("=" * 80)
print(f"  {'Original':<45} Refined")
print("-" * 80)
for i, (orig, ref) in enumerate(comparison_rows[:10]):
    print(f"  {orig:<45} {ref}")
if len(comparison_rows) > 10:
    print(f"  ... and {len(comparison_rows) - 10} more rows in '{comparison_filename}'")
print("=" * 80)
print()

# Sort cron schedule list in ascending order
cron_schedule.sort()

# If key does not exist adds key with default value 0 and increments it by 1. Otherwise, increments existing value by 1.
cron_dict = {}
for element in cron_schedule:
    cron_dict[element] = cron_dict.get(element, 0) + 1

# Print number of elements in the dictionary.
count = len(cron_dict)
print(f"Found {count} unique cron expressions after deduplication (identical lines counted as one).\n")

# Loop through the dictionary and print keys and values
print("=" * 80)
print("DUPLICATE CRON ENTRIES (appearing 100 or more times)")
print("  These are cron expressions that repeat most frequently in the input file.")
print("=" * 80)
print(f"  {'Cron Expression':<60} Count")
print("-" * 80)
high_freq = [(k, v) for k, v in sorted(cron_dict.items(), key=lambda x: x[1], reverse=True) if v >= 100]
for key, value in high_freq[:10]:
    print(f"  {key:<60} {value}")
if len(high_freq) > 10:
    print(f"  ... and {len(high_freq) - 10} more entries not shown")
print("=" * 80)
print()

# Loop through all keys in cron dictionary and split them into a separtate list of substrings and add them to list.
all_cron_substrings = []
for key in cron_dict:
    cron_substrings_list = key.split()
    all_cron_substrings.append(cron_substrings_list)

# Loop through list and print out list of substrings
total = len(all_cron_substrings)
print("=" * 80)
print(f"PARSED CRON FIELDS — first 10 of {total} entries")
print("  Each entry is split into fields: [minute, hour, day_of_month, month, day_of_week]")
print("=" * 80)
for i in range(total):
    if i < 10:
        print(f"  {i + 1:>3}. {all_cron_substrings[i]}")
    else:
        print(f"  ... and {total - 10} more entries not shown")
        break
print("=" * 80)

def matches_pattern(cron_substring: str):
    # Define the possible patterns for a cron substring
    cron_substrings_pattern = [
        r"^\*$",                                    # "*" for every value
        r"^\*/\d+$",                                # "*/n" for step values
        r"^\d+$",                                   # "n" single value
        r"^\d+-\d+$",                               # "n-m" for a range of values
        r"^\d+-\d+/\d+$",                           # "n-m/x" for range with steps
        r"^\d+(?:,\d+)*$",                          # "n,m" for a list of single values
        r"^(?:\d+|\d+-\d+)(?:,(?:\d+|\d+-\d+))*$", # "1-5,10,15-20" or "13-23,00-06" mixed list
    ]
    
    # Loop through the regex patterns and check if there's a match
    for pattern in cron_substrings_pattern:
        if re.match(pattern, cron_substring):  # Using match instead of search for strict matching
            return pattern

    return "Invalid cron pattern"  # Return if no pattern matched

# Leap year check
'''
def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)

# Validate cron field pattern against a range (e.g., 1-31, 1,3,5)

def validate_field(field: str, min_value: int, max_value: int, year: int = None) -> bool:
    if field == "*":
        return True
    if re.match(r"^\d+$", field):
        return min_value <= int(field) <= max_value
    if re.match(r"^\d+-\d+$", field):
        start, end = map(int, field.split('-'))
        return min_value <= start <= end <= max_value
    if re.match(r"^\d+(?:,\d+)*$", field):
        values = map(int, field.split(','))
        return all(min_value <= value <= max_value for value in values)
    if re.match(r"^\*/\d+$", field):
        return int(field.split('/')[1]) <= max_value
    if field == "29" and max_value == 2 and not is_leap_year(year):
        return False  # Special case for February 29th
    return False

# Validate the full cron pattern (day_of_month, month, day_of_week)

def validate_cron_fields(day_of_month: str, month: str, day_of_week: str, test_date: datetime) -> bool:
    return (
        validate_field(day_of_month, 1, MAX_DAYS_IN_MONTH, test_date.year) and
        validate_field(month, 1, MAX_MONTH) and
        validate_field(day_of_week, 0, MAX_DAYS_IN_WEEK)
    )
'''
# Parse cron field and return set of actual values

def parse_cron_field(field_str, min_val, max_val):
    """
    Parse a cron field and return set of matching values.

    Args:
        field_str: Cron field string (e.g., "*/15", "1-5", "1,3,5", "*")
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Set of integers matching the pattern, or None if invalid

    Examples:
        parse_cron_field("*/15", 0, 59) -> {0, 15, 30, 45}
        parse_cron_field("1-5", 0, 23) -> {1, 2, 3, 4, 5}
        parse_cron_field("1,3,5", 0, 59) -> {1, 3, 5}
        parse_cron_field("*", 0, 23) -> {0, 1, 2, ..., 23}
    """
    field_str = field_str.strip()
    result = set()

    # Handle asterisk (all values)
    if field_str == '*':
        return set(range(min_val, max_val + 1))

    # List of values (e.g. 1,3,5 or 1-5,10,15-20) - CHECK COMMA FIRST!
    if ',' in field_str:
        parts = field_str.split(',')
        for part in parts:
            part = part.strip()
            # Recursively parse each part
            parsed = parse_cron_field(part, min_val, max_val)
            if parsed is None:
                return None
            result.update(parsed)
        return result

    # Step pattern (e.g. */5 or 1-10/2)
    if '/' in field_str:
        base, step = field_str.split('/')
        if not step.strip().isdigit():
            return None
        step = int(step)

        if base.strip() == '*':
            # */n pattern: start from min_val and increment by step
            return set(range(min_val, max_val + 1, step))
        elif '-' in base:
            # Range with step (e.g., 1-10/2)
            start, end = map(int, base.split('-'))
            if not (min_val <= start <= max_val and min_val <= end <= max_val):
                return None
            return set(range(start, end + 1, step))
        else:
            # Single value with step (less common)
            if not base.strip().isdigit():
                return None
            val = int(base)
            if min_val <= val <= max_val:
                return {val}
            return None

    # Range pattern (e.g. 1-10)
    if '-' in field_str:
        parts = field_str.split('-')
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            return None
        start, end = map(int, parts)
        if not (min_val <= start <= max_val and min_val <= end <= max_val):
            return None
        return set(range(start, end + 1))

    # Single value
    if field_str.isdigit():
        val = int(field_str)
        if min_val <= val <= max_val:
            return {val}
        return None

    return None  # Not recognized


def is_cron_field_in_range(field_str, min_val, max_val):
    """
    Validate that a cron field is within valid range.

    Args:
        field_str: Cron field string
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid, False otherwise
    """
    result = parse_cron_field(field_str, min_val, max_val)
    return result is not None


def validate_last_3_cron_fields(entry):
    """
    Validate that the last 3 cron fields (day_of_month, month, day_of_week) are in range.

    Args:
        entry: List of cron fields

    Returns:
        True if all last 3 fields are valid, False otherwise
    """
    if len(entry) < 5:
        raise ValueError("Entry must have 5 fields")

    checks = [
        (entry[2], 1, 31),  # Day of month
        (entry[3], 1, 12),  # Month
        (entry[4], 0, 6),   # Day of week
    ]

    for field, min_val, max_val in checks:
        if not is_cron_field_in_range(field, min_val, max_val):
            return False

    return True


def validate_all_cron_fields(entry):
    """
    Validate all 5 cron fields (minute, hour, day_of_month, month, day_of_week).

    Args:
        entry: List of cron fields

    Returns:
        True if all fields are valid, False otherwise
    """
    if len(entry) < 5:
        return False

    checks = [
        (entry[0], 0, MAX_MINUTES),      # Minute
        (entry[1], 0, MAX_HOURS),        # Hour
        (entry[2], 1, MAX_DAYS_IN_MONTH),  # Day of month
        (entry[3], 1, MAX_MONTH),        # Month
        (entry[4], 0, MAX_DAYS_IN_WEEK), # Day of week
    ]

    for field, min_val, max_val in checks:
        if not is_cron_field_in_range(field, min_val, max_val):
            return False

    return True

# Generate list of validated minute and hour substrings from cron schedule

min_hour_list = []
validation_stats = {
    'total_entries': 0,
    'invalid_field_count': 0,
    'invalid_pattern': 0,
    'invalid_range': 0,
    'valid_entries': 0
}

# Lists to store invalid entries with their reasons
invalid_pattern_entries = []
invalid_range_entries = []
invalid_field_count_entries = []

print()

def generate_unique_substrings(cron_list):
    """
    Extracts minute and hour fields from cron entries after validating:
    - Entry has at least 5 fields
    - All fields match valid cron pattern syntax
    - All 5 fields (minute, hour, day_of_month, month, day_of_week) are in valid ranges

    Updates global validation_stats dictionary with statistics about validation results.

    Args:
        cron_list: List of cron entries (each entry is a list of fields)

    Returns:
        None (updates global min_hour_list and validation_stats)
    """
    for i in range(len(cron_list)):
        entry = cron_list[i]
        validation_stats['total_entries'] += 1

        # Skip if entry doesn't have at least 5 fields
        if len(entry) < 5:
            validation_stats['invalid_field_count'] += 1
            invalid_field_count_entries.append(' '.join(entry))
            continue

        # Validate each field has a valid cron pattern
        is_valid_pattern = True
        invalid_field_index = -1
        for idx, field in enumerate(entry[:5]):  # Check first 5 fields (min, hour, day_of_month, month, day_of_week)
            if matches_pattern(field.strip()) == "Invalid cron pattern":
                is_valid_pattern = False
                invalid_field_index = idx
                break

        if not is_valid_pattern:
            validation_stats['invalid_pattern'] += 1
            invalid_pattern_entries.append({
                'entry': ' '.join(entry),
                'invalid_field': entry[invalid_field_index] if invalid_field_index >= 0 else 'unknown',
                'field_index': invalid_field_index
            })
            continue

        # Validate all 5 fields are in range
        if not validate_all_cron_fields(entry):
            validation_stats['invalid_range'] += 1
            invalid_range_entries.append(' '.join(entry))
            continue

        # If all validations pass, add min and hour to list
        validation_stats['valid_entries'] += 1
        entry[0] = entry[0].strip()
        entry[1] = entry[1].strip()
        min_hour_list.append([entry[0], entry[1]])

generate_unique_substrings(all_cron_substrings)


def count_min_hour_combinations():
    """
    Count occurrences of each unique [minute, hour] combination.

    Returns:
        Dictionary with [minute, hour] tuple as key and count as value
    """
    min_hour_count = {}
    for min_hour in min_hour_list:
        key = tuple(min_hour)  # Convert list to tuple so it can be used as dict key
        min_hour_count[key] = min_hour_count.get(key, 0) + 1
    return min_hour_count


def display_validation_statistics():
    """
    Display statistics about cron validation results.
    """
    print("=" * 80)
    print("CRON VALIDATION STATISTICS")
    print("=" * 80)
    print(f"Total entries processed:        {validation_stats['total_entries']}")
    print(f"Valid entries:                  {validation_stats['valid_entries']}")
    print(f"Invalid entries (field count):  {validation_stats['invalid_field_count']}")
    print(f"Invalid entries (pattern):      {validation_stats['invalid_pattern']}")
    print(f"Invalid entries (range):        {validation_stats['invalid_range']}")

    total_invalid = (validation_stats['invalid_field_count'] +
                     validation_stats['invalid_pattern'] +
                     validation_stats['invalid_range'])

    if validation_stats['total_entries'] > 0:
        valid_percent = (validation_stats['valid_entries'] / validation_stats['total_entries']) * 100
        print(f"Validation success rate:        {valid_percent:.2f}%")
    print("=" * 80)
    print()


def display_min_hour_combinations(limit=50):
    """
    Display minute/hour combinations in a formatted way.

    Args:
        limit: Maximum number of combinations to display (default: 50)
    """
    min_hour_count = count_min_hour_combinations()

    print("=" * 80)
    print("UNIQUE MINUTE/HOUR COMBINATIONS")
    print("=" * 80)
    print(f"Total unique combinations: {len(min_hour_count)}")
    print(f"Total minute/hour entries: {len(min_hour_list)}")
    print()

    # Sort by count (descending) then by minute and hour
    sorted_combinations = sorted(min_hour_count.items(),
                                 key=lambda x: (-x[1], x[0][0], x[0][1]))

    print(f"{'Minute':<10} {'Hour':<10} {'Count':<10}")
    print("-" * 80)

    for i, ((minute, hour), count) in enumerate(sorted_combinations):
        if i >= limit:
            remaining = len(sorted_combinations) - limit
            print(f"\n... and {remaining} more combinations")
            break
        print(f"{minute:<10} {hour:<10} {count:<10}")

    print("=" * 80)
    print()


def display_invalid_entries():
    """
    Display all invalid entries with details about why they failed validation.
    """
    print("=" * 80)
    print("INVALID ENTRIES DETAILS")
    print("=" * 80)
    print()

    no_invalid = not invalid_field_count_entries and not invalid_pattern_entries and not invalid_range_entries

    if no_invalid:
        print("  ✓ No invalid entries found. All cron expressions passed validation.")
    else:
        # Display invalid field count entries
        if invalid_field_count_entries:
            print(f"INVALID FIELD COUNT ({len(invalid_field_count_entries)} entries):")
            print("-" * 80)
            for entry in invalid_field_count_entries:
                print(f"  {entry}")
            print()

        # Display invalid pattern entries
        if invalid_pattern_entries:
            print(f"INVALID PATTERN ({len(invalid_pattern_entries)} entries):")
            print("-" * 80)
            field_names = ['minute', 'hour', 'day_of_month', 'month', 'day_of_week']
            for item in invalid_pattern_entries:
                field_name = field_names[item['field_index']] if item['field_index'] < len(field_names) else 'unknown'
                print(f"  Entry: {item['entry']}")
                print(f"  Invalid field: '{item['invalid_field']}' (position: {item['field_index']}, {field_name})")
                print()

        # Display invalid range entries
        if invalid_range_entries:
            print(f"INVALID RANGE ({len(invalid_range_entries)} entries):")
            print("-" * 80)
            for entry in invalid_range_entries:
                print(f"  {entry}")
            print()

    print("=" * 80)
    print()


# Display validation statistics
display_validation_statistics()

# Display minute/hour combinations
display_min_hour_combinations(limit=10)

# Display invalid entries
display_invalid_entries()


