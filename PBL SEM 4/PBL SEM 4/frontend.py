import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Constraints fro real life visualisation
PLATFORM_FEE = 10.0
TAX_RATE = 0.20

class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PBL Sem 4: Hybrid Stock Analyzer Bridge")
        self.root.geometry("1150x880")
        self.root.configure(bg="#FAFAFA")
        
        # Header System
        header = tk.Label(root, text="HYBRID STOCK ANALYZER (C BACKEND -> PYTHON FRONTEND)", 
                          font=("Courier", 14, "bold"), bg="#FAFAFA", fg="#111111")
        header.pack(pady=10)
        
        #  Input Area
        input_frame = tk.LabelFrame(root, text=" 1. Global Price Vector Array Entry ", 
                                    font=("Courier", 10, "bold"), bg="#FFFFFF", bd=1, relief="solid")
        input_frame.pack(fill="x", padx=20, pady=5)
        
        lbl = tk.Label(input_frame, text="Enter comma or space separated prices:", 
                       font=("Courier", 9), bg="#FFFFFF", fg="#666666")
        lbl.pack(anchor="w", padx=10, pady=5)
        
        default_vector = "100, 115, 102, 117, 121, 119, 108, 122, 120, 124, 112, 111, 114"
        self.price_input = tk.Text(input_frame, height=2, font=("Courier", 11), bd=1, relief="solid")
        self.price_input.insert("1.0", default_vector)
        self.price_input.pack(fill="x", padx=10, pady=5)
        
        btn = tk.Button(input_frame, text="EXECUTE NATIVE C-BACKEND (STOCK.EXE)", font=("Courier", 10, "bold"), 
                        bg="#111111", fg="#FFFFFF", activebackground="#333333", activeforeground="#FFFFFF",
                        command=self.run_c_backend, relief="flat", padx=15, pady=5)
        btn.pack(pady=10)

        #  Mathematical Graph Display
        self.chart_frame = tk.LabelFrame(root, text=" 2. Mathematical Function Coordinate System ", 
                                         font=("Courier", 10, "bold"), bg="#FFFFFF", bd=1, relief="solid")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        #  C-Output Reports and calculations
        output_frame = tk.LabelFrame(root, text=" 3. Performance Yields & Transaction Calculation Breakdown ", 
                                     font=("Courier", 10, "bold"), bg="#FFFFFF", bd=1, relief="solid")
        output_frame.pack(fill="x", padx=20, pady=10)
        
        # Net Profits Display Bar
        results_grid = tk.Frame(output_frame, bg="#FFFFFF")
        results_grid.pack(fill="x", padx=10, pady=5)
        
        self.greedy_lbl = tk.Label(results_grid, text="NET GREEDY PROFIT: —", font=("Courier", 11, "bold"), fg="#117744", bg="#FFFFFF")
        self.greedy_lbl.pack(side="left", expand=True, anchor="w")
        
        self.dp_lbl = tk.Label(results_grid, text="NET DP PROFIT: —", font=("Courier", 11, "bold"), fg="#115588", bg="#FFFFFF")
        self.dp_lbl.pack(side="right", expand=True, anchor="e")
        
        # Calculation Ledger Area (Replaces raw terminal transcript output box)
        self.ledger_text = tk.Text(output_frame, height=8, font=("Courier", 10), bg="#FAFAFA", bd=1, relief="solid", state="disabled")
        self.ledger_text.pack(fill="x", padx=10, pady=10)
        
        self.canvas = None
        self.run_c_backend()

    def calculate_and_log_transactions(self, prices):
        """Simulates logic internally to map chart elements and format transaction-by-transaction metrics."""
        ledger_entries = []
        g_txs = []
        
        ledger_entries.append("**********************************************************************************************************************")
        ledger_entries.append("                     BRUTE-FORCE GREEDY TRANSACTION OVERHEAD LEDGER")
        ledger_entries.append("**********************************************************************************************************************")
        ledger_entries.append(f"{'TX_LOOP':<8} | {'BUY_NODE':<10} | {'SELL_NODE':<11} | {'GROSS_PROFIT':<13} | {'STCG_TAX':<9} | {'NET_YIELD':<10}")
        ledger_entries.append("-" * 90)
        
        tx_count = 1
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                gross_tx_profit = (prices[i] - PLATFORM_FEE) - (prices[i-1] + PLATFORM_FEE)
            
                tax = gross_tx_profit * TAX_RATE if gross_tx_profit > 0 else 0
                net = gross_tx_profit - tax
                g_txs.append({"buy": i-1, "sell": i})
                ledger_entries.append(
                    f"Tx #{tx_count:<4} | "
                    f"D{i:<2} @ {prices[i-1]:<5.1f} | "
                    f"D{i+1:<2} @ {prices[i]:<6.1f} | "
                    f"{gross_tx_profit:<13.1f} | "
                    f"{tax:<9.1f} | "
                    f"{net:<10.1f} INR"
                )
                tx_count += 1
        
        if tx_count == 1:
            ledger_entries.append(" [NOTICE] No single discrete day intervals crossed required platform breakeven floors.")
            
        # Dynamic Programming Single Leg Optimization Processing Matrix Tracker
        min_idx, min_cost, max_dp, dp_tx = 0, prices[0] + PLATFORM_FEE, 0.0, {"buy": -1, "sell": -1}
        for i in range(1, len(prices)):
            gross = (prices[i] - PLATFORM_FEE) - min_cost
            if gross > 0:
                net = gross - (gross * TAX_RATE)
                if net > max_dp:
                    max_dp = net
                    dp_tx = {"buy": min_idx, "sell": i}
            if (prices[i] + PLATFORM_FEE) < min_cost:
                min_cost = prices[i] + PLATFORM_FEE
                min_idx = i
                
        ledger_entries.append("\n**********************************************************************************************************************")
        ledger_entries.append("                     OPTIMIZED DYNAMIC PROGRAMMING POSITION LEDGER")
        ledger_entries.append("**********************************************************************************************************************")
        if dp_tx["buy"] != -1:
            dp_gross = (prices[dp_tx["sell"]] - PLATFORM_FEE) - (prices[dp_tx["buy"]] + PLATFORM_FEE)
            dp_tax_val = dp_gross * TAX_RATE
            ledger_entries.append(
                f"Opt Position -> Buy Node: Day {dp_tx['buy']+1} ({prices[dp_tx['buy']]:.1f} INR) | "
                f"Sell Node: Day {dp_tx['sell']+1} ({prices[dp_tx['sell']]:.1f} INR)"
            )
            ledger_entries.append(
                f"             -> Gross: {dp_gross:.1f} INR | "
                f"STCG Tax Deducted: {dp_tax_val:.1f} INR | "
                f"Net Profit Realized: {max_dp:.1f} INR"
            )
        else:
            ledger_entries.append(" [NOTICE] Asset trend values failed to unlock structural breakeven lines.")
        ledger_entries.append("**********************************************************************************************************************")
            
        return g_txs, dp_tx, "\n".join(ledger_entries)

    def run_c_backend(self):
        raw_data = self.price_input.get("1.0", "end-1c")
        prices = [float(x.strip()) for x in raw_data.replace(",", " ").split() if x.strip()]
        
        if len(prices) < 2:
            messagebox.showerror("Execution Error", "Insufficient price elements inside array vector.")
            return

        # 1. Write current input parameters directly down to disk
        prices_str = " ".join(map(str, [int(p) for p in prices]))
        with open("prices.txt", "w") as f:
            f.write(prices_str)

        exe_path = "./stock.exe"
        if not os.path.exists(exe_path):
            self.ledger_text.configure(state="normal")
            self.ledger_text.delete("1.0", "end")
            self.ledger_text.insert("1.0", f"CRITICAL INTERFACE ERROR: Local binary source '{exe_path}' missing from directory environment.\n\nCompile your C codebase files via terminal using:\ngcc main.c data.c display.c dp.c fileio.c graph.c greedy.c analysis.c -o stock.exe")
            self.ledger_text.configure(state="disabled")
            return

        # 2. Spawn and execute background C binary process via pipes
        input_commands = "3\n3\n5\n"
        try:
            process = subprocess.Popen(
                [exe_path],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True
            )
            process.communicate(input=input_commands)
            time.sleep(0.05) # Yield thread briefly to flush drive IO streams

            # 3. Read variables generated inside result.txt by your fileio.c file
            greedy_profit, dp_profit = 0, 0
            if os.path.exists("result.txt"):
                with open("result.txt", "r") as rf:
                    for line in rf.readlines():
                        if "Greedy Profit:" in line:
                            greedy_profit = int(line.split(":")[-1].strip())
                        if "DP Profit:" in line:
                            dp_profit = int(line.split(":")[-1].strip())

            # Update numeric display panels
            self.greedy_lbl.configure(text=f"NET GREEDY PROFIT (FROM C-BACKEND): {greedy_profit} INR")
            self.dp_lbl.configure(text=f"NET DP PROFIT (FROM C-BACKEND): {dp_profit} INR")
            
            # 4. Generate ledger mathematical calculations matrix details
            g_txs, dp_tx, calculation_ledger = self.calculate_and_log_transactions(prices)
            
            # Output calculations sheet directly inside text box widget framework
            self.ledger_text.configure(state="normal")
            self.ledger_text.delete("1.0", "end")
            self.ledger_text.insert("1.0", calculation_ledger)
            self.ledger_text.configure(state="disabled")

            # 5. Render Math Chart
            self.plot_mathematical_graph(prices, g_txs, dp_tx)

        except Exception as e:
            messagebox.showerror("Pipeline Linking Error", str(e))

    def plot_mathematical_graph(self, prices, g_txs, dp_tx):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(10, 4.0), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F9F9F9')

        days = [f"D{i+1}" for i in range(len(prices))]
        ax.plot(days, prices, color='#111111', linewidth=1.5, label='Price Curve', zorder=1)

        # Draw the mathematical breakeven line projection threshold from the initial entry anchor coordinates
        breakeven_val = prices[0] + (2 * PLATFORM_FEE)
        ax.axhline(y=breakeven_val, color='#FF453A', linestyle='--', linewidth=1.5, label='f(x) Breakeven Floor')

        greedy_buys = [t["buy"] for t in g_txs]
        greedy_sells = [t["sell"] for t in g_txs]

        # Apply strategy visual indicator markers onto the line graph coordinates
        for i in range(len(prices)):
            if i == dp_tx["buy"]:
                ax.scatter(days[i], prices[i], color='#FF9F0A', marker='s', s=100, label='DP Buy (Orange)' if i==dp_tx["buy"] else "", zorder=3)
            elif i == dp_tx["sell"]:
                ax.scatter(days[i], prices[i], color='#0A84FF', marker='s', s=100, label='DP Sell (Blue)' if i==dp_tx["sell"] else "", zorder=3)
            elif i in greedy_buys:
                ax.scatter(days[i], prices[i], color='#117744', marker='^', s=90, label='Greedy Buy (Green)' if i==greedy_buys[0] else "", zorder=2)
            elif i in greedy_sells:
                ax.scatter(days[i], prices[i], color='#CC3300', marker='v', s=90, label='Greedy Sell (Red)' if i==greedy_sells[0] else "", zorder=2)
            else:
                ax.scatter(days[i], prices[i], color='#CCCCCC', marker='o', s=25, zorder=1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=8)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend(loc="upper left", prop={'family': 'monospace', 'size': 8})

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalyzerApp(root)
    root.mainloop()