import boto3
import os
from datetime import datetime, timedelta
from strands import Agent, tool
from strands.models.ollama import OllamaModel

# --- 1. THE ACTION TOOLS ---

@tool
def get_idle_ec2_instances(**kwargs):
    """Scans for running EC2 instances to identify potential idle servers."""
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    idle_report = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            idle_report.append({
                "ID": instance['InstanceId'],
                "Type": instance['InstanceType'],
                "Tag": instance.get('Tags', [{'Value': 'Unnamed'}])[0]['Value']
            })
    return f"Running Instances: {idle_report}"

@tool
def get_unattached_volumes(**kwargs):
    """Checks for EBS volumes not attached to any server (direct waste)."""
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    unattached = [{"ID": v['VolumeId'], "SizeGB": v['Size']} for v in volumes['Volumes']]
    return f"Unattached Volumes: {unattached}"

@tool
def get_verified_pricing(**kwargs):
    """Provides standard 2026 AWS pricing to ensure math accuracy."""
    return {
        "t2.micro": 0.0116,   # $/hr
        "c5.xlarge": 0.17,    # $/hr
        "gp3_storage": 0.08,  # $/GB-mo
        "unattached_eip": 0.005 # $/hr
    }

@tool
def tag_resource_for_cleanup(resource_id: str, days_until_deletion: int = 30, **kwargs):
    """Tags a resource for future deletion. Best for non-critical/dev waste."""
    ec2 = boto3.client('ec2')
    deletion_date = (datetime.now() + timedelta(days=days_until_deletion)).strftime('%Y-%m-%d')
    try:
        ec2.create_tags(
            Resources=[resource_id],
            Tags=[
                {'Key': 'Status', 'Value': 'Idle-Flagged'},
                {'Key': 'Cleanup_Date', 'Value': deletion_date}
            ]
        )
        return f"SUCCESS: {resource_id} tagged for cleanup on {deletion_date}."
    except Exception as e:
        return f"ERROR: {str(e)}"

@tool
def stop_idle_instance(instance_id: str, **kwargs):
    """Stops an instance. ONLY call if user has explicitly approved."""
    ec2 = boto3.client('ec2')
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        return f"SUCCESS: {instance_id} stopped."
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- 2. THE BRAIN SETUP ---

ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")

SYSTEM_PROMPT = """
You are a Senior FinOps Engineer. 
Your goal is to find cloud waste and provide a path to savings.

STEPS:
1. Use 'get_idle_ec2_instances' and 'get_unattached_volumes' to find waste.
2. Use 'get_verified_pricing' to ensure your math is correct.
3. If you find a cost discrepancy (e.g. costs higher than compute alone), investigate storage.
4. ALWAYS suggest 'tag_resource_for_cleanup' first for dev resources.
5. Provide a 'FinOps Dashboard' table at the top of your report.
"""

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    model=ollama_model,
    tools=[get_idle_ec2_instances, get_unattached_volumes, get_verified_pricing, tag_resource_for_cleanup, stop_idle_instance]
)

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("🔍 Starting Deep FinOps Analysis...")
    report = agent("Analyze AWS waste, explain any cost discrepancies, and propose a tagging/stop strategy.")
    
    print("\n--- REPORT GENERATED ---\n")
    print(report)

    # Save logic
    filename = f"finops_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(report))
    print(f"\n✅ Final report saved to: {filename}")