import os
import json

def generate_multi_level_js_data(root_dir, output_file):
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
            
            # The suffixes from your screenshot mapped to clean keys
            glb_files = {
                "1_tok": "1_tok",
                "4_tok": "4_tok",
                "16_tok": "16_tok",
                "64_tok": "64_tok",
                "128_full": "128_full"
            }
            
            # Process the .glb files
            for suffix, key in glb_files.items():
                file_name = f"{sha}_{suffix}.glb"
                file_path = os.path.join(item_path, file_name)
                
                if os.path.exists(file_path):
                    entry["models"][key] = f"{root_dir}/{sha}/{file_name}"
            
            # Process the conditioning image (.png)
            image_name = f"{sha}.png"
            image_path = os.path.join(item_path, image_name)
            
            if os.path.exists(image_path):
                entry["models"]["target_image"] = f"{root_dir}/{sha}/{image_name}"
            
            data["entries"].append(entry)
            
    data["total_count"] = len(data["entries"])

    # Write the output to a JavaScript file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Note the target variable for the multi-level gallery!
        f.write("window.arMultiLevelData = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
        
    print(f"Successfully processed {data['total_count']} entries. Saved to {output_file}")

if __name__ == "__main__":
    # IMPORTANT: Update this to point to your actual ar multi level folder
    ROOT_FOLDER = "static/shapes/ar_ours_multi_levels/data_ar_ours_multi_level_reduced" 
    OUTPUT_JS_FILE = "static/ar_multi_level_data.js"
    
    generate_multi_level_js_data(ROOT_FOLDER, OUTPUT_JS_FILE)