# Prompt for updating the website with Claude

**Just changing photos?** You don't need Claude. Add, delete or rename files in the `photos` folders (see README.md, "Managing photos").

**Changing the design or text?** Start a new chat with Claude, attach the zipped site folder (or connect the GitHub repository), plus a Figma link, screenshots or sketches if you have them. Then paste everything below the line, filling in the part in [brackets].

---

I'm a photographer and this is my portfolio website. I'd like your help changing its design. The site files are attached.

**How the site works (please keep it working this way):**
- It's a static site hosted for free on GitHub Pages. A GitHub Action (`.github/workflows/publish.yml`) runs `build.py` on every push and publishes the `_site` folder it creates. Please keep it free: no paid services, no frameworks, no server code.
- **Photos are managed by folders, and I want to keep it that way.** `photos/galleries.txt` lists the galleries in order. Each gallery's photos live in `photos/<gallery>/` and appear in filename order; the first one is the gallery's cover. `photos/site/` holds the landing page and About photos (fixed names). `build.py` resizes everything and builds the gallery pages, Portfolio cards and landing page "Selected work" tiles from these folders. Please don't hard-code photo lists into the pages.
- Page sources are in `src/`. `{{HEADER …}}`, `{{FOOTER}}`, `{{TITLE}}`, `{{PHOTOS}}`, `{{CATEGORY_CARDS}}` and `{{SELECTED_WORK}}` are filled in by `build.py`. Every gallery page uses `src/gallery.html`. Colors, fonts and sizes are variables at the top of `src/css/style.css`; behavior is in `src/js/main.js`.
- Current style: editorial and minimal. White background, Cormorant Garamond for giant titles, EB Garamond for everything else, small widely spaced italic text for nav and labels, sharp black buttons, and photos staggered at different heights (pairs in `<div class="spread">`, each photo with class `l` or `p`).
- Clicking any gallery photo enlarges it in the middle of the screen. The X (or Esc) closes it and returns to the same gallery; arrow keys and swiping move between photos. Please keep this.
- The forms in `src/index.html` and `src/contact.html` email me with the subject "Photo Shoot Inquiry" through FormSubmit (the form's `action` address). Please don't change the address or remove the hidden `_subject` field unless I ask.
- It must look good on phones as well as computers.

**What I want to change:**
[Describe what you'd like: a different font or colors, a new landing page layout, rewritten About text, the tagline, the questions in the inquiry form, an Instagram link, and so on. Paste a Figma link or attach screenshots of sites you like if you have them.]

**How I'd like you to work:**
1. Ask me any questions first, especially about the overall look I'm going for. I'm not a coder, so please explain choices in plain language.
2. Run `build.py` and show me screenshots of the main pages, on a computer and on a phone, so I can react before we finish.
3. When we're done, give me the complete updated site folder as a zip, and tell me which files changed, so I can copy them into my site folder and push them with GitHub Desktop.
