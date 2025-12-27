### Log Analyzer

1. What problem am I solving?
- The Mess: Apps create thousands of log lines every day.
- The Struggle: Humans cannot read them all to find errors.
- The Fix: We need a tool to scan these logs automatically and tell us if the system is "Healthy" or "In Trouble."

2. What input does my script need?
- The script requires two main pieces of information:
- The Source: A text-based log file (e.g., app.log) containing various log entries.
- The Destination: A filename where the final summary should be saved (e.g., log_summary.txt).

3. What output should my script give?
- INFO: Total count (Everything is fine).
- WARNING: Total count (Keep an eye on this).
- ERROR: Total count (Something is broken!).
- TOTAL: The sum of all the above.

4. What are the main steps? (The Logic)
- Step 1: Double Check – Make sure the file exists and isn't empty before starting.
- Step 2: Read Line-by-Line – Open the file and look at one line at a time (this saves memory).
- Step 3: Match Keywords – Turn the text to UPPERCASE so we don't miss "error" vs "ERROR," then add to the count.
- Step 4: Build Report – Organize the numbers into a clean table format.
- Step 5: Save & Show – Save the report to a file and print it on the screen for the user.

---- Why this structure works for DevOps ----
- Error Handling: By checking if the file exists before processing, you prevent the automation from "crashing" mid-way.
- OOP Approach: By using a Class (LogAnalyzer), the code is modular. You could easily import this into a larger monitoring dashboard later without rewriting it.
- Case Insensitivity: Converting lines to .upper() makes the automation "smarter" and less prone to missing data due to formatting differences.