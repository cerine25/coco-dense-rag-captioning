from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.experiment_common import EXPERIMENT_ROOT, read_json, sha256_ids, split_ids


DIMENSIONS = {"clip-b32": 512, "siglip-b16": 768, "dinov2-s": 384}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    original_splits = {
        name: split_ids(ROOT / "artifacts" / "splits" / f"{name}.json")
        for name in ("kb", "val", "test")
    }
    new_split = read_json(EXPERIMENT_ROOT / "splits" / "test_1000.json")
    rows = new_split["images"]
    new_ids = {int(row["image_id"]) for row in rows}

    require(len(original_splits["test"]) == 100, "Expected 100 original test images")
    require(len(rows) == 1000 and len(new_ids) == 1000, "Expected 1000 unique new test images")
    for split_name, ids in original_splits.items():
        overlap_count = len(ids & new_ids)
        require(
            overlap_count == 0,
            f"New test split overlaps original {split_name}: {overlap_count} IDs",
        )
    require(
        all(row["source"] == "val2017" for row in rows),
        "New test split contains records not sourced from val2017",
    )

    references = read_jsonl(EXPERIMENT_ROOT / "tables" / "eval_refs_test_1000.jsonl")
    reference_ids = {int(row["image_id"]) for row in references}
    require(reference_ids == new_ids, "Reference IDs do not match the new test split")
    counts = {image_id: 0 for image_id in new_ids}
    for row in references:
        counts[int(row["image_id"])] += 1
    require(
        all(count == 5 for count in counts.values()),
        "Expected five references per image",
    )

    for encoder, dimension in DIMENSIONS.items():
        directory = EXPERIMENT_ROOT / "embeddings" / encoder
        ids = np.load(directory / "ids_test_1000.npy")
        vectors = np.load(directory / "test_1000_img.npy")
        require(ids.shape == (1000,), f"{encoder}: expected 1000 embedding IDs")
        require(
            vectors.shape == (1000, dimension),
            f"{encoder}: expected embedding shape {(1000, dimension)}, got {vectors.shape}",
        )
        require(vectors.dtype == np.float32, f"{encoder}: embeddings must be float32")
        require(
            bool(np.isfinite(vectors).all()),
            f"{encoder}: embeddings contain non-finite values",
        )
        require(
            bool(np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5)),
            f"{encoder}: embeddings are not L2-normalized",
        )
        require(
            set(int(image_id) for image_id in ids) == new_ids,
            f"{encoder}: embedding IDs do not match the new test split",
        )

    frozen_paths = [
        ROOT / "artifacts" / "splits" / "test.json",
        ROOT / "artifacts" / "splits" / "val.json",
        ROOT / "artifacts" / "splits" / "kb.json",
        ROOT / "reports" / "tables" / "encoder_comparison_test.csv",
    ]
    missing_frozen_paths = [path for path in frozen_paths if not path.is_file()]
    if missing_frozen_paths:
        raise FileNotFoundError(
            "Missing frozen files required for verification: "
            + ", ".join(str(path.relative_to(ROOT)) for path in missing_frozen_paths)
        )

    report = {
        "original_test_count": len(original_splits["test"]),
        "new_test_count": len(new_ids),
        "overlap_count": len(original_splits["test"] & new_ids),
        "overlap_with_original_splits": {
            name: len(ids & new_ids) for name, ids in original_splits.items()
        },
        "new_test_id_hash": sha256_ids(new_ids),
        "frozen_file_hashes": {
            path.relative_to(ROOT).as_posix(): sha256_file(path) for path in frozen_paths
        },
    }
    (EXPERIMENT_ROOT / "manifests").mkdir(parents=True, exist_ok=True)
    (EXPERIMENT_ROOT / "manifests" / "verification.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Verified: 1000-image split is disjoint from all frozen splits and aligned")


if __name__ == "__main__":
    main()
