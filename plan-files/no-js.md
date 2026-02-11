# No-JS Build System Plan

## The Problem

The site currently uses JavaScript (`header.js`, `navbar.js`, `footer.js`) to inject shared components into each page at runtime. This means:

- With JS disabled, visitors get page content but no header, navigation, or footer
- Every visitor's browser rebuilds the same static HTML on every page load
- Screen readers and crawlers see incomplete HTML on initial load

## The Solution: Python Build Script

Move from runtime component assembly (JS in the browser) to build-time assembly (Python on your machine). The end result is the same HTML, but pre-assembled into complete pages before deployment.

## Directory Structure

```
personal-website/
  src/                    # What you edit day-to-day
    pages/
      about.html
      blog.html
      resume.html
    components/
      header.html         # Replaces header.js - same content, plain HTML
      navbar.html         # Replaces navbar.js - same content, plain HTML
      footer.html         # Replaces footer.js - same content, plain HTML
      noscript.html       # The noscript fallback message
    index.html
  pages/                  # Built output (same location as current files)
    about.html            # Complete pages with all components injected
    blog.html
    resume.html
  index.html              # Built output at root (served by GitHub Pages)
  public/                 # Static assets (unchanged, stays where it is)
    style.css
    profile.jpg
  build.py                # The build script
  plan-files/             # Existing plan docs (unchanged)
```

Build output goes to the project root - exactly where your current HTML files
already live. GitHub Pages continues to serve from `/` with no config change.
`src/`, `build.py`, and `plan-files/` sit alongside the built output but
GitHub Pages simply ignores them (it only serves files browsers request).

## GitHub Pages Deployment

No changes needed. GitHub Pages already serves from `/` (root). The built
`index.html` and `pages/` directory land in the exact same locations as your
current files. Push and it's live, same as today.

## How It Works

1. Each `src/` HTML file uses placeholder comments where components go:
   ```html
   <!-- component:header -->
   <!-- component:navbar -->
   <div id="about-content" class="page-content">
     <!-- your actual page content, unchanged -->
   </div>
   <!-- component:footer -->
   <!-- component:noscript -->
   ```

2. Each `src/components/` file is plain HTML (no JS needed):
   ```html
   <!-- header.html -->
   <div class="header">
     <img id="header-pic" src="../public/profile.jpg"
          alt="Profile picture headshot of Andrew Antles">
     <h1 id="header-text">AndrewAntles.Net</h1>
   </div>
   ```

3. `build.py` reads each page, replaces `<!-- component:X -->` with the
   contents of `components/X.html`, and writes the result to the project root.

4. You open the root-level files in your browser for local testing. You commit
   and push everything.

## The Build Script (Conceptual)

```python
"""
Usage:
  python build.py          # One-time build
  python build.py --watch  # Watch for changes and auto-rebuild
"""
import re
import sys
import time
import shutil
from pathlib import Path

ROOT = Path(".")
SRC = ROOT / "src"
COMPONENTS = SRC / "components"

def load_components():
    """Read all component HTML files into a dict."""
    components = {}
    for f in COMPONENTS.glob("*.html"):
        components[f.stem] = f.read_text()
    return components

def inject_components(html, components):
    """Replace <!-- component:name --> markers with component HTML."""
    def replacer(match):
        name = match.group(1)
        return components.get(name, match.group(0))
    return re.sub(r"<!-- component:(\w+) -->", replacer, html)

def build():
    """Run a full build: inject components into src/ pages, write to root."""
    components = load_components()
    for src_file in SRC.rglob("*.html"):
        if COMPONENTS in src_file.parents:
            continue  # Skip component files themselves
        relative = src_file.relative_to(SRC)
        dest = ROOT / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = src_file.read_text()
        html = inject_components(html, components)
        dest.write_text(html)
    print("Build complete.")

def get_mtimes(directories):
    """Get a dict of {filepath: modification_time} for all files."""
    mtimes = {}
    for directory in directories:
        for f in directory.rglob("*"):
            if f.is_file():
                mtimes[f] = f.stat().st_mtime
    return mtimes

def watch():
    """Poll for file changes and rebuild when detected."""
    watch_dirs = [SRC]
    print("Watching for changes... (Ctrl+C to stop)")
    build()  # Initial build
    last_mtimes = get_mtimes(watch_dirs)
    try:
        while True:
            time.sleep(1)  # Check every second
            current_mtimes = get_mtimes(watch_dirs)
            if current_mtimes != last_mtimes:
                changed = [
                    str(f) for f in current_mtimes
                    if current_mtimes.get(f) != last_mtimes.get(f)
                ]
                print(f"Changes detected: {', '.join(changed)}")
                build()
                last_mtimes = current_mtimes
    except KeyboardInterrupt:
        print("\nStopped watching.")

if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch()
    else:
        build()
```

## Watch Mode Details

The `--watch` flag keeps the build script running in a terminal and automatically
rebuilds when you change any file in `src/`.

**How it works:**
- Uses simple polling: every 1 second, it checks if any file modification times
  have changed
- When a change is detected, it runs a full rebuild (which takes milliseconds
  for a site this size)
- No external dependencies - uses only Python standard library (`time.sleep` +
  `Path.stat().st_mtime`)
- Prints which files changed so you can see what triggered the rebuild

**How to use it:**
```
# Terminal tab 1: watch mode (leave this running)
python build.py --watch

# Terminal tab 2: your normal work
# Edit src/pages/about.html, save
# Tab 1 prints: "Changes detected: src/pages/about.html" + "Build complete."
# Refresh browser to see changes
```

**How to stop it:** `Ctrl+C` in the terminal where it's running. It's not a
background daemon - it's a foreground process in a terminal tab. Close the tab
or Ctrl+C and it's gone. Nothing to clean up.

**Why polling instead of `watchdog`:**
- `watchdog` is a third-party library that uses OS-level file system events
  (more efficient, instant detection)
- Polling with `time.sleep(1)` adds at most 1 second of delay, which is
  imperceptible for a dev workflow
- Zero dependencies means no `pip install`, no virtual environment, no
  requirements.txt - just `python build.py --watch` and it works
- If you later want instant detection, `pip install watchdog` and swap the
  `watch()` function - the rest of the script stays identical

## Migration Steps

1. Create `src/` directory structure and `src/components/`
2. Copy existing HTML pages into `src/pages/` and `src/index.html`
3. Convert each JS component file to a plain HTML file in `src/components/`
4. Replace `<script>` tags and empty `<div>` targets in src pages with
   `<!-- component:X -->` markers
5. Create `src/components/noscript.html`
6. Write and test `build.py`
7. Run `python build.py` - verify root-level output matches current site
8. Commit and push, verify site works on GitHub Pages
9. Remove the old `components/` JS files once confirmed working

## What You Keep, What Changes

- **Keep:** All your page content, CSS, assets, GitHub Pages hosting, DNS
  config, GitHub Pages `/` root setting
- **Change:** Your editable HTML source moves into `src/`; the root-level HTML
  files become build output (overwritten by `build.py`); JS component files
  become plain HTML component files in `src/components/`
- **Remove:** `components/header.js`, `components/navbar.js`,
  `components/footer.js`, `components/blog-menu.js` (their logic becomes the
  build script; their output becomes HTML component files)
- **Add:** `build.py`, `src/` directory tree, `src/components/noscript.html`

**Important:** Once migrated, you edit files in `src/` only. The root-level
HTML files are build output - any direct edits to them will be overwritten
the next time you run `build.py`.

## Dev Workflow

```
Option A: Manual build
  1. Edit files in src/
  2. Run: python build.py
  3. Open pages/about.html in browser to check
  4. Repeat 1-3 until happy
  5. Commit and push

Option B: Watch mode
  1. Run: python build.py --watch  (in a terminal tab, leave it running)
  2. Edit files in src/
  3. Refresh browser to see changes (build happens automatically)
  4. Repeat 2-3 until happy
  5. Ctrl+C the watch, commit and push
```

## Key Concept: Build Time vs Runtime

This is the same idea behind React's SSR/SSG, Next.js static export, and every
static site generator. The principle: if the output is the same for every
visitor, assemble it once ahead of time rather than in every browser. You're
implementing this concept directly in Python, which is exactly the kind of
hands-on understanding that transfers to frameworks later.
