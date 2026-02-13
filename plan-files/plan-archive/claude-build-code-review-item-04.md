# Plan: Add Author(s) to Blog Frontmatter

## Goal
Add support for author information in blog post frontmatter to accommodate potential guest bloggers or multi-author posts in the future.

## Current State
- Blog posts have frontmatter with `title`, `date`, and `summary` fields
- The `build.py` script parses frontmatter using a simple key-value parser
- Templates (`post.html` and `blog.html`) display date and title but no author info
- No author information is currently tracked or displayed

## Proposed Changes

### 1. Frontmatter Schema Update
- Add an `author` field to frontmatter
- Field will be optional with a default value of "Andrew Antles"
- Support single author (string) initially
- Design to allow future expansion to multiple authors (could be comma-separated or list)

### 2. Code Changes in build.py

**parse_frontmatter() function (lines 80-94):**
- No changes needed - already handles arbitrary key-value pairs

**build_posts() function (lines 168-253):**
- Extract author from metadata: `author = meta.get("author", "Andrew Antles")`
- Pass author to template: `page = page.replace("{{ author }}", author)`
- Add author to posts_meta dictionary for listing page

**build_blog_listing() function (lines 256-292):**
- Optionally include author in blog listing tiles if not default author
- This allows highlighting guest posts

### 3. Template Updates

**src/templates/post.html:**
- Add author display after the date/time element
- Use semantic HTML with proper microdata/schema
- Format: `<p class="post-meta"><time>...</time> by <span class="author">{{ author }}</span></p>`

**src/templates/blog.html:**
- No changes needed initially (author in listing is optional)
- Could add later if guest posts become common

### 4. Update Existing Posts
Update all existing markdown posts in `/posts/` to include author field:
- 2024-03-01-google-ml-crash-course.md
- 2026-01-18-security-program-week-1.md
- 2026-01-25-security-program-week-2.md
- 2026-02-01-security-program-week-3.md

Add: `author: "Andrew Antles"` to each frontmatter section

### 5. Testing Plan
1. Run build.py to ensure no errors
2. Check that author displays correctly on individual post pages
3. Verify existing posts still render properly
4. Check that omitting author field uses default value
5. Manually inspect HTML output for proper semantic markup

## Future Enhancements (Not in Scope)
- Support for multiple authors (comma-separated or YAML list)
- Author bio/profile pages
- Filter blog by author
- Author avatars/images
- Structured data markup for SEO

## Accessibility Considerations
- Use semantic HTML elements
- Ensure author info is readable by screen readers
- Maintain proper heading hierarchy
- No visual-only indicators for authorship

## Risks & Mitigation
- **Risk**: Breaking existing posts that don't have author field
  - **Mitigation**: Use default value in meta.get()
- **Risk**: Build errors if frontmatter parsing changes
  - **Mitigation**: Test thoroughly before committing
- **Risk**: Visual layout issues with new author display
  - **Mitigation**: Check existing CSS, add minimal styling if needed

## Success Criteria
- All posts build without errors
- Author information displays on individual post pages
- Default author "Andrew Antles" is used when field is omitted
- HTML remains valid and accessible
- Git history shows clear, incremental changes
