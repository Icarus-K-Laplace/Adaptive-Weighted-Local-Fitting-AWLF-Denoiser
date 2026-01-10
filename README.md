# Adaptive-Weighted-Local-Fitting-AWLF-Denoiser
Adaptive Weighted Local Fitting (AWLF) denoiser for salt-and-pepper noise: combines local statistics, gradient cues, and robust trimming to adaptively blend polynomial fitting with median restoration. Built for transparent, reproducible evaluation across noise levels, prioritizing honest baselines over hype.
**A robust image restoration algorithm for high-density salt-and-pepper noise removal.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 Overview

The **Adaptive Weighted Local Fitting (AWLF)** denoiser is a hybrid algorithm designed to restore images corrupted by impulse noise (salt-and-pepper). unlike standard median filters, AWLF preserves fine details and edges by dynamically switching between **polynomial fitting** and **robust statistical estimation** based on local image features.

This approach performs exceptionally well even under **extreme noise conditions (up to 80% density)**, maintaining structural integrity where traditional methods fail.

##Algorithm Logic
AWLF (Adaptive Weighted Local Fitting) targets salt-and-pepper (impulse) noise. The pipeline restores only pixels marked as noisy by a binary mask, and decides per-pixel whether to trust a polynomial fit (detail-preserving) or median estimate (robust).

Inputs / Outputs
Input: grayscale image I in [0, 255]
Input: noise mask M where M[x, y] = 1 means “isy pixel”
Output: restored image R
1) Local feature map (computed once per image)
We compute lightweight local features used to derive an adaptive restoration weight:

Local mean via 3x3 box blur.
Local contrast via local std (from blurred I^2 - mean^2).
“Intensity score” = sigmoid(z-score) where z-score is (I - local_mean) / local_std.
This is a statistical normalization, not physical temperature.
Edge strength = normalized Sobel gradient magnitude.
High-intensity mask = pixels above the image 85th percentile.
Local consistency = 1 - std(neighborhood(intensity_score)).
2) Adaptive weight per noisy pixel
For each noisy pixel (x, y), compute a scalar w that controls how strongly the algorithm trusts fitting:

Base weight increases with the intensity score.
Bright-region boost: if high-intensity mask is true, increase weight.
Edge suppression: if edge strength is high, reduce weight (be conservative on edges).
Consistency factor: more stable neighborhoods increase weight.
Final w is clamped to a safe range (e.g., [0.01, 20.0]).
Interpretation:

Larger w → trust polynomial fitting more.
Smaller w → trust median more.
3) Collect valid neighbors (ignore noisy pixelsFor each noisy pixel, search window sizes in {3, 5, 7}:
Gather neighbor values where mask == 0 (non-noisy).
Stop early when the number of valid pixels reaches min_valid_pixels (default 5).
If not enough valid pixels are found in all windows, fall back to a small-window median.
4) Robust local fitting + median blending (core restoration)
Given valid neighbor values V:

Sort V and optionally trim extremes (trim ratio decreases as w increases).
Choose fit complexity:
If few samples: use linear fit
If enough samples: use cubic fit
Compute:
neighbor_median = median(V)
fit_median = median(fitted_values) (after polynomial fitting)
Decision rule (this is the original core logic and is intentionally kept):

If w > 8.0: use fit_median
Else if w < 0.3: use neighbor_median
Else: linearly fit_median and neighbor_median with alpha = (w - 0.3) / 7.7
Finally clamp the restored value to [0, 255].
Practical notes
The method is designed for impulse noise; it is not intended for Gaussian noise.
Performance depends on noise-mask quality: missed noisy pixels remain corrupted; false positives blur clean details.
Runtime is dominated by per-noisy-pixel neighborhood search and local fitting; high noise density increases compute time.
## 🚀 Key Features

*   **Hybrid Restoration Strategy**: Seamlessly blends polynomial fitting (for edges/details) and median filtering (for smooth regions).
*   **Adaptive Weighting**: Calculates pixel-wise weights based on:
    *   Local Gradient Magnitude (Edge Strength)
    *   Local Contrast (Standard Deviation)
    *   Normalized Intensity (Z-Score)
*   **Robustness**: Effective removal of noise from 20% up to 80% density.
*   **Detail Preservation**: Minimizes the "blurring" artifact common in standard median filters.

## 📊 Performance

Benchmark results on infrared scene data (PSNR/SSIM/FSIM):

| Noise Density | PSNR (dB) | SSIM | FSIM (%) | Improvement (vs Baseline) |
|:---:|:---:|:---:|:---:|:---:|
| **20%** | **33.42** | **0.9796** | **99.87** | +20.73 dB / +0.89 SSIM |
| **40%** | **31.55** | **0.9555** | **99.80** | +21.66 dB / +0.91 SSIM |
| **80%** | **28.19** | **0.8819** | **99.55** | +20.86 dB / +0.86 SSIM |

*> Note: Tested on `scene1.png`. Processing time for 80% noise approx. 170s on CPU (Standard mode).*

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AWLF-Denoiser.git
   cd AWLF-Denoiser
