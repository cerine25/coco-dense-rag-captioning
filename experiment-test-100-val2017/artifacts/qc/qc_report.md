# QC — g1-v1.1
**PASS** — 40 checks, 0 failures, 0 warnings

| check | status | detail |
|---|---|---|
| KB split size | PASS | 10000 vs 10000 |
| KB ID hash = splits_meta | PASS |  |
| val split size | PASS | 100 vs 100 |
| val ID hash = splits_meta | PASS |  |
| test split size | PASS | 100 vs 100 |
| test ID hash = splits_meta | PASS |  |
| splits are pairwise disjoint | PASS |  |
| invalid images (corrupt/missing) | PASS | 0 |
| unique IDs in images.csv | PASS |  |
| exact duplicates (SHA-256) across/within splits | PASS | 0 images |
| no NaNs in pixel statistics | PASS |  |
| KB: 5 captions per image | PASS | min=5 max=5 |
| val: 5 references per image | PASS |  |
| test: 5 references per image | PASS |  |
| unique caption IDs (KB) | PASS |  |
| LEAKAGE CHECK: no val/test images in kb_captions | PASS |  |
| LEAKAGE CHECK: no evaluation caption IDs in the KB | PASS |  |
| raw captions unchanged (raw may differ from clean; raw is non-empty) | PASS |  |
| info: val references identical to a KB caption (text) | PASS | 1.0% — normal for generic captions; not image leakage |
| info: test references identical to a KB caption (text) | PASS | 1.4% — normal for generic captions; not image leakage |
| metadata available for every image | PASS |  |
| text attributes available only for the KB | PASS |  |
| embeddings clip-b32/kb | PASS | shape=(10000, 512) |
| embeddings clip-b32/val | PASS | shape=(100, 512) |
| embeddings clip-b32/test | PASS | shape=(100, 512) |
| clip-b32 index: ntotal=KB and self-retrieval | PASS |  |
| embeddings siglip-b16/kb | PASS | shape=(10000, 768) |
| embeddings siglip-b16/val | PASS | shape=(100, 768) |
| embeddings siglip-b16/test | PASS | shape=(100, 768) |
| siglip-b16 index: ntotal=KB and self-retrieval | PASS |  |
| embeddings dinov2-s/kb | PASS | shape=(10000, 384) |
| embeddings dinov2-s/val | PASS | shape=(100, 384) |
| embeddings dinov2-s/test | PASS | shape=(100, 384) |
| dinov2-s index: ntotal=KB and self-retrieval | PASS |  |
| LEAKAGE CHECK: val never retrieves itself (k=10) | PASS |  |
| info: val near-duplicates in the KB | PASS | cos>=0.97: 0/100 | dHash<=4: 0 |
| LEAKAGE CHECK: test never retrieves itself (k=10) | PASS |  |
| info: test near-duplicates in the KB | PASS | cos>=0.97: 0/100 | dHash<=4: 0 |
| smoke test val: NN-caption CIDEr > random | PASS | NN=0.674 random=0.024 | Jaccard classes@1=0.546 |
| smoke test test: NN-caption CIDEr > random | PASS | NN=0.622 random=0.033 | Jaccard classes@1=0.506 |