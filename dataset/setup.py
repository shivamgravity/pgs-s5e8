import os
import zipfile
import time
import threading
from kaggle.api.kaggle_api_extended import KaggleApi
from tqdm import tqdm

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.{decimal_places}f}{unit}"
        size /= 1024
    return f"{size:.{decimal_places}f}TB"

def get_file_size_with_progress(file_path, update_interval=0.5):
    """Monitor file size growth during download"""
    if not os.path.exists(file_path):
        return
    
    last_size = 0
    start_time = time.time()
    
    while True:
        try:
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                # File might be complete or download paused
                time.sleep(update_interval * 2)
                if os.path.getsize(file_path) == current_size:
                    break
            
            # Calculate download speed
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed = current_size / elapsed_time
                speed_str = f"{human_readable_size(speed)}/s"
            else:
                speed_str = "calculating..."
            
            print(f"\r📥 Downloaded: {human_readable_size(current_size)} | Speed: {speed_str}", end="", flush=True)
            
            last_size = current_size
            time.sleep(update_interval)
            
        except FileNotFoundError:
            break
        except Exception as e:
            print(f"\nError monitoring download: {e}")
            break

def extract_with_progress(zip_path, extract_path):
    """Extract zip file with progress bar"""
    print(f"\n📦 Extracting {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        members = z.infolist()
        total_size = sum(member.file_size for member in members)
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="\nExtracting") as pbar:
            for member in members:
                z.extract(member, path=extract_path)
                pbar.update(member.file_size)

def print_file_sizes(folder):
    """Print sizes of all files in the directory"""
    print("\n📁 Files in directory after extraction:")
    total_size = 0
    for fname in sorted(os.listdir(folder)):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            sz = os.path.getsize(fpath)
            total_size += sz
            print(f"  📄 {fname}: {human_readable_size(sz)}")
    
    if total_size > 0:
        print(f"\n📊 Total size: {human_readable_size(total_size)}")

def download_with_progress_monitoring(api, competition, file_name, download_path):
    """Download a single file with live progress monitoring"""
    print(f"\n🚀 Starting download of {file_name}...")
    
    # Expected file path (Kaggle API adds .zip extension)
    expected_zip_path = os.path.join(download_path, file_name + ".zip")
    
    # Start progress monitoring in a separate thread
    progress_thread = threading.Thread(
        target=get_file_size_with_progress, 
        args=(expected_zip_path,),
        daemon=True
    )
    progress_thread.start()
    
    # Start the actual download
    try:
        api.competition_download_file(competition, file_name=file_name, path=download_path)
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return None
    
    # Wait for progress monitoring to complete
    progress_thread.join(timeout=2)
    print()  # New line after progress
    
    return expected_zip_path

def download_all_with_progress_monitoring(api, competition, download_path):
    """Download all competition files with progress monitoring"""
    print(f"\n🚀 Starting download of all files from {competition}...")
    
    # Expected file path
    expected_zip_path = os.path.join(download_path, competition + ".zip")
    
    # Start progress monitoring in a separate thread
    progress_thread = threading.Thread(
        target=get_file_size_with_progress, 
        args=(expected_zip_path,),
        daemon=True
    )
    progress_thread.start()
    
    # Start the actual download
    try:
        api.competition_download_files(competition, path=download_path)
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return None
    
    # Wait for progress monitoring to complete
    progress_thread.join(timeout=2)
    print()  # New line after progress
    
    return expected_zip_path

def download_kaggle_competition(competition, download_path):
    """Download Kaggle competition data with live progress tracking"""
    # Create download directory
    os.makedirs(download_path, exist_ok=True)
    
    # Initialize Kaggle API
    print("🔑 Authenticating with Kaggle API...")
    api = KaggleApi()
    try:
        api.authenticate()
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    print(f"\n🎯 Target competition: {competition}")
    print(f"📁 Download path: {download_path}")
    
    
    # Download all competition files
    print("\n📦 Downloading all competition files...")
    zip_path = download_all_with_progress_monitoring(api, competition, download_path)
        
    if zip_path and os.path.exists(zip_path):
       print(f"✅ Download complete: {human_readable_size(os.path.getsize(zip_path))}")
       extract_with_progress(zip_path, download_path)
       os.remove(zip_path)
       print("\n🗑 Removed zip file after extraction")
    else:
       print("⚠️  Download failed or file not found")
    
    # Show final results
    print_file_sizes(download_path)
    print("\n🎉 Download and extraction complete!")

if __name__ == "__main__":
    COMPETITION_NAME = "playground-series-s5e8"
    DOWNLOAD_PATH = "../dataset" # downloading in the same folder
    
    # Download everything with live progress
    download_kaggle_competition(COMPETITION_NAME, DOWNLOAD_PATH)
