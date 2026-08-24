# ManimCE PQH Project Package Standard

**Version:** 1.1  
**Effective date:** 2026-08-24  
**Reference environment:** Manim Community Edition 0.20.1  
**Default final format:** 1920x1080, 30 fps, H.264, yuv420p, MP4

## 1. Purpose

This protocol extends the existing ManimCE PQH workflow. A final ManimCE delivery is no longer considered complete when only an MP4 is produced. Every final project must be delivered as a reproducible `.zip` package containing the rendered video, exact source code, storyboard, project style/dependencies, render/QA evidence, and reproduction instructions.

## 2. Mandatory workflow

For every project, use this order:

1. Review the user request and existing project/style code.
2. Prepare or update a storyboard before implementing a substantial visual/narrative revision.
3. Implement the scene using the established JP classroom style when applicable.
4. Validate Python syntax and lesson data.
5. Run a literal `-pql` QA render.
6. Correct runtime, LaTeX, framing, overlap, continuity, and timing issues.
7. Run a literal `-pqh` final render from the exact accepted source.
8. Verify the MP4 with `ffprobe`.
9. Fully decode the MP4 with FFmpeg and require an empty error log.
10. Export dense audit frames and visually inspect critical transitions.
11. Calculate SHA-256 for the final MP4.
12. Build the mandatory project ZIP described below.
13. Deliver the ZIP as the primary artifact. The MP4 may also be exposed separately for convenience.

A project that fails any required gate is not final.

## 3. Mandatory ZIP structure

```text
<Project_Name>_PQH_PACKAGE/
├── README.md
├── src/
│   ├── <scene_source>.py
│   └── jp_classroom_style.py
├── storyboard/
│   └── STORYBOARD.md
├── render/
│   └── <Project_Name>_FINAL_pqh.mp4
├── qa/
│   ├── VIDEO_TECHNICAL.tsv
│   ├── SHA256SUMS.txt
│   ├── full_decode.log
│   ├── render_pql.log
│   ├── render_pqh.log
│   └── audit_frames/
├── protocol/
│   └── PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD.md
└── workflow/
    └── <workflow>.yml
```

Assets required by the scene must be included under `assets/` with project-relative paths.

## 4. Storyboard requirement

The storyboard must define pedagogical objective, visual continuity strategy, act order, persistent objects, camera/zoom behavior, equation progression, timing intent, transition rules, final conceptual takeaway, and known QA risks.

## 5. Source traceability

The package must contain the exact `.py` source used for the final PQH render and every local style/helper file required to reproduce it. For GitHub Actions renders, source reconstruction must be deterministic and SHA-256 validation must occur before `-pql`.

## 6. Render gates

Literal PQL:

```bash
manim -pql <scene.py> <SceneClass> --format=mp4 --disable_caching
```

Literal PQH:

```bash
manim -pqh <scene.py> <SceneClass> --format=mp4 --disable_caching
```

For headless Docker/GitHub Actions environments, `xdg-open` may be neutralized while preserving the literal `-pqh` invocation.

## 7. Technical acceptance

Final PQH must satisfy 1920x1080, 30 fps, H.264, yuv420p, readable by ffprobe, full FFmpeg decode exit 0, empty full-decode error log, and recorded final MP4 SHA-256.

## 8. Visual QA acceptance

Dense audit frames must be reviewed for safe-frame compliance, no harmful overlap, no stale labels, no merge artifacts, no discontinuous diagrams, camera-safe magnification, causally ordered equations, spatial continuity, and a conclusion consistent with the immediately prior state.

## 9. README requirements

The root README must state project title/version, ManimCE version, scene class/source, storyboard, exact PQL/PQH commands, final technical specifications, MP4 SHA-256, package map, reproduction instructions, QA status, and notable design decisions.

## 10. Naming convention

Recommended package: `<Project_Name>_<VERSION>_FINAL_PQH_PROJECT.zip`.

Recommended video: `<Project_Name>_<VERSION>_FINAL_pqh.mp4`.

## 11. GitHub Actions artifact rule

The workflow artifact must include, at minimum, final PQH MP4, exact scene source, exact style/helper source, storyboard, technical metadata, SHA-256, full decode log, audit frames, PQL log, and this protocol or versioned equivalent.

## 12. Definition of done

A ManimCE project is DONE only when storyboard/source match, PQL passes, PQH passes, technical QA passes, full decode passes, visual audit passes, exact sources are preserved, final SHA is recorded, and the complete project ZIP exists and is downloadable.
