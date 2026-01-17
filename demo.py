import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import AdaptiveWeightedFilter
from src.utils import load_image, save_image

def main():
    input_path = "examples/lena_noisy.png"
    
    try:
        print(f"Loading {input_path}...")
        img = load_image(input_path)
        
        print("Initializing AWLF Filter (Reference Implementation)...")
        # Notice: A window size of 7 makes Python loops very slow, proving the need for Fast version
        filter_engine = AdaptiveWeightedFilter(window_size=5)
        
        print("Processing... (This might take a moment due to pure Python implementation)")
        start_time = time.time()
        
        result = filter_engine.process(img)
        
        elapsed = time.time() - start_time
        print(f"Done! Processing time: {elapsed:.4f}s")
        print(f"Resolution: {img.shape}")
        
        save_image("examples/result_reference.png", result)
        print("Result saved to examples/result_reference.png")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
