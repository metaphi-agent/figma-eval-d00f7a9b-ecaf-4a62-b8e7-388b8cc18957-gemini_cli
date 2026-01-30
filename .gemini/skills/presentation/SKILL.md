---
name: presentation
description: Creates presentation slide decks from provided content. Use when user wants slides, a deck, or a presentation. Expects research/content to be provided - does not conduct research.
---

# Presentation Production Pipeline

## Scope

This sub-agent **designs and produces** presentations. It does NOT research.

**Expected inputs** (from user or orchestrator):
- Topic/title
- Target audience
- Content to present (key points, data, narrative)
- Optional: slide count preference, style notes

If research is needed, the orchestrator gathers it first.

## Tools

| Tool | Function |
|------|----------|
| `Bash` | Run scripts (validate, compile, upload) |
| `mcp__ppt_storyboard_generator__generate_storyboard` | Create narrative arc |
| `mcp__chart_generator__generate_chart_from_csv` | CSV data to chart PNG |
| `mcp__gemini_nanobanana__generate_image` | Generate images (you craft the prompt) |
| `mcp__react_slide_generator__generate_slide_component` | Content to React component |
| `Read`, `Write`, `Glob` | File operations |

## Workflow

### 0. Check Session State (MANDATORY FIRST STEP)

```bash
python {skill_dir}/scripts/check_manifest.py \
  {project_root}/presentation/manifest.json \
  "{topic}"
```

| Output | Action |
|--------|--------|
| `COMPLETE:<gcs_url>` | Return URL to user, done |
| `RESUME:<phase>` | Skip to that phase |
| `FRESH:*` | Start from step 1 |

### 1. Create Storyboard

```
mcp__ppt_storyboard_generator__generate_storyboard(
  topic="...",
  slide_count=6-8,
  target_audience="...",
  key_points=[...],
  save_path="{project_root}/storyboard.json"
)
```

Update manifest: `phase = "storyboard"`

### 2. Produce Slides

For EACH slide in storyboard.json:

#### 2a. Determine Slide Type

Read [SLIDE_TYPES.md](SLIDE_TYPES.md) for decision matrix.

| Content | Type | Visual Strategy |
|---------|------|-----------------|
| Title/intro | `title` | Generate hero image |
| Has CSV data | `chart` | Generate chart from CSV |
| Abstract concept | `image` | Generate abstract art |
| Bullet points | `content` | Text only |
| Compare two things | `two_column` | Layout is visual |
| Quote | `quote` | Typography is visual |

#### 2b. Generate Chart (for data slides)

If slide references CSV data:

```
mcp__chart_generator__generate_chart_from_csv(
  csv_path="{project_root}/data/{filename}.csv",
  chart_type="bar|line|pie|area",
  output_path="{project_root}/public/assets/chart_{n}.png",
  title="Chart Title"
)
```

Chart type selection:
- Time series: `line`
- Comparisons (3-7 items): `bar`
- Parts of whole: `pie`
- Trends with multiple series: `area`

#### 2c. Generate Image (for concept slides)

Read [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) for prompt patterns.

**Craft the prompt yourself** based on slide context:

1. Identify narrative beat (problem, solution, growth, conclusion)
2. Choose composition (diagonal, radial, geometric, organic)
3. Include theme colors (#D97548 terracotta, #FAF8F6 cream)
4. Add mood and "minimalist, professional presentation style"

```
mcp__gemini_nanobanana__generate_image(
  prompt="<your crafted prompt from design system>",
  save_path="{project_root}/public/assets/slide_{n}_art.png",
  aspect_ratio="16:9",
  image_size="1K"
)
```

**Skip image generation if**:
- Slide has chart (chart is the visual)
- Slide has 4+ bullet points (text is content)
- Slide is quote (typography is visual)
- Slide is comparison (layout is visual)

#### 2d. Generate React Component

For each slide:

```
mcp__react_slide_generator__generate_slide_component(
  slide_number=N,
  slide_type="title|content|chart|image|two_column|quote",
  title="Slide Title",
  content={...},
  image_path="assets/slide_N_art.png",  # relative, no leading slash
  output_path="{project_root}/src/slides/SlideN.tsx"
)
```

**Critical - Image Paths**:
- ALWAYS relative: `assets/filename.png`
- NEVER absolute URLs or paths with leading slash

Update manifest: add to `artifacts.slide_components[]`

### 3. Validate Slides (MANDATORY BEFORE BUILD)

```bash
python {skill_dir}/scripts/validate_slides.py {project_root}/src/slides/
```

| Output | Action |
|--------|--------|
| `VALID:N` | Continue to step 4 |
| `INVALID:export_mismatch:<file>` | Fix export pattern |
| `INVALID:absolute_path:<file>` | Fix to relative path |
| `INVALID:missing_asset:<file>:<asset>` | Generate missing asset |

Fix issues and re-validate before proceeding.

### 4. Compile Presentation

```bash
python {skill_dir}/scripts/compile_presentation.py {project_root}
```

| Output | Action |
|--------|--------|
| `SUCCESS:<dist_path>` | Continue to step 5 |
| `ERROR:typescript:<file>:<line>:<msg>` | Fix component, retry (max 3) |
| `ERROR:npm_install:<details>` | Report to user |
| `ERROR:build:<details>` | Report to user |

Update manifest: `phase = "build"`

### 5. Upload and Register (ALL STEPS MANDATORY)

```bash
python {skill_dir}/scripts/upload_and_register.py \
  {project_root} \
  {task_id} \
  "{presentation_title}"
```

| Output | Action |
|--------|--------|
| `SUCCESS:<gcs_url>:<artifact_id>` | Done |
| `ERROR:upload:<details>` | Report to user |
| `ERROR:register:<details>` | Report to user |
| `ERROR:thumbnail:<details>` | Log warning, still report success |

### 6. Finalize Session

```bash
python {skill_dir}/scripts/write_manifest.py \
  {project_root}/presentation/manifest.json \
  complete \
  "{gcs_url}" \
  "{artifact_id}" \
  "{title}"
```

Report to user:
- Presentation URL (gcs_url)
- Slide count
- Any warnings

## Edge Cases

| Situation | Action |
|-----------|--------|
| No CSV for "data" slide | Convert to `content` type with bullet points |
| Image generation fails | Log warning, use text-only slide |
| Build fails 3 times | Stop, report errors with file:line details |
| User requests < 4 slides | Generate directly without storyboard tool |
| Manifest shows COMPLETE | Ask user: use existing or create new? |
| Missing required content | Ask orchestrator/user for content before proceeding |

## Quality Checklist

Before reporting success:
- [ ] All slides render (no TypeScript errors)
- [ ] All image paths are relative
- [ ] Artifact registered (has artifact_id)
- [ ] GCS URL accessible
- [ ] Manifest updated to phase=complete
