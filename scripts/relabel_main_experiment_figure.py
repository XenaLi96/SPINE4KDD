#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "main_exp.png"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BLACK = (0, 0, 0, 255)
TARGET = (0, 205, 35, 255)
MODEL = (203, 76, 76, 255)


def relabel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    color: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont,
) -> None:
    draw.rectangle(box, fill=BLACK)
    left, top, right, bottom = box
    width, height = draw.textsize(text, font=font)
    x = left + (right - left - width) / 2
    y = top + (bottom - top - height) / 2
    draw.text((x, y), text, fill=color, font=font)


def main() -> None:
    image = Image.open(IMAGE).convert("RGBA")
    if image.size != (4926, 1323):
        raise ValueError(f"Unexpected main_exp.png size: {image.size}")

    draw = ImageDraw.Draw(image)
    label_font = ImageFont.truetype(FONT_PATH, 42)
    compact_font = ImageFont.truetype(FONT_PATH, 36)

    labels = [
        ((340, 130, 710, 320), "PPP target", TARGET, label_font),
        ((1090, 130, 1510, 320), "SPINE", MODEL, label_font),
        ((1870, 100, 2240, 250), "PPP target", TARGET, label_font),
        ((2520, 100, 2850, 250), "SPINE", MODEL, label_font),
        ((3460, 100, 3840, 250), "PPP target", TARGET, label_font),
        ((4120, 100, 4490, 250), "SPINE", MODEL, label_font),
        ((1870, 720, 2240, 805), "PPP target", TARGET, label_font),
        ((2520, 720, 2850, 805), "SPINE", MODEL, label_font),
        ((3450, 720, 4060, 805), "PPP target  Delta C1qa", TARGET, compact_font),
        ((4110, 720, 4720, 805), "SPINE  Delta C1qa", MODEL, compact_font),
    ]
    for box, text, color, font in labels:
        relabel(draw, box, text, color, font)

    image.save(IMAGE)


if __name__ == "__main__":
    main()
