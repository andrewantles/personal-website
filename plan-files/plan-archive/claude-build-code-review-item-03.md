# Build Code Review Item 3: Move posts directory under src/

## Overview
This plan addresses item 3 from the blog build code review: moving the posts directory under src/ and updating .gitignore to ignore src/.

## Current State
- Posts are located at `/posts/` (root level)
- .gitignore currently ignores `.DS_Store`, `.claude`, `.venv/`, and `./src/`
- build.py references `POSTS_DIR = ROOT / "posts"`

## Goals
1. Move the posts directory from root to under src/
2. Update .gitignore to properly ignore the src/ directory (note: already partially done)
3. Update build.py to reference the new posts location at `src/posts`
4. Ensure the build process continues to work correctly

## Implementation Steps

### 1. Move posts directory
```bash
mv /Users/andrewantles/code/personal-website/posts /Users/andrewantles/code/personal-website/src/posts
```

### 2. Update .gitignore
The .gitignore already has `./src/` which should work, but we'll verify it's correctly formatted. Standard practice is to use `src/` without the leading `./`.

### 3. Update build.py
Change line 28 from:
```python
POSTS_DIR = ROOT / "posts"
```
to:
```python
POSTS_DIR = SRC / "posts"
```

This is cleaner since `SRC` is already defined as `ROOT / "src"` on line 25.

### 4. Test the build
Run `python build.py` to ensure:
- Posts are found at the new location
- Markdown files are converted to HTML
- Images are copied correctly
- The blog listing page is generated

## Rationale

### Why move posts under src/?
1. **Organization**: Source content (posts, components, templates) is logically grouped
2. **Clarity**: Separates source materials from output and configuration
3. **Version control**: Makes it easier to selectively ignore/track content
4. **Build separation**: Clear distinction between what gets built (src/) and what is built (pages/, public/)

### Why gitignore src/?
1. **Avoid duplication**: Source markdown shouldn't be tracked if we're only deploying HTML
2. **Clean repository**: Keeps the repo focused on configuration and output
3. **Flexibility**: Makes it easier to work with external content sources

However, there's a consideration here: if src/ is gitignored, we lose version control over:
- The posts themselves (markdown source)
- Components and templates

**Recommendation**: We should reconsider this. Typically, you'd want to track source files (markdown, components) in git and gitignore the build output (pages/, public/). The current approach seems backwards. I'll flag this in the PR for discussion.

## Testing Checklist
- [ ] Posts directory successfully moved to src/posts
- [ ] build.py updated to use new path
- [ ] .gitignore updated/verified
- [ ] Build completes without errors
- [ ] Generated HTML files appear in pages/blog/
- [ ] Blog listing page generated at pages/blog.html
- [ ] Images copied to public/blog-files/
- [ ] All existing posts are built correctly

## Rollback Plan
If issues arise:
1. `git checkout main` to return to previous state
2. Or manually revert: `mv src/posts posts` and revert build.py change
