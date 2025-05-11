# Prompter
Prompt creation tool for image-generation AI with language auto-translation and text weight adjustment.

**Author:** Damizon  
**Language:** 🇬🇧 English  
**Type:** Desktop GUI application (Python-based)

---

## 🧠 What is Prompter?

**Prompter** is a simple and intuitive desktop tool for creating complex image generation prompts for AI models like Stable Diffusion. It allows you to fill in structured fields (style, composition, lighting, etc.), translate them to English, and copy the result to your clipboard in one click.

You can also assign **weights to specific words or phrases**, increasing or decreasing their importance in the generated image.

---

## ✨ Features

- 8 core input fields (subject, style, medium, realism, background, lighting, etc.)
- Auto-translation to English (from any language)
- Clipboard-ready final prompt
- Save prompt to `.txt` file
- Weight editor for selected text (e.g. `(white background:1.3)`)
- Clean, fixed-size interface (based on `tkinter`)
- Works as `.py` or standalone `.exe`

---

## ⚖️ How to use weights

1. Highlight any text fragment inside a field.
2. Click **Weight +** to increase weight (e.g. `sky → (sky:1.1)`)
3. Click **Weight -** to decrease weight (e.g. `sky → (sky:0.9)`)
4. Max weight: `10.0`, min weight: `0.1`
5. You can adjust weights repeatedly.

---

## 🚀 How to run

### ✅ Option 1 – Ready-to-use `.exe` (Windows)


Run the file:  Prompter.exe


No Python required.

---

### ✅ Option 2 – From source using `start.bat`

1. Make sure you have **Python 3.8+** installed.  
If not, download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Run the script:	install.bat (For first time)									
				
This will install all required packages automatically:
- `deep-translator`
- `pyperclip`
3. Run: start.bat
It will launch the app using your installed Python interpreter.

---

## 🧾 Optional – Create a standalone `.exe`

For advanced users:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=ikonka.ico prompter.py
