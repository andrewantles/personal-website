# Single-Page Application Migration Plan

## Current State Assessment

### What We Have
- **4 HTML pages**: `index.html` (redirect), `about.html`, `blog.html`, `resume.html`
- **4 JavaScript components**: `header.js`, `navbar.js`, `footer.js`, `blog-menu.js`
- **No build tools**: Pure vanilla HTML/CSS/JS served statically
- **Self-hosted fonts**: Atkinson Hyperlegible (Next + Mono variants)
- **No external dependencies**: Fully self-contained, no Google services

### The Problem
Every content page repeats the same boilerplate:
```html
<div id="header"></div>
<script src="../components/header.js"></script>
<div id="menu-container"></div>
<script src="../components/navbar.js"></script>
<!-- unique page content -->
<footer id="footer"></footer>
<script src="../components/footer.js"></script>
```

This creates:
1. **Maintenance burden**: Changes to layout structure require editing every HTML file
2. **Inconsistency risk**: Easy to forget updating one page
3. **Code smell**: The component pattern is already 80% of the way to an SPA—we inject content dynamically but still duplicate the injection points

---

## Proposed Architecture

### Approach: Vanilla JavaScript SPA with Hash-Based Routing

**Why this approach:**
- **Zero dependencies**: Aligns with minimalist philosophy
- **No build step**: Keeps deployment simple (static file hosting)
- **Browser-native**: Uses standard Web APIs
- **Tiny footprint**: Entire router can be ~50 lines of code
- **SEO acceptable**: For a personal site with 3-4 pages, hash routing is fine
- **Progressive enhancement path**: Can add History API later if needed

**What changes:**
| Before | After |
|--------|-------|
| Multiple HTML files | Single `index.html` shell |
| Full page reloads on navigation | Dynamic content swap |
| Duplicated header/nav/footer in each file | Single instance, always present |
| `pages/about.html` | `#/about` route → loads `views/about.html` |
| Browser manages navigation | JavaScript router manages navigation |

---

## New File Structure

```
personal-website/
├── index.html                    # Single shell (header + nav + content area + footer)
├── router.js                     # Client-side routing logic
├── views/                        # Page content fragments (no <html>, <head>, etc.)
│   ├── about.html
│   ├── blog.html
│   └── resume.html
├── components/                   # Reusable components (simplified)
│   ├── header.js
│   ├── navbar.js
│   ├── footer.js
│   └── blog-menu.js
├── public/
│   ├── style.css
│   ├── fonts/
│   └── ... (unchanged)
├── posts/
│   └── ... (markdown files)
└── CLAUDE.md
```

### Key Differences

1. **`views/` directory**: Contains only the unique content for each page—no `<html>`, `<head>`, `<body>`, or shared components. Just the "meat" of each page.

2. **Single `index.html`**: Acts as the application shell:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head><!-- all meta, styles, fonts --></head>
   <body>
     <div id="header"></div>
     <div id="menu-container"></div>
     <main id="content"></main>  <!-- Views load here -->
     <footer id="footer"></footer>
     <script src="components/header.js"></script>
     <script src="components/navbar.js"></script>
     <script src="components/footer.js"></script>
     <script src="router.js"></script>
   </body>
   </html>
   ```

3. **`router.js`**: Listens for hash changes and loads appropriate view into `#content`.

---

## Router Implementation

### How Hash-Based Routing Works

**The URL pattern:**
- `yoursite.com/#/about` → loads About page
- `yoursite.com/#/blog` → loads Blog page
- `yoursite.com/#/resume` → loads Resume page
- `yoursite.com/` or `yoursite.com/#/` → redirects to `#/about`

**The mechanism:**
1. User clicks a nav link (`<a href="#/blog">`)
2. Browser updates URL hash (no page reload)
3. `hashchange` event fires
4. Router reads hash, fetches corresponding view HTML
5. Router injects view HTML into `<main id="content">`

### Router Code (~50 lines)

```javascript
// router.js - Minimal hash-based SPA router

const routes = {
  '/about': 'views/about.html',
  '/blog': 'views/blog.html',
  '/resume': 'views/resume.html'
};

const defaultRoute = '/about';

async function loadView(path) {
  const viewPath = routes[path];

  if (!viewPath) {
    // Unknown route - redirect to default
    window.location.hash = '#' + defaultRoute;
    return;
  }

  try {
    const response = await fetch(viewPath);
    if (!response.ok) throw new Error('View not found');

    const html = await response.text();
    document.getElementById('content').innerHTML = html;

    // Execute any scripts in the loaded view
    executeViewScripts();

    // Update page title based on route
    updatePageTitle(path);

    // Scroll to top on navigation
    window.scrollTo(0, 0);

  } catch (error) {
    console.error('Failed to load view:', error);
    document.getElementById('content').innerHTML = '<p>Page not found.</p>';
  }
}

function executeViewScripts() {
  // Re-run scripts that need to execute after view load
  // e.g., blog-menu.js for blog page
  const content = document.getElementById('content');
  const scripts = content.querySelectorAll('script');
  scripts.forEach(script => {
    const newScript = document.createElement('script');
    newScript.textContent = script.textContent;
    if (script.src) newScript.src = script.src;
    script.parentNode.replaceChild(newScript, script);
  });
}

function updatePageTitle(path) {
  const titles = {
    '/about': 'Andrew Antles',
    '/blog': 'Blog | Andrew Antles',
    '/resume': 'Resume | Andrew Antles'
  };
  document.title = titles[path] || 'Andrew Antles';
}

function handleRouteChange() {
  const hash = window.location.hash.slice(1) || defaultRoute; // Remove '#'
  loadView(hash);
}

// Listen for hash changes
window.addEventListener('hashchange', handleRouteChange);

// Handle initial page load
window.addEventListener('DOMContentLoaded', handleRouteChange);
```

---

## Migration Steps

### Phase 1: Create the Application Shell

**Goal**: Build the single `index.html` that will contain all shared elements.

**Tasks:**
1. Create new `index.html` at root with:
   - All `<head>` content (meta tags, CSS links, font preloads)
   - Header container (`<div id="header">`)
   - Navigation container (`<div id="menu-container">`)
   - Content area (`<main id="content">`)
   - Footer container (`<footer id="footer">`)
   - Script tags for all components + router

2. Ensure proper accessibility:
   - `<main>` landmark for content area
   - `aria-live="polite"` on content area for screen reader announcements
   - Skip-to-content link functionality

### Phase 2: Extract View Fragments

**Goal**: Convert existing pages to content-only fragments.

**Tasks:**
1. Create `views/` directory
2. For each existing page (`about.html`, `blog.html`, `resume.html`):
   - Extract only the unique content (everything between nav and footer)
   - Save as `views/[page].html`
   - Remove all `<html>`, `<head>`, `<body>`, header/nav/footer markup

**Example transformation:**

Before (`pages/about.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>...</head>
<body>
  <div id="header"></div>
  <script src="../components/header.js"></script>
  <div id="menu-container"></div>
  <script src="../components/navbar.js"></script>

  <main>
    <p>Unique about content...</p>
  </main>

  <footer id="footer"></footer>
  <script src="../components/footer.js"></script>
</body>
</html>
```

After (`views/about.html`):
```html
<p>Unique about content...</p>
```

### Phase 3: Implement the Router

**Goal**: Add client-side navigation.

**Tasks:**
1. Create `router.js` with the code shown above
2. Update `navbar.js` to use hash links:
   ```javascript
   // Change from:
   { name: 'About', href: 'about.html' }
   // To:
   { name: 'About', href: '#/about' }
   ```
3. Test all navigation paths
4. Handle edge cases:
   - Direct URL access (e.g., user bookmarks `yoursite.com/#/blog`)
   - Browser back/forward buttons
   - Invalid routes

### Phase 4: Handle Page-Specific Scripts

**Goal**: Ensure scripts like `blog-menu.js` run at the right time.

**The challenge**: In a traditional multi-page site, scripts run on page load. In an SPA, views load dynamically, so scripts must be triggered after view injection.

**Solutions:**
1. **Inline scripts in views**: Include `<script>` tags in view fragments; router re-executes them after injection.
2. **Event-driven initialization**: Components listen for a custom `viewloaded` event.
3. **Route-specific hooks**: Router calls initialization functions based on current route.

**Recommended approach** (Option 3):
```javascript
// In router.js
const viewInitializers = {
  '/blog': initBlogPage,
  '/resume': initResumePage
};

async function loadView(path) {
  // ... fetch and inject HTML ...

  // Run page-specific initialization
  if (viewInitializers[path]) {
    viewInitializers[path]();
  }
}

function initBlogPage() {
  // Initialize blog menu, load posts, etc.
}

function initResumePage() {
  // Any resume-specific initialization
}
```

### Phase 5: Update Navbar Component

**Goal**: Navbar links work with the router and show active state.

**Changes to `navbar.js`:**
```javascript
const navLinks = [
  { name: 'About', href: '#/about' },
  { name: 'Blog', href: '#/blog' },
  { name: 'Resume', href: '#/resume' }
];

function updateActiveLink() {
  const currentHash = window.location.hash || '#/about';
  document.querySelectorAll('#menu-container a').forEach(link => {
    if (link.getAttribute('href') === currentHash) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    } else {
      link.classList.remove('active');
      link.removeAttribute('aria-current');
    }
  });
}

// Call on hash change
window.addEventListener('hashchange', updateActiveLink);
```

### Phase 6: Cleanup

**Goal**: Remove obsolete files and finalize structure.

**Tasks:**
1. Delete old `pages/` directory (after confirming everything works)
2. Update any remaining hardcoded links
3. Test all functionality:
   - Navigation between all pages
   - Browser back/forward
   - Direct URL access
   - Bookmarking
   - Screen reader navigation
4. Update `CLAUDE.md` if needed

---

## Accessibility Considerations

### Screen Reader Support

**Content area announcements:**
```html
<main id="content" aria-live="polite" aria-atomic="true">
  <!-- Views load here -->
</main>
```
- `aria-live="polite"`: Screen readers announce content changes
- `aria-atomic="true"`: Announce entire region, not just changed parts

**Focus management:**
After navigation, move focus to the content area or a heading:
```javascript
async function loadView(path) {
  // ... load content ...

  // Move focus to content heading or container
  const heading = document.querySelector('#content h1, #content h2');
  if (heading) {
    heading.setAttribute('tabindex', '-1');
    heading.focus();
  }
}
```

### Skip Link Updates

The skip-to-content link should work with the SPA:
```html
<a href="#content" class="skip-link">Skip to content</a>
```

---

## SEO Considerations

### Hash Routing Limitations

Hash-based routing (`#/about`) has SEO limitations:
- Search engines historically ignored content after `#`
- Modern crawlers (Googlebot) can execute JavaScript, but it's not guaranteed
- Social media link previews may not work correctly

### Why It's Acceptable Here

1. **Personal site**: Not dependent on search traffic for business
2. **Limited pages**: Only 3-4 pages, not a content-heavy site
3. **Simplicity**: Avoids server-side rendering complexity

### Future Enhancement Path

If SEO becomes important, migrate to History API routing:
- URLs become `/about`, `/blog`, `/resume` (no hash)
- Requires server configuration to serve `index.html` for all routes
- Same router logic, different URL handling

---

## Alternative Approaches Considered

### 1. Server-Side Includes (SSI)
- **Pros**: No JavaScript needed, works everywhere
- **Cons**: Requires server support, not available on all static hosts
- **Verdict**: Less portable than client-side solution

### 2. Build-Time Static Generation (11ty, Hugo, Jekyll)
- **Pros**: Best SEO, fastest load times, no client-side JavaScript needed
- **Cons**: Adds build step and tooling complexity
- **Verdict**: Good option if blog grows; overkill for current 3-page site

### 3. Lightweight Frameworks (Lit, Preact, Alpine.js)
- **Pros**: More features, established patterns
- **Cons**: Adds dependencies, learning curve
- **Verdict**: Consider if app complexity grows significantly

### 4. Web Components
- **Pros**: Native browser feature, encapsulated
- **Cons**: More complex than simple JS, polyfills for older browsers
- **Verdict**: Could enhance current components later without full SPA

---

## Rollback Plan

If issues arise during migration:

1. **Keep old `pages/` directory** until fully tested (rename to `pages-backup/`)
2. **Git branch**: Do all work on a feature branch
3. **Quick rollback**: Restore `index.html` redirect to `pages/about.html`

---

## Testing Checklist

- [ ] All nav links work and update URL
- [ ] Browser back/forward buttons work correctly
- [ ] Direct URL access works (e.g., `site.com/#/blog`)
- [ ] Page titles update on navigation
- [ ] Active nav link styling works
- [ ] Screen reader announces page changes
- [ ] Focus moves appropriately after navigation
- [ ] Blog page functionality works (post loading)
- [ ] Resume page PDF embeds work
- [ ] Mobile navigation works
- [ ] No console errors
- [ ] All links point to correct hash routes

---

## Estimated Complexity

| Phase | Complexity | Notes |
|-------|------------|-------|
| 1. App Shell | Low | Copy/paste from existing, minor restructuring |
| 2. Extract Views | Low | Removing boilerplate from existing files |
| 3. Router | Medium | New code, but straightforward |
| 4. Script Handling | Medium | Requires understanding of script execution timing |
| 5. Navbar Updates | Low | Small modifications to existing code |
| 6. Cleanup | Low | Testing and file deletion |

---

## Summary

This migration eliminates header/nav/footer duplication by moving to a single-page architecture with:

- **One HTML file** that serves as the application shell
- **View fragments** containing only unique page content
- **A ~50-line router** handling client-side navigation
- **Zero new dependencies** maintaining the minimalist approach

The result is a more maintainable codebase where layout changes happen in one place, while preserving the lightweight, dependency-free philosophy of the site.
