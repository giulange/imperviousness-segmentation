"""Wrapper di training/inferenza YOLO-seg (Ultralytics). Estratto da DL_modeling.py.

Gestisce anche la selezione di una slice MIG dell'A100 via CUDA_VISIBLE_DEVICES
(la VM `ai-lab` ha l'A100 in MIG: una GPU logica = una slice da 10GB).
"""

from __future__ import annotations

import os
import subprocess

__all__ = ["first_mig_uuid", "train", "predict"]


def first_mig_uuid():
    """UUID della prima slice MIG (o None se MIG non attiva). Usa `nvidia-smi -L`."""
    try:
        out = subprocess.check_output(["nvidia-smi", "-L"], text=True)
    except Exception:
        return None
    for tok in out.split():
        if tok.startswith("MIG-"):
            return tok.strip(")")
    return None


def _pin_mig(mig_uuid):
    if mig_uuid:
        os.environ["CUDA_VISIBLE_DEVICES"] = mig_uuid


def train(data_yaml, *, model="yolov8n-seg.pt", epochs=100, imgsz=480, batch=4,
          workers=2, cache=True, device=0, mig_uuid=None, **kwargs):
    """Allena un modello YOLO-seg. Se `mig_uuid` è dato, pinna quella slice MIG."""
    _pin_mig(mig_uuid)
    from ultralytics import YOLO

    yolo = YOLO(model)
    return yolo.train(data=str(data_yaml), epochs=epochs, imgsz=imgsz, batch=batch,
                      workers=workers, cache=cache, device=device, **kwargs)


def predict(weights, source, *, imgsz=480, device=0, mig_uuid=None, **kwargs):
    """Inferenza con un modello allenato su immagini/cartella `source`."""
    _pin_mig(mig_uuid)
    from ultralytics import YOLO

    yolo = YOLO(str(weights))
    return yolo.predict(source=str(source), imgsz=imgsz, device=device, **kwargs)
