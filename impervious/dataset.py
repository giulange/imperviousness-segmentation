"""Costruzione del dataset YOLO: split train/val/test + data.yaml.

Estratto da DL_modeling.py. Prende i tile che hanno una label (.txt) e li copia
nella struttura attesa da Ultralytics: images/{train,val,test} + labels/{...}.
"""

from __future__ import annotations

import glob
import random
import shutil
from pathlib import Path

import yaml

__all__ = ["split_train_val_test", "write_data_yaml"]

_SPLITS = ("train", "val", "test")


def split_train_val_test(tiles_dir, out_dir, *, ratios=None, seed=3008) -> dict:
    """Divide i tile annotati in train/val/test e li copia in `out_dir`.

    `tiles_dir` contiene i .tif e i .txt affiancati. Ritorna il conteggio per split.
    """
    ratios = ratios or {"train": 0.7, "val": 0.2, "test": 0.1}
    tiles_dir, out_dir = Path(tiles_dir), Path(out_dir)

    labels = sorted(glob.glob(str(tiles_dir / "*.txt")))
    stems = [Path(p).stem for p in labels if (tiles_dir / f"{Path(p).stem}.tif").exists()]
    random.seed(seed)
    random.shuffle(stems)

    n = len(stems)
    n_tr = int(n * ratios["train"])
    n_va = int(n * ratios["val"])
    buckets = {"train": stems[:n_tr], "val": stems[n_tr:n_tr + n_va], "test": stems[n_tr + n_va:]}

    for split in _SPLITS:
        (out_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (out_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
        for stem in buckets[split]:
            shutil.copy2(tiles_dir / f"{stem}.tif", out_dir / "images" / split / f"{stem}.tif")
            shutil.copy2(tiles_dir / f"{stem}.txt", out_dir / "labels" / split / f"{stem}.txt")
    return {s: len(buckets[s]) for s in _SPLITS}


def write_data_yaml(yaml_path, dataset_root, classes) -> str:
    """Scrive il data.yaml di Ultralytics con path assoluto e nomi classi."""
    data = {
        "path": str(Path(dataset_root).resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": dict(classes),
    }
    with open(yaml_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return str(yaml_path)
