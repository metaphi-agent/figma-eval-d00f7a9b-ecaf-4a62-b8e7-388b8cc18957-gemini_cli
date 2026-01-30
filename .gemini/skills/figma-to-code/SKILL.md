---
name: figma-to-code
description: Convert Figma designs to production-ready frontend code.
---

# Figma to Code

Convert Figma designs to production React code with Tailwind v4.

## Step 0: Check Manifest

```bash
python {skill_dir}/scripts/check_manifest.py {project_root}/figma-to-code/manifest.json
```

| Output | Action |
|--------|--------|
| `COMPLETE:<path>` | Done, return result |
| `RESUME:building` | Skip to Step 6 |
| `RESUME:extracted` | Skip to Step 3 |
| `FRESH:*` | Start from Step 1 |

## Step 1: Extract from Figma

file_key is from URL: `figma.com/file/<FILE_KEY>/...`

```python
# 1. Get file structure, auto-select the primary design page
# - Skip intro/readme pages (e.g., "Hello", "Welcome", "Cover", "README")
# - Pick pages named "Design", "Screens", "Main", "App", or similar
# - If only one substantive page exists, use it
# - If genuinely ambiguous, pick the first non-intro page
mcp__figma__get_figma_file(file_key)

# 2. Get page node ID
mcp__figma__get_page_node_id(file_key, page_name)

# 3. Export visual overview
mcp__figma__get_page_visual_overview(file_key, page_node_id, output_dir, format="png", scale=1)

# 4. Get node hierarchy (use depth=1 to avoid timeouts)
mcp__figma__get_node_tree(file_key, node_id, depth=1)

# 5. Extract components and styles
mcp__figma__get_node_components(file_key, node_id)
mcp__figma__get_node_styles(file_key, node_id)

# 6. Export assets (SVG for icons, PNG for photos)
mcp__figma__export_node_images(file_key, node_ids, output_dir, format="svg", scale=2.0)
```

### Asset Handling

**Export by type:**
| Asset Type | Format | Scale | Output Dir |
|------------|--------|-------|------------|
| Icons | SVG | 1x | `public/assets/icons/` |
| Logos | SVG | 1x | `public/assets/` |
| Photos/Products | PNG | 2x | `public/assets/images/` |
| Illustrations | SVG or PNG | 2x | `public/assets/` |

**In code:**
```tsx
// Icons - use relative paths (required for Modal/GCS subdirectory deployment)
<img src="./assets/icons/cart.svg" alt="" className="w-6 h-6" />

// Photos - always lazy load, always add alt
<img
  src="./assets/images/product-1.png"
  alt="Product name"
  loading="lazy"
  className="w-full h-auto"
/>
```

**Rules:**
- **Use relative paths (`./assets/...`) not absolute (`/assets/...`)** - required for `base: './'`
- Export at 2x scale for retina displays
- Use descriptive filenames (`hero-banner.png` not `Frame-123.png`)
- All `<img>` tags need `alt` attributes
- Photos below the fold get `loading="lazy"`

Save tokens to `{project_root}/figma-to-code/design_tokens.json`

## Step 2: Export Ground Truth

Export every frame at scale=2 to `{project_root}/ground_truth/`

Write `ground_truth/manifest.json`:
```json
{
    "figma_file_key": "abc123",
    "total_frames": 12,
    "frames": [
        {"name": "Login", "node_id": "123:456", "gt_image": "Login.png", "target_route": "/login"},
        {"name": "Dashboard", "node_id": "123:789", "gt_image": "Dashboard.png", "target_route": "/"}
    ]
}
```

Update manifest: `python {skill_dir}/scripts/write_manifest.py {project_root}/figma-to-code/manifest.json extracted {figma_file_key}`

## Step 3: Visual Analysis

READ the exported PNGs before coding. Document:
- Layout structure and visual hierarchy
- Spacing patterns and color usage
- All interactive elements and their states

## Step 4: Component & Interaction Audit

### 4a: Component Inventory

Map Figma components to React:
| Figma | React | Props |
|-------|-------|-------|
| Button/Primary/Large | `<Button>` | `variant="primary" size="lg"` |
| Input/Error | `<Input>` | `error={true}` |

### 4b: Auto-Layout → CSS Mapping

Translate Figma auto-layout directly:

| Figma Auto-Layout | CSS |
|-------------------|-----|
| Horizontal, gap: 16 | `flex flex-row gap-4` |
| Vertical, gap: 8 | `flex flex-col gap-2` |
| Space between | `justify-between` |
| Padding: 16,24 | `px-6 py-4` |
| Hug contents | `w-fit` |
| Fill container | `flex-1` or `w-full` |

### 4c: Interaction States

For each interactive component, implement ALL states from Figma:

**Buttons/Links:**
- Default, Hover, Active/Pressed, Disabled, Loading

**Form Inputs:**
- Empty, Filled, Focused, Error, Disabled
- Validation messages (inline errors, success indicators)

**Transitions:** Use `transition-colors duration-150` for color changes, `transition-transform` for movement.

### 4d: Form Handling

For any form in the design:
- Controlled inputs with React state
- Validation on blur and submit
- Error states matching Figma error variants
- Loading state on submit button
- Success/error feedback after submission

```tsx
// Standard form pattern
const [errors, setErrors] = useState<Record<string, string>>({});
const [isSubmitting, setIsSubmitting] = useState(false);

const validate = (field: string, value: string) => {
  // Return error message or empty string
};
```

### 4e: Edge States

Implement these if they appear in Figma (or add sensible defaults):
- Empty states (no data)
- Loading skeletons
- Error states
- Text overflow (`truncate` or `line-clamp-2`)

## Step 5: Scaffold Project

**⚠️ NEVER use interactive CLI tools** (`npm create`, `npm init`, `npx create-*`).

```bash
python {skill_dir}/scripts/scaffold.py {project_root} react "<App Title>"
```

Creates project with correct Vite config (`base: './'` for GCS, `allowedHosts: true` for Modal).

## Step 6: Generate Components

Update manifest: `python {skill_dir}/scripts/write_manifest.py {project_root}/figma-to-code/manifest.json building`

### Performance Requirements

**Images:**
- Use `loading="lazy"` on below-fold images
- Optimize SVGs (remove unnecessary attributes)
- Use appropriate formats: SVG for icons, WebP/PNG for photos

**Code:**
- Lazy load routes: `React.lazy(() => import('./pages/Dashboard'))`
- Avoid inline styles; use Tailwind classes
- Extract repeated patterns into components

### Component Structure
```
src/
├── components/
│   ├── ui/          # Atoms: Button, Input, Icon
│   └── blocks/      # Organisms: Header, Card, Modal
├── pages/           # Route components
└── App.tsx
```

## Step 7: Deploy & Push

### 7a: Create Preview

```bash
cd {project_root} && npm install
```

```python
mcp__app_preview__create_app_preview(
    task_id=<task_id>,
    project_root="{project_root}"
)
```

Creates a Modal sandbox running `npm run dev`. The preview URL is used by the verifier to take screenshots.

Save the preview URL to manifest:
```bash
python {skill_dir}/scripts/write_manifest.py {project_root}/figma-to-code/manifest.json preview <preview_url>
```

### 7b: Push to GitHub

```python
mcp__github__create_repository(name=<repo_name>, org="metaphi-agent")
mcp__github__push_files(...)  # All generated files
```

### 7c: Build for GCS Archive

```bash
cd {project_root} && npm run build
```

Creates `dist/` folder for permanent GCS static archive.

Update manifest: `python {skill_dir}/scripts/write_manifest.py {project_root}/figma-to-code/manifest.json complete {project_root}/dist`

## Multi-Turn Iteration

The GitHub repo is the SINGLE SOURCE OF TRUTH.
- On EVERY iteration, push changes to the repo BEFORE responding
- NEVER show code changes without pushing them first
- Re-deploy after each iteration so preview stays current

## Rules

- Check manifest first (Step 0) for session recovery
- Build ALL frames - no cherry-picking
- Extract from Figma first - never guess colors/fonts
- Implement ALL interaction states from Figma
- Use the extracted icons and assets as per the design. do not substitute with general library based imports if corresponding assets exist in figma file. 
- Map auto-layout to flexbox/grid directly
- No `tailwind.config.js` - use CSS `@theme` only
- Export real assets - no placeholder URLs
- Lazy load images and routes
- Push to GitHub repo (required)
