import os
import argparse
import sys

class LogAnalyzer:
    """
    A class to parse log files and generate summaries of log levels.
    """

    def __init__(self, input_file, output_file=None, filter_level=None):
        """Initialize with file paths and an optional filter level."""
        self.input_file = input_file
        self.output_file = output_file
        # Normalize filter level to uppercase if provided
        self.filter_level = filter_level.upper() if filter_level else None
        self.log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    def process_logs(self):
        """Reads the log file and updates the log_counts dictionary."""
        # Validation: Check if file exists
        if not os.path.exists(self.input_file):
            print(f"Error: The file '{self.input_file}' was not found.")
            return False
        
        if os.path.getsize(self.input_file) == 0:
            print(f"Error: The file '{self.input_file}' is empty.")
            return False

        try:
            with open(self.input_file, 'r') as file:
                for line in file:
                    upper_line = line.upper()
                    
                    # Logic for filtering or general counting
                    if self.filter_level:
                        if self.filter_level in upper_line:
                            self.log_counts[self.filter_level] = self.log_counts.get(self.filter_level, 0) + 1
                    else:
                        for level in self.log_counts.keys():
                            if level in upper_line:
                                self.log_counts[level] += 1
            return True
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def get_summary(self):
        """Returns a formatted string of the analysis results."""
        total = sum(self.log_counts.values())
        
        # Build dynamic summary
        summary_lines = ["--- Log Analysis Summary ---"]
        
        # If filtering, only show that level. Otherwise show all.
        for level, count in self.log_counts.items():
            if self.filter_level and level != self.filter_level:
                continue
            summary_lines.append(f"{level:<8}: {count}")
            
        summary_lines.append(f"TOTAL    : {total}")
        summary_lines.append("-" * 28)
        return "\n".join(summary_lines)

    def run(self):
        """Orchestrates the processing and reporting."""
        if self.process_logs():
            report = self.get_summary()
            
            # Print to terminal
            print(report)
            
            # Save to file if output path was provided
            if self.output_file:
                try:
                    with open(self.output_file, 'w') as out:
                        out.write(report)
                    print(f"Success! Report saved to: {self.output_file}")
                except Exception as e:
                    print(f"Failed to write report to file: {e}")

def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="DevOps Tool: Analyze log files and generate summaries."
    )

    # Required Arguments
    parser.add_argument("--file", required=True, help="Path to the input log file")
    
    # Optional Arguments
    parser.add_argument("--out", help="Path to save the summary report")
    parser.add_argument("--level", help="Filter summary to a specific level (INFO, WARNING, ERROR)")

    args = parser.parse_args()

    # Create analyzer instance and execute
    analyzer = LogAnalyzer(
        input_file=args.file, 
        output_file=args.out, 
        filter_level=args.level
    )
    analyzer.run()

if __name__ == "__main__":
    main()