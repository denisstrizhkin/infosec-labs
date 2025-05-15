from typing import Self

import sys
import base64
from pathlib import Path

import typer
from PIL import Image


def get_stdin() -> str:
    return sys.stdin.read()


class BitIterator:
    def __init__(self, data: bytes):
        self._data = data
        self._byte_i = 0
        self._bit_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self._byte_i >= len(self._data):
            raise StopIteration

        byte = self._data[self._byte_i]
        bit = (byte >> (7 - self._bit_i)) & 1

        self._bit_i += 1
        if self._bit_i >= 8:
            self._bit_i = 0
            self._byte_i += 1

        return bit


def encode_img(img: Image.Image, s: str):
    data = base64.b64encode(s.encode("utf8")) + b"\0"
    img_size = img.width * img.height
    if img_size * 3 // 8 < len(data):
        raise ValueError("Not enough pixels to encode all of the data.")

    for i, bit in enumerate(BitIterator(data)):
        pi = i // 3
        rgbi = i % 3
        xy = (pi % img.width, pi // img.width)
        rgb = list(img.getpixel(xy))
        rgb[rgbi] = (rgb[rgbi] & 0b11111110) | bit
        img.putpixel(xy, tuple(rgb))


def main(img_path: Path):
    img = Image.open(img_path).convert("RGB")

    data = get_stdin()
    encode_img(img, data)

    new_name = img_path.stem + "_encoded.png"
    img.save(img_path.with_name(new_name))


if __name__ == "__main__":
    typer.run(main)
