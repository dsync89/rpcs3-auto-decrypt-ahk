import zipfile
import subprocess
import os
import sys

# SOURCE_ROM_PATH="z:\\roms-1g1r\\erista-redump-sony-playstation-3-1g1r"
EXTRACTED_ROM_DIR="r:\\ROMS-1G1R\\erista-redump-sony-playstation-3"

IRD_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), "ird")

PS3DEC_EXE_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "PS3Dec.exe")

def extract_zip(zip_file_path, destination_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        print("Extracting %s to %s" % (zip_file_path, destination_folder))
        
        total_size = sum(file_info.file_size for file_info in zip_ref.infolist())
        extracted_size = 0
        
        for member in zip_ref.infolist():
            extracted_size += member.file_size
            progress = (extracted_size / total_size) * 100
            sys.stdout.write("Extracting: {:.2f}%".format(progress))
            sys.stdout.flush()
            sys.stdout.write('\r')
            
            zip_ref.extract(member, destination_folder)
        
        print("\nExtraction complete!")

def read_ird_hex(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().rstrip()
            return content
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def decrypt_iso(disc_key_hex, encrypted_rom_filepath, decrypted_rom_filepath):
    command = [PS3DEC_EXE_PATH, "d", "key", disc_key_hex, encrypted_rom_filepath, decrypted_rom_filepath]    

    # Run the command and capture its output
    try:
        process = subprocess.run(command, text=True, capture_output=True, check=True)
        print("Command output:")
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        sys.exit(2)

def replace_file(file1, file2):
    try:
        if os.path.exists(file1):
            os.remove(file1)  # Remove file1 if it exists
        os.rename(file2, file1)  # Rename file2 to file1
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("Script directory:", script_dir)
    print("IRD path:", IRD_PATH)
    print("PS3DEC_EXE path:", PS3DEC_EXE_PATH)

    if len(sys.argv) < 3:
        print("Usage: python script_name.py <source_rom_filepath> <extracted_rom_dir>")
        sys.exit(99)
    
    SOURCE_ROM_PATH = sys.argv[1]
    EXTRACTED_ROM_DIR = sys.argv[2]
    
    # Your script logic here that uses the 'filename'
    # For example, you can open and process the file
    
    print(f"Processing file: {SOURCE_ROM_PATH}")

    if not os.path.exists(EXTRACTED_ROM_DIR):
        print("Destination folder not found!")
        sys.exit(1)

    extract_zip(SOURCE_ROM_PATH, EXTRACTED_ROM_DIR)

    print("Finding IRD...")
    ird_filename = "{}{}".format(os.path.basename(SOURCE_ROM_PATH)[:-3], "dkey")
    ird_filepath = os.path.join(IRD_PATH, ird_filename)

    if not os.path.exists(ird_filepath):
        print("Cannot find IRD file: {}".format(ird_filepath))
        sys.exit(2)

    print("Found IRD: %s" % ird_filepath)

    # read ird hex
    disc_key_hex = read_ird_hex(ird_filepath)

    # run decrypt
    encrypted_rom_filename = "{}{}".format(os.path.basename(SOURCE_ROM_PATH)[:-3], "iso")
    encrypted_rom_filepath = os.path.join(EXTRACTED_ROM_DIR, encrypted_rom_filename)

    decrypted_rom_filename = "{}{}".format(os.path.basename(SOURCE_ROM_PATH)[:-3], "dec.iso")
    decrypted_rom_filepath = os.path.join(EXTRACTED_ROM_DIR, decrypted_rom_filename)
    decrypt_iso(disc_key_hex, encrypted_rom_filepath, decrypted_rom_filepath)

    replace_file(encrypted_rom_filepath, decrypted_rom_filepath)

    print("File: {} extracted and decrypted!".format(SOURCE_ROM_PATH))
    sys.exit(0)