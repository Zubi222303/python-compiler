import tkinter as tk
from tkinter import scrolledtext

class OutputPanel:
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text="Output", padx=5, pady=5)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_area = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=('Consolas', 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)
    
    def clear(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
    
    def append(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)