#!/usr/bin/env python3
"""Build the Verdant starter: houseplants and the pots they go in.

    python3 .dev/verdant.py

People buy a plant for a place -- a dark corner, a bright sill, a flat with a
cat in it -- so this shop is organised by conditions rather than by species.
That is what it exercises that the others do not: attributes a shopper filters
by (light, pet safety, size) rather than ones they pick a variation from, and a
catalogue where the useful information is care rather than specification.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, care_cards, check_list, column, columns, cover, cta, footer_part, group,
    header_part, heading, image, numbered_steps, para, paragraphs, product_row, section,
    section_head, spec_rows, story_split, tiles_hero, eyebrow,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "verdant")

accordion = bp.accordion
page_intro = bp.page_intro

IMAGES = {
    "cat-bright": "Two small terracotta wall pots of herbs on a sunlit cream wall",
    "cat-medium": "A shelf of trailing plants above a bed against an exposed brick wall",
    "cat-low": "A leafy plant beside a tall window in a concrete-walled room",
    "story-1": "Seedlings in small labelled cups in a row on a dark blue shelf",
    "care-1": "A single monstera leaf laid flat on a pale grey surface",
    "promo-1": "The inside of a glasshouse, with raised beds of cacti either side",
    "contact-1": "A plant shop seen from the stairs, plants along the sill and shelves",
    "about-1": "A path through a conservatory dense with ferns and palms",
    "repot-1": "A seedling with two pale leaves rising from dark crumbly soil",
    "journal-1": "Two potted grasses on a sunlit windowsill in front of an open window",
    "journal-2": "Two hands holding a small white pot of greenery",
    "journal-3": "An old glasshouse with a large agave behind a weathered bench",
    "aloe": "An aloe with thick blue-green leaves in a pale cork-textured pot",
    "haworthia": "A dark-striped haworthia in a plain white square pot",
    "echeveria": "A pale grey-lilac echeveria rosette photographed close on a white ledge",
    "spider-plant": "A spider plant with arching variegated leaves in a dark woven basket",
    "boston-fern": "A bushy green fern in a white pot against a pale wall",
    "hanging-fern": "A trailing fern spilling from a small hanging basket on fine chains",
    "fittonia": "A fittonia with white-veined leaves in a white ribbed pot",
    "pothos-globe": "A rooted pothos cutting in a round glass globe on a wooden stand",
    "philodendron": "A trailing philodendron with dark leaves in a woven basket",
    "barrel-cactus": "A small barrel cactus in a chalky cream glazed pot",
    "column-cactus": "A tall slim columnar cactus against a pale concrete wall",
    "bunny-ear-cactus": "A bunny-ear cactus in a small white pot on a pale ledge",
    "terracotta-pot": "A small cactus in a terracotta pot against a plain cream wall",
    "stoneware-pot": "Two small speckled stoneware pots beside a chipped white bowl",
    "hanging-planter": "A white hanging planter of trailing greenery on a long cord",
    "potting-trowel": "A garden trowel loaded with dark potting soil beside spilled compost",
    "potting-mix": "The rim of a terracotta pot filled with dark potting soil",
    "glass-vases": "Slender cuttings standing in two clear glass vases against a pale wall",
}

CATEGORIES = [
    ("Bright light", "bright", "For a south-facing sill or a metre from any big window."),
    ("Medium light", "medium", "The middle of most rooms: bright, but out of direct sun."),
    ("Low light", "low", "North-facing rooms, hallways and the corner nobody plants."),
    ("Pots", "pots", "Terracotta, stoneware, hanging planters and propagation glass."),
    ("Care", "care", "Peat-free compost and the one trowel worth owning."),
]

POST_CATEGORIES = [
    ("Plant care", "plant-care", "Watering, light and what to do when it sulks."),
    ("From the nursery", "from-the-nursery", "What has just come in, and what it needs."),
]

POT_SIZES = ["12 cm", "17 cm", "22 cm"]
LIGHT_LEVELS = ["Bright", "Medium", "Low"]
PET_SAFE = ["Pet safe", "Keep away from pets"]

# slug, name, category, price by pot size, photo, days_ago, light, pet, sold out sizes,
# short, long, care rows
PLANTS = [
    ("spider-plant", "Spider Plant", "medium", ("16.00", "24.00", "32.00"), "spider-plant", 3,
     "Medium", "Pet safe", [],
     "Pet safe, nearly indestructible, and gives you free plants all summer.",
     "Arching striped leaves and runners that make babies you can pot on. It copes with most light, most watering habits and most rooms, which is why it has been in every kitchen since 1974.",
     [("Light", "Bright to medium, indirect"), ("Water", "Weekly in summer, less in winter"),
      ("Pets", "Safe"), ("Grows to", "50 cm, plus runners"), ("Difficulty", "Very easy")]),
    ("boston-fern", "Boston Fern", "medium", ("22.00", "30.00", "42.00"), "boston-fern", 8,
     "Medium", "Pet safe", ["22 cm"],
     "Pet safe, soft, and the best plant for a steamy bathroom.",
     "It wants humidity more than it wants light, which makes a bathroom or a kitchen its natural home. Crisp brown fronds mean the air is too dry rather than the soil.",
     [("Light", "Medium, indirect"), ("Water", "Keep just moist, never dry"),
      ("Pets", "Safe"), ("Grows to", "60 cm across"), ("Difficulty", "Easy")]),
    ("aloe", "Aloe Vera", "bright", ("14.00", "20.00", "28.00"), "aloe", 14,
     "Bright", "Keep away from pets", [],
     "Wants a sunny sill and to be forgotten between waterings.",
     "A succulent, so the usual rules invert: full sun, gritty compost, and a soak only once the soil is dry all the way through. Overwatering is the one thing it will not forgive.",
     [("Light", "Direct sun"), ("Water", "Every three to four weeks, soak and drain"),
      ("Pets", "Mildly toxic if chewed"), ("Grows to", "50 cm"), ("Difficulty", "Very easy")]),
    ("pothos-globe", "Pothos in Glass", "low", ("18.00", "26.00", "34.00"), "pothos-globe", 20,
     "Low", "Keep away from pets", [],
     "A rooted cutting in a glass globe: no compost, no repotting, no mess.",
     "Pothos roots happily in water and will live in it for years. Change the water every fortnight, add a drop of feed a month, and pot it into compost whenever you feel like it.",
     [("Light", "Low to bright, indirect"), ("Water", "Change the water fortnightly"),
      ("Pets", "Mildly toxic if chewed"), ("Trails to", "1 m"), ("Difficulty", "Very easy")]),
    ("philodendron", "Trailing Philodendron", "low", ("24.00", "34.00", "46.00"), "philodendron", 27,
     "Low", "Keep away from pets", [],
     "Dark heart-shaped leaves that trail a metre from a shelf in shade.",
     "One of the few plants that genuinely grows in a dim room rather than merely surviving there. Pinch the tips out twice a year and it thickens instead of going leggy.",
     [("Light", "Low to medium, indirect"), ("Water", "When the top 5 cm is dry"),
      ("Pets", "Toxic if chewed"), ("Trails to", "1.5 m"), ("Difficulty", "Easy")]),
    ("fittonia", "Fittonia", "medium", ("12.00", "18.00", "24.00"), "fittonia", 34,
     "Medium", "Pet safe", [],
     "Pet safe, palm-sized, and faints when thirsty so you always know.",
     "White veins on deep green, and a talent for collapsing flat when it wants water then standing back up within an hour. Small enough for a desk, and happiest in a terrarium.",
     [("Light", "Medium, indirect"), ("Water", "When it flops, about twice a week"),
      ("Pets", "Safe"), ("Grows to", "20 cm"), ("Difficulty", "Easy")]),
    ("hanging-fern", "Hanging Fern", "medium", ("28.00", "38.00", "52.00"), "hanging-fern", 42,
     "Medium", "Pet safe", ["12 cm"],
     "Pet safe, and the right plant for the corner above a bath.",
     "Hung on fine chains with a sealed liner, so it can be watered where it hangs. Like all ferns it wants humidity, which is why it does well where other plants sulk.",
     [("Light", "Medium, indirect"), ("Water", "Twice a week, keep just moist"),
      ("Pets", "Safe"), ("Trails to", "60 cm"), ("Difficulty", "Easy")]),
    ("echeveria", "Echeveria", "bright", ("11.00", "16.00", "22.00"), "echeveria", 50,
     "Bright", "Pet safe", [],
     "Pet safe, the size of a teacup, and turns pink in enough sun.",
     "A rosette succulent that colours up at the edges in bright light and stays grey-green in shade. Gritty compost, a soak once it is dry, and nothing at all in midwinter.",
     [("Light", "Direct sun"), ("Water", "Every three weeks, soak and drain"),
      ("Pets", "Safe"), ("Grows to", "12 cm across"), ("Difficulty", "Very easy")]),
    ("haworthia", "Haworthia Zebra", "bright", ("13.00", "18.00", "25.00"), "haworthia", 58,
     "Bright", "Pet safe", [],
     "Pet safe, striped white, and happy on a desk under a lamp.",
     "Tougher than it looks and tolerant of less light than most succulents, which makes it the one that survives an office. The white stripes are raised, not painted.",
     [("Light", "Bright, indirect to direct"), ("Water", "Every three weeks"),
      ("Pets", "Safe"), ("Grows to", "15 cm"), ("Difficulty", "Very easy")]),
    ("barrel-cactus", "Barrel Cactus", "bright", ("15.00", "22.00", "30.00"), "barrel-cactus", 66,
     "Bright", "Keep away from pets", ["12 cm"],
     "Round, ribbed and spiny: a sill plant for a very sunny window.",
     "Slow enough that the one you buy is roughly the one you keep. Full sun, gritty compost, and nothing to drink between November and February.",
     [("Light", "Direct sun"), ("Water", "Monthly in summer, none in winter"),
      ("Pets", "Spines rather than poison"), ("Grows to", "25 cm"), ("Difficulty", "Very easy")]),
    ("column-cactus", "Column Cactus", "bright", ("26.00", "36.00", "48.00"), "column-cactus", 74,
     "Bright", "Keep away from pets", [],
     "A tall, slim column for a corner that gets real sun.",
     "Architectural, and grows about five centimetres a year, so it holds its shape for a decade. Give it the brightest spot you have and keep it dry in winter.",
     [("Light", "Direct sun"), ("Water", "Monthly in summer, none in winter"),
      ("Pets", "Spines rather than poison"), ("Grows to", "1 m, slowly"), ("Difficulty", "Very easy")]),
    ("bunny-ear-cactus", "Bunny Ear Cactus", "bright", ("14.00", "20.00", "27.00"), "bunny-ear-cactus", 82,
     "Bright", "Keep away from pets", [],
     "Pads like ears, and fine bristles that get everywhere: handle with a cloth.",
     "Charming and deceptively unfriendly: the tufts are glochids, which come off at a touch and are miserable to remove. Beautiful on a high sill, wrong at a toddler's height.",
     [("Light", "Direct sun"), ("Water", "Monthly in summer, none in winter"),
      ("Pets", "Bristles: keep out of reach"), ("Grows to", "40 cm"), ("Difficulty", "Very easy")]),
]

# slug, name, category, price, sale, photo, days_ago, short, long
GOODS = [
    ("terracotta-pot", "Terracotta Pot", "pots", "14.00", "", "terracotta-pot", 26,
     "Unglazed terracotta with a drainage hole and a matching saucer.",
     "Unglazed clay breathes, which is why terracotta forgives a heavy hand with the watering can. Comes with a saucer, in the same three sizes as the plants."),
    ("stoneware-pot", "Stoneware Pot", "pots", "28.00", "22.00", "stoneware-pot", 41,
     "Speckled stoneware with a matte glaze, glazed inside.",
     "Thrown stoneware with a soft matte glaze and a sealed interior, so it holds water rather than marking a shelf. Reduced while we clear the sand colourway."),
    ("hanging-planter", "Hanging Planter", "pots", "34.00", "", "hanging-planter", 58,
     "A glazed pot on a long cord, for trailing plants.",
     "A shallow glazed pot hung on a cotton cord from a brass ring, with a sealed liner so it can be watered where it hangs."),
    ("glass-vases", "Propagation Vases, 2", "pots", "24.00", "", "glass-vases", 69,
     "Two slim glass vases for rooting cuttings on a sill.",
     "Hand-blown glass narrow enough to hold a single cutting upright, so you can watch the roots come. Two, because one cutting is never one cutting."),
    ("potting-trowel", "Potting Trowel", "care", "18.00", "", "potting-trowel", 76,
     "A narrow steel trowel sized for pots rather than borders.",
     "Narrow enough to work around a rootball without wrecking it, with a hardwood handle and a steel blade that will outlast the plants."),
    ("potting-mix", "Potting Mix, 10 L", "care", "12.00", "", "potting-mix", 92,
     "Peat-free compost with bark and perlite, for houseplants.",
     "Peat-free, with bark for structure and perlite for drainage, mixed for pots rather than borders. Ten litres repots about four medium plants."),
]

REVIEWS = {
    "spider-plant": [
        ("Priya N.", 5, "Arrived better packed than anything I have ordered, and it has not sulked for a day."),
        ("Cal R.", 4, "Bigger than I expected for the 17 cm, which is a good problem. It has thrown out two runners already."),
    ],
    "philodendron": [
        ("Dee M.", 5, "In the darkest corner of a north-facing flat for four months and it has grown half a metre."),
    ],
    "potting-trowel": [
        ("Tom H.", 5, "Narrow enough to get around a rootball without hacking at it. Should have bought one years ago."),
    ],
}


def spec_list(rows):
    items = "\n".join("<li>%s: %s</li>" % (label, value) for label, value in rows)
    return '<!-- wp:list -->\n<ul class="wp-block-list">%s</ul>\n<!-- /wp:list -->' % items


def plant_products():
    products = []
    for (slug, name, category, prices, photo, days, light, pet, sold_out,
         short, long_text, care) in PLANTS:
        variations = []
        for size, price in zip(POT_SIZES, prices):
            variations.append({
                "attributes": {"pot-size": size},
                "regular_price": price,
                "stock_status": "outofstock" if size in sold_out else "instock",
            })
        products.append({
            "slug": slug,
            "name": name,
            "type": "variable",
            "sku": "VE-" + slug[:6].upper(),
            "short_description": short,
            "description": paragraphs(long_text) + "\n\n" + spec_list(care),
            "categories": [category],
            "featured": slug in ("spider-plant", "pothos-globe", "philodendron", "haworthia",
                                 "aloe", "echeveria"),
            "stock_status": "instock",
            "image": photo + ".webp",
            "days_ago": days,
            "attributes": [
                {"slug": "pot-size", "taxonomy": True, "options": POT_SIZES, "visible": True, "variation": True},
                {"slug": "light", "taxonomy": True, "options": [light], "visible": True, "variation": False},
                {"slug": "pets", "taxonomy": True, "options": [pet], "visible": True, "variation": False},
            ],
            "variations": variations,
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        })
    return products


def goods_products():
    products = []
    for slug, name, category, price, sale, photo, days, short, long_text in GOODS:
        product = {
            "slug": slug,
            "name": name,
            "type": "simple",
            "sku": "VE-" + slug[:6].upper(),
            "regular_price": price,
            "short_description": short,
            "description": paragraphs(long_text),
            "categories": [category],
            "featured": False,
            "stock_status": "outofstock" if slug == "hanging-planter" else "instock",
            "image": photo + ".webp",
            "days_ago": days,
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        }
        if sale:
            product["sale_price"] = sale
        products.append(product)
    return products


CARE_CARDS = [
    ("sun", "Light, honestly described",
     "Every plant is filed by the light it actually needs, not the light it will tolerate for a month before it gives up."),
    ("droplet", "Water on a schedule you can keep",
     "The card in the box says how often, in weeks, for the room you bought it for. No misting rituals."),
    ("paw", "Pet safe, marked plainly",
     "Filter the shop to what is safe around a cat or a dog. The rest carry a warning on the label."),
]

REPOT_STEPS = [
    ("Wait for roots", "Repot when roots show through the drainage holes, not on a calendar. Most plants want it every second spring."),
    ("Go up one size", "12 cm to 17 cm, not 12 cm to 22 cm. A pot too large holds water the roots cannot reach and rots them."),
    ("Keep the depth", "Same soil line as before. Burying the stem is the commonest way to lose a plant to a repot."),
    ("Water, then wait", "Water it in, then leave it a fortnight before feeding. New compost has everything it needs."),
]


def home():
    return "\n\n".join([
        tiles_hero(
            "Plants for the room you actually have",
            "Find the plant for your light",
            "Filed by the light they need rather than how they look on a shelf, with a care card in every box and a first-month guarantee.",
            ("Shop all plants", "{{shop}}"),
            ("Read the care guide", "{{page:plant-care}}"),
            [("bright", "Bright light", "A sunny sill, or a metre from a big window"),
             ("medium", "Medium light", "The middle of most rooms, out of direct sun"),
             ("low", "Low light", "North-facing rooms, hallways, dark corners")]),
        product_row("new-arrivals", "Just in", "New this month", "Shop all plants", "{{shop}}"),
        care_cards(CARE_CARDS, "What you get with every plant", kicker="The basics", bg="surface"),
        product_row("featured", "Hard to kill", "Plants that forgive you", "Shop the easy ones", "{{shop}}", carousel=True),
        spec_rows(
            [("Light", "Bright to medium, indirect"), ("Water", "Weekly in summer, less in winter"),
             ("Pets", "Safe around cats and dogs"), ("Grows to", "50 cm, plus runners"),
             ("Pot sizes", "12, 17 and 22 cm"), ("Difficulty", "Very easy")],
            "Spider plant, in short", kicker="This month's plant",
            photo="spider-plant", alt=IMAGES["spider-plant"]),
        story_split(
            "The nursery",
            "Grown for four months before we sell them",
            "We buy plugs and grow them on in our own glasshouse, which is why a plant from here does not sulk for a month when it reaches you: it has already been in a pot, in British light, through a winter.",
            ["Grown on for at least four months before sale",
             "Peat-free compost in every pot",
             "First month guaranteed: if it fails, we replace it"],
            ("Read about the nursery", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        numbered_steps(REPOT_STEPS, "Repotting, in four steps", kicker="Plant care"),
        journal_row(),
        cta(
            "The first month",
            "If it dies, we replace it",
            "Plants fail in the first month for reasons that are usually ours: a bad batch, a cold van, a week on a doormat. Tell us within thirty days and the next one is free.",
            ["Thirty days on every plant",
             "A care card in the box, written for your room",
             "Advice by email from the people who grew it"],
            ("Create an account", "{{account}}"),
            ("Read the care guide", "{{page:plant-care}}"),
            "promo-1"),
    ])


def journal_row():
    body = section_head("From the nursery", kicker="Journal", link_text="Read the journal", link_href="{{page:journal}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def plant_care():
    watering = [
        ("Spider plant, philodendron", "When the top 5 cm is dry, about weekly in summer"),
        ("Cacti and succulents", "Every three to four weeks, none in midwinter"),
        ("Ferns and fittonia", "Keep just moist, never let them dry out"),
        ("Aloe, echeveria, haworthia", "Soak and drain, every three weeks"),
        ("Every plant, in winter", "Roughly half as often as summer"),
    ]
    return "\n\n".join([
        section(page_intro("Plant care", "Light first, then water",
                           "Nearly every houseplant that dies indoors is either in the wrong light or being watered on a schedule that ignores the season."),
                pad=("70", "50")),
        section(image("care-1", IMAGES["care-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        care_cards(CARE_CARDS, "How we file them", kicker="Light"),
        spec_rows(watering, "How often to water", kicker="A rough guide", photo="journal-1", alt=IMAGES["journal-1"]),
        numbered_steps(REPOT_STEPS, "Repotting, in four steps", kicker="Every second spring"),
        section(group("\n".join([
            heading("Something wrong?", level=2, align="center"),
            para("Yellow lower leaves usually mean too much water. Crisp brown edges usually mean air that is too dry. Send us a photograph and we will tell you which.",
                 align="center", color="muted"),
            buttons(button("Ask us", "{{page:contact}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def about():
    return "\n\n".join([
        section(page_intro("The nursery", "A glasshouse, and four months of patience",
                           "We grow what we sell, which takes longer and is the entire difference."),
                pad=("70", "50")),
        section(image("about-1", IMAGES["about-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        story_split(
            "2016",
            "We started because the plants we bought kept dying",
            "Most houseplants are grown fast in Dutch glasshouses, shipped in a warm lorry and sold within a week. They look perfect and then collapse in an ordinary room. We buy plugs and grow them on slowly in our own light, so what leaves here is already used to it.",
            ["Grown on for at least four months",
             "Peat-free compost, always",
             "Pots and plants packed in paper, never plastic"],
            ("Shop the nursery", "{{shop}}"),
            "story-1", IMAGES["story-1"]),
        numbered_steps([
            ("Plugs", "We buy small, from three growers we have visited, and never from a middleman who cannot name the nursery."),
            ("Four months", "They grow on in our glasshouse, in British light, with the heating off from April."),
            ("Hardened", "A fortnight in an unheated room before they are listed, which is where the weak ones show."),
            ("Packed", "In paper, with a care card written for the room you said you were buying for."),
        ], "How a plant gets here", kicker="Four steps"),
        spec_rows([
            ("Founded", "2016, in two polytunnels"),
            ("Glasshouse", "400 square metres"),
            ("Plants grown on a year", "About 18,000"),
            ("Peat used", "None, since 2016"),
            ("People", "Seven, three of them growers"),
        ], "The nursery in numbers", kicker="About us", photo="promo-1", alt=IMAGES["promo-1"]),
    ])


def contact():
    details = columns(*[
        column(group("\n".join([
            bp.icon("tyche/" + name, cls="tyche-icon tyche-icon--large"),
            heading(title, level=2, size="large", cls="tyche-usp__title"),
            para(body, color="muted"),
        ]), layout="flex", orientation="vertical", gap="20", cls="tyche-usp"))
        for name, title, body in (
            ("headset", "Plant questions", "hello@example.com<br>Send a photograph and we will tell you what it wants."),
            ("clock", "The glasshouse", "Friday and Saturday, 10am to 4pm<br>Closed if it is below freezing"),
            ("map-pin", "Where", "Ash Lane Nursery<br>Follow the track past the farm shop"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Come and see them growing",
                           "The glasshouse is open at the end of the week. Bring a photograph of the room and we will pick something for it."),
                pad=("70", "50")),
        section(details, pad=("0", "60")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Watering, light, repotting and delivery are all covered in the care guide and the help pages.", align="center", color="muted"),
            buttons(button("Read the care guide", "{{page:plant-care}}", style="tyche-outline"),
                    button("Read the FAQ", "{{page:faq}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Choosing", (
            ("How do I know what light I have?", "Stand where the plant will go at noon and hold your hand up. A sharp shadow is bright light, a soft one is medium, no real shadow is low. Every plant here is filed by that."),
            ("Which are safe around a cat?", "Filter the shop by pet safety. The spider plant, the ferns, the fittonia, the echeveria and the haworthia are all safe; the rest carry a warning on the label."),
            ("What size should I buy?", "The 12 cm is a desk or a sill, the 17 cm is a side table, the 22 cm is a floor plant. Pot sizes are the diameter across the top."),
        )),
        ("Delivery", (
            ("How do they travel?", "Wrapped in paper with the pot bagged so the compost stays in. Plants leave on Monday and Tuesday so nothing sits in a depot over a weekend."),
            ("What if it arrives damaged?", "Send a photograph within 48 hours. A creased leaf is usually cosmetic and will grow out; anything worse and we replace it."),
        )),
        ("After it arrives", (
            ("It has dropped leaves. Is it dying?", "Probably not. A few leaves after a move is normal while it adjusts to your light. Leave it somewhere stable for a fortnight before doing anything."),
            ("When should I repot?", "When roots come through the drainage holes, usually every second spring. Go up one pot size only."),
            ("Do you guarantee them?", "For the first thirty days. If it fails in that time, tell us and we replace it."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "Choosing, delivery, and what to do in the first fortnight."), pad=("70", "50")),
        section(body, pad=("0", "80")),
    ])


def delivery():
    rows = [
        ("Standard delivery", "$7, plants leave Monday and Tuesday"),
        ("Free delivery", "On orders over $60"),
        ("Pots and care only", "$4, sent any working day"),
        ("Collection", "Free, from the glasshouse on Friday or Saturday"),
        ("First month", "If a plant fails within 30 days we replace it"),
    ]
    return "\n\n".join([
        section(page_intro("Delivery and returns", "Plants travel on Mondays",
                           "Nothing living goes into the post on a Thursday, because nothing living should spend a weekend in a depot."),
                pad=("70", "50")),
        spec_rows(rows, "Delivery", kicker="What it costs", bg=None, photo="repot-1", alt=IMAGES["repot-1"]),
        section(group("\n\n".join([
            heading("Returns", level=2),
            para("Pots, compost and feed can go back unopened within thirty days. Plants are living things, so they cannot be resold once they have left: if something is wrong with one, we replace it rather than asking for it back.",
                 color="muted"),
            heading("The first month", level=2),
            para("If a plant fails within thirty days, send a photograph and we will send another. It happens, usually to a batch rather than a plant, and we would rather know.",
                 color="muted"),
            heading("Damaged in the post", level=2),
            para("Photograph the box and the plant within 48 hours. Creased leaves usually grow out and we will say so; a snapped stem gets a replacement.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("plant-care", "Plant care", plant_care, "page-no-title"),
    ("about", "The nursery", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("delivery-returns", "Delivery and returns", delivery, "page-no-title"),
    ("journal", "Journal", None, ""),
]

POSTS = [
    ("how-much-light-have-you-got", "How much light have you actually got?", "plant-care", "journal-2", 5, [
        "Almost every houseplant that dies indoors dies of light, not water. The trouble is that eyes adjust and rooms lie: a hallway that feels bright to you is dusk to a fiddle leaf fig.",
        "The shadow test settles it. At noon, stand where the plant will live and hold your hand a foot above a sheet of paper. A sharp-edged shadow means bright light. A soft, fuzzy one means medium. If there is barely a shadow at all, that is low light, and you want a philodendron or a pothos rather than a cactus.",
        "Do it again in December. A south-facing sill in summer and the same sill in winter are two different places, which is why the care card in the box gives a summer figure and a winter one.",
    ]),
    ("watering-is-a-season-not-a-schedule", "Watering is a season, not a schedule", "plant-care", "journal-1", 17, [
        "A plant watered every Sunday is being watered for the calendar, not for the conditions. In July that might be right. In January it is usually drowning.",
        "Growth stops when light drops, and a plant that is not growing is barely drinking. From November to February most of these want roughly half what they wanted in June: the cacti stop entirely, the philodendron goes to a fortnight.",
        "Feel the soil instead of counting days. Push a finger in to the second knuckle. If it comes out damp, wait. Yellow lower leaves almost always mean the finger test was skipped.",
    ]),
    ("what-four-months-does", "What four months in our glasshouse does", "from-the-nursery", "journal-3", 33, [
        "Most houseplants sold here were grown in the Netherlands in glasshouses lit and heated to keep them moving, then shipped in a warm lorry and sold within the week. They look immaculate on the shelf.",
        "Then they arrive in a normal room, and the difference between the growing conditions and the living room is a shock: leaves drop, growth stalls, and people conclude they cannot keep plants.",
        "We buy plugs and grow them on for at least four months, with the heating off from April, and give them a fortnight in an unheated room before they are listed. That last fortnight is where the weak ones show, and it is the reason we can promise the first month.",
    ]),
]

MENU = [
    ("Bright light", "{{cat:bright}}", "cat:bright"),
    ("Medium light", "{{cat:medium}}", "cat:medium"),
    ("Low light", "{{cat:low}}", "cat:low"),
    ("Pots", "{{cat:pots}}", "cat:pots"),
    ("Plant care", "{{page:plant-care}}", "page:plant-care"),
    ("Journal", "{{page:journal}}", "page:journal"),
]


def menu_markup():
    links = []
    for label, href, target in MENU:
        data = {"label": label, "url": href, "isTopLevelLink": True}
        if target.startswith("cat:"):
            data.update({"kind": "taxonomy", "type": "product_cat", "id": "{{catid:%s}}" % target[4:]})
        else:
            data.update({"kind": "post-type", "type": "page", "id": "{{pageid:%s}}" % target[5:]})
        links.append(bp.block("navigation-link", data))
    return "\n".join(links)


def parts():
    return [
        {
            "slug": "header",
            "title": "Header",
            "area": "header",
            "content": header_part("Free delivery over $60 &middot; every plant guaranteed for its first month",
                                   "Read the care guide", "{{page:plant-care}}",
                                   layout="header-stacked-no-announcement"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "A small nursery that grows what it sells. Plants filed by the light they need, in peat-free compost, guaranteed for their first month.",
                [
                    ("Shop", [("Bright light", "{{cat:bright}}"), ("Medium light", "{{cat:medium}}"),
                              ("Low light", "{{cat:low}}"), ("Pots and care", "{{cat:pots}}")]),
                    ("Learn", [("Plant care", "{{page:plant-care}}"), ("Journal", "{{page:journal}}"),
                               ("FAQ", "{{page:faq}}"), ("Delivery and returns", "{{page:delivery-returns}}")]),
                    ("Nursery", [("About us", "{{page:about}}"), ("Contact", "{{page:contact}}"),
                                 ("My account", "{{account}}"), ("All plants", "{{shop}}")]),
                ],
                legal="Grown in peat-free compost."),
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
    "journal": "How we grow them, how to keep them alive, and what is coming out of the glasshouse.",
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
            {"name": "Pot size", "slug": "pot-size", "type": "select", "order_by": "menu_order", "terms": POT_SIZES},
            {"name": "Light", "slug": "light", "type": "select", "order_by": "menu_order", "terms": LIGHT_LEVELS},
            {"name": "Pets", "slug": "pets", "type": "select", "order_by": "menu_order", "terms": PET_SAFE},
        ],
    }

    products = plant_products() + goods_products()

    manifest = {
        "schema": 1,
        "slug": "verdant",
        "theme": {"slug": "tyche", "style": ["Verdant"]},
        "settings": {
            "title": "Verdant",
            "tagline": "Plants for the room you actually have",
            "front_page": "home",
            "posts_page": "journal",
            "currency": "USD",
            "country": "US:OR",
            "shipping": {"country": "US", "flat_rate": "7.00", "free_over": "60"},
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
