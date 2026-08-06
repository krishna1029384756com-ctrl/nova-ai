import tkinter as tk

window = None
canvas = None
emotion_label = None
status_label = None
message_label = None

# Same palette as frontend/style.css, so the desktop window matches the web UI
BG_OUTER = "#070B14"
CARD_BG = "#121826"
BORDER = "#1E293B"
ACCENT = "#3B82F6"
TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_MSG = ("Segoe UI", 10)

WIDTH = 380
HEIGHT = 260


def _rounded_rect(cv, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return cv.create_polygon(points, smooth=True, **kwargs)


# All update_* functions are safe to call from ANY thread (e.g. Flask's
# request-handling thread). Tkinter widgets may only be touched from the
# main thread, so we hop over to it via window.after(0, ...) instead of
# touching the widgets directly.

def update_emotion(text):
    if window and emotion_label:
        window.after(0, lambda: emotion_label.config(text=text))


def update_status(text):
    if window and status_label:
        window.after(0, lambda: status_label.config(text=f"Status: {text}"))


def update_message(text):
    if window and message_label:
        window.after(0, lambda: message_label.config(text=text))


def hide():
    if window:
        window.after(0, window.withdraw)


def show():
    if window:
        window.after(0, window.deiconify)
        window.after(0, window.lift)


def close():
    if window:
        window.after(0, window.destroy)


def start(start_hidden=True):
    global window, canvas, emotion_label, status_label, message_label

    window = tk.Tk()
    window.title("NOVA")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.resizable(False, False)
    window.configure(bg=BG_OUTER)
    window.protocol("WM_DELETE_WINDOW", hide)

    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg=BG_OUTER, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # A rounded "card" behind everything, echoing the glassmorphism panels
    # used in frontend/style.css (chat-container / modal-box).
    _rounded_rect(canvas, 14, 14, WIDTH - 14, HEIGHT - 14, 24, fill=CARD_BG, outline=BORDER, width=1)

    card = tk.Frame(canvas, bg=CARD_BG)
    canvas.create_window(WIDTH // 2, HEIGHT // 2, window=card, width=WIDTH - 70, height=HEIGHT - 50)

    title = tk.Label(card, text="🤖  NOVA", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_PRIMARY)
    title.pack(pady=(4, 14))

    emotion_label = tk.Label(card, text="😊 Happy", font=FONT_LABEL, bg=CARD_BG, fg=ACCENT)
    emotion_label.pack(pady=2)

    status_label = tk.Label(card, text="Status: Starting...", font=FONT_LABEL, bg=CARD_BG, fg=TEXT_SECONDARY)
    status_label.pack(pady=2)

    message_label = tk.Label(
        card, text="Welcome to NOVA!", font=FONT_MSG, bg=CARD_BG, fg=TEXT_SECONDARY,
        wraplength=WIDTH - 110, justify="center"
    )
    message_label.pack(pady=(14, 4))

    if start_hidden:
        window.withdraw()

    window.mainloop()
