#  Stock Buy-Sell Analyzer (PBL Sem 4)

A **full-stack hybrid Data Structures & Algorithms project** combining:

*  Python (Frontend + UI using Tkinter)
*  C (Backend for high-performance computation via subprocess)
*  Multiple Greedy and DP algos.

---

##  Project Overview

This project simulates a **stock market analysis system** that compares multiple algorithmic approaches to the Buy-Sell problem using real stock price data.

It features a **rich GUI built with Tkinter** and integrates a **C backend executable** for optimized computation, demonstrating real-world hybrid system design.

---

## Key Objectives

* Implement and compare multiple DSA algorithms on stock data
* Build a professional GUI using Python Tkinter
* Integrate C backend using Python `subprocess`
* Demonstrate performance differences between algorithms
* Maintain per-user history with duplicate detection
* Visualize results using Matplotlib

---

## Algorithms Implemented

### 1. Brute force Greedy Algorithm

* Multiple transactions allowed
* Adds all profitable differences

### 2. Smart optimised DP (Dynamic Programming)

* Single best buy-sell transaction
* Tracks minimum price and maximum profit

---

## System Architecture

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

##  Features

###  UI Features (Tkinter)


* Animated stock price chart
* Expanded, high-visibility mathematical chart canvas.
* Profit comparison 

---

### Functional Features

* Greedy vs DP 
* Real-time chart visualization
* Execution history 

---

###  Backend Integration

* C executable used for:

  * Greedy computation
  * DP computation
  * Graph-based profit
* Python fallback if C backend is unavailable

---

##  Project Structure

```
Stock-Based-training-kit/
│
├── frontend.py                # Main Python Tkinter interface and Matplotlib engine
├── main.c                     # C architecture coordinating menus and pipes
├── data.c                     # Ingests vector parameters from prices.txt
├── dp.c                       # Contains the friction-adjusted DP state logic
├── greedy.c                   # Contains the friction-adjusted Greedy loop logic
├── display.c                  # Textual asset curve handling
├── graph.c                    # State profit matrix logic
├── analysis.c                 # Compares algorithms and handles thresholds
├── fileio.c                   # Writes results out to result.txt
│
├── prices.txt                 # Intermediate data bridge file used by C loaders
├── result.txt                 # Final output metrics read by Python
├── stock.exe                  # Compiled high-performance C binary executable
└── README.md                  # Project system documentation
```

---

##  Installation & Setup

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

```bash
gcc main.c data.c display.c dp.c fileio.c graph.c greedy.c analysis.c -o stock.exe
```

---

### 4. Run Application

```bash
python stock_analyzer_gui.py
```

---

##  How It Works

1. User enters stock prices
2. Python GUI processes input
3. Optional C backend executes optimized logic
4. Python aggregates all algorithm outputs
5. Results displayed via charts

---


---

## Future Enhancements

* Replace Tkinter with React / Streamlit dashboard
* Add real stock API (Yahoo Finance / Alpha Vantage)
* Convert backend into full C++ high-performance engine
* Add database (SQLite / Firebase)
* Add LSTM deep learning prediction module

---

## Author

**Anushreya Tomar**
GitHub: [https://github.com/anushreya0606](https://github.com/anushreya0606)

---

## Disclaimer

This project is for **educational and academic purposes only**. It is not financial advice and should not be used for real trading decisions.
