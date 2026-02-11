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
  src/                    # What you edit
    pages/
      about.html
      blog.html
      resume.html
    components/
      header.html         # Replaces header.js - same content, plain HTML
      navbar.html          # Replaces navbar.js - same content, plain HTML
      footer.html          # Replaces footer.js - same content, plain HTML
      noscript.html        # The noscript fallback message
    index.html
  build/                  # What gets deployed (git-ignored)
    pages/
      about.html          # Complete pages with all components injected
      blog.html
      resume.html
    index.html
  public/                 # Static assets (unchanged, copied to build/)
    style.css
    profile.jpg
  build.py                # The build script
```

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

3. `build.py` reads each page, replaces `<!-- component:X -->` with the contents of `components/X.html`, and writes the result to `build/`.

4. You open `build/` files in your browser for testing. You deploy `build/`, not `src/`.

## The Build Script (Conceptual)

```python
"""
Usage: python build.py
Reads src/, injects components, writes to build/
"""
import re
from pathlib import Path

SRC = Path("src")
BUILD = Path("build")
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
    components = load_components()
    # Process all HTML files in src/, preserving directory structure
    for src_file in SRC.rglob("*.html"):
        if COMPONENTS in src_file.parents:
            continue  # Skip component files themselves
        relative = src_file.relative_to(SRC)
        dest = BUILD / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        html = src_file.read_text()
        html = inject_components(html, components)
        dest.write_text(html)
    # Copy static assets
    # (could use shutil.copytree for public/)

if __name__ == "__main__":
    build()
```

## Migration Steps

1. Create `src/` and `build/` directories
2. Move existing HTML pages into `src/`
3. Convert each JS component to a plain HTML file in `src/components/`
4. Replace `<script>` tags and empty `<div>` targets in pages with `<!-- component:X -->` markers
5. Create the `noscript.html` component
6. Write and test `build.py`
7. Add `build/` to `.gitignore`
8. Update deployment to serve from `build/`
9. Remove the old JS component files once everything works

## What You Keep, What Changes

- **Keep:** All your page content, CSS, assets, GitHub Pages hosting
- **Change:** HTML files gain a `src/` vs `build/` split; JS component files become HTML component files
- **Remove:** `header.js`, `navbar.js`, `footer.js` (their logic becomes the build script; their output becomes HTML component files)
- **Add:** `build.py`, `src/components/noscript.html`

## Dev Workflow

```
1. Edit files in src/
2. Run: python build.py
3. Open build/pages/about.html in browser to check
4. Commit src/ and push (build/ is git-ignored)
```

Note: If the edit-build-refresh cycle feels slow, the script runs in milliseconds for a site this size. You could also add a `--watch` flag later that auto-rebuilds when `src/` files change, but that's optional.

## Key Concept: Build Time vs Runtime

This is the same idea behind React's SSR/SSG, Next.js static export, and every static site generator. The principle: if the output is the same for every visitor, assemble it once ahead of time rather than in every browser. You're implementing this concept directly in Python, which is exactly the kind of hands-on understanding that transfers to frameworks later.
