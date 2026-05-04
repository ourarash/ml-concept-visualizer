#!/usr/bin/env python3
"""Generate synthetic loss surfaces for development and testing.

These are PLACEHOLDER surfaces that mimic the qualitative behavior described in
Li et al., "Visualizing the Loss Landscape of Neural Nets" (NeurIPS 2018):

  - With skip connections: smooth, approximately convex bowl
  - Without skip connections: chaotic landscape with many local minima
  - Deeper networks without skip connections have MORE chaotic landscapes

The surfaces are NOT computed from real models. Replace with real data generated
by tomgoldstein/loss-landscape's plot_surface.py + h5_to_json.py for accuracy.

Usage:
    python tools/synth_surfaces.py          # writes to ./data/
    python tools/synth_surfaces.py --outdir /some/other/path
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final


GRID_SIZE: Final[int] = 51
RANGE: Final[tuple[float, float]] = (-1.0, 1.0)


@dataclass(frozen=True)
class SurfaceConfig:
    """Parameters for one synthetic surface."""

    name: str
    model_label: str
    depth: int
    skip: bool
    base_curvature: float
    noise_modes: int
    noise_amplitude: float
    seed: int


# fmt: off
CONFIGS: tuple[SurfaceConfig, ...] = (
    SurfaceConfig("resnet20",         "ResNet-20",          20,  True,  1.0, 0,  0.0,   42),
    SurfaceConfig("resnet20_noshort", "ResNet-20-noshort",  20,  False, 0.8, 6,  0.25,  43),
    SurfaceConfig("resnet56",         "ResNet-56",          56,  True,  1.2, 0,  0.0,   44),
    SurfaceConfig("resnet56_noshort", "ResNet-56-noshort",  56,  False, 0.6, 10, 0.55,  45),
    SurfaceConfig("resnet110",        "ResNet-110",         110, True,  1.4, 2,  0.03,  46),
    SurfaceConfig("resnet110_noshort","ResNet-110-noshort", 110, False, 0.4, 16, 1.0,   47),
)
# fmt: on


def _linspace(lo: float, hi: float, n: int) -> list[float]:
    """Pure-Python linspace (no numpy dependency)."""
    if n == 1:
        return [(lo + hi) / 2.0]
    step = (hi - lo) / (n - 1)
    return [lo + i * step for i in range(n)]


def _simple_hash(seed: int, i: int, j: int) -> float:
    """Deterministic pseudo-random float in [0, 1) from integer inputs.

    Uses a basic LCG-style hash — NOT cryptographic, just reproducible noise.
    """
    h = seed * 374761393 + i * 668265263 + j * 2147483647
    h = (h ^ (h >> 13)) * 1274126177
    h = h ^ (h >> 16)
    return (h & 0x7FFFFFFF) / 0x7FFFFFFF


def generate_surface(cfg: SurfaceConfig) -> list[list[float]]:
    """Build a 2D loss surface on a GRID_SIZE x GRID_SIZE grid in RANGE^2.

    Skip-on surfaces are smooth bowls. Skip-off surfaces add Gaussian bumps
    (hills) at pseudo-random locations, creating ridges and valleys that trap
    gradient descent — the valleys between bumps act as local minima.
    """
    xs = _linspace(RANGE[0], RANGE[1], GRID_SIZE)
    ys = _linspace(RANGE[0], RANGE[1], GRID_SIZE)

    # Pre-generate Gaussian bump parameters for noshort surfaces.
    # Each bump is a hill that creates barriers; valleys form between bumps.
    bumps: list[tuple[float, float, float, float]] = []  # (cx, cy, height, sigma)
    for m in range(cfg.noise_modes):
        cx = _simple_hash(cfg.seed, m, 0) * 1.6 - 0.8   # center x in [-0.8, 0.8]
        cy = _simple_hash(cfg.seed, m, 1) * 1.6 - 0.8   # center y
        height = cfg.noise_amplitude * (0.5 + _simple_hash(cfg.seed, m, 2))
        sigma = 0.12 + _simple_hash(cfg.seed, m, 3) * 0.18  # width 0.12–0.30
        bumps.append((cx, cy, height, sigma))

    z: list[list[float]] = []
    for i, x in enumerate(xs):
        row: list[float] = []
        for j, y in enumerate(ys):
            # Base bowl centered at (0, 0) — the "global minimum"
            base = cfg.base_curvature * (x * x + y * y)

            # Gaussian bumps create ridges and barriers.
            # Radial damping keeps the center (trained checkpoint) clean.
            r2 = x * x + y * y
            radial_damp = r2 / (r2 + 0.03)

            bump_sum = 0.0
            for cx, cy, height, sigma in bumps:
                dist2 = (x - cx) ** 2 + (y - cy) ** 2
                bump_sum += height * math.exp(-dist2 / (2.0 * sigma * sigma))

            depth_factor = 1.0 + 0.003 * cfg.depth if not cfg.skip else 1.0
            value = base + bump_sum * radial_damp * depth_factor

            # Small offset so log(z+1) is well-behaved at the minimum
            value = max(value, 0.005)
            row.append(round(value, 6))
        z.append(row)

    return z


def write_surface(cfg: SurfaceConfig, outdir: Path) -> None:
    """Generate and write one surface JSON file."""
    z = generate_surface(cfg)
    payload = {
        "model": cfg.model_label,
        "skip": cfg.skip,
        "depth": cfg.depth,
        "xrange": list(RANGE),
        "yrange": list(RANGE),
        "z": z,
        "_synthetic": True,
        "_note": "Placeholder surface for development. Replace with real data.",
    }
    path = outdir / f"{cfg.name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(",", ":"))
    print(f"  wrote {path}  ({len(z)}x{len(z[0])} grid)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data",
        help="Output directory for JSON files (default: ./data/)",
    )
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(CONFIGS)} synthetic surfaces...")
    for cfg in CONFIGS:
        write_surface(cfg, args.outdir)
    print("Done. These are PLACEHOLDERS — see tools/h5_to_json.py for real data.")


if __name__ == "__main__":
    main()
