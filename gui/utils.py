import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas

def create_label_entry(parent, label_text, row, col=0, show=None, width=30):
    ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky="w", padx=5, pady=2)
    entry = ttk.Entry(parent, width=width)
    if show:
        entry.config(show=show)
    entry.grid(row=row, column=col+1, sticky="w", padx=5, pady=2)
    return entry

def create_label_combo(parent, label_text, row, values, col=0, width=27):
    ttk.Label(parent, text=label_text).grid(row=row, column=col, sticky="w", padx=5, pady=2)
    combo = ttk.Combobox(parent, values=values, state="readonly", width=width)
    combo.grid(row=row, column=col+1, sticky="w", padx=5, pady=2)
    return combo
