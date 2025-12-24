import os

def analyze_logs(input_file, output_file):
    # Dictionary to maintain counts
    log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    
    try:
        # Check if file is empty before processing
        if os.path.getsize(input_file) == 0:
            print(f"Error: The file '{input_file}' is empty.")
            return

        with open(input_file, 'r') as file:
            for line in file:
                # Convert line to uppercase to ensure case-insensitive matching
                upper_line = line.upper()
                
                if "INFO" in upper_line:
                    log_counts["INFO"] += 1
                elif "WARNING" in upper_line:
                    log_counts["WARNING"] += 1
                elif "ERROR" in upper_line:
                    log_counts["ERROR"] += 1

        # Generate the summary string
        summary = (
            "--- Log Analysis Summary ---\n"
            f"INFO:    {log_counts['INFO']}\n"
            f"WARNING: {log_counts['WARNING']}\n"
            f"ERROR:   {log_counts['ERROR']}\n"
            f"TOTAL:   {sum(log_counts.values())}\n"
            "----------------------------"
        )

        # Print to terminal
        print(summary)

        # Write summary to output file
        with open(output_file, 'w') as out:
            out.write(summary)
        
        print(f"\nSuccess! Summary written to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define file paths
    INPUT_LOG = "app.log"
    OUTPUT_REPORT = "log_summary.txt"
    
    analyze_logs(INPUT_LOG, OUTPUT_REPORT)