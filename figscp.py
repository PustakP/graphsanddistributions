import os
import shutil

def move_files(keyword, folder_name):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Get all files in the current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Move files containing the keyword to the destination folder
    for file in files:
        if keyword in file:
            shutil.move(file, os.path.join(folder_name, file))
            print(f"Moved {file} to {folder_name}")

def main():
    # Move Gaussian figures
    move_files("Gaussian", "Gaussian Figures")
    
    # Move Poisson figures
    move_files("Poisson", "Poisson Figures")

    # Move all other files to a folder named "Other"
    move_files(".png", "Other")

if __name__ == "__main__":
    main()
    print("File moving completed.")