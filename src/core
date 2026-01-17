import numpy as np
import math

class AdaptiveWeightedFilter:
    """
    Reference implementation of AWLF.
    
    This class demonstrates the mathematical logic of weight calculation 
    and pixel restoration in a readable, sequential manner.
    """
    
    def __init__(self, window_size: int = 5, sensitivity: float = 10.0):
        """
        Args:
            window_size (int): Size of the local neighborhood (must be odd).
            sensitivity (float): Parameter controlling weight decay.
        """
        if window_size % 2 == 0:
            raise ValueError("Window size must be odd.")
        self.w = window_size
        self.h = sensitivity
        self.pad = window_size // 2

    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Apply filter to the image.
        
        Args:
            image (np.ndarray): Input image (2D grayscale, uint8).
            
        Returns:
            np.ndarray: Denoised image.
        """
        # Type check to enforce 8-bit restriction
        if image.dtype != np.uint8:
            print("Warning: Input converted to uint8. For 16-bit support, use AWLF-Fast.")
            image = (image / 256).astype(np.uint8) if image.max() > 255 else image.astype(np.uint8)

        h, w = image.shape
        output = image.copy()
        
        # Symmetrical padding for boundary handling
        padded = np.pad(image, (self.pad, self.pad), mode='symmetric').astype(np.float64)
        
        # --- The "Textbook" Loop (No vectorization optimization) ---
        # This nested loop structure is great for understanding but slow for execution.
        for i in range(h):
            for j in range(w):
                self._process_pixel(padded, output, i, j)
                
        return output

    def _process_pixel(self, padded_img, output_img, i, j):
        """
        Internal method to process a single pixel.
        Separated for clarity of algorithm logic.
        """
        # Extract local window
        center_y, center_x = i + self.pad, j + self.pad
        window = padded_img[i:i+self.w, j:j+self.w]
        
        center_val = window[self.pad, self.pad]
        
        # 1. Noise Detection (Simple Min-Max strategy for reference)
        local_min = np.min(window)
        local_max = np.max(window)
        
        if local_min < center_val < local_max:
            # Not an impulse noise, keep original
            return
            
        # 2. Weighted Restoration
        weights = np.zeros_like(window)
        spatial_dist = np.zeros_like(window)
        
        # Calculate spatial Euclidean distance weights
        for wy in range(self.w):
            for wx in range(self.w):
                dist = (wy - self.pad)**2 + (wx - self.pad)**2
                # Adaptive weight based on intensity difference and spatial distance
                intensity_diff = abs(window[wy, wx] - center_val)
                weights[wy, wx] = 1.0 / (1.0 + intensity_diff * dist / self.h + 1e-6)
        
        # Exclude the center pixel itself from calculation if it's noise
        weights[self.pad, self.pad] = 0
        
        # Normalize
        total_weight = np.sum(weights)
        if total_weight > 0:
            restored_val = np.sum(window * weights) / total_weight
            output_img[i, j] = int(restored_val)
        else:
            # Fallback to median if weights fail
            output_img[i, j] = int(np.median(window))
