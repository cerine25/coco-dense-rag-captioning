# Technical report

The preserved report is `phase1_technical_report.pdf`; its editable source and
bibliography are `phase1_technical_report.tex` and `report-phase1.bib`.

## Build

Build from this directory so the relative figure paths resolve:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error phase1_technical_report.tex
```

The build requires a LaTeX distribution with `latexmk`, BibTeX, and the
packages used by the source. It reads EDA figures from `../artifacts/eda/` and
the comparison figure from `figures/`. The two title-page logos are optional;
they are included only when their files exist under
`figures/latex-figures/`. No logo assets are included in this repository.

The existing PDF was preserved and was not rebuilt during cleanup. The build
command has not been verified in a clean environment.
