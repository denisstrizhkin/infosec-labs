from typing import Self
import base64
from pathlib import Path

import typer
from PIL import Image


class BitIterator:
    def __init__(self, img: Image.Image):
        self._img = img
        self._rgb_i = 0
        self._pixel_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self._pixel_i >= self._img.width * self._img.height:
            raise StopIteration

        xy = (
            self._pixel_i % self._img.width,
            self._pixel_i // self._img.width,
        )
        rgb = list(self._img.getpixel(xy))
        bit = rgb[self._rgb_i] & 0b00000001

        self._rgb_i += 1
        if self._rgb_i >= 3:
            self._rgb_i = 0
            self._pixel_i += 1

        return bit


class ByteIterator:
    def __init__(self, img: Image.Image):
        self._bit_iter = BitIterator(img)
        self._bit_i = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> bytes:
        byte = 0
        for i in range(8):
            byte = (byte << 1) | next(self._bit_iter)
        return byte.to_bytes(1)


def decode_img(img: Image.Image) -> str:
    data = b""
    for byte in ByteIterator(img):
        if byte == b"\0":
            try:
                return base64.b64decode(data).decode("utf8")
            except Exception as e:
                raise ValueError(
                    f"Encoded data is incorrect or corrupted: {e}"
                )
        data += byte

    raise ValueError("Image does not contain encoded data")


def main(img_path: Path):
    img = Image.open(img_path).convert("RGB")

    data = decode_img(img)
    print(data)


if __name__ == "__main__":
    typer.run(main)
