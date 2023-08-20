"""
Generate .AHK file for each game. The name of the .AHK file is based on the zip files from source dir.
"""
import os
import shutil

ahk_template_file = ".\\template.ahk"
source_directory = "z:\\roms-1g1r\\erista-redump-sony-playstation-3-1g1r\\"
destination_directory = ".\\out"

def gen_ahk(source_file, dest_dir, filenames):
    for filename in filenames:
        filename = filename.replace(".zip", "")
        dest_path = f"{dest_dir}/{filename}.ahk"
        
        shutil.copy(source_file, dest_path)
        
        print("File %s copied and renamed to %s" % (source_file, dest_path))

def main():
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    zip_files = [f for f in os.listdir(source_directory) if f.endswith(".zip")]

    gen_ahk(ahk_template_file, destination_directory, zip_files)

if __name__ == "__main__":
    main()

# EOF