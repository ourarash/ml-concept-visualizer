# 🧠 ML Concept Visualizer

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=flat-square)](https://ourarash.github.io/ml-concept-visualizer/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#)

> **Interactive visualizations for machine learning, deep learning, and performance-engineering concepts used in lectures.**

**By Arash Saifhashemi**

## 🌐 [View All Visualizations](https://ourarash.github.io/ml-concept-visualizer/)

Browse the full catalog of interactive visualizations on the **[live website](https://ourarash.github.io/ml-concept-visualizer/)** or explore them directly by opening the HTML files in your browser.

## ✨ Features

- 🎯 **Interactive Visualizations** covering ML fundamentals to advanced optimization
- 📱 **Fully Responsive** - works on desktop, tablet, and mobile
- 🎨 **No Installation Required** - runs entirely in your browser
- 📚 **Educational Focus** - designed for teaching and learning
- ⚡ **Real-time Interaction** - adjust parameters and see immediate results

## 📂 Visualization Categories

### 📊 Classical ML & Clustering

Traditional machine learning algorithms, evaluation metrics, and clustering methods

- Classification Metrics Explorer (Accuracy, Precision, Recall, F1, ROC, PR curves)
- Decision Trees, KNN, Logistic Regression, SVM
- Neural Network Classification
- K-Means & Hierarchical Clustering

### 🧩 CNN Architectures

Convolutional neural networks and deep learning building blocks

- Convolution operations and output formulas
- neuFlow 3×3 convolution hardware dataflow
- Pooling strategies (max, average)
- ResNet architecture and bottleneck blocks
- 1×1 convolutions and dimensionality reduction

### 📚 ML Fundamentals

Core concepts essential for understanding modern ML

- Softmax activation function
- Internal covariate shift and batch normalization
- Backpropagation and the chain rule
- Mathematical foundations

### 🗣️ NLP & Language Models

Interactive visualizations spanning classical text representations to modern language models

- Bag of Words, TF-IDF, and N-gram language modeling
- Word embeddings, cosine similarity, and sentence embeddings
- RNNs, LSTMs, Seq2Seq encoder-decoder pipelines, and cross-attention
- Pretraining, transfer learning, BERT, and the historical progression of language models
- Transformer internals including RoPE, KV cache, prefill/decode, FlashAttention, paged attention, and masked attention
- Decoding and alignment methods including greedy/beam search, temperature, top-k/top-p sampling, contrastive decoding, speculative decoding, perplexity, and RLHF

### 🧮 Quantization

Numeric formats and quantized inference/training concepts

- Quantization basics: scale, zero-point, clipping, rounding, and reconstruction error
- Floating-point format explorer for FP32, BF16, FP16, and FP8 variants
- Quantization-aware training and fake-quantization gradient flow
- Calibration, granularity, and INT8 deployment tradeoffs

### ⚡ GEMM Optimization

General Matrix Multiply optimization techniques

- Baseline vs. tiled implementations
- Strassen's Matrix Multiplication algorithm
- Cache cliff analysis
- Cache miss derivations (tiled and non-tiled)
- Interactive tiling visualizers
- img2col transformation pattern

### 🚀 AI Accelerators & CPU Architectures

Deep dive into hardware design for machine learning

- **CISC vs RISC vs VLIW:** Comparing CPU architecture philosophies
- **TPU v1 & v7 Architectures:** Interactive block diagrams and dataflow deep dives
- **Systolic Arrays:** The heart of matrix multiplication units
- **TPU Programming Model:** Visualizing CISC-like instruction sets for accelerators
- **Vector Units:** SIMD and vector processing specialized for ML
- **Array vs. Vector Processors:** Visualizing space-time mapping and execution differences
- **Vector ILP:** Accumulation of vector chunks and pipeline throughput
- **SIMT & GPU Warps:** Visualizing SPMD execution on hardware lanes
- **Branch Divergence Profiler:** Measuring throughput and utilization in divergent kernels
- **CUDA Branch Divergence Hardware Masking:** Active-mask, program-counter, and efficiency tracking
- **Dynamic Warp Formation:** Comparing baseline SIMT execution against warp regrouping
- **CUDA Architecture & Execution Flow:** Thread hierarchy, hardware layout, and host/device orchestration
- **Tensor Cores & Memory Coalescing:** Specialized execution units and memory-transaction behavior
- **AoS vs. SoA:** How data layout influences memory behavior and vector efficiency
- **Shared Memory Bank Conflicts:** Strides, broadcasts, multicast, and padding fixes
- **CUDA Streams:** Overlapping transfers and kernel execution across streams

### 🔥 Kernel Optimization

Data reuse and computational efficiency patterns

- Spatial and temporal reuse
- Data movement optimization
- Loop-nest transformations

### 💾 Cache & Memory Optimization

Understanding the memory hierarchy

- Cache hierarchy concepts
- Memory access patterns
- Performance implications

### 🔄 Dataflow Patterns

Hardware execution patterns for neural networks

- Input-stationary dataflow
- Output-stationary dataflow
- Weight-stationary dataflow
- Weight-stationary accelerator (8 PE parallel)
- Simplified NVDLA convolution dataflow

### 📈 Performance Modeling

Analyzing and predicting system performance

- Roofline model visualization
- Performance bounds and bottlenecks

## 📁 Repository Structure

```
ml-concept-visualizer/
├── index.html                          # Main landing page
├── fundamentals/                       # Core ML concepts
├── nlp/                                # NLP, embeddings, sequence models, and language-model visualizations
├── quantization/                       # Numeric formats, quantization, and QAT visualizations
├── classical-ml-classification/        # Traditional ML algorithms
├── cnn-architectures/                  # Deep learning & CNNs
├── gemm-optimization/                  # Matrix multiplication optimization
│   ├── strassen.html
│   ├── systolic-array.html
│   └── ...
├── gpu/                                # GPU, SIMT, and CUDA architecture visualizations
│   ├── flynn-taxonomy.html
│   ├── memory-banks.html
│   ├── nvidia/
│   │   ├── bank-conflicts.html
│   │   ├── cuda-execution-architecture.html
│   │   ├── cuda-execution-flow.html
│   │   ├── cuda-hardware-memory-architecture.html
│   │   ├── cuda-memory-coalescing.html
│   │   ├── nvidia-multithreading.html
│   │   └── cuda-snippets/
│   └── ...
├── gradient-descent/                   # Optimization and training dynamics
│   ├── back-propagation.html
│   └── ...
├── tpu/                                # AI Accelerators
│   ├── tpu1.html                       # TPU Block Diagram
│   ├── tpu-v1-programming-model.html   # TPU Instruction Flow
│   ├── vliw.html                       # CISC vs RISC vs VLIW
│   ├── tpu-vector-unit.html
│   └── ...
├── kernel-optimization/                # Kernel-level optimizations
├── cache-optimization/                 # Memory hierarchy
├── dataflow-loop-nests/               # Hardware dataflow patterns
├── scripts/                            # Repo consistency checks
├── .github/workflows/                  # Automated consistency checks
└── performance-modeling/               # Performance analysis
```

## 🚀 Quick Start

### Option 1: View Online (Recommended)

Visit the **[live website](https://ourarash.github.io/ml-concept-visualizer/)** to browse all visualizations.

### Option 2: Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/ourarash/ml-concept-visualizer.git
   cd ml-concept-visualizer
   ```

2. Open any HTML file in your browser:

   ```bash
   # macOS
   open index.html
   ```

## 🤝 Contributing

Contributions are welcome! Please follow the existing folder structure and naming conventions.

## 🌟 Acknowledgments

Created by **Arash Saifhashemi** for educational purposes in ML/DL and systems optimization courses.

---

**⭐ Star this repo** if you find it helpful!
