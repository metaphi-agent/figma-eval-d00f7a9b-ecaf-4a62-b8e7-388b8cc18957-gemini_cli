---
name: webapp
description: Build web applications, dashboards, landing pages. Also handles UI revamps of existing codebases. Creates Modal dev servers for live preview with hot reload.
---

# Web Application Builder

Build production-ready React applications with live preview.

## Why Modal Dev Servers

Websites are **not static**. They have:
- Dynamic routes (`/user/:id`, `/post/:slug`)
- Client-side routing that needs server fallback
- Hot reload during development

**Modal Sandbox** runs `npm run dev` - a real dev server with hot reload. User watches the app being built in real-time.

## Workflow

### 0. Check Session State (FIRST)

```bash
python {skill_dir}/scripts/check_manifest.py {project_root}/webapp/manifest.json
```

| Output | Action |
|--------|--------|
| `COMPLETE:<url>` | Return URL to user, done |
| `RESUME:building` | Skip to step 3, continue building |
| `RESUME:scaffold` | Skip to step 2, start server |
| `FRESH:*` | Start from step 1 |

### 1. Read Skills First (MANDATORY)

Before writing ANY code:

1. **[REACT_PROJECT.md](REACT_PROJECT.md)** - Project structure, package.json, vite.config
2. **Choose design based on context:**
   - Enterprise, B2B, professional, data-heavy: **[DESIGN_LIGHT.md](DESIGN_LIGHT.md)**
   - AI products, consumer, creative, mobile-first: **[DESIGN_DARK.md](DESIGN_DARK.md)**

### 2. Scaffold & Start Server

Run scaffold script to create project structure:
```bash
python {skill_dir}/scripts/scaffold.py {project_root} <light|dark> "App Title"
python {skill_dir}/scripts/write_manifest.py {project_root}/webapp/manifest.json init "App Title" <light|dark>
```

This creates package.json, vite.config.ts, index.html, and src/ with correct configs.

Then install and start dev server:
```bash
cd {project_root} && npm install
```

Then immediately create preview:
```
mcp__app_preview__create_app_preview(
    task_id=<task_id>,
    project_root="{project_root}"
)
```

Update manifest with preview URL:
```bash
python {skill_dir}/scripts/write_manifest.py {project_root}/webapp/manifest.json preview <preview_url>
```

**Share the preview URL with user right away.** They can now watch as you build.

### 3. Build the App (User Watches Live)

Now write the real code:
- Pages, components, layouts
- Apply design tokens from chosen skill
- Hot reload updates the preview automatically

User sees changes in real-time. They can give feedback during development.

**Quality bar:** Match the polish of the best apps. Complete UI - brand name, navigation, proper page structure, professional styling.

### 4. Iterate Based on Feedback

User is watching and may request changes as you build:
- Make the requested changes
- Hot reload shows updates
- Continue until user is satisfied

### 5. Production Build

When user approves:
```bash
cd {project_root} && npm run build
```

If build fails:
1. Read error output
2. Fix the issue (see REACT_PROJECT.md for common errors)
3. Re-run until success

### 6. Final Deploy (Optional)

If user wants a permanent URL:

```
mcp__gcs_uploader__upload_dist_to_gcs(
    dist_path="{project_root}/dist",
    gcs_prefix="webapps/<task_id>"
)

mcp__artifact_registry__declare_artifact(
    artifact_type="webapp",
    task_id=<task_id>,
    output_url=<gcs_url>,
    title="..."
)

mcp__thumbnail_generator__generate_web_thumbnail(
    page_url=<gcs_url>,
    artifact_id=<artifact_id>
)
```

**Note:** For apps requiring a server (Expo, SSR, complex routing), the Modal preview URL IS the deliverable.

---

# UI Revamp Mode

For modernizing existing codebases.

## Mindset

Backend stays the same. UI gets reimagined to be **brilliant**.

You're not tweaking colors - you're fundamentally rethinking how the interface presents features. New layouts, new component structures, new interactions, new visual hierarchy.

## Workflow

### 1. Clone & Start Server

Clone the repo, install deps, start Modal dev server immediately. User gets live preview of current state.

### 2. Audit

Study the app:
- Every feature, flow, interaction
- API calls and data flow
- What works, what doesn't

Present a vision for the reimagined UI.

### 3. Reimagine (User Watches Live)

Rebuild the frontend with design skill tokens:
- Keep ALL API calls and business logic intact
- Presentation layer is yours to reinvent
- Hot reload shows changes as you work

### 4. Test

Use Playwright to verify:
- Key flows still work
- Responsive behavior
- API integrations intact

### 5. Push & PR

Commit changes, push to remote, create PR for review.

---

## Rules

- ALWAYS read skill files before writing code
- ALWAYS start dev server early so user can watch
- NEVER use postcss.config.js (Tailwind v4 uses @tailwindcss/vite)
- NEVER hardcode hex colors (use design tokens)
- Write complete code - no placeholders, no TODOs
