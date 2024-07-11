from s3 import create_bucket, list_buckets, delete_bucket, delete_all_objects
from ec2 import create_instance, list_instances, terminate_instance
from botocore.exceptions import ClientError

# Create a function that asks the user to create a bucket
# If the user says yes, ask the user to enter the bucket name
# If the user says no, print a message

def ask_create_bucket():
    response = input("Do you want to create a bucket? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        bucket_name = input("Enter the bucket name you want to create: ").strip()
        create_bucket(bucket_name)
    else:
        print("You chose not to create a bucket")
    # Asks me if i want to list all buckets in a region
    response = (
        input("Do you want to list all buckets in the region? (yes/no): ")
        .strip()
        .lower()
    )
    if response in ["yes", "y"]:
        list_buckets()
    else:
        print("You chose not to list all buckets")
    # Asks me if i want to delete a bucket. If yes, it asks me for the bucket name
    # If it fails due to the bucket not being empty, it asks me if i want to delete all objects in the bucket
    response = input("Do you want to delete a bucket? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        try:
            bucket_name = input("Enter the bucket name you want to delete: ").strip()
            delete_bucket(bucket_name)
        except ClientError as e:
            print(f"Error: {e}")
            if "BucketNotEmpty" in str(e):
                response = (
                    input("Do you want to delete all objects in the bucket? (yes/no): ")
                    .strip()
                    .lower()
                )
                if response in ["yes", "y"]:
                    delete_all_objects(bucket_name)
                    response = (
                        input("Do you want to delete the bucket now? (yes/no): ")
                        .strip()
                        .lower()
                    )
                    if response in ["yes", "y"]:
                        delete_bucket(bucket_name)
                else:
                    print("You chose not to delete all objects in the bucket")
    else:
        print("You chose not to delete a bucket")

def ask_create_instance():
    # Ask the user if they want to create an instance
    response = input("Do you want to create an instance? (yes/no): ").strip().lower()
    # If yes, ask the user to enter the instance name
    if response in ["yes", "y"]:
        user_input = input("Enter the instance name you want to create: ").strip()
        create_instance(user_input)
    else:
        print("You chose not to create an instance")
    # Ask the user if they want to terminate an instance
    response = input("Do you want to terminate an instance? (yes/no): ").strip().lower()
    # If yes, ask the user to list all instances name and id
    if response in ["yes", "y"]:
        list_instances()
        instance_id = input("Enter the instance id you want to terminate: ").strip()
        terminate_instance(instance_id)