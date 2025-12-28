import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

class AWSAutomator:
    def __init__(self):
        try:
            # Initialize clients
            self.sessions = {
                'ec2': boto3.client('ec2'),
                's3': boto3.client('s3'),
                'iam': boto3.client('iam'),
                'lambda': boto3.client('lambda')
            }
        except (NoCredentialsError, PartialCredentialsError):
            print("❌ Error: AWS Credentials not found. Run 'aws configure'.")
            exit()
        except Exception as e:
            print(f"❌ Initialization Error: {e}")
            exit()
            
        self.report_data = {}

    def fetch_ec2(self):
        print("🔍 Scanning EC2 Instances...")
        try:
            instances = []
            response = self.sessions['ec2'].describe_instances()
            for res in response.get('Reservations', []):
                for ins in res.get('Instances', []):
                    name = next((t['Value'] for t in ins.get('Tags', []) if t['Key'] == 'Name'), 'Unnamed')
                    instances.append({"ID": ins['InstanceId'], "Name": name, "State": ins['State']['Name']})
            
            if not instances:
                return "No EC2 instances found."
            return instances
        except ClientError as e:
            return f"EC2 Error: {e.response['Error']['Message']}"

    def fetch_s3(self):
        print("🔍 Scanning S3 Buckets...")
        try:
            buckets = [b['Name'] for b in self.sessions['s3'].list_buckets().get('Buckets', [])]
            if not buckets:
                return "No S3 buckets found."
            return buckets
        except ClientError as e:
            return f"S3 Error: {e.response['Error']['Message']}"

    def fetch_iam(self):
        print("🔍 Scanning IAM Users...")
        try:
            users = [u['UserName'] for u in self.sessions['iam'].list_users().get('Users', [])]
            if not users:
                return "No IAM users found."
            return users
        except ClientError as e:
            return f"IAM Error: {e.response['Error']['Message']}"

    def fetch_lambda(self):
        print("🔍 Scanning Lambda Functions...")
        try:
            functions = [f['FunctionName'] for f in self.sessions['lambda'].list_functions().get('Functions', [])]
            if not functions:
                return "No Lambda functions found."
            return functions
        except ClientError as e:
            return f"Lambda Error: {e.response['Error']['Message']}"

    def run(self):
        while True:
            print("\n" + "="*30)
            print("      🚀 AWS RESOURCE AUTOMATOR 🚀")
            print("="*30)
            print("Available: ec2, s3, iam, lambda, all")
            print("Press 'q' to quit")
            
            choice = input("\nWhat should I scan? > ").strip().lower()

            if choice == 'q':
                print("Exiting... Happy Cloud-ing! ☁️")
                break
            
            self.report_data = {}

            if choice == 'ec2':
                self.report_data['ec2'] = self.fetch_ec2()
            elif choice == 's3':
                self.report_data['s3'] = self.fetch_s3()
            elif choice == 'iam':
                self.report_data['iam'] = self.fetch_iam()
            elif choice == 'lambda':
                self.report_data['lambda'] = self.fetch_lambda()
            elif choice == 'all':
                self.report_data['ec2'] = self.fetch_ec2()
                self.report_data['s3'] = self.fetch_s3()
                self.report_data['iam'] = self.fetch_iam()
                self.report_data['lambda'] = self.fetch_lambda()
            else:
                print(f"❌ '{choice}' is not a valid option.")
                continue

            self.save_and_display()

    def save_and_display(self):
        print("\n--- RESULTS ---")
        print(json.dumps(self.report_data, indent=2))
        
        filename = 'aws_interactive_report.json'
        try:
            with open(filename, 'w') as f:
                json.dump(self.report_data, f, indent=4)
            print(f"\n✅ Report updated in {filename}")
        except IOError as e:
            print(f"❌ File Error: Could not save report. {e}")

if __name__ == "__main__":
    automator = AWSAutomator()
    automator.run()