# A Comparative Study of RAG Techniques for Image Captioning

## Project overview

This project explores how retrieval-augmented generation (RAG) can support
image captioning. The goal is to prepare a reproducible MS COCO-based pipeline
and, in later stages, compare captioning approaches for caption quality,
relevance, and visual grounding.

## Current progress

Work so far focuses on data preprocessing and two test experiments. The
preprocessing pipeline prepares dataset splits, processes images and captions,
creates metadata and embeddings, and includes exploratory analysis and quality
checks. The experiments exercise the project on two different test-set sizes;
they are not a completed comparison of multiple RAG caption-generation
methods. Full method evaluation and analysis remain future work.

## Experiment snapshots

- [`experiment-test-100-val2017/`](experiment-test-100-val2017/) contains the
  Phase 1 preprocessing work and a 100-image test experiment.
- [`experiment-test-1000-val2017/`](experiment-test-1000-val2017/) contains a
  supplemental experiment using 1,000 images from COCO `val2017`.

The 1,000-image experiment is a separate, larger test track, not an
independent dataset or a replacement for the Phase 1 experiment. The folders
are separate project snapshots; consult each folder's README for its
configuration, available artifacts, and reproduction instructions.

## Repository structure

```text
.
├── experiment-test-100-val2017/
└── experiment-test-1000-val2017/
```

Each snapshot contains its own notebooks, configuration, scripts, reports, and
project documentation. Requirements and commands may differ by snapshot, so
use the instructions in the folder you intend to run.

## Dataset and scope

The project uses the MS COCO 2017 dataset. Dataset files, pretrained model
weights, and some generated binary artifacts may need to be obtained or
generated separately; check the relevant snapshot's documentation before
running its notebooks. The project is still in progress, and results from the
two test experiments should not be interpreted as a final evaluation of RAG
captioning techniques.

## Next steps

Planned work includes completing caption generation with the selected RAG
approaches, evaluating generated captions and retrieval, and analyzing
hallucinations and experimental limitations.

## Third-party materials

MS COCO, pretrained models, and any other third-party materials remain subject
to their respective licenses and terms. Consult those terms before
redistributing datasets or model weights.
