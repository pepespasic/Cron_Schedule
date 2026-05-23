#!/usr/bin/env python3
"""
Convert cron_schedule.txt to job_cron.tsv
Creates a tab-delimited file with job_name and cron_schedule columns.
"""

def convert_to_tsv(input_file, output_file, preview_limit=10):
    """
    Convert cron schedule text file to TSV format.

    Args:
        input_file: Path to input file (cron_schedule.txt)
        output_file: Path to output file (job_cron.tsv)
        preview_limit: Number of rows to preview (default: 10)
    """
    # Read all cron schedules
    print("=" * 80)
    print("STEP 1: Reading Input File")
    print("=" * 80)
    with open(input_file, 'r') as f:
        cron_schedules = f.readlines()
    print(f"✓ Successfully read {len(cron_schedules):,} cron schedules from '{input_file}'")
    print(f"  Explanation: Each line contains one cron schedule expression")
    print()

    # Write to TSV file
    print("=" * 80)
    print("STEP 2: Creating TSV File")
    print("=" * 80)
    with open(output_file, 'w') as f:
        # Write header
        f.write("job_name\tcron_schedule\n")
        print("✓ Header row written: 'job_name\\tcron_schedule'")
        print(f"  Explanation: Tab-delimited header with two columns")
        print()

        # Write each job with unique job name
        for idx, cron_schedule in enumerate(cron_schedules, start=1):
            # Generate job name with zero-padding (job00001, job00002, etc.)
            job_name = f"job{idx:05d}"

            # Remove trailing newline from cron_schedule if present
            cron_schedule = cron_schedule.rstrip('\n')

            # Write tab-delimited row
            f.write(f"{job_name}\t{cron_schedule}\n")

    print(f"✓ Data rows written: {len(cron_schedules):,} jobs")
    print(f"  Explanation: Each cron schedule gets a unique job name (job00001-job{len(cron_schedules):05d})")
    print()

    # Show preview
    print("=" * 80)
    print(f"STEP 3: Preview of Output (First {preview_limit} Rows)")
    print("=" * 80)
    with open(output_file, 'r') as f:
        for i, line in enumerate(f):
            if i < preview_limit:
                print(line.rstrip())
            else:
                break

    remaining = len(cron_schedules) + 1 - preview_limit  # +1 for header
    if remaining > 0:
        print(f"... and {remaining:,} more rows")
    print()

    # Summary
    print("=" * 80)
    print("CONVERSION SUMMARY")
    print("=" * 80)
    print(f"Input file:       {input_file}")
    print(f"Output file:      {output_file}")
    print(f"Format:           Tab-delimited (TSV)")
    print(f"Header:           Yes (1 row)")
    print(f"Data rows:        {len(cron_schedules):,}")
    print(f"Total rows:       {len(cron_schedules) + 1:,}")
    print(f"Job name format:  job00001 to job{len(cron_schedules):05d}")
    print("=" * 80)


if __name__ == "__main__":
    # Prompt user for input filename
    print("=" * 80)
    print("CRON SCHEDULE TO TSV CONVERTER")
    print("=" * 80)
    print()

    user_input = input("Enter input filename (default: cron_schedule.txt): ").strip()

    # Use default if user just presses Enter
    if user_input == "":
        input_filename = "cron_schedule.txt"
        print(f"Using default: {input_filename}")
    else:
        input_filename = user_input
        print(f"Using: {input_filename}")

    # Generate output filename based on input filename
    # e.g., cron_schedule.txt -> job_cron.tsv
    #       my_crons.txt -> my_crons.tsv
    if input_filename.endswith('.txt'):
        base_name = input_filename[:-4]  # Remove .txt extension
        output_filename = f"{base_name}.tsv"
    else:
        output_filename = f"{input_filename}.tsv"

    print(f"Output will be saved to: {output_filename}")
    print()

    # Check if input file exists
    try:
        with open(input_filename, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"ERROR: File '{input_filename}' not found!")
        print("Please make sure the file exists and try again.")
        exit(1)

    # Perform conversion
    convert_to_tsv(input_filename, output_filename, preview_limit=10)

    print("\n✓ CONVERSION COMPLETE!")
    print(f"\nYou can now use '{output_filename}' in your applications.")
