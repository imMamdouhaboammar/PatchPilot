#!/usr/bin/env python3
"""
build_social_preview.py
=======================

Generates a 1280x640 GitHub social preview image for PatchPilot.

The image is a clean, technical banner: dark navy background with
brand text on the left, a pull-request workflow diagram on the right.

No third-party dependencies beyond Pillow.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Brand colors
BG_TOP = (13, 17, 23)         # GitHub dark
BG_BOTTOM = (26, 35, 50)      # navy
ACCENT = (88, 166, 255)       # GitHub accent blue
ACCENT_DIM = (48, 96, 160)
SUCCESS = (63, 185, 80)       # GitHub green
WARN = (255, 191, 0)          # amber
TEXT = (240, 246, 252)
TEXT_DIM = (139, 148, 158)
GRID = (33, 38, 45)

WIDTH = 1280
HEIGHT = 640
OUTPUT = Path(__file__).resolve().parent.parent / ".github" / "social-preview.png"

# macOS TrueType collections: index 0 is Regular, 1 is Bold in Helvetica.ttc
HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
HELVETICA_NEU = "/System/Library/Fonts/HelveticaNeue.ttc"
MENLO = "/System/Library/Fonts/Menlo.ttc"


def load_font(path: str, size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    index = 1 if bold else 0
    return ImageFont.truetype(path, size, index=index)


def measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def gradient_bg(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), BG_TOP)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / height
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img


def draw_grid(img: Image.Image) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    step = 40
    for x in range(0, img.width, step):
        draw.line([(x, 0), (x, img.height)], fill=GRID + (40,), width=1)
    for y in range(0, img.height, step):
        draw.line([(0, y), (img.width, y)], fill=GRID + (40,), width=1)
    img.paste(overlay, (0, 0), overlay)


def draw_brand(draw: ImageDraw.ImageDraw) -> None:
    title_font = load_font(HELVETICA, 96, bold=True)
    sub_font = load_font(HELVETICA, 30)
    micro_font = load_font(HELVETICA, 18)
    pill_font = load_font(HELVETICA, 18, bold=True)

    x = 70
    y = 220

    # Accent dot
    draw.ellipse([x, y + 18, x + 30, y + 48], fill=ACCENT)
    # Brand name
    draw.text((x + 50, y - 5), "PatchPilot", font=title_font, fill=TEXT)

    # Subtitle
    draw.text(
        (x + 4, y + 130),
        "A PR-only GitHub coding agent kit for ChatGPT Web",
        font=sub_font,
        fill=TEXT_DIM,
    )

    # Pill with the workflow
    pill_text = "  inspect  ->  branch  ->  commit  ->  open PR  ->  hand off  "
    tw, _ = measure(draw, pill_text, font=pill_font)
    pill_w = tw + 40
    pill_h = 48
    py = y + 195
    draw.rounded_rectangle(
        [x, py, x + pill_w, py + pill_h],
        radius=pill_h // 2,
        fill=(22, 27, 34),
        outline=ACCENT_DIM,
        width=2,
    )
    draw.text((x + 20, py + 13), pill_text.strip(), font=pill_font, fill=ACCENT)

    # Footer
    footer = "github.com/imMamdouhaboammar/PatchPilot   -   MIT   -   v1.1.0"
    draw.text((x, 560), footer, font=micro_font, fill=TEXT_DIM)


def draw_workflow(draw: ImageDraw.ImageDraw) -> None:
    """Three-node PR workflow on the right side."""
    cx_main = 1060
    cy_main = 320
    r = 22
    label_font = load_font(HELVETICA, 14, bold=True)
    cap_font = load_font(HELVETICA, 18)

    nodes = [
        (cx_main, cy_main - 140, "main", ACCENT, (248, 249, 250)),
        (cx_main - 200, cy_main, "feat", SUCCESS, (13, 17, 23)),
        (cx_main, cy_main + 140, "PR #1", WARN, (13, 17, 23)),
    ]

    # Connecting lines (drawn first so nodes sit on top)
    draw.line([nodes[0][:2], nodes[1][:2]], fill=ACCENT_DIM, width=3)
    draw.line([nodes[1][:2], nodes[2][:2]], fill=ACCENT_DIM, width=3)
    # PR review back to main
    for t in range(0, 11):
        x0, y0 = nodes[2][:2]
        x1, y1 = nodes[0][:2]
        t_norm = t / 10
        x = x0 + (x1 - x0) * t_norm
        y = y0 + (y1 - y0) * t_norm
        if t % 2 == 0:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(139, 148, 158))

    for x, y, label, color, text_color in nodes:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=BG_TOP, width=3)
        tw, th = measure(draw, label, font=label_font)
        draw.text((x - tw / 2, y - th / 2 - 2), label, font=label_font, fill=text_color)

    # Caption
    cap_text = "PR-only by design"
    tw, _ = measure(draw, cap_text, font=cap_font)
    draw.text(
        (cx_main - tw / 2, 510),
        cap_text,
        font=cap_font,
        fill=TEXT_DIM,
    )


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img = gradient_bg(WIDTH, HEIGHT)
    draw_grid(img)
    d = ImageDraw.Draw(img)
    draw_brand(d)
    draw_workflow(d)
    img.save(OUTPUT, format="PNG", optimize=True)
    size = OUTPUT.stat().st_size
    print(f"Wrote {OUTPUT} ({size:,} bytes, {WIDTH}x{HEIGHT}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
