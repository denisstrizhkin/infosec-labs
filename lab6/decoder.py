import sys
import base64
from pathlib import Path

import typer
from PIL import Image


def get_stdin_b64() -> bytes:
    s = sys.stdin.read()
    return base64.b64encode(s.encode("utf8"))


def decode_rgb(r: int, g: int, b: int) -> int:
    r = (r & 0b00000111) << 5
    g = (g & 0b00000111) << 2
    b = b & 0b00000011
    return r | g | b


def decode_img(img: Image.Image) -> str:
    data = b""
    img_size = img.width * img.height
    for i in range(img_size):
        x = i % img.width
        y = i // img.width
        (r, g, b) = img.getpixel((x, y))
        c = decode_rgb(r, g, b)
        if c == 0:
            return base64.b64decode(data).decode("utf8")
        data += c.to_bytes()
    raise ValueError("Image does not contain encoded data")


def main(img_path: Path):
    img = Image.open(img_path).convert("RGB")

    data = decode_img(img)
    print(data)


if __name__ == "__main__":
    typer.run(main)
