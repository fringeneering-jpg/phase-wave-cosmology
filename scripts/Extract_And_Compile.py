import os
import shutil
import json

# 1. Define the messy list of paths you provided
sources = [
    r"C:\Users\jaden\Downloads\json\subagents",
    r"C:\Users\jaden\Downloads\json\subagents\efe592c3-52b9-4f06-8d98-fe1071482fb1",
    r"C:\Users\jaden\Downloads\json\subagents\d96081fe-c85e-45ad-b8ca-fefd8989227c",
    r"C:\Users\jaden\Downloads\json\subagents\d3e68784-ae98-4b08-993a-d280a9810f6b",
    r"C:\Users\jaden\Downloads\session.v4.jsonl"
]

# 2. Define the new folder name
target_dir = r"C:\Users\jaden\Downloads\Compiled_JSONs"
output_file = os.path.join(target_dir, "_compiled_master.jsonl")

# Create the new folder if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Gather unique files to avoid duplicates
files_to_process = set()

for src in sources:
    if os.path.isfile(src):
        if src.endswith(('.json', '.jsonl')):
            files_to_process.add(os.path.abspath(src))
    elif os.path.isdir(src):
        for root, _, files in os.walk(src):
            for f in files:
                if f.endswith(('.json', '.jsonl')):
                    files_to_process.add(os.path.abspath(os.path.join(root, f)))
    else:
        print(f"Path not found (skipping): {src}")

# 3. Extract / Copy files into the new folder
print(f"Extracting {len(files_to_process)} unique files to {target_dir}...")
copied_paths = []

for src_file in files_to_process:
    base_name = os.path.basename(src_file)
    dest_path = os.path.join(target_dir, base_name)
    
    # Handle naming collisions if two files have the exact same name from different folders
    counter = 1
    while os.path.exists(dest_path) and dest_path not in copied_paths:
        name, ext = os.path.splitext(base_name)
        dest_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
        counter += 1
        
    shutil.copy2(src_file, dest_path)
    copied_paths.append(dest_path)

# 4. Compile them all together into a master file
print(f"Compiling into {output_file}...")

with open(output_file, 'w', encoding='utf-8') as outfile:
    for file_path in copied_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                if file_path.endswith('.jsonl'):
                    # Append JSONL files line by line
                    for line in infile:
                        if line.strip():
                            outfile.write(line.strip() + '\n')
                elif file_path.endswith('.json'):
                    # Load standard JSON and convert to JSONL format so they play nice together
                    data = json.load(infile)
                    if isinstance(data, list):
                        for item in data:
                            outfile.write(json.dumps(item, ensure_ascii=False) + '\n')
                    else:
                        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

print(f"\nDone! You can find the extracted files and the compiled master file in:")
print(target_dir)