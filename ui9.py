"""
╔══════════════════════════════════════════════════════════════╗
║   Stock Buy-Sell Analyzer  —  PBL Sem 4  |  DSA Project     ║
║                                                               ║
║   FEATURES:                                                   ║
║   ✦ Open login — any username works, no fixed password       ║
║   ✦ All sections collapsible (Results, Matrix, Bars, etc.)   ║
║   ✦ Algorithm 1: Greedy         O(n)  multiple trades        ║
║   ✦ Algorithm 2: DP             O(n)  single trade           ║
║   ✦ Algorithm 3: Graph Matrix   O(n²) single trade           ║
║   ✦ Algorithm 4: Divide&Conquer O(n log n) single trade      ║
║   ✦ Algorithm 5: Kadane's Algo  O(n)  max-subarray variant   ║
║   ✦ Backpropagation visualizer                               ║
║   ✦ Per-user history with duplicate detection                ║
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
    pip install matplotlib
    python stock_analyzer_gui.py
"""

import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import subprocess, os, json, hashlib, math, random
from datetime import datetime

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
C_BACKEND_PATH = r"C:\Users\anushreya\OneDrive\Desktop\PBL SEM 4\stock_solver.exe"
HISTORY_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis_history.json")

# ── Main app colours ─────────────────────────────────────────
BG        = "#F2EFE9"
SURFACE   = "#FFFFFF"
SURFACE2  = "#EDEBE5"
BORDER    = "#D8D3CB"
INK       = "#1A1612"
INK_L     = "#7A7268"
ACCENT    = "#C4380A"
GREEN     = "#1A6640"
GREEN_L   = "#D6EFE0"
BLUE      = "#1A4E6E"
GOLD      = "#A06A00"
HDR_BG    = "#111111"
STATUS_BG = "#1A1612"
DP_COLOR  = "#5B2D8E"
TEAL      = "#0D7377"
ROSE      = "#9B2335"   # Kadane colour

# ── Login colours ────────────────────────────────────────────
LG_BG     = "#0A0A0F"
LG_CARD   = "#12121A"
LG_BORDER = "#2A2A3A"
LG_ACCENT = "#FF4500"
LG_GOLD   = "#C9A84C"
LG_TEXT   = "#F0EDE8"
LG_MUTED  = "#666070"
LG_GREEN  = "#00C97B"

# ── Presets ──────────────────────────────────────────────────
PRESETS = {
    "Sample Data" : [100, 180, 260, 310,  40, 535, 695],
    "Bull Run"    : [50,  80,  120, 175, 220, 300, 420, 510],
    "Bear Market" : [800, 650, 500, 380, 300, 200, 150, 100],
    "Volatile"    : [200, 80,  350, 120, 500,  90, 600, 250, 700, 300],
}


# ══════════════════════════════════════════════════════════════
#  HISTORY MANAGER
# ══════════════════════════════════════════════════════════════
class HistoryManager:
    def __init__(self):
        self._data = self._load()

    def _load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE) as f: return json.load(f)
            except: pass
        return {}

    def _save(self):
        try:
            with open(HISTORY_FILE, "w") as f: json.dump(self._data, f, indent=2)
        except Exception as e:
            print(f"[History] {e}")

    def _key(self, prices):
        return hashlib.md5(json.dumps(prices).encode()).hexdigest()

    def find_duplicate(self, prices):
        return self._data.get(self._key(prices))

    def save(self, username, prices, greedy, dp, graph, dc, kadane):
        self._data[self._key(prices)] = {
            "prices": prices, "greedy": greedy, "dp": dp,
            "graph": graph, "dc": dc, "kadane": kadane,
            "user": username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._save()

    def all_records(self): return list(self._data.values())
    def clear(self):       self._data = {}; self._save()


history_mgr = HistoryManager()


# ══════════════════════════════════════════════════════════════
#  C BACKEND (optional)
# ══════════════════════════════════════════════════════════════
def call_c_backend(prices):
    if not os.path.exists(C_BACKEND_PATH): return None
    try:
        result = subprocess.run(
            [C_BACKEND_PATH] + [str(p) for p in prices],
            capture_output=True, text=True, timeout=5)
        out = {}
        for line in result.stdout.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = int(v.strip())
        return out.get("GREEDY", 0), out.get("DP", 0), out.get("GRAPH", 0)
    except Exception as e:
        print(f"[C backend] {e}"); return None


# ══════════════════════════════════════════════════════════════
#  ALGORITHMS
# ══════════════════════════════════════════════════════════════

# 1. GREEDY — O(n), multiple transactions
def greedy_profit(prices):
    return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))

# 2. DYNAMIC PROGRAMMING — O(n), single transaction
def dp_profit(prices):
    mn, best = prices[0], 0
    for p in prices[1:]:
        mn = min(mn, p)
        best = max(best, p - mn)
    return best

# 3. GRAPH adjacency matrix — O(n²)
def build_graph(prices):
    n = len(prices)
    return [[prices[j] - prices[i] if j > i else 0 for j in range(n)] for i in range(n)]

def max_profit_graph(g):
    return max((g[i][j] for i in range(len(g)) for j in range(i+1, len(g))), default=0)

# 4. DIVIDE & CONQUER — O(n log n), single transaction
#    Recursively splits array. Max profit = max(left, right, cross).
#    Cross = buy at left-half minimum, sell at right-half maximum.
def _dc_helper(prices, lo, hi):
    if lo >= hi: return 0
    mid          = (lo + hi) // 2
    left_profit  = _dc_helper(prices, lo,    mid)
    right_profit = _dc_helper(prices, mid+1, hi)
    left_min     = min(prices[lo : mid+1])
    right_max    = max(prices[mid+1 : hi+1])
    cross        = max(0, right_max - left_min)
    return max(left_profit, right_profit, cross)

def dc_profit(prices):
    return _dc_helper(prices, 0, len(prices) - 1)

# 5. KADANE'S ALGORITHM — O(n), applied to price differences
#    Classic max-subarray on the daily-change array.
#    Finds the contiguous window of days with maximum total gain.
#    Equivalent to best single buy-sell but via a different approach.
def kadane_profit(prices):
    diffs = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    max_ending = max_so_far = 0
    for d in diffs:
        max_ending = max(0, max_ending + d)
        max_so_far = max(max_so_far, max_ending)
    return max_so_far

# Backpropagation simulation — 1-neuron linear model pred = w*today + b
def simulate_backprop(prices, epochs=60, lr=0.01):
    if len(prices) < 2: return [], [], [], []
    mn, mx = min(prices), max(prices)
    rng    = mx - mn if mx != mn else 1
    xs = [(p - mn) / rng for p in prices[:-1]]
    ys = [(p - mn) / rng for p in prices[1:]]
    w, b = 0.1, 0.0
    losses, weights, biases = [], [], []
    for _ in range(epochs):
        preds = [w*x + b for x in xs]
        loss  = sum((p-y)**2 for p,y in zip(preds,ys)) / len(ys)
        dw    = -2 * sum((y-p)*x for x,y,p in zip(xs,ys,preds)) / len(ys)
        db    = -2 * sum( y-p    for   y,p in zip(ys, preds))   / len(ys)
        w -= lr*dw; b -= lr*db
        losses.append(loss); weights.append(w); biases.append(b)
    final_preds = [round((w*x + b)*rng + mn, 1) for x in xs]
    return losses, weights, biases, final_preds

# Transaction extractor (greedy valleys/peaks)
def get_transactions(prices):
    txs, i, n = [], 0, len(prices)
    while i < n - 1:
        while i < n-1 and prices[i] >= prices[i+1]: i += 1
        if i == n-1: break
        buy = i
        while i < n-1 and prices[i] <= prices[i+1]: i += 1
        txs.append(("BUY",  buy, prices[buy]))
        txs.append(("SELL", i,   prices[i]))
    return txs


# ══════════════════════════════════════════════════════════════
#  SCROLL FRAME
# ══════════════════════════════════════════════════════════════
class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        bg = kw.get("bg", BG)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        sb          = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner  = tk.Frame(self.canvas, bg=bg)
        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


# ══════════════════════════════════════════════════════════════
#  COLLAPSIBLE SECTION WIDGET
# ══════════════════════════════════════════════════════════════
class CollapsibleSection(tk.Frame):
    def __init__(self, parent, title="SECTION", start_open=False, **kw):
        super().__init__(parent, bg=SURFACE,
                         highlightbackground=BORDER, highlightthickness=1)
        self._open = start_open

        hdr = tk.Frame(self, bg=SURFACE2, cursor="hand2")
        hdr.pack(fill=tk.X)

        tk.Frame(hdr, bg=ACCENT, width=9, height=9).pack(side=tk.LEFT, padx=(12,6), pady=10)
        self._title_lbl = tk.Label(hdr, text=title, bg=SURFACE2, fg=INK_L,
                                   font=("Courier", 8, "bold"))
        self._title_lbl.pack(side=tk.LEFT, pady=10)

        self._summary_var = tk.StringVar(value="")
        self._summary_lbl = tk.Label(hdr, textvariable=self._summary_var,
                                     bg=SURFACE2, fg=ACCENT, font=("Courier", 8))
        self._summary_lbl.pack(side=tk.LEFT, padx=8)

        self._chev = tk.Label(hdr, text="▲" if start_open else "▼",
                              bg=SURFACE2, fg=INK_L, font=("Courier", 9))
        self._chev.pack(side=tk.RIGHT, padx=14)

        for w in (hdr, self._title_lbl, self._summary_lbl, self._chev):
            w.bind("<Button-1>", lambda e: self.toggle())

        self.body = tk.Frame(self, bg=SURFACE)
        if start_open:
            self.body.pack(fill=tk.X)

    def toggle(self):
        self._open = not self._open
        if self._open:
            self.body.pack(fill=tk.X)
            self._chev.config(text="▲")
        else:
            self.body.forget()
            self._chev.config(text="▼")

    def open(self):
        if not self._open: self.toggle()

    def set_summary(self, text):
        self._summary_var.set(text)


# ══════════════════════════════════════════════════════════════
#  LOGIN WINDOW  —  OPEN LOGIN (any username, just enter a name)
# ══════════════════════════════════════════════════════════════
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Analyzer  |  Sign In")
        self.state("zoomed")
        self.configure(bg=LG_BG)
        self.resizable(True, True)
        self._anim_frame = 0
        self._anim_id    = None
        self._build_canvas_bg()
        self._build_login_card()
        self._animate_bg()

    def _build_canvas_bg(self):
        self._bg_canvas = tk.Canvas(self, bg=LG_BG, highlightthickness=0)
        self._bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.after(100, self._draw_grid)

    def _draw_grid(self):
        w = self.winfo_width() or 1400
        h = self.winfo_height() or 900
        c = self._bg_canvas
        c.delete("grid")
        for x in range(0, w, 60):
            c.create_line(x, 0, x, h, fill="#15151F", width=1, tags="grid")
        for y in range(0, h, 60):
            c.create_line(0, y, w, y, fill="#15151F", width=1, tags="grid")
        random.seed(42)
        c.delete("dot")
        for _ in range(18):
            x   = random.randint(0, w); y = random.randint(0, h)
            r   = random.randint(2, 8)
            col = random.choice(["#FF4500","#C9A84C","#5B2D8E","#1A6640"])
            c.create_oval(x-r, y-r, x+r, y+r, fill=col, outline="",
                          tags="dot", stipple="gray50")

    def _animate_bg(self):
        self._anim_frame += 1
        t     = self._anim_frame * 0.03
        pulse = 0.5 + 0.5 * math.sin(t)
        alpha = int(30 + pulse * 20)
        w = self.winfo_width() or 1400
        h = self.winfo_height() or 900
        cx, cy = w//2, h//2
        r = int(280 + pulse * 40)
        c = self._bg_canvas
        c.delete("orb")
        for i in range(5):
            ri = r - i*40
            bright = max(0, alpha - i*8)
            c.create_oval(cx-ri, cy-ri, cx+ri, cy+ri,
                          outline=f"#{bright:02x}{bright//4:02x}00",
                          width=1, tags="orb")
        self._anim_id = self.after(40, self._animate_bg)

    def _build_login_card(self):
        outer = tk.Frame(self, bg=LG_BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(outer, bg=LG_CARD,
                        highlightbackground=LG_BORDER, highlightthickness=1)
        card.pack(ipadx=50, ipady=40)

        # Logo
        logo_row = tk.Frame(card, bg=LG_CARD); logo_row.pack(pady=(0, 6))
        tk.Label(logo_row, text="[ ",  bg=LG_CARD, fg=LG_GOLD,   font=("Courier New",28,"bold")).pack(side=tk.LEFT)
        tk.Label(logo_row, text="DSA", bg=LG_CARD, fg=LG_ACCENT, font=("Courier New",28,"bold")).pack(side=tk.LEFT)
        tk.Label(logo_row, text=" ]",  bg=LG_CARD, fg=LG_GOLD,   font=("Courier New",28,"bold")).pack(side=tk.LEFT)

        tk.Label(card, text="S T O C K   B U Y - S E L L   A N A L Y Z E R",
                 bg=LG_CARD, fg=LG_TEXT, font=("Courier New",9,"bold")).pack()
        tk.Label(card, text="PBL · Semester 4  ·  Data Structures & Algorithms",
                 bg=LG_CARD, fg=LG_MUTED, font=("Courier New",8)).pack(pady=(2,0))

        tk.Frame(card, bg=LG_ACCENT, height=1).pack(fill=tk.X, pady=(20, 22))

        # ── Open login: just enter your name ──────────────────
        tk.Label(card, text="ENTER YOUR NAME TO BEGIN",
                 bg=LG_CARD, fg=LG_MUTED,
                 font=("Courier New",8,"bold")).pack(anchor="w", padx=4)

        tk.Label(card,
                 text="No password needed — just type any name and press Enter",
                 bg=LG_CARD, fg=LG_MUTED,
                 font=("Courier New",7)).pack(anchor="w", padx=4, pady=(2,8))

        uf = tk.Frame(card, bg=LG_BORDER,
                      highlightbackground=LG_BORDER, highlightthickness=1)
        uf.pack(fill=tk.X, pady=(0, 16))
        tk.Label(uf, text=" ⟫ ", bg=LG_BORDER, fg=LG_ACCENT,
                 font=("Courier New",11,"bold")).pack(side=tk.LEFT)
        self._user_var = tk.StringVar()
        user_entry = tk.Entry(uf, textvariable=self._user_var,
                              bg=LG_BORDER, fg=LG_TEXT,
                              font=("Courier New",14),
                              insertbackground=LG_ACCENT,
                              relief="flat", bd=0, width=22)
        user_entry.pack(side=tk.LEFT, pady=12, padx=(0, 10))
        user_entry.focus_set()

        self._sv_err = tk.StringVar(value="")
        self._err_lbl = tk.Label(card, textvariable=self._sv_err,
                                 bg=LG_CARD, fg=LG_ACCENT,
                                 font=("Courier New",8))
        self._err_lbl.pack(pady=(0, 4))

        self._login_btn = tk.Button(card, text="▶▶  LET'S GO",
                                    bg=LG_ACCENT, fg=LG_TEXT,
                                    font=("Courier New",12,"bold"),
                                    relief="flat", bd=0,
                                    padx=20, pady=14, cursor="hand2",
                                    activebackground="#a82d06",
                                    command=self._enter)
        self._login_btn.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card,
                 text="Your session history is saved under your name",
                 bg=LG_CARD, fg=LG_MUTED,
                 font=("Courier New",7)).pack()

        self.bind("<Return>", lambda e: self._enter())

    def _enter(self):
        name = self._user_var.get().strip()
        if not name:
            self._sv_err.set("⚠  Please enter your name."); return
        if len(name) > 30:
            self._sv_err.set("⚠  Name too long (max 30 chars)."); return
        self._sv_err.set(f"✓  Welcome, {name}! Loading...")
        self._err_lbl.config(fg=LG_GREEN)
        self._login_btn.config(state="disabled")
        self.after(600, lambda: self._open_main(name))

    def _open_main(self, username):
        try:
            if self._anim_id:
                self.after_cancel(self._anim_id)
        except Exception:
            pass
        self.destroy()
        StockApp(username).mainloop()


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════
class StockApp(tk.Tk):
    def __init__(self, username="user"):
        super().__init__()
        self._username  = username
        self.title("Stock Buy-Sell Analyzer  |  PBL Sem 4")
        self.state("zoomed")
        self.configure(bg=BG)
        self.resizable(True, True)

        self._anim        = None
        self._hover_line  = None
        self._hover_annot = None

        self._build_ui()
        self._load_preset("Volatile")
        self.after(200, self.analyze)

    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_statusbar()

        sf   = ScrollFrame(self, bg=BG)
        sf.pack(fill=tk.BOTH, expand=True)
        body = sf.inner

        # Row 1: input card + price chart
        row1 = tk.Frame(body, bg=BG)
        row1.pack(fill=tk.X, padx=18, pady=(16, 0))
        self._build_input_card(row1)
        self._build_chart_card(row1)

        # ── Collapsible: Transaction Timeline
        self._tl_sec = CollapsibleSection(body, title="TRANSACTION TIMELINE", start_open=False)
        self._tl_sec.pack(fill=tk.X, padx=18, pady=(14, 0))
        self._tl_inner = tk.Frame(self._tl_sec.body, bg=SURFACE)
        self._tl_inner.pack(fill=tk.X, padx=14, pady=(4, 12))
        tk.Label(self._tl_inner, text="No data yet",
                 bg=SURFACE, fg=INK_L, font=("Courier",9)).pack(pady=10)

        # ── Collapsible: Results (5 algos)
        self._res_sec = CollapsibleSection(body, title="RESULTS — ALL ALGORITHMS", start_open=True)
        self._res_sec.pack(fill=tk.X, padx=18, pady=(14, 0))
        self._build_results_inside(self._res_sec.body)

        # ── Collapsible: Profit Matrix
        self._mat_sec = CollapsibleSection(body, title="PROFIT MATRIX (GRAPH ALGORITHM)", start_open=False)
        self._mat_sec.pack(fill=tk.X, padx=18, pady=(14, 0))
        self._matrix_host = tk.Frame(self._mat_sec.body, bg=SURFACE)
        self._matrix_host.pack(fill=tk.X, padx=14, pady=(4, 12))
        tk.Label(self._matrix_host, text="No data yet",
                 bg=SURFACE, fg=INK_L, font=("Courier",9)).pack(pady=16)

        # ── Collapsible: Algorithm Comparison bars
        self._cmp_sec = CollapsibleSection(body, title="ALGORITHM COMPARISON", start_open=True)
        self._cmp_sec.pack(fill=tk.X, padx=18, pady=(14, 0))
        self._build_comparison_inside(self._cmp_sec.body)

        # ── Collapsible: Backpropagation
        self._bp_sec = CollapsibleSection(body, title="BACKPROPAGATION — NEURAL NETWORK PRICE LEARNING", start_open=False)
        self._bp_sec.pack(fill=tk.X, padx=18, pady=(14, 0))
        self._build_bp_panel(self._bp_sec.body)

        # History
        self._build_history_panel(body)

    # ── HEADER ───────────────────────────────────────────────
    def _build_header(self):
        hdr   = tk.Frame(self, bg=HDR_BG); hdr.pack(fill=tk.X)
        inner = tk.Frame(hdr,  bg=HDR_BG); inner.pack(fill=tk.X, pady=(10,8))
        row   = tk.Frame(inner, bg=HDR_BG); row.pack(anchor="center")
        tk.Label(row, text="Stock Buy-Sell ", bg=HDR_BG, fg="#F2EFE9",
                 font=("Georgia",22,"bold")).pack(side=tk.LEFT)
        tk.Label(row, text="Analyzer", bg=HDR_BG, fg=ACCENT,
                 font=("Georgia",22,"bold italic")).pack(side=tk.LEFT)
        badge = tk.Frame(inner, bg=HDR_BG)
        badge.place(relx=1.0, rely=0.5, anchor="e", x=-18)
        tk.Label(badge, text=f"⟫  {self._username.upper()}",
                 bg=ACCENT, fg="white",
                 font=("Courier New",9,"bold"),
                 padx=10, pady=4).pack(side=tk.LEFT)
        tk.Button(badge, text="⏻", bg="#2A2A2A", fg=INK_L,
                  font=("",10), relief="flat", bd=0,
                  cursor="hand2", padx=6, pady=2,
                  command=self._logout).pack(side=tk.LEFT, padx=(4,0))
        tk.Frame(self, bg=ACCENT, height=3).pack(fill=tk.X)

    def _logout(self):
        self.destroy(); LoginWindow().mainloop()

    # ── STATUS BAR ───────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg=STATUS_BG, height=28)
        bar.pack(fill=tk.X); bar.pack_propagate(False)
        inner = tk.Frame(bar, bg=STATUS_BG); inner.pack(side=tk.LEFT, padx=18, pady=4)
        self._sv_status = tk.StringVar(value="Ready — enter prices to begin")
        self._sv_days   = tk.StringVar(value="—")
        self._sv_range  = tk.StringVar(value="—")
        for var, prefix in [(self._sv_status,""),
                            (self._sv_days,"  ·  Days: "),
                            (self._sv_range,"  ·  Range: ")]:
            if prefix:
                tk.Label(inner, text=prefix, bg=STATUS_BG, fg="#888880",
                         font=("Courier",9)).pack(side=tk.LEFT)
            tk.Label(inner, textvariable=var, bg=STATUS_BG, fg=ACCENT,
                     font=("Courier",9,"bold")).pack(side=tk.LEFT)

    # ── CARD HELPERS ─────────────────────────────────────────
    def _card(self, parent, **kw):
        return tk.Frame(parent, bg=SURFACE,
                        highlightbackground=BORDER, highlightthickness=1, **kw)

    def _card_title(self, parent, text):
        row = tk.Frame(parent, bg=SURFACE); row.pack(fill=tk.X, padx=16, pady=(12,8))
        tk.Frame(row, bg=ACCENT, width=9, height=9).pack(side=tk.LEFT, padx=(0,7))
        tk.Label(row, text=text.upper(), bg=SURFACE, fg=INK_L,
                 font=("Courier",8,"bold")).pack(side=tk.LEFT)

    # ── INPUT CARD ───────────────────────────────────────────
    def _build_input_card(self, parent):
        card = self._card(parent)
        card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,14), ipadx=6, ipady=6)
        card.config(width=420); card.pack_propagate(False)
        self._card_title(card, "Price Input")

        prow = tk.Frame(card, bg=SURFACE); prow.pack(fill=tk.X, padx=16, pady=(0,10))
        self._preset_btns = {}
        for name in PRESETS:
            b = tk.Button(prow, text=name, bg=SURFACE2, fg=INK_L,
                          font=("Courier",9), relief="flat", bd=0,
                          padx=10, pady=5, cursor="hand2",
                          command=lambda n=name: self._load_preset(n))
            b.pack(side=tk.LEFT, padx=(0,6))
            self._preset_btns[name] = b

        tk.Label(card, text="Enter prices (comma or space separated):",
                 bg=SURFACE, fg=INK_L, font=("Courier",9)
                 ).pack(anchor="w", padx=16, pady=(2,4))
        tf = tk.Frame(card, bg=SURFACE2,
                      highlightbackground=BORDER, highlightthickness=1)
        tf.pack(fill=tk.X, padx=16, pady=(0,12))
        self._price_text = tk.Text(tf, height=3, bg=SURFACE2, fg=INK,
                                   font=("Courier",10), relief="flat", bd=0,
                                   insertbackground=INK, wrap=tk.WORD)
        self._price_text.pack(fill=tk.BOTH, padx=8, pady=6)

        tk.Label(card, text="Trading Mode:", bg=SURFACE, fg=INK_L,
                 font=("Courier",9)).pack(anchor="w", padx=16, pady=(0,6))
        mf = tk.Frame(card, bg=SURFACE2,
                      highlightbackground=BORDER, highlightthickness=1)
        mf.pack(fill=tk.X, padx=16, pady=(0,12))
        self._mode = tk.StringVar(value="both")
        self._mode_btns = {}
        for txt, val in [("Multiple Tx\n(Greedy)","multi"),
                          ("Single Tx (DP)","single"),
                          ("Compare Both","both")]:
            b = tk.Button(mf, text=txt, bg=SURFACE2, fg=INK_L,
                          font=("Courier",9), relief="flat", bd=0,
                          padx=10, pady=7, cursor="hand2",
                          command=lambda v=val: self._set_mode(v))
            b.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3, pady=3)
            self._mode_btns[val] = b
        self._set_mode("both")

        tk.Button(card, text="▶  Analyze",
                  bg=ACCENT, fg="white",
                  font=("Georgia",13,"bold"),
                  relief="flat", bd=0, padx=12, pady=12,
                  cursor="hand2", activebackground="#a82d06",
                  command=self.analyze).pack(fill=tk.X, padx=16, pady=(0,4))

    def _load_preset(self, name):
        for n, b in self._preset_btns.items():
            b.config(bg=ACCENT if n==name else SURFACE2,
                     fg="white" if n==name else INK_L)
        self._price_text.delete("1.0", tk.END)
        self._price_text.insert("1.0", ", ".join(map(str, PRESETS[name])))

    def _set_mode(self, val):
        self._mode.set(val)
        for v, b in self._mode_btns.items():
            b.config(bg=INK if v==val else SURFACE2,
                     fg="white" if v==val else INK_L)

    def _parse_prices(self):
        raw = self._price_text.get("1.0", tk.END).replace(",", " ").split()
        return [int(x) for x in raw if x.lstrip("-").isdigit()]

    # ── PRICE CHART ──────────────────────────────────────────
    def _build_chart_card(self, parent):
        card = self._card(parent)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=6)
        self._card_title(card, "Real-Time Price Chart  (hover to see price)")
        self._fig, self._ax = plt.subplots(figsize=(7,3.6), dpi=96)
        self._fig.patch.set_facecolor(SURFACE)
        self._ax.set_facecolor(BG)
        for sp in self._ax.spines.values(): sp.set_edgecolor(BORDER)
        self._ax.tick_params(colors=INK_L, labelsize=8)
        self._canvas = FigureCanvasTkAgg(self._fig, master=card)
        self._canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,10))
        self._canvas.mpl_connect("motion_notify_event", self._on_hover)

    def _on_hover(self, event):
        if event.inaxes != self._ax or not hasattr(self,"_chart_prices"): return
        if event.xdata is None: return
        prices = self._chart_prices
        idx    = max(0, min(int(round(event.xdata))-1, len(prices)-1))
        ax     = self._ax
        for attr in ("_hover_line","_hover_annot"):
            obj = getattr(self, attr, None)
            if obj:
                try: obj.remove()
                except: pass
        self._hover_line  = ax.axvline(x=idx+1, color=ACCENT, lw=1.2,
                                       linestyle="--", alpha=0.7, zorder=10)
        self._hover_annot = ax.annotate(
            f"Day {idx+1}\n₹{prices[idx]}",
            xy=(idx+1, prices[idx]), xytext=(10,10), textcoords="offset points",
            fontsize=8, color="white",
            bbox=dict(boxstyle="round,pad=0.4", fc=ACCENT, ec="none", alpha=0.9),
            zorder=11)
        self._canvas.draw_idle()

    # ── RESULTS (inside collapsible) ─────────────────────────
    def _build_results_inside(self, parent):
        inner = tk.Frame(parent, bg=SURFACE)
        inner.pack(fill=tk.X, padx=14, pady=(8, 12))

        # 5 result rows side-by-side
        cols_frame = tk.Frame(inner, bg=SURFACE)
        cols_frame.pack(fill=tk.X)

        self._rv_greedy = self._result_col(cols_frame, GREEN,    "Greedy",          "Multiple Tx · O(n)")
        self._rv_dp     = self._result_col(cols_frame, DP_COLOR, "DP",              "Single Tx · O(n)")
        self._rv_graph  = self._result_col(cols_frame, GOLD,     "Graph",           "Matrix · O(n²)")
        self._rv_dc     = self._result_col(cols_frame, TEAL,     "Divide & Conquer","Recursive · O(n log n)")
        self._rv_kadane = self._result_col(cols_frame, ROSE,     "Kadane's",        "Max-Subarray · O(n)")

        tk.Frame(inner, bg=BORDER, height=1).pack(fill=tk.X, pady=(10,6))
        self._sv_verdict     = tk.StringVar(value="")
        self._sv_backend_note= tk.StringVar(value="")
        tk.Label(inner, textvariable=self._sv_verdict,
                 bg=SURFACE, fg=INK_L, font=("Courier",8),
                 wraplength=900, justify="left").pack(anchor="w")
        tk.Label(inner, textvariable=self._sv_backend_note,
                 bg=SURFACE, fg=GOLD, font=("Courier",7)).pack(anchor="w", pady=(2,0))

    def _result_col(self, parent, color, label, sub):
        col = tk.Frame(parent, bg=SURFACE,
                       highlightbackground=BORDER, highlightthickness=1)
        col.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0,8), ipadx=10, ipady=8)
        var = tk.StringVar(value="—")
        tk.Label(col, textvariable=var, bg=SURFACE, fg=color,
                 font=("Georgia",28,"bold")).pack(anchor="w", padx=10, pady=(8,0))
        tk.Label(col, text=label, bg=SURFACE, fg=INK,
                 font=("Courier",8,"bold")).pack(anchor="w", padx=10)
        tk.Label(col, text=sub, bg=SURFACE, fg=INK_L,
                 font=("Courier",7)).pack(anchor="w", padx=10, pady=(0,6))
        return var

    # ── COMPARISON BARS (inside collapsible) ─────────────────
    def _build_comparison_inside(self, parent):
        inner = tk.Frame(parent, bg=SURFACE)
        inner.pack(fill=tk.X, padx=14, pady=(8,12))
        self._bars = {}
        for name, color, sub in [
            ("Greedy", GREEN,    "O(n)  · multiple transactions"),
            ("DP",     DP_COLOR, "O(n)  · single transaction"),
            ("Graph",  GOLD,     "O(n²) · adjacency matrix"),
            ("D&C",    TEAL,     "O(n log n) · divide & conquer"),
            ("Kadane", ROSE,     "O(n)  · max-subarray on diffs"),
        ]:
            row = tk.Frame(inner, bg=SURFACE); row.pack(fill=tk.X, pady=(0,6))
            tk.Label(row, text=f"{name.upper()}  {sub}",
                     bg=SURFACE, fg=INK_L,
                     font=("Courier",7)).pack(anchor="w", pady=(0,2))
            track = tk.Frame(row, bg=SURFACE2, height=24,
                             highlightbackground=BORDER, highlightthickness=1)
            track.pack(fill=tk.X); track.pack_propagate(False)
            fill = tk.Frame(track, bg=color, height=24)
            fill.place(relx=0, rely=0, relwidth=0.0, relheight=1.0)
            lbl = tk.Label(track, text="0", bg=color, fg="white",
                           font=("Courier",8,"bold"))
            lbl.place(relx=0.02, rely=0.5, anchor="w")
            self._bars[name] = (fill, lbl)

        self._sv_cmp = tk.StringVar(value="")
        tk.Label(inner, textvariable=self._sv_cmp,
                 bg=SURFACE2, fg=INK_L,
                 font=("Courier",8), wraplength=800,
                 justify="left", padx=8, pady=6
                 ).pack(fill=tk.X, pady=(6,0))

    # ── BACKPROPAGATION PANEL ────────────────────────────────
    def _build_bp_panel(self, parent):
        info_row = tk.Frame(parent, bg=SURFACE)
        info_row.pack(fill=tk.X, padx=14, pady=(8,10))

        chart_frame = tk.Frame(info_row, bg=SURFACE)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._bp_fig = plt.figure(figsize=(10, 3.2), dpi=90)
        self._bp_fig.patch.set_facecolor(SURFACE)
        gs = gridspec.GridSpec(1, 3, figure=self._bp_fig, wspace=0.4)
        self._bp_ax_loss   = self._bp_fig.add_subplot(gs[0])
        self._bp_ax_weight = self._bp_fig.add_subplot(gs[1])
        self._bp_ax_pred   = self._bp_fig.add_subplot(gs[2])
        for ax in (self._bp_ax_loss, self._bp_ax_weight, self._bp_ax_pred):
            ax.set_facecolor(BG)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
            ax.tick_params(colors=INK_L, labelsize=7)

        self._bp_canvas = FigureCanvasTkAgg(self._bp_fig, master=chart_frame)
        self._bp_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        explain = tk.Frame(info_row, bg=SURFACE2,
                           highlightbackground=TEAL, highlightthickness=2)
        explain.pack(side=tk.LEFT, fill=tk.Y, padx=(12,0), pady=2, ipadx=10, ipady=8)
        tk.Label(explain, text="HOW BACKPROP WORKS", bg=SURFACE2, fg=TEAL,
                 font=("Courier",8,"bold")).pack(anchor="w", pady=(0,6))
        for line in ["Model:    pred = w × today + b",
                     "Loss:     MSE = mean((pred−actual)²)",
                     "Backward: ∂L/∂w and ∂L/∂b computed",
                     "Update:   w = w − lr × ∂L/∂w",
                     "",
                     "Loss drops each epoch as weights",
                     "adjust to fit tomorrow's price."]:
            tk.Label(explain, text=line, bg=SURFACE2,
                     fg=INK_L if line else SURFACE2,
                     font=("Courier",8)).pack(anchor="w")

        sf = tk.Frame(explain, bg=SURFACE2); sf.pack(fill=tk.X, pady=(10,0))
        self._sv_bp_init  = tk.StringVar(value="—")
        self._sv_bp_final = tk.StringVar(value="—")
        self._sv_bp_drop  = tk.StringVar(value="—")
        for label, var in [("Init Loss",self._sv_bp_init),
                            ("Final Loss",self._sv_bp_final),
                            ("% Drop",self._sv_bp_drop)]:
            col = tk.Frame(sf, bg=SURFACE2); col.pack(side=tk.LEFT, padx=6)
            tk.Label(col, textvariable=var, bg=SURFACE2, fg=TEAL,
                     font=("Courier",12,"bold")).pack()
            tk.Label(col, text=label, bg=SURFACE2, fg=INK_L,
                     font=("Courier",7)).pack()

    def _render_bp(self, prices, losses, weights, biases, preds):
        epochs = list(range(1, len(losses)+1))
        for ax, setup in [
            (self._bp_ax_loss,   lambda a: (
                a.plot(epochs, losses, color=TEAL, lw=2),
                a.fill_between(epochs, losses, alpha=0.15, color=TEAL),
                a.set_title("Loss per Epoch", fontsize=8, color=INK_L, pad=4),
                a.set_xlabel("Epoch", fontsize=7, color=INK_L),
                a.set_ylabel("MSE",   fontsize=7, color=INK_L))),
            (self._bp_ax_weight, lambda a: (
                a.plot(epochs, weights, color=ACCENT,   lw=2, label="weight w"),
                a.plot(epochs, biases,  color=DP_COLOR, lw=2, linestyle="--", label="bias b"),
                a.set_title("Weight & Bias", fontsize=8, color=INK_L, pad=4),
                a.set_xlabel("Epoch", fontsize=7, color=INK_L),
                a.legend(fontsize=7, framealpha=0.7))),
            (self._bp_ax_pred,   lambda a: (
                a.plot(list(range(2,len(prices)+1)), prices[1:],
                       color=BLUE, lw=2, marker="o", ms=4, label="Actual"),
                a.plot(list(range(2,len(prices)+1)), preds,
                       color=GOLD, lw=1.5, marker="s", ms=3,
                       linestyle="--", label="Predicted"),
                a.set_title("Predicted vs Actual", fontsize=8, color=INK_L, pad=4),
                a.set_xlabel("Day", fontsize=7, color=INK_L),
                a.legend(fontsize=7, framealpha=0.7))),
        ]:
            ax.clear(); ax.set_facecolor(BG)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
            ax.tick_params(colors=INK_L, labelsize=7)
            setup(ax)

        self._bp_fig.tight_layout()
        self._bp_canvas.draw()

        init_l  = losses[0]  if losses else 0
        final_l = losses[-1] if losses else 0
        drop    = (init_l-final_l)/init_l*100 if init_l else 0
        self._sv_bp_init.set(f"{init_l:.4f}")
        self._sv_bp_final.set(f"{final_l:.4f}")
        self._sv_bp_drop.set(f"{drop:.1f}%")

    # ── HISTORY PANEL ────────────────────────────────────────
    def _build_history_panel(self, parent):
        card = self._card(parent)
        card.pack(fill=tk.X, padx=18, pady=(14,20), ipady=6)
        title_row = tk.Frame(card, bg=SURFACE)
        title_row.pack(fill=tk.X, padx=16, pady=(12,8))
        tk.Frame(title_row, bg=ACCENT, width=9, height=9).pack(side=tk.LEFT, padx=(0,7))
        tk.Label(title_row, text="ANALYSIS HISTORY",
                 bg=SURFACE, fg=INK_L, font=("Courier",8,"bold")).pack(side=tk.LEFT)
        tk.Label(title_row, text="↑ duplicates auto-detected",
                 bg=SURFACE, fg=INK_L, font=("Courier",7)).pack(side=tk.RIGHT, padx=8)
        tk.Button(title_row, text="Clear History",
                  bg=SURFACE2, fg=INK_L, font=("Courier",8),
                  relief="flat", bd=0, padx=10, pady=3, cursor="hand2",
                  command=self._clear_history).pack(side=tk.RIGHT)
        self._hist_container = tk.Frame(card, bg=SURFACE)
        self._hist_container.pack(fill=tk.X, padx=14, pady=(0,10))
        self._refresh_history()

    def _refresh_history(self):
        for w in self._hist_container.winfo_children(): w.destroy()
        records = history_mgr.all_records()
        if not records:
            tk.Label(self._hist_container, text="No analyses saved yet.",
                     bg=SURFACE, fg=INK_L, font=("Courier",9)).pack(pady=14)
            return
        # Header
        hdr = tk.Frame(self._hist_container, bg=SURFACE2)
        hdr.pack(fill=tk.X, pady=(0,4))
        for col, wid in [("#",3),("Timestamp",18),("User",12),("Prices",28),
                          ("Greedy",7),("DP",7),("Graph",7),("D&C",7),("Kadane",7)]:
            tk.Label(hdr, text=col, bg=SURFACE2, fg=INK_L,
                     font=("Courier",8,"bold"), width=wid, anchor="w"
                     ).pack(side=tk.LEFT, padx=4, pady=4)
        # Data rows
        for i, rec in enumerate(reversed(records)):
            row_bg = SURFACE if i%2==0 else SURFACE2
            row    = tk.Frame(self._hist_container, bg=row_bg)
            row.pack(fill=tk.X, pady=1)
            ps = str(rec["prices"])
            ps = ps[:34]+"...]" if len(ps)>37 else ps
            for val, wid, color in [
                (str(i+1),              3,  INK_L),
                (rec["timestamp"],      18, INK),
                (rec["user"],           12, ACCENT),
                (ps,                    28, INK_L),
                (str(rec["greedy"]),    7,  GREEN),
                (str(rec["dp"]),        7,  DP_COLOR),
                (str(rec.get("graph","—")), 7, GOLD),
                (str(rec.get("dc","—")),   7, TEAL),
                (str(rec.get("kadane","—")),7, ROSE),
            ]:
                tk.Label(row, text=val, bg=row_bg, fg=color,
                         font=("Courier",8), width=wid, anchor="w"
                         ).pack(side=tk.LEFT, padx=4, pady=5)
            rec_copy = rec.copy()
            tk.Button(row, text="↺ Re-load",
                      bg=SURFACE2, fg=INK_L, font=("Courier",7),
                      relief="flat", bd=0, padx=6, pady=2, cursor="hand2",
                      command=lambda r=rec_copy: self._reload_from_history(r)
                      ).pack(side=tk.LEFT, padx=(2,8))

    def _reload_from_history(self, record):
        self._price_text.delete("1.0", tk.END)
        self._price_text.insert("1.0", ", ".join(map(str, record["prices"])))
        self.analyze()

    def _clear_history(self):
        if messagebox.askyesno("Clear History","Delete all analysis history?"):
            history_mgr.clear(); self._refresh_history()

    # ══════════════════════════════════════════════════════════
    #  ANALYZE
    # ══════════════════════════════════════════════════════════
    def analyze(self):
        try:   prices = self._parse_prices()
        except: messagebox.showerror("Input Error","Enter valid integer prices."); return
        if len(prices) < 2:
            messagebox.showerror("Input Error","Enter at least 2 prices."); return

        # Duplicate check
        existing = history_mgr.find_duplicate(prices)
        if existing:
            msg = (f"These exact prices were already analyzed!\n\n"
                   f"  By: {existing['user']}  at  {existing['timestamp']}\n"
                   f"  Greedy:{existing['greedy']}  DP:{existing['dp']}"
                   f"  D&C:{existing.get('dc','—')}  Kadane:{existing.get('kadane','—')}\n\n"
                   f"Load cached results?")
            if messagebox.askyesno("Duplicate Detected 🔁", msg):
                self._sv_status.set("Loaded from history ✓")
                self._display(prices,
                              existing["greedy"], existing["dp"],
                              existing.get("graph",0), existing.get("dc",0),
                              existing.get("kadane",0))
                return

        # Compute all algorithms
        c_result = call_c_backend(prices)
        if c_result:
            gp, dp, gmax = c_result
            self._sv_backend_note.set("✦ Greedy/DP/Graph from C · D&C & Kadane from Python")
        else:
            gp   = greedy_profit(prices)
            dp   = dp_profit(prices)
            g    = build_graph(prices)
            gmax = max_profit_graph(g)
            self._sv_backend_note.set("")

        dc     = dc_profit(prices)
        kadane = kadane_profit(prices)

        history_mgr.save(self._username, prices, gp, dp, gmax, dc, kadane)
        self._sv_status.set("Analysis complete ✓")
        self._display(prices, gp, dp, gmax, dc, kadane)

    def _display(self, prices, gp, dp, gmax, dc, kadane):
        self._sv_days.set(str(len(prices)))
        self._sv_range.set(f"{min(prices)} – {max(prices)}")

        self._rv_greedy.set(str(gp))
        self._rv_dp.set(str(dp))
        self._rv_graph.set(str(gmax))
        self._rv_dc.set(str(dc))
        self._rv_kadane.set(str(kadane))

        # Verdict
        single_best = max(dp, dc, kadane, gmax)
        self._sv_verdict.set(
            f"✦ Greedy (multiple trades): {gp}   |   "
            f"Best single-trade: {single_best}  "
            f"(DP={dp}, D&C={dc}, Kadane={kadane}, Graph={gmax})   |   "
            f"Kadane = DP: {'✓' if kadane==dp else '✗'}"
        )

        txs          = get_transactions(prices)
        graph_matrix = build_graph(prices)

        self._animate_chart(prices, txs)
        self._render_timeline(prices, txs)
        self._render_matrix(graph_matrix)
        self._render_bars(gp, dp, gmax, dc, kadane)

        losses, weights, biases, preds = simulate_backprop(prices)
        self._render_bp(prices, losses, weights, biases, preds)
        self._bp_sec.set_summary(f"Final MSE: {losses[-1]:.4f}  ·  {len(losses)} epochs")

        # Update section summaries
        self._res_sec.set_summary(
            f"Greedy:{gp}  DP:{dp}  D&C:{dc}  Kadane:{kadane}  Graph:{gmax}")
        self._mat_sec.set_summary(
            f"Best cell: {max(gmax,0)}  ·  {len(prices)}×{len(prices)} matrix")
        self._cmp_sec.set_summary(
            f"Winner: {'Greedy' if gp>=max(dp,dc,kadane,gmax) else 'Single-trade'}")

        self._refresh_history()

    # ── ANIMATED PRICE CHART ─────────────────────────────────
    def _animate_chart(self, prices, txs):
        if self._anim:
            try: self._anim.event_source.stop()
            except: pass
            self._anim = None

        self._chart_prices = prices
        buy_days  = {t[1] for t in txs if t[0]=="BUY"}
        sell_days = {t[1] for t in txs if t[0]=="SELL"}
        n         = len(prices)
        days      = list(range(1, n+1))

        ax = self._ax; ax.clear()
        ax.set_facecolor(BG)
        for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
        ax.tick_params(colors=INK_L, labelsize=8)
        ax.set_xlim(0.5, n+0.5)
        ax.set_ylim(max(0,min(prices)*0.88), max(prices)*1.10)
        ax.set_xticks(days)
        ax.set_xticklabels([f"D{d}" for d in days], fontsize=8)
        ax.grid(color=BORDER, lw=0.5, linestyle="--", alpha=0.6)

        line, = ax.plot([], [], color=BLUE, lw=2.4, zorder=3)
        dots  = []

        def update(frame):
            xs = days[:frame+1]; ys = prices[:frame+1]
            line.set_data(xs, ys)
            while ax.collections: ax.collections[0].remove()
            for d in dots:
                try: d.remove()
                except: pass
            dots.clear()
            if len(xs) > 1:
                ax.fill_between(xs, ys, max(0,min(prices)*0.88),
                                alpha=0.13, color=BLUE, zorder=1)
            for i, (x, y) in enumerate(zip(xs, ys)):
                if i in buy_days:
                    d, = ax.plot(x, y, "o", color=GREEN, ms=10,
                                 zorder=6, mec="white", mew=2); dots.append(d)
                elif i in sell_days:
                    d, = ax.plot(x, y, "o", color=ACCENT, ms=10,
                                 zorder=6, mec="white", mew=2); dots.append(d)
            self._canvas.draw_idle()
            return line,

        self._anim = FuncAnimation(self._fig, update, frames=n,
                                   interval=100, blit=False, repeat=False)
        ax.legend(handles=[
            mpatches.Patch(color=BLUE,   label="Price"),
            mpatches.Patch(color=GREEN,  label="BUY"),
            mpatches.Patch(color=ACCENT, label="SELL"),
        ], fontsize=7, framealpha=0.85, loc="upper right")
        self._canvas.draw()

    # ── TIMELINE ─────────────────────────────────────────────
    def _render_timeline(self, prices, txs):
        for w in self._tl_inner.winfo_children(): w.destroy()
        action = {}
        for typ, idx, _ in txs: action.setdefault(idx,[]).append(typ)
        buys  = sum(1 for t in txs if t[0]=="BUY")
        sells = sum(1 for t in txs if t[0]=="SELL")
        self._tl_sec.set_summary(
            f"{buys} buys · {sells} sells · {len(prices)} days — click to expand")
        for i, price in enumerate(prices):
            acts    = action.get(i, [])
            is_buy  = "BUY"  in acts
            is_sell = "SELL" in acts
            bg      = GREEN_L if is_buy else "#FDEEE9" if is_sell else SURFACE2
            border  = GREEN   if is_buy else ACCENT    if is_sell else BORDER
            cell    = tk.Frame(self._tl_inner, bg=bg,
                               highlightbackground=border, highlightthickness=2)
            tk.Label(cell, text=f"Day {i+1}", bg=bg, fg=INK_L,
                     font=("Courier",7)).pack()
            tk.Label(cell, text=str(price), bg=bg, fg=INK,
                     font=("Courier",12,"bold")).pack()
            for act in acts:
                tk.Label(cell, text=act,
                         bg=GREEN if act=="BUY" else ACCENT,
                         fg="white", font=("Courier",7,"bold"),
                         padx=5, pady=1).pack(pady=(3,0))
            self.after(50*i, lambda c=cell: c.pack(
                side=tk.LEFT, padx=4, pady=2, ipadx=6, ipady=6))

    # ── PROFIT MATRIX ────────────────────────────────────────
    def _render_matrix(self, graph):
        for w in self._matrix_host.winfo_children(): w.destroy()
        n = len(graph)
        if n > 10:
            tk.Label(self._matrix_host,
                     text="Matrix hidden for >10 days (too large to display clearly)",
                     bg=SURFACE, fg=INK_L, font=("Courier",9)).pack(pady=16); return
        mx_val, mx_i, mx_j = 0, -1, -1
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] > mx_val: mx_val, mx_i, mx_j = graph[i][j], i, j
        cell_w = max(3, min(5, 40//n))
        tk.Label(self._matrix_host, text="i\\j", bg=INK, fg="#F2EFE9",
                 font=("Courier",7), width=cell_w, relief="flat"
                 ).grid(row=0, column=0, padx=1, pady=1)
        for j in range(n):
            tk.Label(self._matrix_host, text=f"D{j+1}", bg=INK, fg="#F2EFE9",
                     font=("Courier",7), width=cell_w, relief="flat"
                     ).grid(row=0, column=j+1, padx=1, pady=1)
        for i in range(n):
            tk.Label(self._matrix_host, text=f"D{i+1}", bg=INK, fg="#F2EFE9",
                     font=("Courier",7), width=cell_w, relief="flat"
                     ).grid(row=i+1, column=0, padx=1, pady=1)
            for j in range(n):
                v = graph[i][j]
                if i==mx_i and j==mx_j: bg_c, fg_c = ACCENT, "white"
                elif v > 0:             bg_c, fg_c = GREEN_L, GREEN
                else:                   bg_c, fg_c = SURFACE2, BORDER
                tk.Label(self._matrix_host, text=str(v), bg=bg_c, fg=fg_c,
                         font=("Courier",7), width=cell_w, relief="flat"
                         ).grid(row=i+1, column=j+1, padx=1, pady=1)

    # ── COMPARISON BARS ──────────────────────────────────────
    def _render_bars(self, gp, dp, gmax, dc, kadane):
        mx   = max(gp, dp, gmax, dc, kadane, 1)
        vals = {"Greedy":gp,"DP":dp,"Graph":gmax,"D&C":dc,"Kadane":kadane}
        for name, (fill, lbl) in self._bars.items():
            pct = max(0.04, vals[name]/mx)
            fill.place(relwidth=pct)
            lbl.config(text=str(vals[name]))
        winner = max(vals, key=vals.get)
        txt = f"✦ {winner} gives the highest value on this dataset."
        if dp: txt += f"\n  Greedy÷DP: {gp/dp:.2f}×  |  Kadane=DP: {'✓' if kadane==dp else '✗'}  |  D&C=DP: {'✓' if dc==dp else '✗'}"
        self._sv_cmp.set(txt)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    LoginWindow().mainloop()