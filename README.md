# Adaptive-Weighted-Local-Fitting-AWLF-Denoiser
Adaptive Weighted Local Fitting (AWLF) denoiser for salt-and-pepper noise: combines local statistics, gradient cues, and robust trimming to adaptively blend polynomial fitting with median restoration. Built for transparent, reproducible evaluation across noise levels, prioritizing honest baselines over hype.
**A robust image restoration algorithm for high-density salt-and-pepper noise removal.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 Overview

The **Adaptive Weighted Local Fitting (AWLF)** denoiser is a hybrid algorithm designed to restore images corrupted by impulse noise (salt-and-pepper). unlike standard median filters, AWLF preserves fine details and edges by dynamically switching between **polynomial fitting** and **robust statistical estimation** based on local image features.

This approach performs exceptionally well even under **extreme noise conditions (up to 80% density)**, maintaining structural integrity where traditional methods fail.

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
