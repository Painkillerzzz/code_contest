import os
import json

def extract_contents_to_jsonl(folder_path, output_file):
    """
    Traverse subdirectories in the given folder path, extract .md and data files, 
    and save the combined results in a JSONL file.

    Args:
        folder_path (str): Path to the main folder containing subdirectories.
        output_file (str): Path to the output JSONL file.
    """
    data_entries = []
    
    subdirs = sorted([d for d in os.listdir(folder_path)], key=lambda x: int(x.split('_')[0]))

    # Iterate over all subdirectories in the folder
    for subdir in subdirs:
        subdir_path = os.path.join(folder_path, subdir)

        # Only process directories
        if os.path.isdir(subdir_path):
            md_file_path = os.path.join(subdir_path, "题面.md")
            data_dir_path = os.path.join(subdir_path, "data")

            # Ensure the required files and directories exist
            if os.path.exists(md_file_path) and os.path.isdir(data_dir_path):
                try:
                    # Read the content of "题面.md"
                    with open(md_file_path, "r", encoding="utf-8") as md_file:
                        md_content = md_file.read()

                    # Gather all .in and .out files in the data directory
                    in_files = sorted(
                        [f for f in os.listdir(data_dir_path) if f.endswith(".in")]
                    )
                    out_files = sorted(
                        [f for f in os.listdir(data_dir_path) if f.endswith(".out")]
                    )
                    
                    in_content = []
                    out_content = []

                    for in_file, out_file in zip(in_files, out_files):
                        assert in_file.replace(".in", ".out") == out_file
                        
                        in_file_path = os.path.join(data_dir_path, in_file)
                        out_file_path = os.path.join(data_dir_path, out_file)

                        # Read the content of .in and .out files
                        with open(in_file_path, "r", encoding="utf-8") as in_f:
                            in_content.append(in_f.read())
                        with open(out_file_path, "r", encoding="utf-8") as out_f:
                            out_content.append(out_f.read())

                    # Append a new entry to the list
                    assert len(in_content) == len(out_content)
                    data_entries.append({
                        "id": int(subdir.split('_', 1)[0]),
                        "name": subdir.split('_', 1)[1],
                        "description": md_content,
                        "inputs": in_content,
                        "outputs": out_content,
                    })
                except Exception as e:
                    print(f"Error processing {subdir}: {e}")

    # Write all entries to a JSONL file
    with open(output_file, "w", encoding="utf-8") as jsonl_file:
        for entry in data_entries:
            jsonl_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Data extraction complete. Output saved to {output_file}")


# Example usage
folder_path = "./raw_data"  # Replace with the path to your main folder
output_file = "./data/data.jsonl"          # Replace with your desired output file name
extract_contents_to_jsonl(folder_path, output_file)
