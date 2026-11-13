---
name: latex-academic-presentation
description: Design, structure, and compile publication-grade academic and scientific presentation slides using LaTeX Beamer.
allowed-tools: Read, Write, Edit, RunCommand
version: 1.0
priority: HIGH
---

# LaTeX Academic & Scientific Presentation Skill

> **PURPOSE**: Guide the creation of publication-grade, mathematically rigorous, and visually elegant presentation slides using **LaTeX Beamer**, adhering to top-tier AI/Data Science academic standards (NeurIPS, ICML, KDD, AAAI, IEEE).

---

## 1. Design & Typography Principles

| Component | Standard / Guideline |
| :--- | :--- |
| **Theme** | Prefer modern minimalist themes: `metropolis` (`beamerthememetropolis`), `Madrid`, `Boadilla`, or clean custom flat color themes. |
| **Aspect Ratio** | Always use widescreen 16:9 (`\documentclass[aspectratio=169]{beamer}`) for modern displays. |
| **Palette** | Academic colors: Primary Navy (`#1b365d` or `#0f2d59`), Secondary Teal (`#008080` or `#00a896`), Accent Coral/Amber (`#d95f02` or `#e65100`), Slate Background (`#f8f9fa`). |
| **Fonts** | Clear sans-serif math: `\usefonttheme{professionalfonts}` with `Fira Sans` or `Latin Modern Sans`. |
| **Information Density** | Maximum 1 core concept per slide. Avoid walls of text; use clean 2-column layouts (`columns`), structured itemize blocks, and callout boxes (`block`, `alertblock`, `exampleblock`). |
| **Figures** | Embed high-resolution vector or raster charts (`\includegraphics[width=...]{...}`) with descriptive captions. |
| **Equations** | Formulate all definitions rigorously using standard LaTeX math notations. |

---

## 2. Standard Scientific Slide Deck Architecture

```text
1. Title & Meta Slide (Title, Authors, Affiliation, Date, GitHub/ArXiv Link)
2. Executive Motivation & Research Question (Why does this matter?)
3. Mathematical Problem Formulation (Point-in-Time, Temporal Barriers, Loss Functions)
4. Dataset Architecture & Empirical Discovery (Integrity audits, EDA key findings)
5. Methodology & Pipeline Architecture (Feature engineering, zero-leakage discipline)
6. Model Benchmarks & Probability Calibration (Heuristics vs Baselines vs Advanced Models, ECE)
7. Quantitative Out-of-Time Results (PR-AUC, ROC-AUC, Brier Score, Decile Lift Tables)
8. Explainability & Mechanistic Insights (SHAP values, Feature Gain, Local Case Studies)
9. Business Translation & Actionable Policy (Expected Value ROI, CRM Playbook)
10. Conclusion, Contributions & Reproducibility (GitHub link, pytest verification)
11. Appendix / Backup Slides (Hyperparameters, Robustness checks, Mathematical proofs)
```

---

## 3. Recommended LaTeX Packages & Structure

```latex
\documentclass[aspectratio=169, 10pt]{beamer}

% Themes & Styling
\usetheme{Madrid}
\usecolortheme{dolphin}
\usefonttheme{professionalfonts}

% Essential Packages
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{colortbl}
\usepackage{hyperref}
\usepackage{xcolor}

% Custom Colors
\definecolor{primary}{RGB}{27, 54, 93}    % Navy
\definecolor{secondary}{RGB}{0, 128, 128} % Teal
\definecolor{accent}{RGB}{217, 95, 2}     % Amber

\setbeamercolor{palette primary}{bg=primary, fg=white}
\setbeamercolor{palette secondary}{bg=secondary, fg=white}
\setbeamercolor{title}{bg=primary, fg=white}
\setbeamercolor{frametitle}{bg=primary, fg=white}
\setbeamercolor{block title}{bg=primary, fg=white}
\setbeamercolor{block body}{bg=primary!10, fg=black}
```

---

## 4. Compilation Commands

```bash
# Standard compilation with pdflatex
pdflatex -interaction=nonstopmode presentation.tex
# Run twice to resolve references and slide counters
pdflatex -interaction=nonstopmode presentation.tex

# Or with latexmk
latexmk -pdf presentation.tex
```
