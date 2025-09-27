"""
Vaporwave effects package
"""

from .base import BaseEffect
from .chromatic import ChromaticAberrationEffect
from .holographic import HolographicEffect
from .neon import NeonGlowEffect
from .scanlines import ScanlinesEffect
from .vhs import VHSEffect

__all__ = [
    "BaseEffect",
    "ChromaticAberrationEffect",
    "HolographicEffect",
    "NeonGlowEffect",
    "ScanlinesEffect",
    "VHSEffect",
]
