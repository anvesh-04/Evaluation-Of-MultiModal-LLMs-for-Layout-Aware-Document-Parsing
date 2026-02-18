import pandas as pd
import base64
import os
from io import BytesIO
from PIL import Image
import glob

# Base path to your dataset
base_path = r"C:\Users\anshg\OneDrive\Desktop\BTP\Evaluation-Of-MultiModal-LLMs-for-Layout-Aware-Document-Parsing\CC-OCR_Dataset\doc_parsing"
folders = ["doc", "table"]
output_base = r"C:\Users\anshg\OneDrive\Desktop\BTP\Evaluation-Of-MultiModal-LLMs-for-Layout-Aware-Document-Parsing\Extracted_parsing_images"

def extract_from_tsv(file_path, save_dir):
    try:
        df = pd.read_csv(file_path, sep='\t')
        os.makedirs(save_dir, exist_ok=True)
        
        print(f"Processing: {os.path.basename(file_path)}...")
        
        # Iterating through the rows to extract base64 images
        # The 'image' column typically contains the base64 string
        for idx, row in df.iterrows():
            img_name = row.get('image_name', f"img_{idx}.png")
            img_data = base64.b64decode(row['image'])
            img = Image.open(BytesIO(img_data))
            
            img.save(os.path.join(save_dir, img_name))
            
        print(f"Successfully extracted {len(df)} images to {save_dir}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

for folder in folders:
    folder_path = os.path.join(base_path, folder)
    
    # Looking for English (eng) TSV files - adjust the pattern if needed
    # This covers both 'doc_scan_eng_*.tsv' and 'doc_photo_eng_*.tsv'
    search_pattern = os.path.join(folder_path, "*eng*.tsv")
    target_files = glob.glob(search_pattern)
    
    for tsv_file in target_files:
        sub_folder_name = os.path.splitext(os.path.basename(tsv_file))[0]
        save_path = os.path.join(output_base, folder, sub_folder_name)
        
        extract_from_tsv(tsv_file, save_path)

print("\nAll English Document Parsing images have been extracted!")