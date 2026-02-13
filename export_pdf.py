import json
import re

from collections import defaultdict
from fpdf import FPDF
from pathlib import Path

def normalize_text(s: str) -> str:
    if not s:
        return ""
    # replace common weird spaces with normal spaces
    s = s.replace("\u00A0", " ")  # non-breaking space
    s = s.replace("\u200B", "")   # zero-width space
    s = s.replace("\uFEFF", "")   # BOM / zero-width no-break

    # Normalize smart punctuation to regular ASCII (helps with PDF rendering and wrapping)
    s = (s.replace("’", "'")
           .replace("‘", "'")
           .replace("“", '"')
           .replace("”", '"')
           .replace("–", "-")
           .replace("—", "-"))

    # put spaces around slashes so long URLs can wrap
    s = s.replace("/", "/ ")
    s = s.replace("-", "- ")  # helps wrap long hyphenated strings
    s = s.replace("_", "_ ")  # helps wrap snake_case

    # remove all control chars except newline and tab
    s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", s)

    # final safety net (never crash)
    s = force_wrap_long_tokens(s, chunk=18)

    return s

def force_wrap_long_tokens(text: str, chunk=20) -> str:
    """
    Ensures no token is longer than `chunk` characters by injecting spaces.
    This prevents fpdf from choking on long URLs/handles.
    """
    parts = text.split(" ")
    out = []
    for p in parts:
        if len(p) <= chunk:
            out.append(p)
        else:
            # break long token into smaller chunks
            out.append(" ".join(p[i:i+chunk] for i in range(0, len(p), chunk)))
    return " ".join(out)


def load_tweets(path="tweets.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def categorize(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["java", "spring", "api", "python", "code", "backend"]):
        return "Software Development"
    if any(k in t for k in ["ai", "robotics", "llm", "chatgpt", "gemini", "grok", "ai model"]):
        return "Tech"
    if any(k in t for k in ["invest", "stock", "market", "sip", "nifty", "amd", "nvda", "tesla", "crypto", "bitcoin", "ethereum"]):
        return "Finance"
    if any(k in t for k in ["discipline", "habit", "consistency", "mindset"]):
        return "Life Advice"
    if any(k in t for k in ["sleep", "focus", "routine", "productivity", "time", "energy", "job", "work"]):
        return "Productivity"
    return "Other"

def group(tweets):
    d = defaultdict(list)
    for t in tweets:
        d[categorize(t["text"])].append(t)
    return d

def export_pdf(grouped, out_path="exports/X2PDF.pdf"):
    Path("exports").mkdir(exist_ok=True)

    pdf = FPDF(format="A4")
    pdf.add_font("OpenSans", "", "fonts/OpenSans-Regular.ttf", uni=True)
    pdf.add_font("OpenSans", "B", "fonts/OpenSans-Bold.ttf", uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)

    def heading(txt):
        pdf.set_font("OpenSans", "B", 18)
        pdf.cell(0, 10, txt, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    def para(txt, size=12):
        pdf.set_font("OpenSans", "", size)
        pdf.multi_cell(0, 7, txt)   # slightly taller line height
        pdf.ln(3)                   # space after paragraph

    pdf.add_page()
    heading("X2PDF")
    para("Your tweets, grouped into categories.")

    for cat in sorted(grouped.keys()):
        pdf.add_page()
        heading(cat)

        for tw in grouped[cat]:
            created = normalize_text(tw.get("created_at", ""))
            text = normalize_text(tw.get("text", ""))

            # Date in gray, smaller font
            pdf.set_font("OpenSans", "", 10)
            pdf.set_text_color(120, 120, 120)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 6, created)

            # Tweet text in black, normal font
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("OpenSans", "", 12)
            pdf.set_x(pdf.l_margin)

            try:
                pdf.multi_cell(0, 7, text)
            except Exception as e:
                print("FAILED TEXT:", repr(tw.get("text", "")))
                print("AFTER normalize:", repr(text))
                print("X:", pdf.get_x(), "Y:", pdf.get_y(), "LM:", pdf.l_margin, "RM:", pdf.r_margin, "W:", pdf.w)
                raise
            
            # Divider line
            pdf.set_draw_color(220, 220, 220)
            x1 = pdf.l_margin
            x2 = pdf.w - pdf.r_margin
            y = pdf.get_y()
            pdf.line(x1, y, x2, y)

            # Space after each tweet
            pdf.ln(6)

    pdf.output(out_path)
    print("Saved:", out_path)

if __name__ == "__main__":
    tweets = load_tweets()
    grouped = group(tweets)
    export_pdf(grouped)