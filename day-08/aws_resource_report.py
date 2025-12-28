import boto3
import json

def generate_aws_report():
    # Initialize sessions for EC2 and S3
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    
    report_data = {
        "ec2_instances": [],
        "s3_buckets": []
    }

    print("--- Fetching AWS Resources ---")

    # 1. Fetch EC2 Instances
    print("Fetching EC2 Instances...")
    ec2_response = ec2.describe_instances()
    
    for reservation in ec2_response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            # Safer way to find the 'Name' tag specifically
            name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
            
            instance_info = {
                "InstanceName": name_tag,
                "InstanceId": instance['InstanceId'],
                "State": instance['State']['Name']
            }
            report_data["ec2_instances"].append(instance_info)
            print(f"Found EC2:\n NAME: {instance_info['InstanceName']}\n Instance ID: {instance_info['InstanceId']}\n Status: {instance_info['State']}")

    # 2. Fetch S3 Buckets
    print("\nFetching S3 Buckets...")
    s3_response = s3.list_buckets()
    buckets = s3_response.get('Buckets', [])
    
    if not buckets:
        print("No S3 buckets found.")
    else:
        for bucket in buckets:
            bucket_name = bucket['Name']
            report_data["s3_buckets"].append(bucket_name)
            print(f"Found Bucket: {bucket_name}")

    # 3. Save to JSON file
    with open('aws_report.json', 'w') as f:
        json.dump(report_data, f, indent=4)
    
    print("\n--- Report saved to aws_report.json ---")

if __name__ == "__main__":
    generate_aws_report()