import re

# Read file and save in an object:
with open("cron_schedule.txt", 'r') as f:
    cron_schedule = f.readlines()

MAX_DAYS_IN_MONTH = 31
MAX_MONTH = 12
# Day of week: 0-6 (Sun-Sat) is standard, but many cron implementations also accept 7 for Sunday
MAX_DAYS_IN_WEEK = 7  # 0,7 = Sunday, 1 = Monday, ..., 6 = Saturday


for i in range(len(cron_schedule)):
    cron_schedule[i] = cron_schedule[i].strip()

# Sort cron schedule list in ascending order
cron_schedule.sort()

# If key does not exist adds key with default value 0 and increments it by 1. Otherwise, increments existing value by 1.
cron_dict = {}
for element in cron_schedule:
    cron_dict[element] = cron_dict.get(element, 0) + 1

# Print number of elements in the dictionary.
count = len(cron_dict)
print(f"Dictionary has {count} elements.\n")

# Loop through the dictionary and print keys and values
for key, value in cron_dict.items():
    if value >= 100:
        print(f"{key} {value}")

# Loop through all keys in cron dictionary and split them into a separtate list of substrings and add them to list.
all_cron_substrings = []
for key in cron_dict:
    cron_substrings_list = key.split()
    all_cron_substrings.append(cron_substrings_list)

# Loop through list and print out list of substrings
for i in range(len(all_cron_substrings)):
    if i < 50:
        print(f"{all_cron_substrings[i]}\n")
    else:
        break


def matches_pattern(cron_substring: str):
    """
    Validate cron field pattern.
    Returns the matching pattern or "Invalid cron pattern".
    """
    cron_substrings_pattern = [
        r"^\*$",                                    # "*" for every value
        r"^\*/\d+$",                                # "*/n" for step values
        r"^\d+$",                                   # "n" single value
        r"^\d+-\d+$",                               # "n-m" for a range
        r"^\d+-\d+/\d+$",                           # "n-m/x" for range with steps
        r"^\d+(?:,\d+)*$",                          # "n,m" list of single values
        r"^(?:\d+|\d+-\d+)(?:,(?:\d+|\d+-\d+))*$", # "13-23,00-06" mixed list
    ]

    # Loop through the regex patterns and check if there's a match
    for pattern in cron_substrings_pattern:
        if re.match(pattern, cron_substring):
            return pattern

    return "Invalid cron pattern"


def is_cron_field_in_range(field_str, min_val, max_val):
    """
    Validate a cron field and check if all values are within range.
    Handles: *, */n, n, n-m, n-m/x, n,m,p, and mixed lists.
    """
    field_str = field_str.strip()

    if field_str == '*':
        return True

    # Check comma lists FIRST (before checking ranges)
    if ',' in field_str:
        parts = field_str.split(',')
        for part in parts:
            part = part.strip()
            if not is_cron_field_in_range(part, min_val, max_val):
                return False
        return True

    # Step pattern (e.g. */5 or 1-10/2)
    if '/' in field_str:
        base, step = field_str.split('/', 1)
        if not step.strip().isdigit():
            return False

        step_val = int(step.strip())
        if step_val <= 0 or step_val > (max_val - min_val + 1):
            return False

        return is_cron_field_in_range(base.strip(), min_val, max_val)

    # Range pattern (e.g. 1-10)
    if '-' in field_str:
        parts = field_str.split('-', 1)
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            return False
        start, end = int(parts[0].strip()), int(parts[1].strip())
        return min_val <= start <= max_val and min_val <= end <= max_val

    # Single value
    if field_str.isdigit():
        val = int(field_str)
        return min_val <= val <= max_val

    return False


# ==============================================================================
# IMPROVED VALIDATION FUNCTIONS
# ==============================================================================

def validate_complete_cron_entry(entry_string):
    """
    Validate a complete cron schedule entry (all 5 fields).

    Args:
        entry_string: String like "*/15 * * * 1-5"

    Returns:
        tuple: (is_valid, error_message)
               (True, "") if valid
               (False, "reason") if invalid
    """
    # Split into fields
    parts = entry_string.strip().split()

    # Check field count
    if len(parts) < 5:
        return False, f"Not enough fields: expected 5, got {len(parts)}"

    if len(parts) > 5:
        # Some cron entries have 6+ fields (with command), we only validate first 5
        parts = parts[:5]

    # Check for invalid content
    if 'None' in entry_string:
        return False, "Contains invalid 'None' value"

    # Field definitions: (value, min, max, name)
    field_defs = [
        (parts[0], 0, 59, "minute"),
        (parts[1], 0, 23, "hour"),
        (parts[2], 1, 31, "day of month"),
        (parts[3], 1, 12, "month"),
        (parts[4], 0, 7, "day of week"),  # 0-7 allowed (0 and 7 both = Sunday)
    ]

    # Validate each field
    for field_value, min_val, max_val, field_name in field_defs:
        # Check pattern validity first
        pattern = matches_pattern(field_value)
        if pattern == "Invalid cron pattern":
            return False, f"Invalid pattern in {field_name}: '{field_value}'"

        # Check range validity
        if not is_cron_field_in_range(field_value, min_val, max_val):
            return False, f"Out of range in {field_name}: '{field_value}' (valid: {min_val}-{max_val})"

    return True, ""


def validate_last_3_cron_fields(entry):
    """
    Validate only the last 3 fields (day, month, weekday).

    Args:
        entry: List of cron fields like ['*/15', '*', '*', '*', '1-5']

    Returns:
        bool: True if valid, False otherwise
    """
    if len(entry) < 5:
        return False

    checks = [
        (entry[2], 1, 31),  # Day of month
        (entry[3], 1, 12),  # Month
        (entry[4], 0, 7),   # Day of week (0-7, where 0 and 7 both = Sunday)
    ]

    for field, min_val, max_val in checks:
        if not is_cron_field_in_range(field, min_val, max_val):
            return False

    return True


def is_valid_cron_schedule(cron_string):
    """
    Quick validation check for a cron schedule string.

    Args:
        cron_string: String like "*/15 * * * 1-5"

    Returns:
        bool: True if valid, False otherwise
    """
    is_valid, _ = validate_complete_cron_entry(cron_string)
    return is_valid


def extract_validated_min_hour_pairs(cron_list):
    """
    Extract minute and hour fields from cron entries ONLY if they're valid.

    Args:
        cron_list: List of lists like [['*/15', '*', '*', '*', '1-5'], ...]

    Returns:
        tuple: (valid_pairs, stats_dict, invalid_entries)
               valid_pairs: List of [minute, hour] pairs that passed validation
               stats_dict: Statistics about validation results
               invalid_entries: List of (entry, error_message) tuples
    """
    valid_pairs = []
    invalid_entries = []
    stats = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'too_few_fields': 0,
        'invalid_patterns': 0,
        'out_of_range': 0,
    }

    for entry in cron_list:
        stats['total'] += 1

        # Check if entry has enough fields
        if len(entry) < 5:
            stats['too_few_fields'] += 1
            stats['invalid'] += 1
            invalid_entries.append((entry, f"Only {len(entry)} fields"))
            continue

        # Reconstruct the full cron string for validation
        cron_string = ' '.join(entry[:5])

        # Validate the complete entry
        is_valid, error_msg = validate_complete_cron_entry(cron_string)

        if is_valid:
            # Extract and add minute/hour pair
            minute_field = entry[0].strip()
            hour_field = entry[1].strip()
            valid_pairs.append([minute_field, hour_field])
            stats['valid'] += 1
        else:
            stats['invalid'] += 1
            if 'pattern' in error_msg.lower():
                stats['invalid_patterns'] += 1
            elif 'range' in error_msg.lower():
                stats['out_of_range'] += 1
            invalid_entries.append((entry, error_msg))

    return valid_pairs, stats, invalid_entries


# ==============================================================================
# IMPROVED PROCESSING WITH VALIDATION
# ==============================================================================

print("\n" + "="*70)
print("PROCESSING CRON ENTRIES WITH VALIDATION")
print("="*70)

min_hour_list, validation_stats, invalid_list = extract_validated_min_hour_pairs(all_cron_substrings)

# Print statistics
print(f"\nValidation Statistics:")
print(f"  Total entries:        {validation_stats['total']}")
print(f"  ✓ Valid entries:      {validation_stats['valid']}")
print(f"  ✗ Invalid entries:    {validation_stats['invalid']}")
if validation_stats['invalid'] > 0:
    print(f"    - Too few fields:   {validation_stats['too_few_fields']}")
    print(f"    - Invalid patterns: {validation_stats['invalid_patterns']}")
    print(f"    - Out of range:     {validation_stats['out_of_range']}")

if validation_stats['total'] > 0:
    success_rate = validation_stats['valid']/validation_stats['total']*100
    print(f"\nSuccess rate: {success_rate:.2f}%")

# Show some invalid entries (if any)
if invalid_list:
    print(f"\n{'='*70}")
    print(f"SAMPLE INVALID ENTRIES (showing first 10):")
    print(f"{'='*70}")
    for i, (entry, error) in enumerate(invalid_list[:10]):
        entry_str = ' '.join(entry) if len(entry) > 0 else '(empty)'
        print(f"{i+1}. {entry_str}")
        print(f"   Error: {error}\n")

# Print sample of valid entries
print(f"\n{'='*70}")
print(f"SAMPLE VALID MINUTE/HOUR PAIRS (showing first 20):")
print(f"{'='*70}")
for i in range(min(20, len(min_hour_list))):
    print(f"{i+1}. Minute: {min_hour_list[i][0]:20s} Hour: {min_hour_list[i][1]}")

print(f"\n{'='*70}")
print(f"Total valid minute/hour pairs: {len(min_hour_list)}")
print(f"{'='*70}\n")
