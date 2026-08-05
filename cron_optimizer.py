#!/usr/bin/env python3
"""
Cron Optimizer
Applies two optimizations to reduce minute-0 load spikes:

1. Periodic patterns (*/N where N is a factor of 60):
   Redistributes jobs across N offset groups (0-59/N, 1-59/N, ..., (N-1)-59/N),
   starting from a random offset and cycling sequentially.

2. Non-periodic patterns (fixed minute 0, e.g. 0 * * * *):
   Replaces the fixed 0 with a random minute in [0, 59].
"""

import csv
import re
import os
import random
from collections import defaultdict


FACTORS_OF_60 = {n for n in range(2, 61) if 60 % n == 0}


def parse_minute_step(minute_field):
    """Return N if minute field is */N with N a factor of 60 (and N > 1), else None."""
    m = re.fullmatch(r'\*/(\d+)', minute_field.strip())
    if m:
        n = int(m.group(1))
        if n in FACTORS_OF_60:
            return n
    return None



def is_fixed_zero(minute_field):
    """Return True if minute field is the literal value 0 (not */N or a range)."""
    return minute_field.strip() == '0'


def distribute(jobs, n):
    """
    Distribute (job_name, cron_expr) pairs across N offset groups.
    Starts at a random offset in [0, N-1] and cycles sequentially
    through all N offsets. Jobs are assigned evenly across groups.

    Returns dict: job_name -> new_cron_expr
    """
    m = len(jobs)
    base = m // n
    remainder = m % n
    start = random.randint(0, n - 1)
    offsets = [(start + i) % n for i in range(n)]  # cycle from random start

    result = {}
    job_idx = 0
    for i, offset in enumerate(offsets):
        count = base + (1 if i < remainder else 0)
        new_minute = f"{offset}-59/{n}" if offset > 0 else f"0-59/{n}"
        for _ in range(count):
            if job_idx >= m:
                break
            job_name, cron_expr = jobs[job_idx]
            parts = cron_expr.strip().split()
            parts[0] = new_minute
            result[job_name] = ' '.join(parts)
            job_idx += 1

    return result


def main():
    print("=" * 60)
    print("CRON OPTIMIZER")
    print("=" * 60)
    print()

    input_file = input("Enter input TSV file: ").strip()
    if not input_file:
        print("No file provided. Exiting.")
        return

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_optimized{ext}"
    txt_file = "cron_schedule_optimized.txt"

    # Read all jobs preserving original order
    jobs = []
    with open(input_file, newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            jobs.append((row['job_name'], row['cron_schedule']))

    print(f"Loaded {len(jobs)} jobs from '{input_file}'.")
    print()

    optimized = {}

    # --- Periodic optimization: */N patterns ---
    step_groups = defaultdict(list)
    for job_name, cron_expr in jobs:
        parts = cron_expr.strip().split()
        if parts:
            n = parse_minute_step(parts[0])
            if n is not None:
                step_groups[n].append((job_name, cron_expr))

    total_periodic = 0
    print("Periodic optimization (*/N patterns):")
    print(f"  {'Pattern':<12} {'Jobs':>6}  {'Groups':>6}  {'Per group':>10}")
    print("  " + "-" * 42)

    for n in sorted(step_groups.keys()):
        group = step_groups[n]
        result = distribute(group, n)
        optimized.update(result)
        total_periodic += len(group)
        base_count = len(group) // n
        rem = len(group) % n
        per_group = f"{base_count}" if rem == 0 else f"{base_count}-{base_count + 1}"
        print(f"  {'*/' + str(n):<12} {len(group):>6}  {n:>6}  {per_group:>10}")

    print()
    print(f"  Optimized : {total_periodic} jobs")

    # --- Non-periodic optimization: fixed minute 0 ---
    total_nonperiodic = 0
    print()
    print("Non-periodic optimization (fixed minute 0):")

    for job_name, cron_expr in jobs:
        if job_name in optimized:
            continue
        parts = cron_expr.strip().split()
        if parts and is_fixed_zero(parts[0]):
            parts[0] = str(random.randint(0, 59))
            optimized[job_name] = ' '.join(parts)
            total_nonperiodic += 1

    print(f"  Optimized : {total_nonperiodic} jobs  (minute 0 -> random 0-59)")

    # --- Summary ---
    total_optimized = total_periodic + total_nonperiodic
    print()
    print(f"Total optimized : {total_optimized} jobs")
    print(f"Total unchanged : {len(jobs) - total_optimized} jobs")

    # Write output files
    with open(output_file, 'w', newline='') as f_tsv, \
         open(txt_file, 'w') as f_txt:
        writer = csv.writer(f_tsv, delimiter='\t')
        writer.writerow(['job_name', 'cron_schedule'])
        for job_name, cron_expr in jobs:
            new_expr = optimized.get(job_name, cron_expr)
            writer.writerow([job_name, new_expr])
            f_txt.write(new_expr + '\n')

    print()
    print(f"Saved to: '{output_file}'")
    print(f"Saved to: '{txt_file}'")


if __name__ == "__main__":
    main()
