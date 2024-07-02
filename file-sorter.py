import os
import time
from datetime import datetime

def change_extension_to_uppercase_and_convert_cr2(file_path):
    base, ext = os.path.splitext(file_path)
    if ext.lower() == '.cr2':
        new_path = base + '.JPG'
        os.rename(file_path, new_path)
    else:
        new_path = base + ext.upper()
        if file_path != new_path:
            os.rename(file_path, new_path)
    return new_path

def get_file_date(file_path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    except Exception as e:
        print(f"Error getting date for {file_path}: {e}")
        return None

def rename_file(file_path, prefix, date_obj, count):
    date_str = date_obj.strftime('%Y%m%d_%H%M')
    new_name = f"{prefix}_{date_str}"
    if count > 0:
        new_name += f"({count})"
    new_name += os.path.splitext(file_path)[1].upper()
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    return new_path

def process_directory(directory):
    media_files = []
    other_files = []
    modified_files = []
    ignored_formatted_files = []
    ignored_exception_files = []
    start_time = time.time()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_path = change_extension_to_uppercase_and_convert_cr2(file_path)

            date_obj = get_file_date(new_path)
            if date_obj:
                if new_path.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.avi')):
                    prefix = "IMG" if new_path.lower().endswith(('.jpg', '.jpeg', '.png')) else "VID"
                    base_name = f"{prefix}_{date_obj.strftime('%Y%m%d_%H%M')}"
                    
                    count = 0
                    while os.path.exists(os.path.join(root, base_name + (f"({count})" if count > 0 else "") + os.path.splitext(new_path)[1])):
                        count += 1

                    new_file_path = rename_file(new_path, prefix, date_obj, count)
                    media_files.append(new_file_path)
                    modified_files.append(new_file_path)
                else:
                    other_files.append(new_path)
            else:
                ignored_exception_files.append(new_path)

    end_time = time.time()
    print("Summary:")
    print(f"Total files found: {len(media_files) + len(other_files)}")
    print(f"Media files found: {len(media_files)}")
    print(f"Files modified: {len(modified_files)}")
    print(f"Ignored (already formatted): {len(ignored_formatted_files)}")
    print(f"Ignored (due to exceptions): {len(ignored_exception_files)}")
    print(f"Ignored (other files): {len(other_files)}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    process_directory('.')
