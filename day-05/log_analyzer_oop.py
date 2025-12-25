import os

class LogAnalyzer:
    """
    A class to parse log files and generate summaries of log levels.
    """

    def __init__(self, input_file, output_file):
        """Initialize the analyzer with file paths and log counters."""
        self.input_file = input_file
        self.output_file = output_file
        # State: Keeping track of counts within the object
        self.log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    def process_logs(self):
        """Reads the log file and updates the log_counts dictionary."""
        try:
            # Pre-check for file existence and size
            if not os.path.exists(self.input_file):
                print(f"Error: The file '{self.input_file}' was not found.")
                return False
            
            if os.path.getsize(self.input_file) == 0:
                print(f"Error: The file '{self.input_file}' is empty.")
                return False

            with open(self.input_file, 'r') as file:
                for line in file:
                    upper_line = line.upper()
                    # Check for log levels
                    for level in self.log_counts.keys():
                        if level in upper_line:
                            self.log_counts[level] += 1
            return True

        except Exception as e:
            print(f"An unexpected error occurred during processing: {e}")
            return False

    def get_summary(self):
        """Returns a formatted string of the analysis results."""
        total = sum(self.log_counts.values())
        summary = (
            "--- Log Analysis Summary (OOP) ---\n"
            f"INFO:    {self.log_counts['INFO']}\n"
            f"WARNING: {self.log_counts['WARNING']}\n"
            f"ERROR:   {self.log_counts['ERROR']}\n"
            f"TOTAL:   {total}\n"
            "----------------------------------"
        )
        return summary

    def save_and_print_report(self):
        """Prints the summary to the console and writes it to a file."""
        report = self.get_summary()
        
        # Print to terminal
        print(report)
        
        # Write to file
        try:
            with open(self.output_file, 'w') as out:
                out.write(report)
            print(f"\nSuccess! Summary written to {self.output_file}")
        except Exception as e:
            print(f"Failed to write report to file: {e}")

if __name__ == "__main__":
    # 1. Instantiate the class (Create the object)
    analyzer = LogAnalyzer("app.log", "log_summary.txt")
    
    # 2. Run the logic
    if analyzer.process_logs():
        analyzer.save_and_print_report()