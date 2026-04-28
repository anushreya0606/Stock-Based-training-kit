# 📈 Stock Buy-Sell Analyzer (PBL Sem 4)

A **full-stack hybrid Data Structures & Algorithms project** combining:

* 🧠 Python (Frontend + UI using Tkinter)
* ⚙️ C (Backend for high-performance computation via subprocess)
* 📊 Multiple DSA algorithms for stock profit analysis

---

## 🚀 Project Overview

This project simulates a **stock market analysis system** that compares multiple algorithmic approaches to the Buy-Sell problem using real stock price data.

It features a **rich GUI built with Tkinter** and integrates a **C backend executable** for optimized computation, demonstrating real-world hybrid system design.

---

## 🎯 Key Objectives

* Implement and compare multiple DSA algorithms on stock data
* Build a professional GUI using Python Tkinter
* Integrate C backend using Python `subprocess`
* Demonstrate performance differences between algorithms
* Maintain per-user history with duplicate detection
* Visualize results using Matplotlib

---

## 🧠 Algorithms Implemented

### 1. Greedy Algorithm (O(n))

* Multiple transactions allowed
* Adds all profitable differences

### 2. Dynamic Programming (O(n))

* Single best buy-sell transaction
* Tracks minimum price and maximum profit

### 3. Graph / Matrix Approach (O(n²))

* Builds adjacency matrix of all profits
* Finds best edge (buy-sell pair)

### 4. Divide & Conquer (O(n log n))

* Recursively splits array
* Combines left, right, and cross profits

### 5. Kadane’s Algorithm (O(n))

* Applied on price differences
* Finds maximum subarray gain

---

## ⚙️ System Architecture

```
Python Tkinter GUI  (Frontend)
        │
        ▼
Subprocess Communication
        │
        ▼
C Backend Executable (stock_solver.exe)
        │
        ▼
Hybrid Result Aggregation (Python)
```

---

## 🖥️ Features

### 🎨 UI Features (Tkinter)

* Modern multi-panel dashboard
* Login screen (open authentication)
* Collapsible result sections
* Animated stock price chart
* Hover tooltips on graph
* Transaction timeline visualization
* Profit comparison bars
* Backpropagation visualizer (ML simulation)

---

### 📊 Functional Features

* Greedy vs DP vs Graph vs D&C vs Kadane comparison
* Real-time chart animation
* Buy/Sell signal visualization
* Price matrix heatmap
* Execution history tracking
* Duplicate analysis detection

---

### ⚙️ Backend Integration

* C executable used for:

  * Greedy computation
  * DP computation
  * Graph-based profit
* Python fallback if C backend is unavailable

---

## 📂 Project Structure

```
Stock-Based-training-kit/
│
├── stock_analyzer_gui.py      # Main Python Tkinter UI
├── stock_solver.c/.exe        # C backend (compiled)
├── analysis_history.json      # Saved user analysis history
│
├── assets/                    # (optional images/resources)
├── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/anushreya0606/Stock-Based-training-kit.git
cd Stock-Based-training-kit
```

---

### 2. Install Python Dependencies

```bash
pip install matplotlib
```

---

### 3. Compile C Backend (if needed)

If you have `stock_solver.c`:

```bash
gcc stock_solver.c -o stock_solver.exe
```

Update path in Python:

```python
C_BACKEND_PATH = "path_to_stock_solver.exe"
```

---

### 4. Run Application

```bash
python stock_analyzer_gui.py
```

---

## 🧪 How It Works

1. User enters stock prices
2. Selects trading mode
3. Python GUI processes input
4. Optional C backend executes optimized logic
5. Python aggregates all algorithm outputs
6. Results displayed via:

   * Charts
   * Tables
   * Animated graphs
   * Comparison bars

---

## 📊 Visual Components

* 📈 Live stock line chart with BUY/SELL markers
* 🧮 Profit matrix (graph algorithm)
* 📊 Bar comparison of algorithms
* 🔁 Transaction timeline (step-by-step)
* 🧠 Neural-style backprop visualization

---

## 🧠 Learning Outcomes

This project demonstrates:

* Algorithm complexity comparison
* Hybrid system design (C + Python)
* GUI development with Tkinter
* Data visualization with Matplotlib
* Subprocess communication in Python

---

## 🔮 Future Enhancements

* Replace Tkinter with React / Streamlit dashboard
* Add real stock API (Yahoo Finance / Alpha Vantage)
* Convert backend into full C++ high-performance engine
* Add database (SQLite / Firebase)
* Add LSTM deep learning prediction module

---

## 👨‍💻 Author

**Anushreya Tomar**
GitHub: [https://github.com/anushreya0606](https://github.com/anushreya0606)

---

## ⚠️ Disclaimer

This project is for **educational and academic purposes only**. It is not financial advice and should not be used for real trading decisions.
