# Adaptive-Weighted-Local-Fitting-AWLF-Denoiser
Adaptive Weighted Local Fitting (AWLF) denoiser for salt-and-pepper noise: combines local statistics, gradient cues, and robust trimming to adaptively blend polynomial fitting with median restoration. Built for transparent, reproducible evaluation across noise levels, prioritizing honest baselines over hype.
**A robust image restoration algorithm for high-density salt-and-pepper noise removal.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 Overview

The **Adaptive Weighted Local Fitting (AWLF)** denoiser is a hybrid algorithm designed to restore images corrupted by impulse noise (salt-and-pepper). unlike standard median filters, AWLF preserves fine details and edges by dynamically switching between **polynomial fitting** and **robust statistical estimation** based on local image features.

This approach performs exceptionally well even under **extreme noise conditions (up to 80% density)**, maintaining structural integrity where traditional methods fail.
A clean, educational, pure Python implementation of the Adaptive Weighted Local Filter algorithm for image restoration. This repository serves as a reference for understanding the underlying mathematics and logic of adaptive filtering.

> **⚠️ Performance Notice**
>
> This is a **reference implementation** optimized for readability, NOT for speed.
> *   **Execution Time**: ~1-3 seconds per frame (512x512) on CPU.
> *   **Data Support**: 8-bit Grayscale/RGB only.
>
> 🚀 **Need Real-time Performance for Industrial Use?**
>
> Please check out [**AWLF-Fast**](https://github.com/Icarus-K-Laplace/AWLF-Fast-Universal) (GPL-3.0).
> The Fast edition features:
> *   **60+ FPS** real-time processing via Numba JIT & Parallelization.
> *   **16-bit / RAW** data support for thermal imaging.
> *   **Memory optimization** for edge devices.
---


## 🧠 Algorithm Pipeline (Theoretical Framework)

This reference implementation follows a 4-stage restoration strategy designed to balance detail preservation with robust noise suppression.

### 1. Inputs & Outputs
*   **Input**: Grayscale image $I \in [0, 255]$
*   **Input**: Noise mask $M$ (where $M(x,y)=1$ indicates impulse noise)
*   **Output**: Restored image $\hat{I}$

### 2. Core Steps

#### Step 1: Local Feature Extraction
We compute lightweight statistical features to guide the restoration process. Unlike physical temperature, we use statistical normalization:
*   **Local Mean ($\mu$)**: Computed via $3\times3$ box blur.
*   **Local Contrast ($\sigma$)**: Standard deviation of the neighborhood.
*   **Intensity Score**: $S = \text{sigmoid}(\frac{I - \mu}{\sigma})$.
*   **Edge Strength**: Normalized Sobel gradient magnitude.

#### Step 2: Adaptive Weighting
For each noisy pixel, a scalar weight $w$ is derived to determine the restoration strategy. The weight is dynamically adjusted:
*   **$w \uparrow$ (Increase)**: In bright regions (high-intensity mask) or statistically consistent neighborhoods.
*   **$w \downarrow$ (Decrease)**: On strong edges to prevent blurring.

> *Interpretation*: Larger $w$ implies higher confidence in the local structure, favoring polynomial fitting. Smaller $w$ favors conservative median filtering.

#### Step 3: Valid Neighbor Collection
The algorithm performs an iterative search (Window sizes: $3 \to 5 \to 7$) to gather valid (non-noisy) pixels $V$.
*   If $|V| < \text{min\_pixels}$, the search expands.
*   This iterative search ensures robustness even in high-density noise scenarios ($>80\%$).

#### Step 4: Hybrid Restoration (Fitting + Blending)
The final pixel value is computed using a hybrid approach:
1.  **Robust Fitting**: Perform Linear or Cubic polynomial fitting on set $V$ to estimate $\hat{I}_{fit}$.
2.  **Median Filtering**: Compute standard median $\hat{I}_{med} = \text{median}(V)$.
3.  **Decision Rule**:
    $$
    \hat{I}(x,y) = 
    \begin{cases} 
    \hat{I}_{fit} & \text{if } w > 8.0 \quad \text{(Trust Structure)} \\
    \hat{I}_{med} & \text{if } w < 0.3 \quad \text{(Trust Median)} \\
    \alpha \hat{I}_{fit} + (1-\alpha) \hat{I}_{med} & \text{otherwise} \quad \text{(Linear Blend)}
    \end{cases}
    $$

---

## ⚠️ Complexity Note

As seen in the pipeline above, the algorithm involves **pixel-wise polynomial fitting** and **iterative neighborhood search**. 

In this **pure Python reference implementation**, these operations are computationally expensive (~1.5s per frame). 

👉 **For industrial applications**, my [**AWLF-Fast**](https://github.com/Icarus-K-Laplace/AWLF-Fast-Universal) edition uses **SIMD vectorization**, **lookup tables**, and **JIT compilation** to achieve **real-time performance (60+ FPS)** while maintaining the same mathematical rigor.


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
## Dataset

Experiments are conducted on the **Tianjin University open UAV remote-sensing infrared grayscale image dataset**.

- Dataset ID (CSTR): `CSTR:14804.11.sciencedb.space.00579`
- Link: https://cstr.cn/14804.11.sciencedb.space.00579
- Note: This repository does **not** redistribute the dataset files. Please download it from the official source and comply with its license/terms.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AWLF-Denoiser.git
   cd AWLF-Denoiser
### High-level Pseudocode
```text
features = compute_features(I)

for each (x, y) where M[x, y] == 1:
    w = compute_weight(features, x, y)

    V = collect_valid_neighbors(I, M, x, y, windows=[3,5,7], min_valid=5)
    if V is empty:
        R[x, y] = median(neighborhood(I, x, y, 3))
        continue

    neighbor_median = median(V)
    fit_median = median(polyfit_values(V, w))

    if w > 8.0:
        R[x, y] = fit_median
    else if w < 0.3:
        R[x, y] = neighbor_median
    else:
        alpha = (w - 0.3) / 7.7
        R[x, y] = alpha * fit_median + (1 - alpha) * neighbor_median

    R[x, y] = clamp(R[x, y], 0, 255)
