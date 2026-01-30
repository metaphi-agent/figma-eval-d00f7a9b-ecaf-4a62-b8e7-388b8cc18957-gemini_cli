---
name: visual-judge
description: Compare deployed app to ground truth using output rubrics.
---

# Visual Judge

Compare deployed app against ground truth screenshots, scoring on coverage and component fidelity.

## Volume Locations

**Ground Truth (read):** `figma-claude-agent` volume
```
/figma-claude/work/{session_id}/ground_truth/
├── manifest.json
├── {node_id}.png
└── ...
```

**App Screenshots (write):** `figma-evals` volume
```
/figma-evals/results/{session_id}/app_screenshots/
├── Login_Page.png
└── ...
```

**Output Files (write):** `figma-evals` volume
```
/figma-evals/{run_id}/
├── output_grade.json    # Aggregated rubric scores
└── vlm_comparison.json  # Per-frame comparison details
```

## Workflow

### Step 1: Load Ground Truth Manifest

Read `{project_root}/ground_truth/manifest.json`:
```json
{
    "figma_file_key": "C9pTFArzeIYdtuLla2wV8w",
    "total_frames": 9,
    "frames": [
        {
            "name": "Homepage - Desktop",
            "node_id": "20:2",
            "gt_image": "20-2.png",
            "target_route": "/",
            "viewport": "desktop"
        },
        {
            "name": "Homepage - Mobile",
            "node_id": "35:740",
            "gt_image": "35-740.png",
            "target_route": "/",
            "viewport": "mobile"
        }
    ]
}
```

### Step 2: Screenshot Deployed App

For each frame in manifest:
```
# Navigate to route
mcp__playwright__browser_navigate(url="{deployed_url}{target_route}")

# Set viewport based on frame.viewport
if viewport == "desktop":
    mcp__playwright__browser_resize(width=1280, height=800)
elif viewport == "mobile":
    mcp__playwright__browser_resize(width=375, height=812)

# Screenshot
mcp__playwright__browser_take_screenshot(filename="{name}.png")
```

### Step 3: Compare with VLM Judge

For each frame, compare GT image vs app screenshot:
```
mcp__vlm_judge__vlm_judge_gemini_3(
    figma_screenshot_path="{project_root}/ground_truth/{gt_image}",
    app_screenshot_path="{work_dir}/app_screenshots/{name}.png",
    frame_name="{name}",
    rubrics_json="{output_rubrics}"
)
```

### Step 4: Write Results

#### `output_grade.json`:
```json
{
    "run_id": "{run_id}",
    "session_id": "{session_id}",
    "task_type": "figma_to_code",
    "judge": "visual-judge",
    "judge_model": "gemini-3-pro-preview",
    "judge_provider": "gemini",
    "overall_score": 3.8,
    "rubric_scores": [
        {"rubric_id": "component_coverage", "score": 4, "matched_level": "Advanced", "thinking_process": "..."},
        {"rubric_id": "layout_accuracy", "score": 3, "matched_level": "Proficient", "thinking_process": "..."}
    ],
    "overall_assessment": "...",
    "rubrics_version": "1.0.0",
    "graded_at": "...",
    "token_usage": {"input_tokens": 0, "output_tokens": 0, "vlm_calls": 0}
}
```

#### `vlm_comparison.json`:
```json
{
    "total_frames_in_design": 69,
    "frames_in_gt": 19,
    "frames_compared": 19,
    "frames": [
        {
            "name": "Login Page",
            "gt_image": "ground_truth/123-456.png",
            "app_image": "app_screenshots/Login_Page.png",
            "rubric_scores": [...],
            "frame_score": 3.9
        }
    ]
}
```

## Dependencies

- Playwright MCP for app screenshots
- VLM Judge MCP for visual comparison
- Output rubrics from `/metaphi-rubrics/figma/output/rubrics.json`
