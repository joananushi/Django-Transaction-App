import os

def delete_image(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        # Handle errors, such as log the error or raise a specific exception
        pass
