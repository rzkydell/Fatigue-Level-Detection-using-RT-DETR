import os

CLASS_NORMAL = "Normal"
CLASS_MEDIUM = "Kelelahan Sedang"
CLASS_HEAVY = "Kelelahan Berat"

def get_next_record_folder(base_dir="record"):
    os.makedirs(base_dir, exist_ok=True)
    existing = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("hasil deteksi")]
    max_num = 0
    for f in existing:
        try:
            num = int(f.split("hasil deteksi")[-1].strip())
            max_num = max(max_num, num)
        except: pass
    new_folder = os.path.join(base_dir, f"hasil deteksi {max_num+1}")
    os.makedirs(new_folder, exist_ok=True)
    return new_folder