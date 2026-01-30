---
name: browser-automation
description: Browser automation via Playwright. Use when user needs to scrape data, extract content, or automate browser workflows.
---

# Browser Automation

Delegate to `browser_agent` for browser-based tasks.

## When to Use

- Scraping data from websites
- Extracting tables, lists, structured data
- Multi-step navigation workflows
- Taking screenshots
- Filling forms
- Any task requiring a real browser (not just HTTP)

## Delegation

Task tool → `web_agent`:
```
[Describe what to scrape/automate]
Save extracted data to {project_root}/data/
```

## Available Tools (Playwright MCP)

The web_agent has access to:
- `browser_navigate` - Go to URL
- `browser_snapshot` - Get page content/DOM
- `browser_click` - Click elements
- `browser_type` - Type text
- `browser_scroll_down/up` - Scroll page
- `browser_wait` - Wait for elements
- `browser_take_screenshot` - Capture screenshot
- `browser_close` - Close browser

## Output

web_agent saves results to files in project_root. Common formats:
- JSON for structured data
- CSV for tabular data
- PNG for screenshots
