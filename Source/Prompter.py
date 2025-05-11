import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
from deep_translator import GoogleTranslator

class PrompterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prompter By Damizon")
        self.geometry("1350x742")
        self.resizable(False, False)
        # 8 fields in pairs
        self.fields = [
            "Main subject (Who or what is in the image)",
            "Style or genre (cyberpunk, baroque, concept art)",
            "Medium and technique (oil on canvas, pencil sketch, 3D render, photo)",
            "Realism or quality level (highly detailed, ultra realistic, 4k, sharp focus)",
            "Composition and framing (portrait, isometric view, aerial view)",
            "Background and environment (snowy forest, underwater, white background)",
            "Lighting and mood (soft lighting, cinematic lighting, sunset glow, neon lights)",
            "Colors / palette / accents / dominant details"
        ]
        self.text_boxes = {}
        self._create_widgets()

    def _create_widgets(self):
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for i in range(0, len(self.fields), 2):
            row_frame = tk.Frame(scroll_frame)
            row_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
            for field in self.fields[i:i+2]:
                frame = tk.Frame(row_frame)
                frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                tk.Label(frame, text=field + ":").pack(anchor="w")
                txt = tk.Text(frame, height=6, wrap="word")
                txt.pack(fill=tk.BOTH, expand=True)
                self.text_boxes[field] = txt

        result_label = tk.Label(self, text="Generated and Translated prompt:")
        result_label.pack(anchor="w", padx=10, pady=(5,0))
        self.result_txt = tk.Text(self, height=8, wrap="word")
        self.result_txt.pack(fill=tk.BOTH, padx=10, pady=(0,10), expand=False)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="Generate Prompt", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save as TXT", command=self._save_to_file).pack(side=tk.LEFT, padx=5)

        # Description label for weights
        weight_label = tk.Label(btn_frame, text="Adjust weight of selected text:")
        weight_label.pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text="Weight -", command=lambda: self._wrap_weight(-0.1)).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text="Weight +", command=lambda: self._wrap_weight(0.1)).pack(side=tk.RIGHT)

    def _wrap_weight(self, delta):
        widget = self.focus_get()
        if not isinstance(widget, tk.Text):
            return
        try:
            start = widget.index("sel.first")
            end = widget.index("sel.last")
        except tk.TclError:
            return
        selected = widget.get(start, end)
        import re
        m = re.match(r"^\((.*?):([0-9]+\.?[0-9]*)\)$", selected)
        if m:
            text = m.group(1)
            weight = float(m.group(2))
        else:
            text = selected
            weight = 1.0
        new_weight = round(max(0.1, min(weight + delta, 10.0)), 1)
        new = f"({text}:{new_weight})"
        widget.delete(start, end)
        widget.insert(start, new)
        end_index = f"{start} + {len(new)} chars"
        widget.tag_add(tk.SEL, start, end_index)
        widget.see(start)

    def _on_ok(self):
        contents = []
        for txt in self.text_boxes.values():
            val = txt.get("1.0", tk.END).strip()
            if val:
                contents.append(val)
        raw_prompt = ", ".join(contents)

        try:
            translated = GoogleTranslator(source='auto', target='en').translate(raw_prompt)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            return

        try:
            pyperclip.copy(translated)
            messagebox.showinfo("Success", "Translated prompt copied to clipboard!")
        except Exception:
            messagebox.showwarning("Warning", "Failed to copy to clipboard.")

        self.result_txt.delete("1.0", tk.END)
        self.result_txt.insert(tk.END, translated)

    def _save_to_file(self):
        content = self.result_txt.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "There is no prompt to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files","*.txt"), ("All files","*.*")]
        )
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Prompt saved as {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

if __name__ == '__main__':
    try:
        import deep_translator
    except ImportError:
        print("Install required packages: pip install deep-translator pyperclip")
    PrompterApp().mainloop()
