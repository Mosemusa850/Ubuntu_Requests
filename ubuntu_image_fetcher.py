import requests
import os
import hashlib
from urllib.parse import urlparse
import datetime
from concurrent.futures import ThreadPoolExecutor

def get_file_hash(filepath):
    """Calculate SHA-256 hash of a file to check for duplicates."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def is_valid_image(content_type):
    """Check if Content-Type header indicates a valid image."""
    valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp']
    return content_type in valid_types

def fetch_and_save_image(url, directory="Fetched_Images"):
    """
    Fetch an image from a URL and save it to the specified directory, avoiding duplicates.
    
    Parameters:
        url (str): URL of the image to fetch
        directory (str): Directory to save the image (default: Fetched_Images)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Send HTTP request with headers to mimic a browser and check safety
        headers = {
            'User-Agent': 'Mozilla/5.0 (Ubuntu; Linux x86_64) UbuntuImageFetcher/1.0',
            'Accept': 'image/*'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Check Content-Type header to ensure it's an image
        content_type = response.headers.get('Content-Type', '')
        if not is_valid_image(content_type):
            print(f"✗ Error for {url}: Invalid content type ({content_type}). Expected an image.")
            return False
        
        # Extract filename from URL or generate one with timestamp
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        
        # Check for duplicates by content hash
        temp_path = file_path + ".tmp"
        with open(temp_path, "wb") as f:
            f.write(response.content)
        
        # Calculate hash of downloaded content
        new_hash = get_file_hash(temp_path)
        
        # Check existing files in directory for duplicates
        for existing_file in os.listdir(directory):
            existing_path = os.path.join(directory, existing_file)
            if existing_path != temp_path and get_file_hash(existing_path) == new_hash:
                print(f"✗ Skipped {url}: Duplicate image found as {existing_file}.")
                os.remove(temp_path)  # Remove temp file
                return False
        
        # Move temp file to final location
        os.rename(temp_path, file_path)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {file_path}")
        return True
    
    except requests.exceptions.HTTPError as http_err:
        print(f"✗ Error for {url}: HTTP error - {http_err}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Error for {url}: Failed to connect to the server.")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Error for {url}: Request timed out.")
        return False
    except requests.exceptions.RequestException as req_err:
        print(f"✗ Error for {url}: Request error - {req_err}")
        return False
    except PermissionError:
        print(f"✗ Error for {url}: Permission denied when saving to '{file_path}'.")
        return False
    except Exception as e:
        print(f"✗ Error for {url}: An unexpected error occurred - {str(e)}")
        return False
    finally:
        # Clean up temporary file if it exists
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    try:
        # Prompt user for multiple URLs
        print("Enter image URLs (one per line, press Enter twice to finish):")
        urls = []
        while True:
            url = input().strip()
            if not url:  # Empty input ends the loop
                break
            urls.append(url)
        
        if not urls:
            print("✗ Error: No URLs provided.")
            return
        
        # Fetch images concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = executor.map(fetch_and_save_image, urls)
        
        # Summarize results
        successes = sum(1 for result in results if result)
        if successes > 0:
            print(f"\nConnection strengthened. Community enriched. ({successes}/{len(urls)} images fetched successfully)")
        else:
            print("\nConnection attempt failed. Please try again.")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()