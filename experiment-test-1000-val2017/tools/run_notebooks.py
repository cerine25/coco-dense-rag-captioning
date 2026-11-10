"""Execute the configured notebook stages and save executed copies."""
import argparse
import os
import stat
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
ORDER = [
    "00_download_annotations",
    "01_make_splits",
    "01b_download_images",
    "02_preprocess_images",
    "03_captions_metadata",
    "04_embeddings_index",
    "05_eda",
    "06_select_config",
    "07_qc_leakage",
    "08_freeze",
    "09_demo_retrieval",
]

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--config", default="config.yaml")
parser.add_argument("--skip", nargs="*", default=[])
parser.add_argument("--only", nargs="*")
parser.add_argument("--out", default="executed_notebooks")
parser.add_argument("--timeout", type=int, default=36000)
parser.add_argument(
    "--allow-frozen-write",
    action="store_true",
    help="allow notebook execution to unlock and rewrite a frozen artifacts directory",
)
args = parser.parse_args()

frozen_manifests = [
    path for path in ROOT.glob("artifacts*/manifest.json") if path.is_file()
]
if frozen_manifests and not args.allow_frozen_write:
    parser.error(
        "frozen artifact manifest found; use a disposable copy and pass "
        "--allow-frozen-write only when intentionally rebuilding"
    )

os.environ["RAG_CONFIG"] = args.config
out = ROOT / args.out
out.mkdir(exist_ok=True)
for art in ROOT.glob("artifacts*"):
    for f in art.rglob("*"):
        if f.is_file():
            f.chmod(f.stat().st_mode | stat.S_IWUSR)
for name in (args.only or ORDER):
    if name in args.skip:
        print("skip", name)
        continue
    t = time.time()
    nb = nbformat.read(ROOT / f"{name}.ipynb", 4)
    try:
        NotebookClient(
            nb,
            timeout=args.timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(ROOT)}},
        ).execute()
        status = "OK"
    except CellExecutionError as e:
        status = "ERREUR"
        print(str(e)[-1800:])
    nbformat.write(nb, out / f"{name}.ipynb")
    print(f"{name:26s} {status}  ({time.time() - t:.0f}s)")
    if status != "OK":
        sys.exit(1)
