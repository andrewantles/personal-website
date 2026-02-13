# Site Modernization Plan

## Current State

- Static HTML site with vanilla JS components
- Single blog post (hardcoded HTML, markdown file unused)
- Minimal CSS (desktop-first, basic responsive)
- Component system: header.js, navbar.js, blog-menu.js

## Observations

**Strengths:**
- Lightweight, no build step, fast loading
- Clean separation of components
- Good foundation for expansion

**Pain Points:**
- Blog posts require manual HTML—friction to publish
- No tagging or categorization
- `blog-menu.js` only lists posts by date, no filtering
- Markdown file exists but isn't rendered

---

## Recommendations

### 1. Blog Tagging System

**Option A: JSON Manifest (Recommended)**
- Create `posts/posts.json` with metadata for each post:
  ```json
  [
    {
      "slug": "google-ml-crash-course",
      "title": "Google ML Crash Course",
      "date": "2024-03-01",
      "tags": ["machine-learning", "notes"],
      "file": "2024-03-01-google-ml-crash-course.md"
    }
  ]
  ```
- `blog-menu.js` reads this manifest and renders tag filters
- Keeps everything static, no build step needed

**Option B: Frontmatter in Markdown**
- Requires a markdown parser (e.g., marked.js + gray-matter)
- More complex but keeps metadata with content

### 2. Blog Navigation Menu

- Extend `blog-menu.js` to:
  - Show tag filter buttons at top
  - List posts with tags displayed as badges
  - Filter posts when a tag is clicked
- Could add simple search (filter by title)

### 3. Style Modernization (Minimal Changes)

| Area | Suggestion | Done? |
|------|------------|-------|
| Typography | Use system font stack for faster loading, modern feel | DONE|
| Spacing | Increase whitespace, larger line-height | DONE|
| Colors | Soften the blue header, add subtle shadows | 
| Cards | Wrap blog list items in card-style containers | DONE |
| Nav | Add hover states, subtle transitions |

**CSS Variables** — Define colors/fonts in `:root` for easy theming.

### 4. Markdown Rendering (Optional)

- Add `marked.js` (~28kb) to render `.md` files client-side
- Create a generic `post.html` template that loads any post by slug
- URL pattern: `post.html?slug=google-ml-crash-course`

---

## Suggested Implementation Order

1. Create `posts.json` manifest
2. Update `blog-menu.js` to read manifest and render tags
3. Add tag filtering logic
4. Modernize CSS (typography, spacing, colors)
5. (Optional) Add markdown rendering for easier authoring

---

## Open Questions

- Do you want to keep it fully static (no build step)?
- Preferred tag UI: buttons, pills, sidebar list?
- Any specific color palette or style references?
