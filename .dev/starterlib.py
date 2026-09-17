#!/usr/bin/env python3
"""Block markup for a starter's pages, built from the theme's own helpers.

A starter's pages are the theme's patterns with the starter's copy and
photographs in them. Rather than hand-write block markup -- the standing trap
that makes the editor offer to "recover" a block -- this borrows the generator
the theme itself uses, and swaps out only the three things that differ:

- text is plain, not a PHP translation call, because a starter's words are
  content, not code;
- an image is a placeholder the importer fills in, not a theme asset;
- a link is a placeholder too, so it points at the store being imported into.

Everything else -- what a section is, how a cover carries its scrim, which
attributes a block comment must repeat -- comes from the theme, so a starter
cannot drift from patterns that are already validated.
"""

import os
import sys

THEME_DEV = os.environ.get("TYCHE_THEME_DEV", os.path.expanduser("~/Fresh Projects/tyche-2/.dev"))
if not os.path.isdir(THEME_DEV):
    raise SystemExit("Cannot find the theme's .dev directory: %s" % THEME_DEV)
sys.path.insert(0, THEME_DEV)

import build_patterns as bp  # noqa: E402


# ---------------------------------------------------------------------------
# Placeholders, in place of the theme's PHP
# ---------------------------------------------------------------------------
def _plain(text):
    return text


def _image_url(slug):
    return "{{img:%s.webp}}" % slug


bp.t = _plain
bp.tk = _plain
bp.ta = _plain
bp.attr_t = _plain
bp.img = _image_url
bp.url = lambda page: "{{%s}}" % ("account" if page == "myaccount" else page)
bp.page_link = lambda slug: "{{page:%s}}" % slug
bp.category_link = lambda slug: "{{cat:%s}}" % slug
bp.sorted_link = lambda orderby: "{{shop}}"
bp.HOME = "{{home}}"
bp.BLOG = "{{page:journal}}"
bp.IF_WOO = ""
bp.END_IF = ""

# Re-export the pieces a starter composes with.
block = bp.block
group = bp.group
columns = bp.columns
column = bp.column
heading = bp.heading
para = bp.para
eyebrow = bp.eyebrow
button = bp.button
buttons = bp.buttons
check_list = bp.check_list
section = bp.section
section_head = bp.section_head
cover = bp.cover
icon = bp.icon
product_collection = bp.product_collection
SCRIM = bp.SCRIM
SCRIM_SIDE = bp.SCRIM_SIDE
SCRIM_TALL = bp.SCRIM_TALL


def image(slug, alt, ratio=None, cls=None, align=None):
    """An image the importer can attach to the media library.

    The theme's own images are files in the theme, so its patterns need no
    attachment ID. A starter's are real uploads, so the ID travels too: without
    it the editor treats the picture as somebody else's and offers to upload it.
    """
    data = {"id": "{{imgid:%s.webp}}" % slug, "sizeSlug": "large", "linkDestination": "none"}
    style = ""
    if ratio:
        data.update({"aspectRatio": ratio, "scale": "cover"})
        style = ' style="aspect-ratio:%s;object-fit:cover"' % ratio
    classes = ["wp-block-image", "size-large"]
    if align:
        data["align"] = align
        classes.append("align" + align)
    if cls:
        data["className"] = cls
        classes.append(cls)
    return ('<!-- wp:image%s -->\n<figure class="%s"><img src="%s" alt="%s" class="wp-image-{{imgid:%s.webp}}"%s/></figure>\n'
            '<!-- /wp:image -->' % (bp.attrs(data), bp._classes(*classes), _image_url(slug), alt, slug, style))


def paragraphs(*texts):
    """Plain paragraphs, for a product description or a journal post."""
    return "\n\n".join(para(text) for text in texts)


def rich(text):
    """A paragraph that carries inline markup such as <strong>."""
    return para(text)


def spec_rows(rows, title, kicker=None, bg="surface"):
    """Label and value rows: origin and roast here, materials or specs elsewhere."""
    lines = []
    for label, value in rows:
        lines.append(columns(
            column(para(label, cls="tyche-spec__label"), width="34%"),
            column(para(value, color="muted")),
            cls="tyche-spec__row", gap="40"))
    body = section_head(title, kicker=kicker) + "\n\n" + \
        group("\n".join(lines), cls="tyche-spec", align="wide", layout="default")
    return section(body, bg=bg)


def numbered_steps(items, title, kicker=None):
    """A real sequence: brewing, a routine, how an order is made."""
    cols = []
    for number, (step_title, note) in enumerate(items, start=1):
        cols.append(column("\n".join([
            para("%02d" % number, cls="tyche-step__number", size="small"),
            heading(step_title, level=3, size="x-large"),
            para(note, color="muted"),
        ])))
    body = section_head(title, kicker=kicker) + "\n\n" + \
        columns(*cols, cls="tyche-steps", align="wide", gap="50")
    return section(body, cls="tyche-steps-section")


def hero_split(eyebrow_text, title, lede, primary, secondary, photo, alt):
    """Text beside one photograph, for a store that opens on a single thing."""
    text = "\n".join([
        eyebrow(eyebrow_text),
        heading(title, level=1, size="colossal"),
        para(lede, size="large", color="muted"),
        buttons(button(primary[0], primary[1]),
                button(secondary[0], secondary[1], style="tyche-outline")),
    ])
    body = columns(
        column(group(text, layout="flex", orientation="vertical", gap="40"), valign="center"),
        column(image(photo, alt, ratio="1/1", cls="tyche-hero-split__image"), width="46%"),
        cls="tyche-hero-split", align="wide", gap="80", valign="center")
    return section(body, pad=("50", "70"))


def category_tiles(tiles, title, kicker=None, link=None):
    """Three or four photographs that lead into the catalogue."""
    cols = []
    for slug, name, note in tiles:
        inner = "\n".join([
            heading('<a href="{{cat:%s}}">%s</a>' % (slug, name), level=3, color="overlay",
                    size="xx-large", cls="tyche-tile__title"),
            para(note, color="overlay", size="small"),
        ])
        cols.append(column(cover(inner, "cat-" + slug, position="bottom left", ratio="4/5",
                                 cls="tyche-tile is-style-tyche-zoom", gradient=SCRIM)))
    head = section_head(title, kicker=kicker,
                        link_text=link[0] if link else None,
                        link_href=link[1] if link else None)
    return section(head + "\n\n" + columns(*cols, cls="tyche-tiles", align="wide", gap="40"),
                   cls="tyche-categories")


def product_row(collection, kicker, title, link_text, link_href, carousel=False, bg=None):
    """A row of the store's own products: the blocks choose them when the page renders."""
    body = section_head(title, kicker=kicker, link_text=link_text, link_href=link_href)
    body += "\n\n" + product_collection(collection, per_page=8 if carousel else 4, cols=4, carousel=carousel)
    return section(body, cls="tyche-product-row", bg=bg)


def story_split(kicker, title, lede, points, cta, photo, alt, flip=False):
    """A photograph beside the story, with a short list of what is true about it."""
    text = "\n".join([
        eyebrow(kicker),
        heading(title, level=2, size="huge"),
        para(lede, size="large", color="muted"),
        check_list(*points),
        buttons(button(cta[0], cta[1], style="tyche-outline")),
    ])
    picture = column(image(photo, alt, ratio="4/5", cls="tyche-story__image"), width="50%")
    words = column(group(text, layout="flex", orientation="vertical", gap="40"), valign="center")
    order = (words, picture) if flip else (picture, words)
    return section(columns(*order, cls="tyche-story", align="wide", gap="80", valign="center"), bg="surface")
