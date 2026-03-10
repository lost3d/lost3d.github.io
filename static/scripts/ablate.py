import os
import json

def generate_ablation_js_data(base_dir, output_file):
    data = {
        "total_count": 0,
        "entries": []
    }

    dir_wo_rida = os.path.join(base_dir, "no_repa_reduced")
    dir_w_rida = os.path.join(base_dir, "ours_reduced")

    # Get all unique SHAs by looking at both directories
    shas = set()
    if os.path.exists(dir_wo_rida):
        shas.update([d for d in os.listdir(dir_wo_rida) if os.path.isdir(os.path.join(dir_wo_rida, d))])
    if os.path.exists(dir_w_rida):
        shas.update([d for d in os.listdir(dir_w_rida) if os.path.isdir(os.path.join(dir_w_rida, d))])

    token_levels = [1, 4, 16]

    for sha in shas:
        entry = {
            "sha256": sha,
            "models": {}
        }
        
        for level in token_levels:
            # Format the label exactly as the HTML expects
            token_label = "1 token" if level == 1 else f"{level} tokens"
            file_name = f"{sha}_{level}_tok.glb"
            
            # 1. Path for w/o RIDA (no_repa_reduced)
            path_wo = os.path.join(dir_wo_rida, sha, file_name)
            if os.path.exists(path_wo):
                key_wo = f"w/o RIDA ({token_label})"
                entry["models"][key_wo] = f"{base_dir}/no_repa_reduced/{sha}/{file_name}"
                
            # 2. Path for w/ RIDA (ours_reduced)
            path_w = os.path.join(dir_w_rida, sha, file_name)
            if os.path.exists(path_w):
                key_w = f"w/ RIDA ({token_label})"
                entry["models"][key_w] = f"{base_dir}/ours_reduced/{sha}/{file_name}"

        # Only add the entry if we actually found models for it
        if entry["models"]:
            data["entries"].append(entry)

    data["total_count"] = len(data["entries"])

    with open(output_file, 'w', encoding='utf-8') as f:
        # Note the target variable for the ablation gallery!
        f.write("window.ablationData = ")
        json.dump(data, f, indent=2)
        f.write(";\n")
        
    print(f"Successfully processed {data['total_count']} entries. Saved to {output_file}")

if __name__ == "__main__":
    # IMPORTANT: Update this to the folder containing BOTH 'no_repa_reduced' and 'ours_reduced'
    BASE_DIR = "static/shapes/ablation" 
    OUTPUT_JS_FILE = "static/ablation_data.js"
    
    generate_ablation_js_data(BASE_DIR, OUTPUT_JS_FILE)