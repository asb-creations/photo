#!/usr/bin/env python3
"""
Builds the ASB Photography website.

You normally never run this yourself: every time something is pushed to
GitHub, the "Publish website" action runs it and puts the result online.

What it does
  * Reads photos/galleries.txt to find out which galleries exist.
  * For each gallery folder in photos/, takes every photo in filename
    order, makes a web-sized copy (2000px) and a preview (900px), and
    builds that gallery's page from src/gallery.html.
  * The first photo in each folder is that gallery's cover on the
    Portfolio page and in "Selected work" on the landing page.
  * Copies photos/site/ (landing + about photos) and src/ into _site/.

Run it locally (optional):  pip install pillow pillow-heif
                            python3 build.py
then open _site/index.html in a browser.
"""
import datetime
import html
import os
import re
import shutil
import sys

from PIL import Image, ImageOps

try:  # lets iPhone .HEIC photos work too
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(ROOT, "photos")
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "_site")

FULL_SIZE = 2000      # longest side of the enlarged photo
PREVIEW_SIZE = 900    # longest side of the gallery preview
IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")

NAV = [("portfolio", "Portfolio"), ("about", "About"), ("contact", "Contact")]


# ---------------------------------------------------------------- helpers
def natural_key(name):
    """Sort 'img2' before 'img10'."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def slug(name):
    base = os.path.splitext(name)[0].lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base or "photo"


def save_resized(img, path, longest, quality):
    copy = img.copy()
    copy.thumbnail((longest, longest), Image.LANCZOS)
    copy.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return copy.size


def open_photo(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)   # respect the phone's rotation
    return img.convert("RGB")


def read_galleries():
    galleries = []
    with open(os.path.join(PHOTOS, "galleries.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                folder, title = [p.strip() for p in line.split(":", 1)]
            else:
                folder, title = line, line.title()
            if not os.path.isdir(os.path.join(PHOTOS, folder)):
                print(f"  ! galleries.txt lists '{folder}' but there is no photos/{folder} folder - skipped")
                continue
            galleries.append((slug(folder), folder, title))
    return galleries


def nav_html(current, label):
    links = "".join(
        f'<a href="{k}.html"{" aria-current=\"page\"" if k == current else ""}>{t}</a>'
        for k, t in NAV
    )
    return f'<nav class="nav" aria-label="{label}">{links}</nav>'


def header_html(current):
    wordmark = "" if current == "home" else '\n    <a class="wordmark" href="index.html">asb photography</a>'
    return f'  <header class="site-header">{wordmark}\n    {nav_html(current, "Main")}\n  </header>'


def footer_html():
    year = datetime.date.today().year
    return (
        '  <footer class="site-footer">\n'
        '    <a class="wordmark" href="index.html">asb photography</a>\n'
        f'    {nav_html(None, "Footer")}\n'
        f'    <p class="copyright">&copy; {year} asb photography</p>\n'
        '  </footer>'
    )


def fill_common(text):
    text = re.sub(r"\{\{HEADER (\w+)\}\}", lambda m: header_html(m.group(1)), text)
    return text.replace("{{FOOTER}}", footer_html())


def add_image_sizes(text):
    """Add width/height to <img src="images/..."> tags so pages don't jump while loading."""
    def repl(m):
        tag, src = m.group(0), m.group(1)
        if "width=" in tag:
            return tag
        path = os.path.join(OUT, src)
        if not os.path.exists(path):
            return tag
        w, h = Image.open(path).size
        return tag.replace(f'src="{src}"', f'src="{src}" width="{w}" height="{h}"')
    return re.sub(r'<img[^>]*src="(images/[^"]+)"[^>]*>', repl, text)


def write_page(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(add_image_sizes(fill_common(text)))


# ---------------------------------------------------------------- build
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "images", "site"))
    shutil.copytree(os.path.join(SRC, "css"), os.path.join(OUT, "css"))
    shutil.copytree(os.path.join(SRC, "js"), os.path.join(OUT, "js"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # Landing + about photos (fixed names, so swapping = replacing the file)
    site_dir = os.path.join(PHOTOS, "site")
    for name in sorted(os.listdir(site_dir)):
        if name.lower().endswith(IMAGE_TYPES):
            img = open_photo(os.path.join(site_dir, name))
            save_resized(img, os.path.join(OUT, "images", "site", slug(name) + ".jpg"), 1600, 82)

    gallery_template = open(os.path.join(SRC, "gallery.html"), encoding="utf-8").read()
    covers = []   # (page, title, cover path, w, h)

    for page, folder, title in read_galleries():
        src_dir = os.path.join(PHOTOS, folder)
        out_dir = os.path.join(OUT, "images", page)
        os.makedirs(out_dir)
        files = sorted(
            (f for f in os.listdir(src_dir) if f.lower().endswith(IMAGE_TYPES) and not f.startswith(".")),
            key=natural_key,
        )
        photos = []
        used = set()
        for f in files:
            try:
                img = open_photo(os.path.join(src_dir, f))
            except Exception as e:  # unreadable file: skip it, keep building
                print(f"  ! could not open photos/{folder}/{f} ({e}) - skipped")
                continue
            name = slug(f)
            while name in used:
                name += "-2"
            used.add(name)
            save_resized(img, os.path.join(out_dir, name + ".jpg"), FULL_SIZE, 82)
            w, h = save_resized(img, os.path.join(out_dir, name + "-sm.jpg"), PREVIEW_SIZE, 78)
            photos.append((name, w, h))

        if not photos:
            print(f"  ! photos/{folder} has no photos - gallery skipped")
            continue

        alt = html.escape(f"{title} photograph by ASB Photography")
        spreads = []
        for i in range(0, len(photos), 2):   # photos go in pairs, in filename order
            tags = []
            for name, w, h in photos[i:i + 2]:
                shape = "p" if h > w else "l"
                tags.append(
                    f'        <a class="photo {shape}" style="--r:{w / h:.3f}" href="images/{page}/{name}.jpg">'
                    f'<img src="images/{page}/{name}-sm.jpg" width="{w}" height="{h}" alt="{alt}" loading="lazy"></a>'
                )
            spreads.append('      <div class="spread">\n' + "\n".join(tags) + "\n      </div>")

        text = gallery_template.replace("{{TITLE}}", html.escape(title)).replace("{{PHOTOS}}", "\n".join(spreads))
        write_page(f"{page}.html", text)
        name, w, h = photos[0]
        covers.append((page, title, f"images/{page}/{name}-sm.jpg", w, h))
        print(f"  {title}: {len(photos)} photo{'' if len(photos) == 1 else 's'}")

    # Portfolio page cards + landing page "Selected work"
    cards = "\n".join(
        f'      <a class="category" href="{p}.html">\n'
        f'        <img src="{src}" width="{w}" height="{h}" alt="{html.escape(t)} gallery">\n'
        f'        <h2>{html.escape(t)}</h2>\n'
        f'        <span class="caption">View gallery &rarr;</span>\n'
        f'      </a>'
        for p, t, src, w, h in covers
    )
    tiles = "\n".join(
        f'        <a class="tile" href="{p}.html"><img src="{src}" width="{w}" height="{h}" '
        f'alt="{html.escape(t)} gallery" loading="lazy"><span class="caption">{html.escape(t)} &rarr;</span></a>'
        for p, t, src, w, h in covers
    )

    for page in ("index", "portfolio", "about", "contact"):
        text = open(os.path.join(SRC, page + ".html"), encoding="utf-8").read()
        text = text.replace("{{CATEGORY_CARDS}}", cards).replace("{{SELECTED_WORK}}", tiles)
        write_page(page + ".html", text)

    print(f"Done. Website is in {os.path.relpath(OUT)}/")


if __name__ == "__main__":
    sys.exit(build())
