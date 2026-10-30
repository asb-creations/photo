# ASB Photography website

> **New here? Open `START-HERE.pdf` first.** It's the step-by-step guide to publishing and updating the site. This README is the technical reference.

The site is hosted for free on GitHub Pages. **To change which photos appear, you only add, delete or rename files in the `photos` folder.** Every time a change reaches GitHub, it rebuilds and republishes the site automatically, which takes about 2 minutes.

---

## Managing photos

```
photos/
  galleries.txt      ← which galleries exist, and their order
  portraits/         ← one folder per gallery
  couples/
  events/
  scenery/
  site/              ← landing page and About page photos
  extras/            ← storage; never shown on the site
```

**Add a photo:** put it in a gallery folder. Any JPG, PNG or iPhone HEIC works, at any size. The site makes web-sized copies automatically, works out whether each photo is portrait or landscape, and adds it to the staggered layout.

**Remove a photo:** delete it, or move it to `extras` to keep it for later.

**Change the order:** photos appear in filename order, so the numbers at the front decide where they go (`010-…`, `020-…`, `030-…`). The gaps leave room: to put a new photo between `020` and `030`, name it `025-anything.jpg`.

**Change a gallery's cover:** the **first** photo in each folder is the cover on the Portfolio page and in "Selected work" on the landing page. Give the photo you want a lower number, like `005-…`.

**Add a gallery** (e.g. Weddings): create a folder `photos/weddings`, add photos, and add the line `weddings: Weddings` to `photos/galleries.txt`. It gets its own page, a Portfolio card and a landing page tile automatically.

**Hide a gallery:** delete its line in `galleries.txt` or put `#` in front of it. The photos stay in the folder.

**Landing page and About photos:** replace a file in `photos/site/` with a new photo **with the same name**:
- `landing-left.jpg`: vertical, under the giant title (currently a portrait)
- `landing-right.jpg`: horizontal, on the right edge of the first screen (currently couples)
- `below-left.jpg`: vertical, first photo after scrolling (currently scenery)
- `below-right.jpg`: horizontal, second photo after scrolling (currently a portrait)
- `about.jpg`: About page

Each landing spot always keeps its shape. A photo of the wrong shape is cropped from the center to fit, so for the best framing, crop it to roughly that shape yourself first (vertical 2:3, horizontal 3:2).

---

## Two ways to make changes

### A. GitHub Desktop (easiest for regular updates)
1. Open the site folder on your computer and add, delete or rename photos in Finder as usual.
2. Open GitHub Desktop. It lists what changed. Type a short note in the "Summary" box (e.g. "New couples photos"), click **Commit to main**, then **Push origin**.
3. The live site updates in about 2 minutes.

### B. On github.com (no app needed, works from a phone)
- **Add photos:** open the repository, go into `photos` → `couples` (or another folder), click **Add file → Upload files**, drag the photos in, then click **Commit changes**.
- **Delete a photo:** click the photo, then **⋯ → Delete file → Commit changes**.
- Renaming photos (to reorder them) is awkward on github.com, so do that in GitHub Desktop.

To check that an update went live, open the **Actions** tab on github.com. A green check next to "Publish website" means it's live; a red X means something went wrong (click it to see why).

---

## One-time setup

1. **Set the email address for the forms.** Open `src/index.html` and `src/contact.html` in any text editor and replace `YOUR-EMAIL@example.com` (once in each file) with her email. The forms use [FormSubmit](https://formsubmit.co), which is free with no account. The first time someone submits a form, FormSubmit emails her an activation link. She clicks it once, and from then on every inquiry arrives as an email titled **Photo Shoot Inquiry**. Send a test inquiry right after the site goes live.
2. **Install [GitHub Desktop](https://desktop.github.com)** and sign in. Create a free GitHub account first if you don't have one.
3. In GitHub Desktop: **File → Add Local Repository**, then choose this folder. When it says the folder isn't a repository yet, click **create a repository**, then **Create Repository**.
4. Click **Publish repository**. **Uncheck "Keep this code private"**, because free GitHub Pages needs a public repository. Name it `<username>.github.io` for the address `https://<username>.github.io`, or use any other name for `https://<username>.github.io/<name>`.
5. On github.com, open the repository → **Settings → Pages**. Under "Build and deployment," set **Source** to **GitHub Actions**.
6. Go to the **Actions** tab → **Publish website** → **Run workflow**. This is only needed the first time, because the site was published before Pages was turned on. After about 2 minutes, the address appears on the Settings → Pages screen.

Use GitHub Desktop for this setup rather than uploading through the website. The folder includes a hidden `.github` folder (the auto-publish instructions), and Macs hide it when you drag files into a browser.

**Optional custom domain** (e.g. asbphotography.com): buy one from any registrar, then enter it under Settings → Pages → Custom domain and follow GitHub's instructions. The domain is the only part that costs money.

---

## What's in the folder

| Path | What it is |
|---|---|
| `photos/` | All photos, and `galleries.txt` (see above) |
| `src/index.html` | Landing page: giant title, tagline, four photos, "Selected work" and the "Inquire below" form |
| `src/about.html`, `src/contact.html`, `src/portfolio.html` | Other pages (`{{…}}` markers are filled in automatically) |
| `src/gallery.html` | The layout every gallery page uses |
| `src/css/style.css` | All colors, fonts and sizes (the main ones are variables at the top) |
| `src/js/main.js` | Enlarged-photo viewer and form sending |
| `build.py` | Turns all of the above into the finished website |
| `.github/workflows/publish.yml` | Tells GitHub to run `build.py` and publish after every change |

To preview the site on your own computer (optional): install Python, run `pip install pillow pillow-heif`, then `python3 build.py`, and open `_site/index.html`.
