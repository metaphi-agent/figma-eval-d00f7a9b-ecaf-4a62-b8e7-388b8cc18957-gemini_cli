#!/usr/bin/env python3
"""
Scaffold a project for Figma-to-code evaluation.

Supports multiple target frameworks:
- react: React + Vite + Tailwind v4
- html: Plain HTML + Tailwind CDN
- (future: react-native, webflow, etc.)

Usage:
    python scaffold.py <project_root> <target_framework> [app_title]

Args:
    project_root: Directory to create project in
    target_framework: "react" or "html"
    app_title: Optional app title (default: "Figma Design")

Output:
    SUCCESS:<project_root>
    ERROR:<message>

Example:
    $ python scaffold.py /work/123 react "Dashboard"
    SUCCESS:/work/123
"""
import json
import os
import sys
from pathlib import Path


# =============================================================================
# React + Vite + Tailwind v4
# =============================================================================

REACT_PACKAGE_JSON = {
    "name": "figma-design",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "dependencies": {
        "react": "^19.0.0",
        "react-dom": "^19.0.0",
        "react-router-dom": "^7.0.0",
        "framer-motion": "^11.0.0",
        "lucide-react": "^0.460.0",
        "clsx": "^2.1.0"
    },
    "devDependencies": {
        "@vitejs/plugin-react": "^4.3.0",
        "vite": "^6.0.0",
        "tailwindcss": "^4.0.0",
        "@tailwindcss/vite": "^4.0.0"
    }
}

REACT_VITE_CONFIG = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: './',
  server: {
    host: true,
    allowedHosts: true
  }
})
'''

REACT_INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

REACT_MAIN_TSX = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <HashRouter>
      <App />
    </HashRouter>
  </React.StrictMode>
)
'''

REACT_APP_TSX = '''export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <h1 className="text-4xl font-semibold text-gray-900 tracking-tight">
            Building from Figma...
          </h1>
          <p className="mt-2 text-gray-500">
            Converting design to code
          </p>
        </div>
      </div>
    </div>
  )
}
'''

REACT_INDEX_CSS = '''@import "tailwindcss";

/* Design tokens will be extracted from Figma */
@theme {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
}
'''


# =============================================================================
# Plain HTML + Tailwind CDN
# =============================================================================

HTML_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* Design tokens will be extracted from Figma */
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
  </style>
</head>
<body class="min-h-screen bg-white">
  <div class="flex items-center justify-center h-screen">
    <div class="text-center">
      <h1 class="text-4xl font-semibold text-gray-900 tracking-tight">
        Building from Figma...
      </h1>
      <p class="mt-2 text-gray-500">
        Converting design to code
      </p>
    </div>
  </div>
</body>
</html>
'''


# =============================================================================
# Scaffold Functions
# =============================================================================

def scaffold_react(project_root: str, title: str) -> None:
    """Create React + Vite + Tailwind v4 project."""
    root = Path(project_root)
    src = root / "src"

    # Create directories
    src.mkdir(parents=True, exist_ok=True)
    (src / "components").mkdir(exist_ok=True)
    (root / "public" / "assets").mkdir(parents=True, exist_ok=True)

    # Write files
    (root / "package.json").write_text(json.dumps(REACT_PACKAGE_JSON, indent=2))
    (root / "vite.config.ts").write_text(REACT_VITE_CONFIG)
    (root / "index.html").write_text(REACT_INDEX_HTML.format(title=title))
    (src / "main.tsx").write_text(REACT_MAIN_TSX)
    (src / "App.tsx").write_text(REACT_APP_TSX)
    (src / "index.css").write_text(REACT_INDEX_CSS)


def scaffold_html(project_root: str, title: str) -> None:
    """Create plain HTML + Tailwind CDN project."""
    root = Path(project_root)

    # Create directories
    root.mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(exist_ok=True)

    # Write files
    (root / "index.html").write_text(HTML_INDEX.format(title=title))


def scaffold(project_root: str, target_framework: str, title: str = "Figma Design") -> None:
    """Create project structure based on target framework."""
    framework = target_framework.lower()

    if framework in ("react", "react-vite", "vite"):
        scaffold_react(project_root, title)
    elif framework in ("html", "static", "tailwind"):
        scaffold_html(project_root, title)
    else:
        # Default to React for unknown frameworks
        # Agent can adapt as needed
        scaffold_react(project_root, title)


def main():
    if len(sys.argv) < 3:
        print("Usage: python scaffold.py <project_root> <target_framework> [app_title]", file=sys.stderr)
        sys.exit(1)

    project_root = sys.argv[1]
    target_framework = sys.argv[2].lower()
    title = sys.argv[3] if len(sys.argv) > 3 else "Figma Design"

    try:
        scaffold(project_root, target_framework, title)
        print(f"SUCCESS:{project_root}")
    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
