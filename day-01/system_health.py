'''
Today’s goal is to write your first Python script.
You will create a Python script that:
Takes threshold values (CPU, disk, memory) from user input
Also fetches system metrics using a Python library (example: psutil)
Compares metrics against thresholds
Prints the result to the terminal
'''
import psutil

# Function to take threshold values from user
def get_thresholds():
    cpu_threshold = int(input("Enter CPU usage threshold (%) : "))
    memory_threshold = int(input("Enter Memory usage threshold (%) : "))
    disk_threshold = int(input("Enter Disk usage threshold (%) : "))
    return cpu_threshold, memory_threshold, disk_threshold

# Function to compare system metrics against thresold
def check_system_health():

    # Get threshold values
    cpu_threshold, memory_threshold, disk_threshold = get_thresholds()

    # Fetch current system metrics
    system_cpu_usage = psutil.cpu_percent(interval=1)
    system_memory_usage = psutil.virtual_memory().percent
    system_disk_usage = psutil.disk_usage('/').percent

    print("\n---System Health Check---\n")

    # CPU check
    print(f"CPU Usage: {system_cpu_usage}%")
    if system_cpu_usage > cpu_threshold:
        print("⚠️ CPU usage is above threshold!")
    else:
        print("✅ CPU usage is within limits.")

    # Memory check
    print(f"Memory Usage: {system_memory_usage}%")
    if system_memory_usage > memory_threshold:
        print("⚠️ Memory usage is above threshold!")
    else:
        print("✅ Memory usage is within limits.")

    # Disk check
    print(f"Disk Usage: {system_disk_usage}%")
    if system_disk_usage > disk_threshold:
        print("⚠️ Disk usage is above threshold!\n")
    else:
        print("✅ Disk usage is within limits.\n")


while True:
    print("=== System Health Check ===\n")
    check_system_health()
    
    choice = input("Run again? (yes/no): ").strip().lower()
    if choice != "yes":
        print("Exiting system health check 👋\n")
        break

    
        

