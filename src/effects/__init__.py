"""Vaporwave effects package.

This module provides image effects for creating vaporwave-style aesthetics,
including chromatic aberration, holographic overlays, neon glow, scanlines,
and VHS distortion effects.
"""

from __future__ import annotations

from enum import StrEnum

from .base import BaseEffect
from .chromatic import ChromaticAberrationEffect
from .holographic import HolographicEffect
from .neon import NeonGlowEffect
from .scanlines import ScanlinesEffect
from .vhs import VHSEffect


class EffectName(StrEnum):
    """Enumeration of available effect names.

    Use these constants instead of magic strings when specifying effects
    to enable type checking and IDE autocompletion.

    Example:
        >>> processor = VaporwaveProcessor()
        >>> processor.process(input_path, output_path, effects=[EffectName.CHROMATIC])
    """

    CHROMATIC = "chromatic"
    HOLOGRAPHIC = "holographic"
    NEON = "neon"
    SCANLINES = "scanlines"
    VHS = "vhs"

    @classmethod
    def all(cls) -> list[str]:
        """Return a list of all effect names as strings."""
        return [effect.value for effect in cls]


# Mapping from effect names to effect classes
EFFECT_REGISTRY: dict[EffectName | str, type[BaseEffect]] = {
    EffectName.CHROMATIC: ChromaticAberrationEffect,
    EffectName.HOLOGRAPHIC: HolographicEffect,
    EffectName.NEON: NeonGlowEffect,
    EffectName.SCANLINES: ScanlinesEffect,
    EffectName.VHS: VHSEffect,
}


def get_effect_class(name: EffectName | str) -> type[BaseEffect]:
    """Get the effect class for a given effect name.

    Args:
        name: The effect name (can be EffectName enum or string).

    Returns:
        The corresponding effect class.

    Raises:
        ValueError: If the effect name is not recognized.

    Example:
        >>> effect_cls = get_effect_class(EffectName.NEON)
        >>> effect = effect_cls(intensity=1.5)
    """
    # Normalize string to enum if needed
    if isinstance(name, str) and not isinstance(name, EffectName):
        try:
            name = EffectName(name.lower())
        except ValueError:
            valid_names = ", ".join(EffectName.all())
            raise ValueError(
                f"Unknown effect: {name!r}. Valid effects are: {valid_names}"
            ) from None

    if name not in EFFECT_REGISTRY:
        valid_names = ", ".join(EffectName.all())
        raise ValueError(f"Unknown effect: {name!r}. Valid effects are: {valid_names}")

    return EFFECT_REGISTRY[name]


__all__ = [
    "BaseEffect",
    "ChromaticAberrationEffect",
    "EffectName",
    "EFFECT_REGISTRY",
    "get_effect_class",
    "HolographicEffect",
    "NeonGlowEffect",
    "ScanlinesEffect",
    "VHSEffect",
]
