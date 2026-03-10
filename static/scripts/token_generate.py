import os
import json

def generate_js_data(root_dir, output_file):
    # Base structure matching your headers
    data = {
        "total_count": 0,
        "entries": []
    }

    # Iterate through the root directory
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        
        # Assume each directory in the root folder is a sha256 hash
        if os.path.isdir(item_path):
            sha = item
            
            entry = {
                "sha256": sha,
                "models": {}
            }
            
            # The suffixes you outlined for your files
            suffixes = ["1_tok", "4_tok", "16_tok", "64_tok", "512_tok", "origin3d"]
            
            for suffix in suffixes:
                file_name = f"{sha}_{suffix}.glb"
                file_path = os.path.join(item_path, file_name)
                
                # If the file exists, add its relative web path to the dictionary
                if os.path.exists(file_path):
                    # This constructs a relative path (e.g., "models_root/sha/sha_1_tok.glb")
                    # Adjust this prefix depending on how your static site routes folders
                    web_path = f"{root_dir}/{sha}/{file_name}"
                    entry["models"][suffix] = web_path
            
            data["entries"].append(entry)
            
    data["total_count"] = len(data["entries"])

    # Write the output to a JavaScript file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("window.comparisonData = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
        
    print(f"Successfully processed {data['total_count']} entries. Saved to {output_file}")

if __name__ == "__main__":
    # Replace 'models_root' with the actual name of your root folder
    ROOT_FOLDER = "static/shapes/tokenization/data_tokenization_gallery_reduced" 
    OUTPUT_JS_FILE = "tokenization.js"
    
    generate_js_data(ROOT_FOLDER, OUTPUT_JS_FILE)