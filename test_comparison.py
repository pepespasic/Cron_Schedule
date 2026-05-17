"""
Side-by-side comparison of ORIGINAL vs IMPROVED validation functions
This demonstrates the bug fix for comma-separated ranges
"""

import re

# ========== ORIGINAL VERSION (WITH BUG) ==========

def is_cron_field_in_range_ORIGINAL(field_str, min_val, max_val):
    """Your original implementation"""
    field_str = field_str.strip()

    if field_str == '*':
        return True

    # Step pattern (e.g. */5 or 1-10/2)
    if '/' in field_str:
        base, step = field_str.split('/')
        if not step.strip().isdigit():
            return False
        return is_cron_field_in_range_ORIGINAL(base.strip(), min_val, max_val)

    # Range pattern (e.g. 1-10)
    if '-' in field_str:
        parts = field_str.split('-')
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            return False
        start, end = map(int, parts)
        return min_val <= start <= max_val and min_val <= end <= max_val

    # List of values (e.g. 1,3,5)
    # ❌ BUG: This checks before recursing, so "13-23" fails isdigit()
    if ',' in field_str:
        values = field_str.split(',')
        for val in values:
            val = val.strip()
            if not val.isdigit():  # ❌ THIS IS THE BUG
                return False
            if not (min_val <= int(val) <= max_val):
                return False
        return True

    # Single value
    if field_str.isdigit():
        val = int(field_str)
        return min_val <= val <= max_val

    return False


# ========== IMPROVED VERSION (BUG FIXED) ==========

def is_cron_field_in_range_IMPROVED(field_str, min_val, max_val):
    """Improved implementation with comma handling fix"""
    field_str = field_str.strip()

    if field_str == '*':
        return True

    # ✅ FIX: Check comma lists FIRST, before checking ranges
    if ',' in field_str:
        parts = field_str.split(',')
        for part in parts:
            part = part.strip()
            # Recursively validate each part
            if not is_cron_field_in_range_IMPROVED(part, min_val, max_val):
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
        return is_cron_field_in_range_IMPROVED(base.strip(), min_val, max_val)

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


# ========== TEST CASES ==========

print("=" * 70)
print("COMPARISON: ORIGINAL vs IMPROVED")
print("=" * 70)

test_cases = [
    # (pattern, min, max, description)
    ("*", 0, 23, "Wildcard"),
    ("5", 0, 23, "Single value"),
    ("1-10", 0, 23, "Simple range"),
    ("*/15", 0, 59, "Step from wildcard"),
    ("1,3,5", 0, 23, "List of single values"),
    ("13-23,00-06", 0, 23, "🔴 BUG TEST: Combined ranges"),
    ("1-5,10-15,20", 1, 31, "🔴 BUG TEST: Mixed list"),
    ("*/100", 0, 59, "🟡 Invalid step (too large)"),
]

print(f"\n{'Pattern':<20} {'Expected':<10} {'Original':<10} {'Improved':<10} {'Status'}")
print("-" * 70)

for pattern, min_v, max_v, description in test_cases:
    # Determine expected result
    if "Invalid" in description:
        expected = False
    else:
        expected = True

    original_result = is_cron_field_in_range_ORIGINAL(pattern, min_v, max_v)
    improved_result = is_cron_field_in_range_IMPROVED(pattern, min_v, max_v)

    # Check if results match expected
    original_status = "✓" if original_result == expected else "✗"
    improved_status = "✓" if improved_result == expected else "✗"

    # Overall status
    if original_result == improved_result == expected:
        status = "✓ Both correct"
    elif original_result != expected and improved_result == expected:
        status = "🔧 FIXED!"
    elif original_result == expected and improved_result != expected:
        status = "⚠️ Regression"
    else:
        status = "✗ Both wrong"

    print(f"{pattern:<20} {str(expected):<10} "
          f"{original_status} {str(original_result):<8} "
          f"{improved_status} {str(improved_result):<8} "
          f"{status}")

print("\n" + "=" * 70)
print("DETAILED ANALYSIS OF BUG")
print("=" * 70)

print("\nTest: '13-23,00-06'")
print("-" * 40)

test_input = "13-23,00-06"
print(f"Input: {test_input}")
print(f"Split by comma: {test_input.split(',')}")
print()

print("ORIGINAL VERSION:")
print("  1. Splits: ['13-23', '00-06']")
print("  2. Checks if '13-23'.isdigit() → False")
print("  3. Returns False (INCORRECT)")
print()

print("IMPROVED VERSION:")
print("  1. Splits: ['13-23', '00-06']")
print("  2. Recursively calls is_cron_field_in_range('13-23', 0, 23)")
print("     → Matches range pattern, validates 13-23")
print("  3. Recursively calls is_cron_field_in_range('00-06', 0, 23)")
print("     → Matches range pattern, validates 00-06")
print("  4. Returns True (CORRECT)")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
The bug was in the ORDER of pattern checking:

ORIGINAL (buggy):
  if '-' in field_str:     # Checks range
  if ',' in field_str:     # Then checks list (but expects isdigit!)

IMPROVED (fixed):
  if ',' in field_str:     # Checks list FIRST
      # Recursively validates each part
  if '-' in field_str:     # Then checks range

Key insight: Comma-separated lists can CONTAIN ranges,
so we must split by comma first and recursively validate each part.
""")
