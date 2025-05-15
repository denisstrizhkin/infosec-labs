import sys
import base64
from pathlib import Path

import typer
from PIL import Image


def get_stdin_b64() -> bytes:
    s = sys.stdin.read()
    return base64.b64encode(s.encode("utf8"))


def encode_red(color: int, data: int) -> int:
    data = (data & 0b11100000) >> 5
    return (color & 0b11111000) | data


def encode_green(color: int, data: int) -> int:
    data = (data & 0b00011100) >> 2
    return (color & 0b11111000) | data


def encode_blue(color: int, data: int) -> int:
    data = data & 0b00000011
    return (color & 0b11111100) | data


def encode_img(img: Image.Image, data: bytes):
    data = data + b"\0"
    img_size = img.width * img.height
    if img_size < len(data):
        raise ValueError("Not enough pixels to encode all of the data.")

    for i, c in enumerate(data):
        x = i % img.width
        y = i // img.width
        (r, g, b) = img.getpixel((x, y))
        r = encode_red(r, c)
        g = encode_green(g, c)
        b = encode_blue(b, c)
        img.putpixel((x, y), (r, g, b))


def main(img_path: Path):
    img = Image.open(img_path).convert("RGB")

    data = get_stdin_b64()
    encode_img(img, data)

    new_name = img_path.stem + "_encoded.png"
    img.save(img_path.with_name(new_name))


if __name__ == "__main__":
    typer.run(main)
