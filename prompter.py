import tkinter as tk
import keyboard
import sys


class TuringPrompter:
    def __init__(self, root, lines):
        self.root = root
        self.root.title("TuringLab Prompter")
        
        # --- PENCERE AYARLARI ---
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.85)
        
        # Ekranın ortasına yerleştir
        screen_width = self.root.winfo_screenwidth()
        window_width = 500
        window_height = 180
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = 50
        
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        
        self.lines = lines
        self.index = 0
        
        # --- METİN TASARIMI ---
        self.label = tk.Label(
            root, 
            text=self.lines[self.index], 
            font=("Arial", 22, "bold"), 
            fg="#E0E0E0", 
            bg="black", 
            wraplength=460, 
            justify="center",
            pady=20
        )
        self.label.pack(expand=True, fill='both')
        
        # --- TUŞ KONTROLLERİ (DÜZELTİLMİŞ) ---
        # Page Down / Numpad * → İleri
        keyboard.add_hotkey('page down', self._safe_next, suppress=True)
        keyboard.add_hotkey('num *', self._safe_next, suppress=True)
        
        # Page Up / Numpad / → Geri
        keyboard.add_hotkey('page up', self._safe_prev, suppress=True)
        keyboard.add_hotkey('num /', self._safe_prev, suppress=True)
        
        # ESC → Çıkış
        keyboard.add_hotkey('esc', self._safe_exit, suppress=False)
        
        print("✓ Teleprompter hazır!")
        print("  → Page Down / Numpad * : İleri")
        print("  → Page Up / Numpad /   : Geri")
        print("  → ESC                  : Çıkış")

    # Thread-safe callback'ler
    def _safe_next(self):
        self.root.after(0, self.next_line)

    def _safe_prev(self):
        self.root.after(0, self.prev_line)
        
    def _safe_exit(self):
        self.root.after(0, self.cleanup_and_exit)

    def next_line(self):
        if self.index < len(self.lines) - 1:
            self.index += 1
            self.label.config(text=self.lines[self.index], fg="#E0E0E0")
        else:
            self.label.config(text="--- SUNUM BİTTİ ---", fg="#FF5555")

    def prev_line(self):
        if self.index > 0:
            self.index -= 1
            self.label.config(text=self.lines[self.index], fg="#E0E0E0")

    def cleanup_and_exit(self):
        keyboard.unhook_all()
        self.root.destroy()


# Senaryo
senaryo = [
    "Merhaba, ben Mehmet Akif Ürey.",
    "Örnek Metin, Örnek Metin,Örnek Metin",
    "Örnek Metin, Örnek Metin",
    "Örnek Metin",
    "Örnek Metin, Örnek Metin",
    "Örnek Metin, Örnek Metin, Örnek Metin",
    "Örnek Metin, Örnek Metin",
    "Örnek Metin, Örnek Metin,Örnek Metin",
]


if __name__ == "__main__":
    root = tk.Tk()
    app = TuringPrompter(root, senaryo)
    
    try:
        root.mainloop()
    finally:
        # Program kapanınca tuş hook'larını temizle
        keyboard.unhook_all()
