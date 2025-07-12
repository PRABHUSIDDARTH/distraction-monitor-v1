import os
import time
from PIL import Image
from mss import mss

# Modify this if you want to save somewhere else
base_dir = "dataset"

# Choose your label for this run
label = input("Label (short / reel / non_short): ").strip()

# Create folder
target_dir = os.path.join(base_dir, label)
os.makedirs(target_dir, exist_ok=True)

with mss() as sct:
    monitor = sct.monitors[1]
    for i in range(1, 51):  # Capture 50 images per session
        filename = os.path.join(target_dir, f"{label}_{i}.jpg")
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save(filename)
        print(f"Saved {filename}")
        time.sleep(1.5)  # 1.5 sec delay between screenshots
