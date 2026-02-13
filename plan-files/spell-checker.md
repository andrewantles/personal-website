# Spell and Grammar Checker Recommendations

Recommendations for checking spelling and grammar in Markdown files.

## Real-time checking (Editor Extensions)

If you're using **VS Code** (or similar editors):

### 1. Code Spell Checker
The most popular option for developers
- Highlights misspellings as you type
- Works great with Markdown
- Customizable dictionaries for technical terms
- Install: `ext install streetsidesoftware.code-spell-checker`

### 2. LTeX
Grammar and spell checking
- Uses LanguageTool (open source)
- Provides grammar suggestions like Word
- More comprehensive than just spell checking
- Install: `ext install valentjn.vscode-ltex`

## Command-line tools (Run on demand)

### 1. vale (Recommended)
Modern prose linter
- Specifically designed for technical writing and documentation
- Highly configurable with style guides
- Can check spelling, grammar, style consistency
- Install: `brew install vale` (or download from GitHub)
- Usage: `vale src/posts/*.md`
- Example config to check your posts directory

### 2. aspell
Traditional spell checker
- Simple, fast, no grammar checking
- Install: `brew install aspell`
- Usage: `aspell check filename.md` (interactive)
- Or batch: `aspell list < file.md` (lists misspellings)

### 3. write-good
Prose linter (Node.js)
- Checks for wordy phrases, passive voice, clichés
- Install: `npm install -g write-good`
- Usage: `write-good src/posts/*.md`

## Recommendation

Start with **vale** because:
- Purpose-built for technical writing
- Configurable (can create custom rules)
- Can integrate into your build/CI process
- Works offline
- No proprietary services involved
