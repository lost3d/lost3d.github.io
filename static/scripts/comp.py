import os
import json

def generate_ar_js_data(root_dir, output_file):
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
            
            # Map your specific file suffixes to clean keys
            glb_files = {
                "0_llamamesh": "llamamesh",
                "1_octgpt": "octgpt",
                "2_shapellm": "shapellm",
                "x_ours_ar": "ours_ar"
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
        # NOTE: Updated the variable name to what the HTML expects for this section
        f.write("window.arComparisonData = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
        
    print(f"Successfully processed {data['total_count']} entries. Saved to {output_file}")

if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your AR comparison folders
    ROOT_FOLDER = "static/shapes/ar_comparison/data_rescaled_reduced" 
    
    # Ensure this saves to where your index.html is looking for it
    OUTPUT_JS_FILE = "static/ar_comparison_data.js" 
    
    generate_ar_js_data(ROOT_FOLDER, OUTPUT_JS_FILE)