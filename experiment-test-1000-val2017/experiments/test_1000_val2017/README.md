# Supplemental 1,000-image experiment

This is a supplemental 1,000-image query sample from COCO `val2017`. Its
selected IDs are disjoint from the original 100-image test IDs, but both
samples come from the same source split; this is not an independent dataset.
It is kept separate from the frozen 100-image Phase 1 experiment and does not
change its validation-based encoder selection.

## Inputs and outputs

The scripts expect the frozen Phase 1 files under `artifacts/`, COCO
`val2017` annotations under `data/raw/annotations/`, and downloaded images
under `data/raw/images/val2017/`. The raw dataset, generated images, and
embeddings are not tracked in Git. The experiment reuses the Phase 1 KB
captions, metadata, and embeddings when evaluating retrieval, so this workflow
cannot be run from a clean clone until the required frozen release assets have
been obtained or regenerated.

`results/encoder_comparison_test_1000.csv` and `.json` preserve the recorded
metrics. `splits/`, `tables/`, and `manifests/` preserve selected IDs,
references, query metadata, and verification evidence. Do not regenerate those
files merely to inspect the recorded results.

## Metric definitions and interpretation

- CIDEr compares the retrieved caption with the five human references using
  `pycocoevalcap`.
- Recall, precision, and MRR are based on category overlap: a retrieved KB
  item is considered relevant if its COCO ground-truth object categories
  intersect the query's COCO ground-truth categories. These are not image-ID
  retrieval metrics or human relevance judgments. Query labels are therefore
  oracle annotations.
- The reported latency is the median of five repeats of chunked NumPy exact
  inner-product search, not FAISS latency. It should not be compared directly
  with `artifacts/index/index_report.json`.
- The current evaluator uses the model/mode list in
  `scripts/compare_encoders.py`, retrieves top 10, and reports category
  metrics at 1, 5, and 10. The experiment `config.yaml` is descriptive rather
  than the active source of these settings.

Image preparation in this experiment uses Pillow thumbnailing and optimized
JPEG output. Unlike the original release preprocessing, it does not explicitly
apply EXIF transpose or set `subsampling=0`; this difference should be
considered in cross-experiment comparisons.

Commands:

```powershell
python scripts/build_test_1000_split.py
python scripts/prepare_test_1000.py
python scripts/build_test_1000_metadata.py
python scripts/build_test_1000_embeddings.py
python scripts/verify_test_1000.py
python scripts/evaluate_test_1000.py
```

Run one encoder or all encoders:

```powershell
python scripts/build_test_1000_embeddings.py --encoder clip-b32
python scripts/build_test_1000_embeddings.py --encoder siglip-b16
python scripts/build_test_1000_embeddings.py --encoder dinov2-s
```

Run all remaining stages:

```powershell
python scripts/run_test_1000.py
```

To resume from an existing stage:

```powershell
python scripts/run_test_1000.py --from-stage embeddings
```

The generated outputs remain under `experiments/test_1000_val2017/`.
