#!/usr/bin/env python3
"""Convert HDF5 loss-surface files from tomgoldstein/loss-landscape to JSON.

The original repo's ``plot_surface.py`` generates ``.h5`` files containing 2D
loss surfaces evaluated on a filter-normalized grid.  This script reads those
files and writes lightweight JSON that the browser visualization can ``fetch``.

Prerequisites
─────────────
  pip install h5py numpy

Generating the .h5 files (run in the loss-landscape repo clone)
───────────────────────────────────────────────────────────────
  # Example: ResNet-56 with skip connections, 51×51 grid, filter-normalized
  mpirun -n 4 python plot_surface.py --mpi --cuda \\
      --model resnet56 \\
      --model_file cifar10/trained_nets/resnet56_sgd_lr=0.1_bs=128_wd=0.0005/model_300.t7 \\
      --x=-1:1:51 --y=-1:1:51 \\
      --dir_type weights --xnorm filter --xignore biasbn \\
      --ynorm filter --yignore biasbn

  # ResNet-56 *without* skip connections
  mpirun -n 4 python plot_surface.py --mpi --cuda \\
      --model resnet56_noshort \\
      --model_file cifar10/trained_nets/resnet56_noshort_sgd_lr=0.1_bs=128_wd=0.0005/model_300.t7 \\
      --x=-1:1:51 --y=-1:1:51 \\
      --dir_type weights --xnorm filter --xignore biasbn \\
      --ynorm filter --yignore biasbn

Running this converter
──────────────────────
  python tools/h5_to_json.py <surface.h5> \\
      --model "ResNet-56" --depth 56 --skip \\
      --output data/resnet56.json

  python tools/h5_to_json.py <surface_noshort.h5> \\
      --model "ResNet-56-noshort" --depth 56 --no-skip \\
      --output data/resnet56_noshort.json

The resulting JSON has the schema expected by ``index.html``:
  { "model": str, "skip": bool, "depth": int,
    "xrange": [float, float], "yrange": [float, float],
    "z": [[float, ...], ...] }
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np


def h5_to_dict(
    h5_path: str,
    *,
    model: str,
    depth: int,
    skip: bool,
    loss_key: str = "train_loss",
) -> dict[str, Any]:
    """Read an HDF5 surface file and return a JSON-serializable dict.

    Args:
        h5_path: Path to the .h5 file produced by plot_surface.py.
        model: Human-readable model name (e.g. "ResNet-56").
        depth: Network depth (20, 56, 110).
        skip: Whether skip connections are enabled.
        loss_key: HDF5 dataset key for the loss matrix.

    Returns:
        Dict matching the JSON schema consumed by the visualizer.
    """
    with h5py.File(h5_path, "r") as f:
        xcoords: np.ndarray = f["xcoordinates"][:]
        ycoords: np.ndarray = f["ycoordinates"][:]
        z_raw: np.ndarray = f[loss_key][:]

    # The h5 stores z[i][j] where i indexes xcoordinates, j indexes
    # ycoordinates.  Our visualizer expects z[row][col] where rows map
    # to the Plotly y-axis and cols to the x-axis — so we transpose.
    z_transposed: np.ndarray = z_raw.T

    return {
        "model": model,
        "skip": skip,
        "depth": depth,
        "xrange": [float(xcoords[0]), float(xcoords[-1])],
        "yrange": [float(ycoords[0]), float(ycoords[-1])],
        "z": [[round(float(v), 6) for v in row] for row in z_transposed],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("h5_file", type=str, help="Path to the .h5 surface file")
    parser.add_argument("--model", required=True, help='Model label, e.g. "ResNet-56"')
    parser.add_argument("--depth", required=True, type=int, help="Network depth (20, 56, 110)")

    skip_group = parser.add_mutually_exclusive_group(required=True)
    skip_group.add_argument("--skip", action="store_true", dest="skip", help="Model has skip connections")
    skip_group.add_argument("--no-skip", action="store_false", dest="skip", help="Model lacks skip connections")

    parser.add_argument("--loss-key", default="train_loss", help="HDF5 dataset key (default: train_loss)")
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output JSON path (default: ./data/<model>.json)",
    )
    args = parser.parse_args()

    output_path = args.output or str(
        Path(__file__).resolve().parent.parent
        / "data"
        / (args.model.lower().replace("-", "").replace(" ", "_") + ".json")
    )

    data = h5_to_dict(
        args.h5_file,
        model=args.model,
        depth=args.depth,
        skip=args.skip,
        loss_key=args.loss_key,
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))

    rows = len(data["z"])
    cols = len(data["z"][0]) if rows > 0 else 0
    print(f"Wrote {output_path}  ({rows}x{cols} grid, skip={args.skip})")


if __name__ == "__main__":
    main()
