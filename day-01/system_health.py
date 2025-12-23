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
    cpu_threshold = int(input("\nEnter CPU usage threshold (%) : "))
    memory_threshold = int(input("\nEnter Memory usage threshold (%) : "))
    disk_threshold = int(input("\nEnter Disk usage threshold (%) : "))
    return cpu_threshold, memory_threshold, disk_threshold

# Function to compare system metrics against thresold
def check_system_health():

    # Get threshold values
    cpu_threshold, memory_threshold, disk_threshold = get_thresholds()

    # Fetch current system metrics
    system_cpu_usage = psutil.cpu_percent(interval=1)
    system_memory_usage = psutil.virtual_memory().percent
    system_disk_usage = psutil.disk_usage('/').percent

    # CPU check
    print(f"\nCPU Usage: {system_cpu_usage}%")
    if system_cpu_usage > cpu_threshold:
        print("⚠️ CPU usage is above threshold!")
    else:
        print("✅ CPU usage is within limits.")

    # Memory check
    print(f"\nMemory Usage: {system_memory_usage}%")
    if system_memory_usage > memory_threshold:
        print("⚠️ Memory usage is above threshold!")
    else:
        print("✅ Memory usage is within limits.")

    # Disk check
    print(f"\nDisk Usage: {system_disk_usage}%")
    if system_disk_usage > disk_threshold:
        print("⚠️ Disk usage is above threshold!")
    else:
        print("✅ Disk usage is within limits.")


print("\n=== System Health Check ===")
check_system_health()

