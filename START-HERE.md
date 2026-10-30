# Your website: start here

This guide walks you through putting your website online for free and keeping your photos up to date. Setup is one time, about 20 minutes, with no coding. After that, updating photos takes a couple of minutes.

**What it costs:** nothing. GitHub hosts the site for free, and the contact forms use a free service. The only optional cost is a custom address like asbphotography.com (see the end).

---

## Part 1: Put the site online (one time)

### 1. Unzip the folder and put it somewhere permanent
Double-click `asb-photography-site.zip`. Move the `asb-photography-site` folder somewhere you'll keep it, such as Documents. **This folder is your website.** You'll come back to it whenever you update photos.

### 2. Create a GitHub account
Go to **github.com** and click **Sign up**. Choose your **username** carefully, because it becomes part of your web address: `https://yourusername.github.io`.

### 3. Install GitHub Desktop
Download it from **desktop.github.com**, open it, and sign in with your new GitHub account. This free app sends your folder to GitHub.

### 4. Add your website folder to GitHub Desktop
1. In GitHub Desktop, click **File → Add Local Repository…**
2. Click **Choose…** and select the `asb-photography-site` folder.
3. It will say the folder "does not appear to be a Git repository." Click the blue **create a repository** link.
4. Leave everything as it is and click **Create Repository**.

### 5. Publish it to GitHub
1. Click **Publish repository** at the top.
2. For **Name**, type your username followed by `.github.io` (for example, `asbphoto.github.io`). This gives you the address `https://asbphoto.github.io`.
3. **Uncheck "Keep this code private."** Free websites must be public. Only the website files are public, which anyone can see on your site anyway.
4. Click **Publish Repository**.

### 6. Turn on the website
1. In GitHub Desktop, click **Repository → View on GitHub**. Your repository opens in the browser.
2. Click **Settings** in the top menu, then **Pages** in the left menu.
3. Under **Build and deployment**, change **Source** to **GitHub Actions**. That's it; there's no save button.

> If you peek at the **Actions** tab now, you may see a red ✗ from step 5. That's expected, because the website wasn't turned on yet. The next step fixes it.

### 7. Add your email address for inquiries
This tells the site where to send inquiry emails, and it also publishes the site.

1. On your repository's page on github.com, click the **src** folder, then **index.html**.
2. Click the **pencil icon** (✏️ "Edit this file") near the top right.
3. Press **Cmd + F** (Ctrl + F on Windows) and search for `YOUR-EMAIL@example.com`.
4. Replace it with your email address. Keep everything around it exactly the same.
5. Click **Commit changes…**, then **Commit changes** again.
6. Go back to the **src** folder and do the same for **contact.html**.
7. Back in GitHub Desktop, click **Fetch origin**, then **Pull origin**. This copies the email change into your folder so it stays in sync.

### 8. See your site
1. On github.com, click the **Actions** tab. Wait until "Publish website" shows a **green ✓**, which takes about 2 minutes.
2. Go to **Settings → Pages**. It shows "Your site is live at…" with your address. Open it!

### 9. Activate the inquiry form
1. On your live site, fill in the **Inquire below** form with a test message and press **Send Inquiry**.
2. Check your email (and spam) for a message from **FormSubmit** and click **Activate Form**.
3. Send one more test from the landing page and one from the **Contact** page. Both should arrive titled **"Photo Shoot Inquiry."**

🎉 Your site is live.

---

## Part 2: Updating photos

Everything happens in the **photos** folder inside your website folder:

```
photos/
  galleries.txt    ← list of galleries and their order
  portraits/       ← one folder per gallery
  couples/
  events/
  scenery/
  site/            ← the landing page and About photos
  extras/          ← storage; never shown on the site
```

| To… | Do this |
|---|---|
| **Add a photo** | Drop it into a gallery folder. Any JPG, PNG or iPhone HEIC works, at any size; the site resizes it for you. |
| **Remove a photo** | Delete it, or move it to `extras` to keep it for later. |
| **Change the order** | Photos appear in filename order, and the number at the front decides where they go (`010-`, `020-`, `030-`…). To put a new photo between `020` and `030`, name it `025-anything.jpg`. |
| **Change a gallery's cover** | The **first** photo in a folder is the cover on the Portfolio page and the landing page. Give the one you want the lowest number, like `005-`. |
| **Add a gallery** (e.g. Maternity) | Make a new folder inside `photos` called `maternity`, add photos, then open `galleries.txt` and add the line `maternity: Maternity`. A page, Portfolio card and landing page tile appear automatically. |
| **Hide a gallery** | In `galleries.txt`, put `#` at the start of its line. |
| **Change a landing or About photo** | In `photos/site`, replace the file with a new photo **with exactly the same name** (see below). |

**The photos in `photos/site`:**

- `landing-left.jpg`: vertical, beside the big title
- `landing-right.jpg`: horizontal, on the right of the first screen
- `below-left.jpg`: vertical, the first photo after scrolling
- `below-right.jpg`: horizontal, the second photo after scrolling
- `about.jpg`: the About page

Each spot keeps its shape. If a photo doesn't match, the site crops it from the center, so crop it yourself first (vertical 2:3, horizontal 3:2) to control the framing.

### Send your changes live
1. Open **GitHub Desktop**. It lists everything you changed.
2. At the bottom left, type a short note in **Summary** (for example, "New couples photos").
3. Click **Commit to main**, then **Push origin** at the top.
4. In about 2 minutes your site updates. If you don't see the change, refresh with **Cmd + Shift + R**.

**From your phone:** on github.com, open a folder such as `photos/couples`, tap **Add file → Upload files**, choose photos, and tap **Commit changes**. Afterwards, click **Pull origin** in GitHub Desktop on your computer so your folder has those photos too. Renaming photos to reorder them is easiest in GitHub Desktop.

---

## If something looks wrong
- **The site didn't change:** open the **Actions** tab on github.com. A yellow dot means it's still working. Wait a minute and refresh.
- **Red ✗ in Actions:** click it, then click **build** to read the message. A photo that couldn't be opened is skipped with a note, so the rest of the site still publishes.
- **GitHub Desktop says "Pull" before you can push:** click **Pull origin**, then **Push origin**. This happens if you changed something on github.com.

---

## Changing the design or text
For new colors, fonts, layout or wording, open **EDITING-WITH-CLAUDE.md** in your website folder. It has a ready-made message to paste into Claude, along with your website folder, so Claude knows exactly how your site works.

## Optional: your own domain (like asbphotography.com)
Buy the domain from any registrar (Squarespace Domains, Namecheap, etc.). Then on github.com go to **Settings → Pages → Custom domain**, enter it, and follow GitHub's instructions for the DNS settings.
