#!/usr/bin/env python3
"""Build the Stride starter: sneakers and streetwear, sold in drops.

    python3 .dev/stride.py

Where Roastery is a catalogue you buy from every week, Stride is a shop built
around a moment: one pair goes on sale on Saturday at ten. That is what it
exercises that the others do not -- a countdown, a release calendar, sizes that
run UK 6 to 12, and a catalogue where the interesting thing is often sold out.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, category_tiles, check_list, column, columns, cover, footer_part, group,
    header_part, heading, image, numbered_steps, para, paragraphs, product_row, section,
    section_head, spec_rows, story_split, cta, eyebrow, SCRIM_SIDE, SCRIM_TALL,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stride")

accordion = bp.accordion
page_intro = bp.page_intro

# The drop the store is built around. Relative, so an import is never counting
# down to a Saturday that has already been and gone.
DROP = "next saturday 10:00"

IMAGES = {
    "hero-1": "A skater standing in a graffiti-covered concrete underpass",
    "cat-sneakers": "White canvas shoes mounted in a row as shelves on a brick wall",
    "cat-apparel": "A folded cream cable-knit sweater and blue jeans on a white ground",
    "cat-accessories": "A pale grey leather backpack against stacked logs, beside legs in white sneakers",
    "story-1": "A skater in light-blue jeans standing on a plywood ramp against a brick wall",
    "drops-1": "A receding row of sneakers along a shelf edge, one red pair in focus",
    "drop-detail": "Legs in black jeans and white canvas sneakers standing on dark gravel",
    "drop-detail": "Legs in black jeans and white canvas sneakers standing on dark gravel",
    "about-1": "A long cast-concrete wall receding into shadow above a polished floor",
    "contact-1": "A woman walking away along a road bridge beside a tall chain-link fence",
    "size-1": "White sneakers seen from above on fan-patterned cobblestones",
    "journal-1": "Hands tying the lace of a white leather sneaker",
    "journal-2": "Looking down at black-and-white sneakers over the edge of a ledge",
    "journal-3": "A woman in a quilted jacket crouching to tie her running shoe",
    "canvas-low-white": "A pair of white canvas low-tops on cracked dark ground",
    "court-low-silver": "Metallic silver-blue leather low-tops shot from directly above",
    "mesh-runner-ice": "Pale blue mesh running shoes resting on a concrete ledge",
    "trail-runner-amber": "Orange and grey running shoes climbing wet concrete steps",
    "runner-2-blush": "A black running shoe with a pink sole, laces being pulled tight",
    "canvas-high-sage": "Sage-grey canvas high-tops with white laces, laid flat",
    "skate-low-black": "Black skate shoes seen from above on sunlit concrete",
    "rain-court-white": "White leather sneakers landing in a puddle, water flying",
    "hooded-jacket": "A person in a blue hooded jacket sitting on a concrete skatepark ledge",
    "cable-knit": "A folded cream cable-knit sweater on a white ground",
    "boxy-tee": "A navy top folded beside a black jacket, seen from above",
    "six-panel-cap": "A person in a six-panel cap seen from the side in low sun",
    "leather-backpack": "A pale grey leather backpack hanging against stacked logs",
    "skate-deck": "A skateboard with red wheels on pale wood, seen from above",
    "ribbed-socks": "Black sneakers and red ribbed socks on a skateboard at a skatepark",
}

CATEGORIES = [
    ("Sneakers", "sneakers", "Runners, courts and trail shoes, in UK 6 to 12."),
    ("Apparel", "apparel", "Heavyweight cotton, cut boxy, made to be worn out."),
    ("Accessories", "accessories", "Socks, laces, care kits and the bag to carry it in."),
]

POST_CATEGORIES = [
    ("Drops", "drops", "What is coming, and when."),
    ("Guides", "guides", "Sizing, care and keeping a pair alive."),
]

UK_SIZES = ["UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "UK 11", "UK 12"]
CLOTHING_SIZES = ["XS", "S", "M", "L", "XL"]
COLOURWAYS = ["Volt", "Black", "Bone", "Olive", "Navy", "White"]

# slug, name, price, sale, colourway, photo, days_ago, sold_out_sizes, short, long, spec rows
SNEAKERS = [
    ("canvas-low-white", "Canvas Low White", "95.00", "", "White", "canvas-low-white", 2, ["UK 6", "UK 12"],
     "Saturday's drop: the canvas low in undyed white. 120 pairs.",
     "Twelve-ounce canvas over a vulcanised sole, undyed so it takes the marks of wherever it goes. One hundred and twenty pairs, UK 6 to 12, and no restock.",
     [("Weight", "340 g in UK 9"), ("Upper", "12 oz undyed canvas"), ("Lining", "Cotton drill"),
      ("Outsole", "Vulcanised rubber"), ("Pairs", "120, then never again"), ("Sizes", "UK 6 to UK 12")]),
    ("court-low-silver", "Court Low Silver", "130.00", "", "Silver", "court-low-silver", 24, [],
     "Metallic leather, cut low, for people who do not want to blend in.",
     "A court shoe in mirrored leather that shifts from silver to blue depending on the light. The same last as the white court, with a padded collar and a stitched toe box.",
     [("Weight", "395 g in UK 9"), ("Upper", "Metallic leather"), ("Collar", "Padded"),
      ("Outsole", "Vulcanised rubber"), ("Sizes", "UK 6 to UK 12")]),
    ("mesh-runner-ice", "Mesh Runner Ice", "120.00", "", "Ice", "mesh-runner-ice", 38, ["UK 7"],
     "An engineered mesh runner in pale blue, built to breathe.",
     "Engineered mesh with no overlays, so there is nothing to rub, over a foam midsole with an 8 mm drop. The pale blue shows dirt, which is the trade for looking like this.",
     [("Weight", "265 g in UK 9"), ("Drop", "8 mm"), ("Upper", "Engineered mesh"),
      ("Midsole", "Supercritical foam"), ("Sizes", "UK 6 to UK 12")]),
    ("trail-runner-amber", "Trail Runner Amber", "165.00", "", "Amber", "trail-runner-amber", 52, ["UK 11"],
     "Orange, grippy, and happiest on wet ground.",
     "A trail shoe with 5 mm lugs and a rand around the toe, in an orange you can find again if you leave it in a hedge. Gusseted tongue, drainage at the arch.",
     [("Weight", "410 g in UK 9"), ("Drop", "6 mm"), ("Upper", "Ripstop with TPU rand"),
      ("Outsole", "Rubber, 5 mm lugs"), ("Sizes", "UK 6 to UK 12")]),
    ("runner-2-blush", "Runner 2 Blush", "140.00", "", "Blush", "runner-2-blush", 66, "sold out",
     "Drop 06. Gone in four minutes, and not coming back.",
     "Knitted upper, supercritical foam, 8 mm drop. The sole is the only colour on it, which is either the point or the problem depending on who you ask.",
     [("Weight", "255 g in UK 9"), ("Drop", "8 mm"), ("Upper", "Recycled knit"),
      ("Midsole", "Supercritical foam"), ("Sizes", "UK 6 to UK 12")]),
    ("canvas-high-sage", "Canvas High Sage", "105.00", "85.00", "Sage", "canvas-high-sage", 84, [],
     "The canvas shoe cut high, in washed sage.",
     "The same canvas and sole as the low, cut over the ankle, with a cotton lining and flat laces. Reduced while we clear the sage.",
     [("Weight", "395 g in UK 9"), ("Upper", "12 oz washed canvas"), ("Collar", "Padded"),
      ("Outsole", "Vulcanised rubber"), ("Sizes", "UK 6 to UK 12")]),
    ("skate-low-black", "Skate Low Black", "95.00", "", "Black", "skate-low-black", 104, ["UK 6"],
     "Flat sole, suede panels, double-stitched where it wears.",
     "A skate shoe that is honest about being one: a flat vulcanised sole for board feel, suede where the ollie goes, and stitching you can re-do rather than glue that cannot be.",
     [("Weight", "375 g in UK 9"), ("Upper", "Suede and canvas"),
      ("Outsole", "Vulcanised rubber, herringbone"), ("Sizes", "UK 6 to UK 12")]),
    ("rain-court-white", "Rain Court White", "135.00", "", "White", "rain-court-white", 130, ["UK 6", "UK 7"],
     "The white court, treated to survive a wet walk home.",
     "The court shoe with a taped seam and a water-repellent finish on the leather, for a city where the forecast is a suggestion. It will still get wet. It will just dry properly.",
     [("Weight", "410 g in UK 9"), ("Upper", "Treated full-grain leather"),
      ("Seams", "Taped"), ("Outsole", "Vulcanised rubber"), ("Sizes", "UK 6 to UK 12")]),
]

# slug, name, price, sale, photo, days_ago, sold_out_sizes, short, long
APPAREL = [
    ("hooded-jacket", "Hooded Jacket", "120.00", "", "hooded-jacket", 14, ["XS"],
     "A lined hooded jacket, cut long enough to sit down in.",
     "Water-repellent shell over a brushed lining, with a hood that stays up and a body long enough to cover you on a cold ledge."),
    ("cable-knit", "Cable Knit", "110.00", "", "cable-knit", 32, [],
     "Undyed lambswool, cabled front and back.",
     "Knitted in undyed lambswool so the colour is the fleece rather than a dye lot, with cables front and back and ribbing that holds its shape."),
    ("boxy-tee", "Boxy Tee", "45.00", "", "boxy-tee", 58, ["L", "XL"],
     "240 gsm cotton, cut wide, collar ribbed twice.",
     "Tubular knit with no side seams to twist in the wash, in a weight that hangs rather than clings. Pre-shrunk, which means what it says."),
]

ACCESSORIES = [
    ("six-panel-cap", "Six-panel Cap", "35.00", "", "six-panel-cap", 20,
     "Washed cotton, low crown, brass buckle.",
     "A cap that sits low rather than standing tall, in washed cotton with a brass buckle at the back."),
    ("leather-backpack", "Leather Backpack", "180.00", "", "leather-backpack", 44,
     "Vegetable-tanned leather, one main compartment, padded sleeve.",
     "Vegetable-tanned leather that darkens with use, with a padded sleeve for a 14-inch laptop and a roll top that buckles down."),
    ("skate-deck", "Skate Deck", "75.00", "", "skate-deck", 72,
     "Seven-ply maple, 8.25 inches, red wheels.",
     "A seven-ply maple deck at 8.25 inches with a mellow concave, set up with 52 mm wheels and sealed bearings. Ready to ride out of the box."),
    ("ribbed-socks", "Ribbed Socks, 3 pairs", "20.00", "", "ribbed-socks", 96,
     "Combed cotton crew socks in red, black and white.",
     "Combed cotton with a terry footbed and a rib that stays up through a session. Three pairs: red, black and white."),
]

REVIEWS = {
    "canvas-low-white": [
        ("Jonah K.", 5, "Got a pair in the last drop. The canvas is heavier than it looks and it has taken a winter without complaint."),
        ("Ade F.", 4, "Fit is true, but the canvas is stiff for the first week. Worth going up half a size if you are between."),
    ],
    "court-low-silver": [
        ("Nina P.", 5, "They catch the light in a way the photographs do not quite manage. Second pair."),
    ],
    "hooded-jacket": [
        ("Sam T.", 5, "Genuinely waterproof, and long enough to sit on a wet ledge in. It has not lost its shape."),
    ],
}


def variations(sizes, price, sale, sold_out):
    out = []
    for size_name in sizes:
        variation = {
            "attributes": {"uk-size" if size_name.startswith("UK") else "size": size_name},
            "regular_price": price,
            "stock_status": "outofstock" if size_name in sold_out else "instock",
        }
        if sale:
            variation["sale_price"] = sale
        out.append(variation)
    return out


def sneaker_products():
    products = []
    for slug, name, price, sale, colourway, photo, days, sold_out, short, long_text, spec in SNEAKERS:
        gone = "sold out" == sold_out
        products.append({
            "slug": slug,
            "name": name,
            "type": "variable",
            "sku": "ST-" + slug[:6].upper(),
            "short_description": short,
            "description": paragraphs(long_text) + "\n\n" + spec_list(spec),
            "categories": ["sneakers"],
            "featured": slug in ("canvas-low-white", "court-low-silver", "trail-runner-amber",
                                 "mesh-runner-ice", "canvas-high-sage"),
            "stock_status": "outofstock" if gone else "instock",
            "image": photo + ".webp",
            "days_ago": days,
            "attributes": [
                {"slug": "uk-size", "taxonomy": True, "options": UK_SIZES, "visible": True, "variation": True},
                {"slug": "colourway", "taxonomy": True, "options": [colourway], "visible": True, "variation": False},
            ],
            "variations": variations(UK_SIZES, price, sale, UK_SIZES if gone else sold_out),
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        })
    return products


def apparel_products():
    products = []
    for slug, name, price, sale, photo, days, sold_out, short, long_text in APPAREL:
        products.append({
            "slug": slug,
            "name": name,
            "type": "variable",
            "sku": "ST-" + slug[:6].upper(),
            "short_description": short,
            "description": paragraphs(long_text),
            "categories": ["apparel"],
            "featured": slug == "hooded-jacket",
            "stock_status": "instock",
            "image": photo + ".webp",
            "days_ago": days,
            "attributes": [
                {"slug": "size", "taxonomy": True, "options": CLOTHING_SIZES, "visible": True, "variation": True},
            ],
            "variations": variations(CLOTHING_SIZES, price, sale, sold_out),
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        })
    return products


def accessory_products():
    products = []
    for slug, name, price, sale, photo, days, short, long_text in ACCESSORIES:
        product = {
            "slug": slug,
            "name": name,
            "type": "simple",
            "sku": "ST-" + slug[:6].upper(),
            "regular_price": price,
            "short_description": short,
            "description": paragraphs(long_text),
            "categories": ["accessories"],
            "featured": slug == "leather-backpack",
            "stock_status": "outofstock" if slug == "shoe-care" else "instock",
            "image": photo + ".webp",
            "days_ago": days,
            "reviews": [],
        }
        if sale:
            product["sale_price"] = sale
        products.append(product)
    return products


def spec_list(rows):
    items = "\n".join("<li>%s: %s</li>" % (label, value) for label, value in rows)
    return '<!-- wp:list -->\n<ul class="wp-block-list">%s</ul>\n<!-- /wp:list -->' % items


def countdown(finished):
    """The drop countdown, from the companion plugin."""
    return bp.block("tyche-companion/countdown", {
        "date": "{{date:%s}}" % DROP,
        "finished": finished,
        "style": {"spacing": {"margin": {"top": "var:preset|spacing|20"}}},
    })


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def drop_hero():
    inner = "\n".join([
        eyebrow("Drop 07 &middot; Saturday, 10:00", color="overlay"),
        heading("Canvas Low White", level=1, size="colossal", color="overlay", cls="tyche-hero__title"),
        para("120 pairs. UK 6 to 12. One per customer, and no restock.", size="large", color="overlay"),
        countdown("The drop is open"),
        buttons(button("Set a reminder", "{{account}}", bg="overlay", color="dark"),
                button("See the release calendar", "{{page:drops}}", style="tyche-outline", color="overlay")),
    ])
    return cover(group(group(inner, layout="default", cls="tyche-hero__content"), align="wide", layout="default"),
                 "hero-1", min_height=82, unit="vh", position="center left", cls="tyche-hero",
                 align="full", gradient=SCRIM_SIDE)


DROP_STEPS = [
    ("Sign up", "An account takes a minute and it is the only way to be in the queue when the clock hits ten."),
    ("Set a reminder", "We email an hour before, and again at five minutes. No other email, ever."),
    ("Buy at 10:00", "The size list opens at ten exactly. One pair per customer, card ready."),
    ("Collect or post", "Free delivery over $90, or collect from the shop from noon the same day."),
]


def home():
    return "\n\n".join([
        drop_hero(),
        category_tiles(
            [("sneakers", "Sneakers", "Runners, courts and trail, UK 6 to 12"),
             ("apparel", "Apparel", "Heavyweight cotton, cut boxy"),
             ("accessories", "Accessories", "Socks, laces and the bag for them")],
            "Shop the shelf", kicker="In stock", link=("See everything", "{{shop}}")),
        product_row("new-arrivals", "Just in", "New this month", "Shop all new", "{{shop}}"),
        numbered_steps(DROP_STEPS, "How a drop works", kicker="Saturdays"),
        product_row("featured", "Always here", "The permanent collection", "Shop the shelf", "{{shop}}", carousel=True),
        spec_rows(
            [("Weight", "340 g in UK 9"), ("Upper", "12 oz undyed canvas"), ("Lining", "Cotton drill"),
             ("Outsole", "Vulcanised rubber"), ("Made in", "Portugal"), ("Pairs", "120, then never again")],
            "The drop, in numbers", kicker="Saturday at ten",
            photo="drop-detail", alt=IMAGES["drop-detail"]),
        story_split(
            "The shop",
            "One room, one wall of shoes",
            "We opened in 2018 with a shutter, a bench and eleven pairs. We still buy what we would wear ourselves, still sell one pair per customer on a drop, and still open the door at noon on Saturdays for whatever is left.",
            ["One pair per customer on every drop",
             "Free delivery over $90, free returns for 30 days",
             "Collect from the shop from noon on a drop day"],
            ("Read about the shop", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        journal_row(),
        newsletter(),
    ])


def journal_row():
    body = section_head("What's been written", kicker="Journal", link_text="Read the journal", link_href="{{page:journal}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def newsletter():
    return cta(
        "Drop alerts",
        "Know before the queue does",
        "One email an hour before a drop, one at five minutes, and nothing else. An account also keeps your size, which saves the thirty seconds that usually decide it.",
        ["An hour's notice, and again at five minutes",
         "Your size remembered at checkout",
         "Nothing else in your inbox, ever"],
        ("Create an account", "{{account}}"),
        ("See the calendar", "{{page:drops}}"),
        "drops-1")

def drops():
    calendar = [
        ("Drop 07 &middot; this Saturday", "Canvas Low White, 120 pairs, UK 6 to 12"),
        ("Drop 08 &middot; in two weeks", "Court Low Silver, second run, 200 pairs"),
        ("Drop 09 &middot; next month", "Hooded Jacket in olive, all sizes"),
        ("Drop 10 &middot; to be announced", "Something we are not allowed to name yet"),
    ]
    return "\n\n".join([
        section(page_intro("Drops", "What is coming, and when",
                           "A drop opens at ten on a Saturday and closes when it is gone. Here is the calendar as far as we know it."),
                pad=("70", "50")),
        section(group("\n".join([
            eyebrow("Next up"),
            heading("Canvas Low White", level=2, size="huge"),
            countdown("Drop 07 is open"),
            buttons(button("Set a reminder", "{{account}}")),
        ]), cls="tyche-drop-panel", align="wide", bg="surface", pad="50", layout="default", gap="30"),
                pad=("0", "60")),
        spec_rows(calendar, "The calendar", kicker="Next four"),
        numbered_steps(DROP_STEPS, "How a drop works", kicker="Saturdays"),
    ])


def size_guide():
    rows = [
        ("UK 6", "EU 39 &middot; US 7 &middot; 24.5 cm"),
        ("UK 7", "EU 40.5 &middot; US 8 &middot; 25.5 cm"),
        ("UK 8", "EU 42 &middot; US 9 &middot; 26.5 cm"),
        ("UK 9", "EU 43 &middot; US 10 &middot; 27.5 cm"),
        ("UK 10", "EU 44.5 &middot; US 11 &middot; 28.5 cm"),
        ("UK 11", "EU 46 &middot; US 12 &middot; 29.5 cm"),
        ("UK 12", "EU 47 &middot; US 13 &middot; 30.5 cm"),
    ]
    clothing = [
        ("XS", "Chest 86 to 91 cm"),
        ("S", "Chest 91 to 97 cm"),
        ("M", "Chest 97 to 102 cm"),
        ("L", "Chest 102 to 107 cm"),
        ("XL", "Chest 107 to 112 cm"),
    ]
    return "\n\n".join([
        section(page_intro("Size guide", "Measure once, at the end of the day",
                           "Feet swell. Measure in the evening, standing, with the socks you will wear."),
                pad=("70", "50")),
        section(image("size-1", IMAGES["size-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        spec_rows(rows, "Shoes", kicker="UK, EU and US", bg=None),
        spec_rows(clothing, "Apparel", kicker="Chest measurement"),
        section(group("\n".join([
            heading("Between sizes?", level=2, align="center"),
            para("Canvas is stiff for a week and then true. The Court is true from the box. The mesh runner comes up small: go up half a size. Apparel is cut boxy, so take your usual size unless you want it bigger.",
                 align="center", color="muted"),
            buttons(button("Ask us before you buy", "{{page:contact}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30")),
    ])


def about():
    return "\n\n".join([
        section(page_intro("The shop", "Eleven pairs and a shutter",
                           "We started in 2018 selling what we wanted to wear, and the shop has stayed that size on purpose."),
                pad=("70", "50")),
        section(image("about-1", IMAGES["about-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        story_split(
            "2018",
            "We buy what we would wear",
            "There is no buying team. Two of us choose, and if neither would wear it, it does not go on the wall. That is why the shelf is short and why the same four shoes keep coming back.",
            ["One pair per customer on a drop, enforced at checkout",
             "No resale bots: accounts older than a week only",
             "Everything photographed on our own feet"],
            ("Shop the shelf", "{{shop}}"),
            "story-1", IMAGES["story-1"]),
        numbered_steps([
            ("Choose", "Two of us, a sample, and a rule: would we wear it out on a Tuesday?"),
            ("Order", "Small runs, paid up front, which is why a drop is 120 pairs and not 1,200."),
            ("Drop", "Saturday at ten, one pair per customer, no restock on a colourway."),
            ("Keep", "Free repairs on soles and eyelets for the first year."),
        ], "How the shelf is chosen", kicker="Four steps"),
    ])


def contact():
    details = columns(*[
        column(group("\n".join([
            bp.icon("tyche/" + name, cls="tyche-icon tyche-icon--large"),
            heading(title, level=2, size="large", family="archivo", cls="tyche-usp__title"),
            para(body, color="muted"),
        ]), layout="flex", orientation="vertical", gap="20", cls="tyche-usp"))
        for name, title, body in (
            ("headset", "Orders and sizing", "hello@example.com<br>We answer the same day, including Saturdays."),
            ("clock", "The shop", "Thursday to Saturday, 11am to 6pm<br>Drop days: doors at noon"),
            ("map-pin", "Where", "Unit 4, Arch Row<br>Under the railway, next to the tyre place"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Come in on a Saturday",
                           "Whatever is left after a drop goes on the wall at noon. Bring the pair you are replacing and we will take them for recycling."),
                pad=("70", "50")),
        section(details, pad=("0", "60")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Sizing, drops, delivery and returns are all covered in the help pages.", align="center", color="muted"),
            buttons(button("Read the FAQ", "{{page:faq}}", style="tyche-outline"),
                    button("Size guide", "{{page:size-guide}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Drops", (
            ("How do I get a pair?", "Have an account before the day, be on the site at ten, and choose your size. It is first come, and a drop of 120 pairs usually lasts under four minutes."),
            ("One pair per customer: how is that enforced?", "By account and by card. A second order on the same drop is refunded, and repeat offenders lose the account."),
            ("Will a colourway come back?", "No. A drop colourway is made once. The permanent colours, like Runner 2 Black, are always here."),
        )),
        ("Sizing", (
            ("Do your shoes fit true?", "The Court is true from the box. Canvas is stiff for a week, then true. The mesh runner comes up small: go up half a size. Full measurements are on the size guide."),
            ("Can I exchange a size?", "Yes, within 30 days, unworn, and we pay the postage both ways."),
        )),
        ("Delivery and returns", (
            ("When does it arrive?", "Orders before 2pm go out the same working day. Free over $90, otherwise $6."),
            ("Can I collect?", "From the shop, from noon on a drop day, or any opening hour after that."),
        )),
        ("Care", (
            ("How do I clean canvas?", "Cool water, a soft brush, no machine. The care kit has a pH-neutral cleaner that will not strip the dye."),
            ("Do you repair?", "Soles and eyelets, free in the first year. Bring them in or post them."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "Drops, sizing, delivery and keeping a pair alive."), pad=("70", "50")),
        section(body, pad=("0", "80")),
    ])


def delivery():
    rows = [
        ("Standard delivery", "$6, two to three working days"),
        ("Free delivery", "On orders over $90"),
        ("Next day", "$12, ordered before 2pm on a working day"),
        ("Collection", "Free, from the shop, noon on a drop day"),
        ("Returns", "Free for 30 days, unworn, in the box"),
    ]
    return "\n\n".join([
        section(page_intro("Delivery and returns", "How it gets to you, and back",
                           "Orders before 2pm go the same day. Drop orders go out on the Monday."),
                pad=("70", "50")),
        spec_rows(rows, "Delivery", kicker="What it costs", bg=None),
        section(group("\n\n".join([
            heading("Returns", level=2),
            para("Thirty days, unworn, in the original box, with the spare laces still in it. Start a return from your account and we send a label. Refunds land within three working days of the parcel reaching us.",
                 color="muted"),
            heading("Drops", level=2),
            para("A drop pair can be returned like anything else, but it goes back on sale rather than being restocked to you, so an exchange for a different size is not always possible.",
                 color="muted"),
            heading("Repairs", level=2),
            para("Soles and eyelets are repaired free in the first year. Beyond that we charge parts only. Bring them to the shop or post them with a note.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("drops", "Drops", drops, "page-no-title"),
    ("size-guide", "Size guide", size_guide, "page-no-title"),
    ("about", "The shop", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("delivery-returns", "Delivery and returns", delivery, "page-no-title"),
    ("journal", "Journal", None, ""),
]

POSTS = [
    ("what-makes-a-drop-sell-out", "What makes a drop sell out in four minutes", "drops", "journal-1", 4, [
        "Drop 06 went in three minutes and fifty seconds. People ask whether that is engineered. It is not, but it is not an accident either.",
        "A drop is 120 pairs because that is what we can pay for up front. Spread across seven sizes, that is seventeen pairs in the middle sizes and six at each end. Seventeen pairs of anything go quickly when four thousand people have an alert set.",
        "What we can do is make it fair: one pair per account, accounts older than a week, and a size list that opens at exactly ten rather than trickling. The rest is arithmetic.",
    ]),
    ("how-to-measure-your-feet", "How to measure your feet properly", "guides", "journal-2", 18, [
        "Most people buy shoes half a size too small, because they measured in the morning, sitting down, in thin socks.",
        "Do it in the evening, standing, with the socks you will actually wear. Put your heel against a wall, mark the longest toe on a sheet of paper, and measure from the wall to the mark. Do both feet: one is usually longer, and that is the one that decides.",
        "Then add about a centimetre. That gap is what stops your toes hitting the front going downhill, and it is the difference between a shoe you wear and one you keep meaning to sell.",
    ]),
    ("keeping-white-leather-white", "Keeping white leather white", "guides", "journal-3", 34, [
        "A white leather court shoe looks best on day one and on day four hundred. The bit in between is where people give up.",
        "Wipe them after each wear with a dry cloth: most marks are dust that has not yet been walked in. Once a month, warm water, a soft brush and a pH-neutral cleaner, then let them dry away from a radiator.",
        "Do not put them in a machine. The drum breaks down the glue on the sole, and a pair that would have lasted two years starts gaping at the toe in six months.",
    ]),
]

MENU = [
    ("Drops", "{{page:drops}}", "page:drops"),
    ("Sneakers", "{{cat:sneakers}}", "cat:sneakers"),
    ("Apparel", "{{cat:apparel}}", "cat:apparel"),
    ("Accessories", "{{cat:accessories}}", "cat:accessories"),
    ("Size guide", "{{page:size-guide}}", "page:size-guide"),
    ("Journal", "{{page:journal}}", "page:journal"),
]


def menu_markup():
    links = []
    for label, href, target in MENU:
        data = {"label": label, "url": href, "isTopLevelLink": True}
        if target and target.startswith("cat:"):
            data.update({"kind": "taxonomy", "type": "product_cat", "id": "{{catid:%s}}" % target[4:]})
        elif target and target.startswith("page:"):
            data.update({"kind": "post-type", "type": "page", "id": "{{pageid:%s}}" % target[5:]})
        links.append(bp.block("navigation-link", data))
    return "\n".join(links)


def parts():
    return [
        {
            "slug": "header",
            "title": "Header",
            "area": "header",
            "content": header_part("Drop 07 opens Saturday at 10:00 &middot; free delivery over $90",
                                   "See the calendar", "{{page:drops}}", layout="header-left-no-announcement"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "A one-room shop under the railway. Drops on Saturday at ten, one pair per customer, and a wall of what is left.",
                [
                    ("Shop", [("Sneakers", "{{cat:sneakers}}"), ("Apparel", "{{cat:apparel}}"),
                              ("Accessories", "{{cat:accessories}}"), ("Everything", "{{shop}}")]),
                    ("Help", [("Size guide", "{{page:size-guide}}"), ("Delivery and returns", "{{page:delivery-returns}}"),
                              ("FAQ", "{{page:faq}}"), ("My account", "{{account}}")]),
                    ("Shop news", [("Drops", "{{page:drops}}"), ("Journal", "{{page:journal}}"),
                                   ("The shop", "{{page:about}}"), ("Contact", "{{page:contact}}")]),
                ],
                legal="One pair per customer. No resale."),
        },
    ]


def write(name, data):
    path = os.path.join(OUT, name)
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent="\t", ensure_ascii=False)
        handle.write("\n")
    return name


# The line under a page's title. The journal's is the store's own, because the
# theme cannot know what this shop writes about.
INTROS = {
    "journal": "What is dropping, how it fits, and how to keep it looking like it did in the box.",
}


def main():
    pages = []
    for slug, title, builder, template in PAGES:
        page = {"slug": slug, "title": title, "content": builder() if builder else ""}
        if slug in INTROS:
            page["excerpt"] = INTROS[slug]
        if template:
            page["template"] = template
        pages.append(page)

    posts = [{
        "slug": slug,
        "title": title,
        "content": paragraphs(*body),
        "excerpt": body[0],
        "categories": [category],
        "image": photo + ".webp",
        "days_ago": days,
    } for slug, title, category, photo, days, body in POSTS]

    terms = {
        "product_cat": [{"name": n, "slug": s, "description": d} for n, s, d in CATEGORIES],
        "category": [{"name": n, "slug": s, "description": d} for n, s, d in POST_CATEGORIES],
        "attributes": [
            {"name": "UK size", "slug": "uk-size", "type": "select", "order_by": "menu_order", "terms": UK_SIZES},
            {"name": "Size", "slug": "size", "type": "select", "order_by": "menu_order", "terms": CLOTHING_SIZES},
            {"name": "Colourway", "slug": "colourway", "type": "select", "order_by": "name", "terms": COLOURWAYS},
        ],
    }

    products = sneaker_products() + apparel_products() + accessory_products()

    manifest = {
        "schema": 1,
        "slug": "stride",
        "theme": {"slug": "tyche", "style": ["Stride"]},
        "settings": {
            "title": "Stride",
            "tagline": "Drops on Saturday at ten",
            "front_page": "home",
            "posts_page": "journal",
            "currency": "USD",
            "country": "US:NY",
            "shipping": {"country": "US", "flat_rate": "6.00", "free_over": "90"},
        },
        "counts": {"products": len(products), "pages": len(pages) - 1, "posts": len(posts), "images": len(IMAGES)},
    }

    written = [
        write("manifest.json", manifest),
        write("terms.json", terms),
        write("products.json", products),
        write("pages.json", pages),
        write("posts.json", posts),
        write("menus.json", [{"slug": "primary", "title": "Primary", "content": menu_markup()}]),
        write("parts.json", parts()),
        write("images.json", [{"file": slug + ".webp", "alt": alt} for slug, alt in sorted(IMAGES.items())]),
    ]

    variation_count = sum(len(p.get("variations", [])) for p in products)
    print("  %d products (%d variations), %d pages, %d posts, %d images"
          % (len(products), variation_count, len(pages), len(posts), len(IMAGES)))
    print("  " + ", ".join(written))


if __name__ == "__main__":
    main()
