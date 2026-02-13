"""
Blog build script for AndrewAntles.Net

Converts markdown posts in /posts/ to HTML pages in /pages/blog/.
Generates a blog listing page at /pages/blog.html.
Injects shared HTML components (header, navbar, footer) at build time.

Usage:
  python build.py          # One-time build
  python build.py --watch  # Watch for changes and auto-rebuild
"""
import re
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

import markdown

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
SRC = ROOT / "src"
COMPONENTS_DIR = SRC / "components"
TEMPLATES_DIR = SRC / "templates"
POSTS_DIR = ROOT / "posts"
PAGES_DIR = ROOT / "pages"
BLOG_DIR = PAGES_DIR / "blog"
IMG_DEST = ROOT / "public" / "img" / "blog-img"

# ---------------------------------------------------------------------------
# Component injection (general-purpose, used for all pages)
# ---------------------------------------------------------------------------

def load_components():
    """Read all component HTML files from src/components/ into a dict."""
    components = {}
    for f in COMPONENTS_DIR.glob("*.html"):
        components[f.stem] = f.read_text()
    return components


def inject_components(html, components):
    """Replace <!-- component:name --> markers with component HTML."""
    def replacer(match):
        name = match.group(1)
        return components.get(name, match.group(0))
    # re.sub replaces arg1 with arg2, from source: arg3
    return re.sub(r"<!-- component:(\w+) -->", replacer, html)

# ---------------------------------------------------------------------------
# Template variable replacement
# ---------------------------------------------------------------------------

def compute_root(dest_path):
    """Uses `pathlib` to compute the relative path from an output file back to the project root.

    Examples:
        pages/blog.html       -> "../"
        pages/blog/post.html  -> "../../"
        index.html            -> "./"
    """
    rel = dest_path.relative_to(ROOT)
    depth = len(rel.parent.parts)
    return "../" * depth if depth > 0 else "./"


def replace_globals(html, root):
    """Replace global template variables: {{ root }} and {{ year }}."""
    html = html.replace("{{ root }}", root)
    html = html.replace("{{ year }}", str(datetime.now().year))
    return html

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Extract YAML frontmatter and body from a markdown file.

    Expects files to start with --- on the first line. Returns a tuple of
    (metadata_dict, body_string). If no frontmatter is found, returns an
    empty dict and the full text.
    """
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = {}
        for line in fm.strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')
        return meta, body.strip()
    return {}, text


def format_date(date_str):
    """Convert '2026-02-01' to 'February 1, 2026'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        # %-d gives day without zero-padding on macOS/Linux
        return dt.strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        return date_str

# ---------------------------------------------------------------------------
# Image handling
# ---------------------------------------------------------------------------

def copy_post_images():
    """Copy image directories from /posts/ to /public/blog-files/.

    Any subdirectory in /posts/ is treated as an image directory and copied
    in its entirety. Existing copies are replaced to keep things fresh.
    """
    # pathlib.mkdir args: `parents=True` creates parents if not exist; 
    #   `exist_ok=True` does not raise error for existing dir
    IMG_DEST.mkdir(parents=True, exist_ok=True)
    for item in POSTS_DIR.iterdir():
        if item.is_dir():
            dest = IMG_DEST / item.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)


def rewrite_image_paths(html, root):
    """Rewrite relative image src paths to point at /public/blog-files/.

    Only rewrites local relative paths. Absolute URLs (http://, https://),
    root-relative paths (/), and data URIs are left untouched.

    Args:
        html: The HTML string to process.
        root: The relative path from the output file to the project root
              (e.g., "../../" for pages/blog/eg_post.html).
    """
    def replacer(match):
        before = match.group(1)   # <img ... src="
        src = match.group(2)      # the path
        after = match.group(3)    # closing quote

        # Skip non-local paths
        if src.startswith(("http://", "https://", "/", "#", "data:")):
            return match.group(0)

        # Strip leading ./ or ../  and any leading "posts/" prefix
        clean = re.sub(r"^(\.\./)*(\./)*", "", src)
        clean = re.sub(r"^posts/", "", clean)

        return f"{before}{root}public/blog-files/{clean}{after}"
    # re.sub replaces arg1 with arg2, from source: arg3
    return re.sub(r'(<img[^>]+src=["\'])([^"\']+)(["\'])', replacer, html)


def extract_first_image_src(html):
    """Return the src of the first local <img> in the HTML, or None."""
    for match in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html):
        src = match.group(1)
        if not src.startswith(("http://", "https://", "/", "#", "data:")):
            return src
    return None

# ---------------------------------------------------------------------------
# Blog post building
# ---------------------------------------------------------------------------

def build_posts(components):
    """Convert markdown posts to HTML and generate the blog listing page."""
    post_template = (TEMPLATES_DIR / "post.html").read_text()
    listing_template = (TEMPLATES_DIR / "blog.html").read_text()
    # pathlib.mkdir args: `parents=True` creates parents if not exist; 
    #   `exist_ok=True` does not raise error for existing dir
    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    posts_meta = []
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])

    for md_file in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        raw = md_file.read_text()
        meta, body = parse_frontmatter(raw)

        # Reset the Markdown instance so toc/state is fresh per post
        md.reset()
        html_content = md.convert(body)
        toc_html = md.toc

        # Extract first image src BEFORE path rewriting (raw relative path)
        raw_thumbnail = extract_first_image_src(html_content)

        # Compute root for this output location
        dest = BLOG_DIR / (md_file.stem + ".html")
        root = compute_root(dest)

        # Rewrite image paths to point at public/blog-files/
        html_content = rewrite_image_paths(html_content, root)

        # Build the TOC block (only if there are headings)
        toc_block = ""
        if "<li>" in toc_html:
            toc_block = (
                '<nav class="toc" aria-label="Table of contents">\n'
                "  <h2>Outline</h2>\n"
                f"  {toc_html}\n"
                "</nav>"
            )

        # Fill in the post template
        # dict.get() returns the second arg if the first does not exist
        title = meta.get("title", md_file.stem)
        date = meta.get("date", "")
        date_display = format_date(date)

        page = post_template
        page = page.replace("{{ title }}", title)
        page = page.replace("{{ date }}", date)
        page = page.replace("{{ date_display }}", date_display)
        page = page.replace("{{ toc }}", toc_block)
        page = page.replace("{{ content }}", html_content)

        # Inject components and resolve global variables
        page = inject_components(page, components)
        page = replace_globals(page, root)

        '''
        Write output:
        `dest` points to an .html post page at this point
        pathlib.mkdir args: `parents=True` creates parents if not exist; 
          `exist_ok=True` does not raise error for existing dir
        '''
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
        print(f"  Built: {dest}")

        # Compute the thumbnail path relative to the listing page
        listing_thumbnail = None
        if raw_thumbnail:
            # re.sub replaces arg1 with arg2, from source: arg3
            clean = re.sub(r"^(\.\./)*(\./)*", "", raw_thumbnail)
            clean = re.sub(r"^posts/", "", clean)
            listing_thumbnail = f"../public/blog-files/{clean}"

        posts_meta.append({
            "title": title,
            "date": date,
            "date_display": date_display,
            "summary": meta.get("summary", ""),
            "slug": md_file.stem,
            "thumbnail": listing_thumbnail,
        })

    # Generate the blog listing page
    build_blog_listing(posts_meta, listing_template, components)


def build_blog_listing(posts_meta, listing_template, components):
    """Generate pages/blog.html with a tile for each post."""
    tiles = []
    for post in posts_meta:
        thumb_html = ""
        if post["thumbnail"]:
            # `loading="lazy" defers image loading until visible in viewport
            thumb_html = (
                f'    <img src="{post["thumbnail"]}" alt="" '
                f'class="post-tile-thumb" loading="lazy">\n'
            )

        tile = (
            f'<a href="./blog/{post["slug"]}.html" class="post-tile">\n'
            f"  <article>\n"
            f"{thumb_html}"
            f'    <div class="post-tile-text">\n'
            f'      <time datetime="{post["date"]}">{post["date_display"]}</time>\n'
            f'      <h3>{post["title"]}</h3>\n'
            f'      <p>{post["summary"]}</p>\n'
            f"    </div>\n"
            f"  </article>\n"
            f"</a>"
        )
        tiles.append(tile)

    tiles_html = "\n".join(tiles)

    dest = PAGES_DIR / "blog.html"
    root = compute_root(dest)

    page = listing_template.replace("{{ post_tiles }}", tiles_html)
    page = inject_components(page, components)
    page = replace_globals(page, root)

    dest.write_text(page)
    print(f"  Built: {dest}")

# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build():
    """Run a full build: copy images, convert posts, generate listing."""
    print("Building...")
    components = load_components()
    copy_post_images()
    build_posts(components)
    print("Build complete.")

# ---------------------------------------------------------------------------
# Watch mode
# ---------------------------------------------------------------------------

def get_mtimes(directories):
    """Get a dict of {filepath: modification_time} for all files."""
    mtimes = {}
    for directory in directories:
        if directory.exists():
            for f in directory.rglob("*"):
                if f.is_file():
                    mtimes[f] = f.stat().st_mtime
    return mtimes


def watch():
    """Poll for file changes and rebuild when detected."""
    watch_dirs = [SRC, POSTS_DIR]
    print("Watching for changes... (Ctrl+C to stop)")
    build()
    last_mtimes = get_mtimes(watch_dirs)
    try:
        while True:
            time.sleep(1)
            current_mtimes = get_mtimes(watch_dirs)
            if current_mtimes != last_mtimes:
                changed = [
                    str(f) for f in current_mtimes
                    if current_mtimes.get(f) != last_mtimes.get(f)
                ]
                print(f"\nChanges detected: {', '.join(changed)}")
                build()
                last_mtimes = current_mtimes
    except KeyboardInterrupt:
        print("\nStopped watching.")


if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch()
    else:
        build()
