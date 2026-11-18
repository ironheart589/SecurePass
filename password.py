import tkinter as tk
from tkinter import messagebox
import string
import secrets
import re

# --- 1. PASSWORD GENERATION LOGIC ---
def generate_password():
    try:
        length = int(length_var.get())
        if length < 4 or length > 64:
            messagebox.showwarning("Invalid Length", "Please enter a length between 4 and 64.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be a valid whole number.")
        return

    char_pool = ""
    required_chars = []
    if lower_var.get():
        char_pool += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if upper_var.get():
        char_pool += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if digits_var.get():
        char_pool += string.digits
        required_chars.append(secrets.choice(string.digits))
    if special_var.get():
        char_pool += string.punctuation
        required_chars.append(secrets.choice(string.punctuation))

    if length < len(required_chars):
        messagebox.showwarning(
            "Invalid Choice",
            f"Length must be at least {len(required_chars)} to include all selected character types."
        )
        return

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
    secrets.SystemRandom().shuffle(password_chars)

    final_password = "".join(password_chars)
    generated_var.set(final_password)


# --- 2. COPY TO CLIPBOARD LOGIC ---
def copy_password():
    pwd = generated_var.get()
    if not pwd:
        messagebox.showinfo("Nothing to Copy", "Generate a password first before copying.")
        return

    root.clipboard_clear()
    root.clipboard_append(pwd)
    root.update()
    messagebox.showinfo("Copied!", "Password copied to clipboard.")


# --- 3. DYNAMIC LIVE STRENGTH CHECKER LOGIC ---
def evaluate_strength(event=None):
    pwd = check_entry.get()

    # If empty, hide all analysis boxes to keep the UI clean
    if not pwd:
        results_container.pack_forget()
        return
    else:
        results_container.pack(fill="x", pady=(10, 0))

    # Check rules using Regex
    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"[0-9]", pwd))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", pwd))

    length = len(pwd)
    variety_count = sum([has_lower, has_upper, has_digit, has_special])

    # Update metric cards
    length_val_lbl.config(text=str(length))
    variety_val_lbl.config(text=f"{variety_count} / 4")

    # Update breakdown indicators
    upper_chk_lbl.config(text="✔" if has_upper else "✘", fg="#22c55e" if has_upper else "#ef4444")
    lower_chk_lbl.config(text="✔" if has_lower else "✘", fg="#22c55e" if has_lower else "#ef4444")
    num_chk_lbl.config(text="✔" if has_digit else "✘", fg="#22c55e" if has_digit else "#ef4444")
    sym_chk_lbl.config(text="✔" if has_special else "✘", fg="#22c55e" if has_special else "#ef4444")

    # Determine Strength label
    if length < 8 or variety_count <= 2:
        strength = "Weak"
        color = "#ef4444"
    elif length >= 12 and variety_count == 4:
        strength = "Strong"
        color = "#22c55e"
    else:
        strength = "Medium"
        color = "#f59e0b"

    strength_lbl.config(text=strength, fg=color)

    # Generate dynamic tips to improve
    tips = []
    if length < 12:
        tips.append("• Use at least 12 characters for better security.")
    if not has_upper:
        tips.append("• Add uppercase letters (A-Z) to increase complexity.")
    if not has_lower:
        tips.append("• Add lowercase letters (a-z) to increase complexity.")
    if not has_digit:
        tips.append("• Add numbers (0-9) to increase complexity.")
    if not has_special:
        tips.append("• Add symbols (!@#$%^&*) to increase complexity.")

    if not tips:
        tips.append("• Excellent password! It meets all strength and variety criteria.")

    tips_text.config(state="normal")
    tips_text.delete("1.0", tk.END)
    tips_text.insert("1.0", "\n".join(tips))
    tips_text.config(state="disabled")


# --- 4. NAVIGATION LOGIC ---
def show_generator():
    checker_frame.pack_forget()
    generator_frame.pack(fill="both", expand=True, padx=20, pady=15)
    btn_gen_nav.config(fg="#ffffff", font=("Segoe UI", 10, "bold"))
    btn_check_nav.config(fg="#94a3b8", font=("Segoe UI", 10))

def show_checker():
    generator_frame.pack_forget()
    checker_frame.pack(fill="both", expand=True, padx=20, pady=15)
    btn_check_nav.config(fg="#ffffff", font=("Segoe UI", 10, "bold"))
    btn_gen_nav.config(fg="#94a3b8", font=("Segoe UI", 10))


# --- 5. MAIN GUI SETUP (DARK THEME) ---
root = tk.Tk()
root.title("Password Utility Suite")
root.geometry("540x650")
root.resizable(False, False)

# Color Palette
BG_DARK = "#0f172a"
CARD_BG = "#1e293b"
CARD_INNER = "#0f172a"
TEXT_LIGHT = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#2563eb"

root.config(bg=BG_DARK)

# Top Navigation Bar
nav_frame = tk.Frame(root, bg="#090d16", height=50)
nav_frame.pack(fill="x", side="top")
nav_frame.pack_propagate(False)

tk.Label(nav_frame, text="🔒 SecurePass", font=("Segoe UI", 11, "bold"), bg="#090d16", fg=TEXT_LIGHT).pack(side="left", padx=20)

nav_links = tk.Frame(nav_frame, bg="#090d16")
nav_links.pack(side="right", padx=15)

btn_gen_nav = tk.Button(nav_links, text="Generator", command=show_generator, bg="#090d16", fg="#ffffff", bd=0, cursor="hand2", activebackground="#090d16", activeforeground="white")
btn_gen_nav.pack(side="left", padx=10)

btn_check_nav = tk.Button(nav_links, text="Strength Checker", command=show_checker, bg="#090d16", fg=TEXT_MUTED, bd=0, cursor="hand2", activebackground="#090d16", activeforeground="white")
btn_check_nav.pack(side="left", padx=10)


# Main View Container
container = tk.Frame(root, bg=BG_DARK)
container.pack(fill="both", expand=True)


# ==========================================
# VIEW 1: PASSWORD GENERATOR
# ==========================================
generator_frame = tk.Frame(container, bg=BG_DARK)

gen_card = tk.Frame(generator_frame, bg=CARD_BG, padx=20, pady=20)
gen_card.pack(fill="x", pady=5)

tk.Label(gen_card, text="Password Generator", font=("Segoe UI", 14, "bold"), bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 15))

len_row = tk.Frame(gen_card, bg=CARD_BG)
len_row.pack(fill="x", pady=6)
tk.Label(len_row, text="Password Length (4-64):", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_MUTED).pack(side="left")
length_var = tk.StringVar(value="12")
tk.Entry(len_row, textvariable=length_var, width=6, font=("Segoe UI", 10), justify="center").pack(side="right")

opts_box = tk.Frame(gen_card, bg=CARD_BG)
opts_box.pack(fill="x", pady=10)

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

tk.Checkbutton(opts_box, text="Lowercase Letters (a-z)", variable=lower_var, bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=CARD_BG, font=("Segoe UI", 9), activebackground=CARD_BG, activeforeground=TEXT_LIGHT).pack(anchor="w", pady=3)
tk.Checkbutton(opts_box, text="Uppercase Letters (A-Z)", variable=upper_var, bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=CARD_BG, font=("Segoe UI", 9), activebackground=CARD_BG, activeforeground=TEXT_LIGHT).pack(anchor="w", pady=3)
tk.Checkbutton(opts_box, text="Digits (0-9)", variable=digits_var, bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=CARD_BG, font=("Segoe UI", 9), activebackground=CARD_BG, activeforeground=TEXT_LIGHT).pack(anchor="w", pady=3)
tk.Checkbutton(opts_box, text="Special Characters (!@#$)", variable=special_var, bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=CARD_BG, font=("Segoe UI", 9), activebackground=CARD_BG, activeforeground=TEXT_LIGHT).pack(anchor="w", pady=3)

tk.Button(gen_card, text="Generate Password", command=generate_password, bg=ACCENT_BLUE, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", activebackground="#1d4ed8").pack(fill="x", pady=(15, 10), ipady=6)

out_row = tk.Frame(gen_card, bg=CARD_BG)
out_row.pack(fill="x", pady=5)
generated_var = tk.StringVar()
tk.Entry(out_row, textvariable=generated_var, state="readonly", font=("Consolas", 11), width=28).pack(side="left", ipady=4, expand=True, fill="x")
tk.Button(out_row, text="Copy", command=copy_password, width=9, font=("Segoe UI", 9, "bold"), bg="#334155", fg=TEXT_LIGHT, relief="flat", cursor="hand2").pack(side="right", padx=(8, 0))


# ==========================================
# VIEW 2: STRENGTH CHECKER
# ==========================================
checker_frame = tk.Frame(container, bg=BG_DARK)

check_card = tk.Frame(checker_frame, bg=CARD_BG, padx=16, pady=16)
check_card.pack(fill="x")

tk.Label(check_card, text="Password Strength Checker", font=("Segoe UI", 13, "bold"), bg=CARD_BG, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
tk.Label(check_card, text="Enter your password to check its strength:", font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))

check_entry = tk.Entry(check_card, font=("Consolas", 11))
check_entry.pack(fill="x", ipady=4)
# Bind key release for instant live updating
check_entry.bind("<KeyRelease>", evaluate_strength)

# --- RESULTS CONTAINER (Hidden initially until user types) ---
results_container = tk.Frame(check_card, bg=CARD_BG)

# Strength Status Row
status_row = tk.Frame(results_container, bg=CARD_BG)
status_row.pack(fill="x", pady=(10, 6))
tk.Label(status_row, text="Strength", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MUTED).pack(side="left")
strength_lbl = tk.Label(status_row, text="-", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_LIGHT)
strength_lbl.pack(side="right")

# Metrics Grid (Length & Character Variety Cards)
metrics_grid = tk.Frame(results_container, bg=CARD_BG)
metrics_grid.pack(fill="x", pady=4)

len_box = tk.Frame(metrics_grid, bg=CARD_INNER, padx=10, pady=8)
len_box.pack(side="left", expand=True, fill="x", padx=(0, 4))
tk.Label(len_box, text="LENGTH", font=("Segoe UI", 8, "bold"), bg=CARD_INNER, fg=TEXT_MUTED).pack()
length_val_lbl = tk.Label(len_box, text="0", font=("Segoe UI", 14, "bold"), bg=CARD_INNER, fg=TEXT_LIGHT)
length_val_lbl.pack()

var_box = tk.Frame(metrics_grid, bg=CARD_INNER, padx=10, pady=8)
var_box.pack(side="right", expand=True, fill="x", padx=(4, 0))
tk.Label(var_box, text="CHARACTER VARIETY", font=("Segoe UI", 8, "bold"), bg=CARD_INNER, fg=TEXT_MUTED).pack()
variety_val_lbl = tk.Label(var_box, text="0 / 4", font=("Segoe UI", 14, "bold"), bg=CARD_INNER, fg=TEXT_LIGHT)
variety_val_lbl.pack()

# Character Breakdown Section
breakdown_box = tk.Frame(results_container, bg=CARD_INNER, padx=12, pady=10)
breakdown_box.pack(fill="x", pady=(6, 4))
tk.Label(breakdown_box, text="CHARACTER BREAKDOWN", font=("Segoe UI", 8, "bold"), bg=CARD_INNER, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 4))

def create_row(parent, label_text):
    row = tk.Frame(parent, bg=CARD_INNER)
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label_text, font=("Segoe UI", 9), bg=CARD_INNER, fg=TEXT_LIGHT).pack(side="left")
    val_lbl = tk.Label(row, text="✘", font=("Segoe UI", 9, "bold"), bg=CARD_INNER, fg="#ef4444")
    val_lbl.pack(side="right")
    return val_lbl

upper_chk_lbl = create_row(breakdown_box, "Uppercase (A-Z)")
lower_chk_lbl = create_row(breakdown_box, "Lowercase (a-z)")
num_chk_lbl = create_row(breakdown_box, "Numbers (0-9)")
sym_chk_lbl = create_row(breakdown_box, "Symbols (!@#$)")

# Tips to Improve Section (Cleaned up borders)
tips_box = tk.Frame(results_container, bg=CARD_INNER, padx=12, pady=10)
tips_box.pack(fill="x", pady=(4, 0))
tk.Label(tips_box, text="TIPS TO IMPROVE", font=("Segoe UI", 8, "bold"), bg=CARD_INNER, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 2))

tips_text = tk.Text(tips_box, height=3, font=("Segoe UI", 8), bg=CARD_INNER, fg=TEXT_LIGHT, bd=0, highlightthickness=0, wrap="word")
tips_text.pack(fill="x")
tips_text.config(state="disabled")


# Start on Generator tab by default
show_generator()

root.mainloop()