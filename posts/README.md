# Notes

`build.py` build script assumes:
- Every blog post begins with a YAML frontmatter section, as follows:
    - Starts and ends with `---`
    - Nothing comes before the `---`; the first `---` is the very beginning of the file
    - Each item in the frontmatter is a key, value pair separated by a `:`; e.g. `key: value`
        - Values that are not dates are strings between double quotes (`""`)
- That post images, and only post images, are kept in a sub-directory here with the same name as the post markdown file.

Frontmatter should include, at a minimum:
- title
- date in format: yyyy-mm-dd
- summary
    - Brief description of the post contents, for use with blog listing tiles.