from typing import Self
import wave
from pathlib import Path


class AudioData:
    def __init__(
        self,
        frames: bytes,
        nchannels: int,
        sampwidth: int,
        framerate: int,
        nframes: int,
    ):
        self._frames = bytearray(frames)
        self._nchannels = nchannels
        self._sampwidth = sampwidth
        self._framerate = framerate
        self._nframes = nframes

    @classmethod
    def open(cls, audio_path: Path) -> Self:
        with open(audio_path, "rb") as f:
            with wave.open(f) as audio:
                return AudioData(
                    audio.readframes(audio.getnframes()),
                    audio.getnchannels(),
                    audio.getsampwidth(),
                    audio.getframerate(),
                    audio.getnframes(),
                )

    def save(self, audio_path: Path):
        with open(audio_path, "wb") as f:
            with wave.open(f) as audio:
                audio.setnchannels(self.nchannels)
                audio.setsampwidth(self.sampwidth)
                audio.setframerate(self.framerate)
                audio.setnframes(self.nframes)
                audio.writeframes(self.frames)

    @property
    def frames(self) -> bytes:
        return self._frames

    @property
    def nchannels(self) -> int:
        return self._nchannels

    @property
    def sampwidth(self) -> int:
        return self._sampwidth

    @property
    def framerate(self) -> int:
        return self._framerate

    @property
    def nframes(self) -> int:
        return self._nframes

    def get_sample(self, nframe: int, nchannel: int) -> bytes:
        start = (nframe * self.nchannels + nchannel) * self.sampwidth
        return self.frames[start : start + self.sampwidth]

    def set_sample(self, nframe: int, nchannel: int, sample: bytes):
        start = (nframe * self.nchannels + nchannel) * self.sampwidth
        self.frames[start : start + self.sampwidth] = sample
