import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone

# Initialize the ECR client
ecr_client = boto3.client('ecr')

# Define constants
RETENTION_PERIOD = 1  # For testing, set to 1 day
MIN_IMG_KEPT = 5

# Function to list all ECR repositories
def list_ecr_repo():
    try:
        response = ecr_client.describe_repositories()
        return [repo['repositoryName'] for repo in response['repositories']]
    except ClientError as e:
        print(f"API Error Occurred: {e}")
        return []

# Function to list images in a repository
def list_images(repository_name):
    try:
        response = ecr_client.describe_images(repositoryName=repository_name)
        images = response['imageDetails']
        return sorted(images, key=lambda x: x['imagePushedAt'])
    except ClientError as e:
        print(f"API Error Occurred: {e}")
        return []

# Function to delete images
def delete_images(repository_name, image_ids):
    try:
        # Batch delete images (max 1000 per request)
        for i in range(0, len(image_ids), 1000):
            batch = image_ids[i:i+1000]
            response = ecr_client.batch_delete_image(
                repositoryName=repository_name,
                imageIds=batch
            )
            deleted = response.get('imageIds', [])
            if deleted:
                print(f"Successfully deleted images: {[img['imageDigest'] for img in deleted]}")
            if 'failures' in response:
                print(f"Failures: {response['failures']}")
    except ClientError as e:
        print(f"API Error Occurred: {e}")
    except Exception as e:
        print(f"Exception Occurred: {e}")

# Function for cleaning up repositories
def clean_up(repository_name):
    images = list_images(repository_name)
    if len(images) <= MIN_IMG_KEPT:
        print(f"Repository {repository_name} has {len(images)} images. So, no clean up needed")
        return

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_PERIOD)
    images_to_delete = [img for img in images if img['imagePushedAt'] < cutoff_date]

    if len(images_to_delete) + MIN_IMG_KEPT > len(images):
        images_to_delete = images_to_delete[:len(images) - MIN_IMG_KEPT]

    image_ids_to_delete = [{'imageDigest': img['imageDigest']} for img in images_to_delete]

    if image_ids_to_delete:
        print(f"Preparing to delete {len(image_ids_to_delete)} images from repository {repository_name}.")
        delete_images(repository_name, image_ids_to_delete)
    else:
        print(f"No images to delete from repository {repository_name}.")

# Main function
def main():
    repositories = list_ecr_repo()
    if not repositories:
        print("No ECR repositories found. Exiting...")
        return
    for repo in repositories:
        clean_up(repo)

# Main execution
if __name__ == '__main__':
    main()
