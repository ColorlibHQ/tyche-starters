#!/usr/bin/env python3
"""Build the Roastery starter: a speciality coffee roaster.

    python3 .dev/roastery.py

Writes roastery/*.json. The photographs are placed by hand in roastery/images/
and only named here, with the alt text that travels with them.

The store sells coffee it roasts itself -- single origins, blends, decaf -- and
the equipment to brew it. Every coffee comes in two bag sizes and three grinds,
which is what makes a coffee shop a good second starter: it exercises variable
products, attribute ordering and the add-to-cart options block properly.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, category_tiles, check_list, column, columns, cover, footer_part, group,
    header_part, heading, hero_split, icon, image, numbered_steps, para, paragraphs, product_row,
    section, section_head, spec_rows, story_split, cta, eyebrow, SCRIM_SIDE,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "roastery")

accordion = bp.accordion
page_intro = bp.page_intro

# ---------------------------------------------------------------------------
# Photographs
# ---------------------------------------------------------------------------
# slug -> alt text. Every one is CC0; credits.json records where each came from.
IMAGES = {
    "hero-1": "A black scoop brimming with roasted coffee beans on a warm tan surface",
    "cat-single-origin": "A drift of dark roasted coffee beans across a dark wooden plank",
    "cat-blends": "Milk poured from a glass pitcher into a stoneware mug of black coffee",
    "cat-equipment": "A barista pouring from a gooseneck kettle into a row of glass brewers",
    "story-1": "A chrome cafe grinder with a clear hopper half full of beans",
    "story-2": "Two hands tamping ground coffee into a portafilter on a walnut station",
    "brew-1": "Hot water falling onto a blooming bed of coffee grounds in a white paper filter",
    "promo-1": "A warm mahogany-panelled bar room with a bicycle hung from the ceiling",
    "contact-1": "A long dim cafe with a figure silhouetted in the bright doorway",
    "origin-detail": "A glass mug of black coffee on a sunlit wooden table, seen from above",
    "about-1": "A wide roastery with daylight flooding in through open shutter doors",
    "journal-1": "Hands pouring brewed coffee from a glass carafe into a stoneware mug",
    "journal-2": "A hand gripping a black and white striped mug of black coffee",
    "journal-3": "An espresso cup and saucer low on a wide walnut table, seen from above",
    "guji": "A white enamel cup filled with roasted coffee beans, seen from above",
    "huila": "A glass jar on its side with roasted beans spilling onto checked linen",
    "nyeri": "Medium-roast coffee beans filling the frame, tan and chocolate brown",
    "antigua": "A plain white ceramic canister with a pale wooden lid",
    "cerrado": "A heaped mound of roasted beans in a shallow pale wooden bowl",
    "sumatra": "Glossy dark-roast beans with oily highlights, close up",
    "house-espresso": "Espresso streaming from a chrome group head into two brown cups",
    "breakfast": "A white cup of black coffee on a saucer on a round wooden table",
    "midnight": "A matte black cup steaming on a dark surface against a bright window",
    "decaf": "A cappuccino dusted with chocolate in a burnt-orange cup and saucer",
    "v60": "A white ceramic cone on a glass server, standing on a digital brew scale",
    "kettle": "Two hands pouring from a hammered copper gooseneck kettle into a filter",
    "grinder": "A vintage wooden box grinder with a brass hopper full of beans",
    "scales": "A glass pour-over carafe and cone standing on a brew scale",
    "filters": "A white paper filter holding a bed of coffee grounds mid-bloom",
    "taster-set": "A small open hessian sack spilling over with roasted coffee beans",
}

# ---------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("Single origin", "single-origin", "One farm, one harvest, one roast date. Bought through importers who publish what they pay."),
    ("Blends", "blends", "Coffees chosen to work together, roasted for milk, for filter, or for both."),
    ("Decaf", "decaf", "Sugarcane and Swiss Water decaf, roasted like everything else here."),
    ("Equipment", "equipment", "The few things worth owning: a dripper, a kettle, a grinder and scales."),
    ("Gifts", "gifts", "Taster sets and gift cards, packed to be opened."),
]

POST_CATEGORIES = [
    ("Brew guides", "brew-guides", "How to get the most out of a bag of coffee at home."),
    ("From the roastery", "from-the-roastery", "What we are roasting, and why."),
]

SIZES = ["250 g", "1 kg"]
GRINDS = ["Whole bean", "Filter", "Espresso"]
ROASTS = ["Light", "Medium", "Dark"]

# slug, name, category, price for 250 g, sale price, roast, photo, short, long, origin rows
COFFEES = [
    ("guji-natural", "Guji Natural", "single-origin", "19.00", "", "Light", "guji",
     "Ethiopia, natural process. Peach, jasmine and a syrupy finish.",
     "Grown at 2,050 metres in the Guji zone by around 400 smallholders who deliver cherry to the Shakiso washing station. Dried whole on raised beds for eighteen days, which is what gives it the peach and the weight.",
     [("Origin", "Guji, Ethiopia"), ("Altitude", "2,050 m"), ("Process", "Natural, dried on raised beds"),
      ("Varietal", "Heirloom"), ("Tasting notes", "Peach, jasmine, brown sugar"), ("Roasted for", "Filter")]),
    ("huila-washed", "Huila Washed", "single-origin", "18.00", "", "Light", "huila",
     "Colombia, washed. Red apple, caramel and a clean finish.",
     "From twelve farms around Pitalito, each under two hectares. Fermented in tanks for eighteen hours and washed in spring water, then dried on covered patios.",
     [("Origin", "Huila, Colombia"), ("Altitude", "1,750 m"), ("Process", "Washed"),
      ("Varietal", "Caturra, Castillo"), ("Tasting notes", "Red apple, caramel, orange"), ("Roasted for", "Filter and espresso")]),
    ("nyeri-aa", "Nyeri AA", "single-origin", "21.00", "", "Light", "nyeri",
     "Kenya, washed. Blackcurrant, grapefruit and a dry finish.",
     "A screen-18 lot from the slopes of Mount Kenya, fermented overnight and soaked in clean water before drying. The acidity is the point: serve it black and let it cool a little.",
     [("Origin", "Nyeri, Kenya"), ("Altitude", "1,800 m"), ("Process", "Washed, soaked"),
      ("Varietal", "SL28, SL34"), ("Tasting notes", "Blackcurrant, grapefruit, cane sugar"), ("Roasted for", "Filter")]),
    ("antigua", "Antigua", "single-origin", "17.50", "", "Medium", "antigua",
     "Guatemala, washed. Cocoa, almond and a soft body.",
     "From a single estate in the Antigua valley, between three volcanoes that drop ash on the fields and keep the soil loose. An easy coffee: it takes milk without disappearing.",
     [("Origin", "Antigua, Guatemala"), ("Altitude", "1,550 m"), ("Process", "Washed"),
      ("Varietal", "Bourbon"), ("Tasting notes", "Cocoa, almond, red apple"), ("Roasted for", "Espresso and filter")]),
    ("cerrado", "Cerrado", "single-origin", "16.00", "14.00", "Medium", "cerrado",
     "Brazil, pulped natural. Hazelnut, milk chocolate and low acidity.",
     "Machine-picked on the flat land of the Cerrado Mineiro and pulped before drying, which keeps some sweetness without the ferment of a full natural. The base of our house espresso, sold on its own while the harvest lasts.",
     [("Origin", "Cerrado Mineiro, Brazil"), ("Altitude", "1,100 m"), ("Process", "Pulped natural"),
      ("Varietal", "Yellow Catuai"), ("Tasting notes", "Hazelnut, milk chocolate, malt"), ("Roasted for", "Espresso")]),
    ("sumatra-mandheling", "Sumatra Mandheling", "single-origin", "18.50", "", "Dark", "sumatra",
     "Indonesia, wet hulled. Cedar, dark chocolate and a heavy body.",
     "Wet hulled at high moisture the way Sumatra has always done it, which is where the cedar and the savoury edge come from. The heaviest coffee we sell, and the one people either love or leave.",
     [("Origin", "Aceh, Sumatra"), ("Altitude", "1,400 m"), ("Process", "Wet hulled"),
      ("Varietal", "Ateng, Jember"), ("Tasting notes", "Cedar, dark chocolate, tobacco"), ("Roasted for", "Espresso")]),
    ("house-espresso", "House Espresso", "blends", "16.00", "", "Medium", "house-espresso",
     "Our everyday espresso: Brazil and Colombia, for milk drinks.",
     "Seventy per cent Cerrado for body and thirty per cent Huila for something to taste through milk. Roasted a little further than our filter coffees so it is forgiving on a home machine.",
     [("Blend", "70% Brazil, 30% Colombia"), ("Process", "Pulped natural and washed"),
      ("Tasting notes", "Milk chocolate, hazelnut, orange"), ("Roasted for", "Espresso"),
      ("Recipe", "18 g in, 36 g out, 28 seconds")]),
    ("breakfast-blend", "Breakfast Blend", "blends", "15.00", "", "Medium", "breakfast",
     "The one to make a litre of. Sweet, round and hard to get wrong.",
     "Guatemala and Brazil in equal parts, roasted for a cafetiere or a filter machine rather than for a scale and a timer. The coffee we drink in the roastery before anyone else arrives.",
     [("Blend", "50% Guatemala, 50% Brazil"), ("Process", "Washed and pulped natural"),
      ("Tasting notes", "Cocoa, almond, baked apple"), ("Roasted for", "Filter and cafetiere"),
      ("Recipe", "60 g per litre")]),
    ("midnight-blend", "Midnight Blend", "blends", "16.50", "", "Dark", "midnight",
     "A proper dark roast: bittersweet, smoky and built for milk.",
     "Sumatra and Brazil taken to the edge of second crack, for anyone who grew up on dark coffee and does not want an apology for it. Excellent as an iced latte.",
     [("Blend", "60% Sumatra, 40% Brazil"), ("Process", "Wet hulled and pulped natural"),
      ("Tasting notes", "Dark chocolate, molasses, smoke"), ("Roasted for", "Espresso and milk"),
      ("Recipe", "18 g in, 34 g out, 30 seconds")]),
    ("swiss-water-decaf", "Swiss Water Decaf", "decaf", "17.00", "", "Medium", "decaf",
     "Colombia, decaffeinated with water alone. Caramel and cocoa.",
     "The same Huila we sell with the caffeine in it, sent to be decaffeinated with water and charcoal rather than solvents. Roasted a shade darker, because decaf beans take heat differently.",
     [("Origin", "Huila, Colombia"), ("Process", "Swiss Water decaffeinated"),
      ("Caffeine", "99.9% removed"), ("Tasting notes", "Caramel, cocoa, red apple"),
      ("Roasted for", "Filter and espresso")]),
]

# slug, name, category, price, sale, photo, short, long
EQUIPMENT = [
    ("v60-dripper", "Ceramic Dripper", "equipment", "28.00", "", "v60",
     "A ceramic cone for one or two cups, with a glass carafe.",
     "Ceramic holds heat better than plastic and forgives a slow pour. Comes with a glass carafe, a scoop and twenty filters to get started."),
    ("pour-over-kettle", "Pour-over Kettle", "equipment", "69.00", "59.00", "kettle",
     "A gooseneck kettle with a thermometer in the lid.",
     "The spout is the whole point: it turns a kettle into something you can aim. One litre, brushed steel, with a dial thermometer so you can stop guessing at 94 degrees."),
    ("hand-grinder", "Hand Grinder", "equipment", "89.00", "", "grinder",
     "Steel burrs, forty clicks, good for filter and espresso.",
     "Conical steel burrs and a stepped adjustment you can feel through the handle. Forty grams in the hopper, which is two large cups, and it grinds them in under a minute."),
    ("brew-scales", "Brew Scales", "equipment", "45.00", "", "scales",
     "Scales that weigh to a tenth of a gram, with a timer.",
     "Coffee is a ratio, and a ratio needs scales. These read to 0.1 g, start timing when the first drop lands, and survive being rinsed."),
    ("paper-filters", "Paper Filters, 100", "equipment", "8.00", "", "filters",
     "One hundred bleached filters for a size 02 cone.",
     "Bleached, because unbleached filters taste of paper unless you rinse them thoroughly. Fits any size 02 cone, ours included."),
    ("taster-set", "Taster Set", "gifts", "42.00", "", "taster-set",
     "Three 100 g bags: one light, one medium, one dark.",
     "The easiest way to find out what someone likes. Three 100 g bags, chosen from what we roasted that week, with a card explaining what each one is and how to brew it."),
]

REVIEWS = {
    "guji-natural": [
        ("Marta L.", 5, "I have bought this three times now. It really does taste of peach, which I did not believe until I made it as a pour-over."),
        ("Ben A.", 4, "Beautiful coffee, though it needs a finer grind than I expected. The card in the bag helped."),
    ],
    "house-espresso": [
        ("Sofia D.", 5, "Forgiving on my machine at home and it still tastes of something through milk. Ordered the kilo bag after the first week."),
    ],
    "hand-grinder": [
        ("Tom R.", 5, "Replaced a blade grinder with this and the difference was bigger than changing the coffee."),
        ("Priya N.", 4, "Solid and quick. Espresso is at the very edge of what it can do, but filter is effortless."),
    ],
}


def coffee_products():
    products = []
    for slug, name, category, price, sale, roast, photo, short, long_text, origin in COFFEES:
        kilo = "%.2f" % (float(price) * 3.4)
        variations = []
        for size in SIZES:
            for grind in GRINDS:
                variations.append({
                    "attributes": {"size": size, "grind": grind},
                    "regular_price": price if size == SIZES[0] else kilo,
                    "stock_status": "instock",
                })
                if sale and size == SIZES[0]:
                    variations[-1]["sale_price"] = sale
        products.append({
            "slug": slug,
            "name": name,
            "type": "variable",
            "sku": "RO-" + slug[:6].upper(),
            "short_description": short,
            "description": paragraphs(long_text) + "\n\n" + spec_list(origin),
            "categories": [category],
            "featured": slug in ("guji-natural", "house-espresso", "nyeri-aa"),
            "stock_status": "instock",
            "image": photo + ".webp",
            "days_ago": 3 if slug in ("guji-natural", "nyeri-aa") else 6 + COFFEES.index(
                next(c for c in COFFEES if c[0] == slug)) * 4,
            "attributes": [
                {"slug": "size", "taxonomy": True, "options": SIZES, "visible": True, "variation": True},
                {"slug": "grind", "taxonomy": True, "options": GRINDS, "visible": True, "variation": True},
                {"slug": "roast", "taxonomy": True, "options": [roast], "visible": True, "variation": False},
            ],
            "variations": variations,
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        })
    return products


def equipment_products():
    products = []
    for slug, name, category, price, sale, photo, short, long_text in EQUIPMENT:
        product = {
            "slug": slug,
            "name": name,
            "type": "simple",
            "sku": "RO-" + slug[:6].upper(),
            "regular_price": price,
            "short_description": short,
            "description": paragraphs(long_text),
            "categories": [category],
            "featured": slug in ("hand-grinder", "taster-set"),
            "stock_status": "outofstock" if slug == "brew-scales" else "instock",
            "image": photo + ".webp",
            "days_ago": 120 + EQUIPMENT.index(next(e for e in EQUIPMENT if e[0] == slug)) * 15,
            "reviews": [{"author": a, "rating": r, "content": c} for a, r, c in REVIEWS.get(slug, [])],
        }
        if sale:
            product["sale_price"] = sale
        products.append(product)
    return products


def spec_list(rows):
    """Origin details inside a product description, as a short list."""
    items = "\n".join("<li>%s: %s</li>" % (label, value) for label, value in rows)
    return '<!-- wp:list -->\n<ul class="wp-block-list">%s</ul>\n<!-- /wp:list -->' % items


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
BREW_STEPS = [
    ("Weigh", "Sixty grams of coffee to a litre of water. For one big cup: 18 g of coffee, 300 g of water."),
    ("Grind", "Medium, like table salt. Grind it now, not this morning: coffee goes flat within the hour."),
    ("Bloom", "Pour twice the coffee's weight in water, wait forty seconds, and watch it swell."),
    ("Pour", "Add the rest in two goes, keeping the bed level. The whole brew should take about three minutes."),
]


def home():
    return "\n\n".join([
        hero_split(
            "This week on the roaster",
            "Ethiopia Guji",
            "Peach, jasmine and brown sugar, from 400 smallholders in the Guji zone. Roasted Tuesday in a twelve-kilo drum and posted the morning after.",
            ("Shop coffee", "{{shop}}"),
            ("Brew guides", "{{page:brew-guides}}"),
            "hero-1", IMAGES["hero-1"]),
        category_tiles(
            [("single-origin", "Single origin", "One farm, one harvest, one roast date"),
             ("blends", "Blends", "Built for milk, for filter, or for both"),
             ("equipment", "Equipment", "The four things worth owning")],
            "Find your coffee", kicker="Shop", link=("See everything", "{{shop}}")),
        product_row("new-arrivals", "On the roaster", "This week's coffee", "Shop all coffee", "{{shop}}"),
        numbered_steps(BREW_STEPS, "Better coffee in four steps", kicker="Brew guide"),
        product_row("featured", "Chosen by us", "What we are drinking", "Shop all coffee", "{{shop}}", carousel=True),
        spec_rows(
            [("Origin", "Guji, Ethiopia"), ("Altitude", "2,050 m"), ("Process", "Natural, dried on raised beds for 18 days"),
             ("Varietal", "Heirloom"), ("Tasting notes", "Peach, jasmine, brown sugar"), ("Roasted", "Tuesday, and every Tuesday")],
            "This week on the roaster", kicker="Guji Natural",
            photo="origin-detail", alt=IMAGES["origin-detail"]),
        story_split(
            "The roastery",
            "A twelve-kilo drum and a lot of note-taking",
            "We started in 2019 with a second-hand roaster in a railway arch, selling to three cafes. The arch is still there. The notebooks now fill a shelf, and every bag carries the date its coffee came out of the drum.",
            ["Bought through importers who publish what they pay the farm",
             "Roasted in twelve-kilo batches, never more than a week ahead",
             "Posted in compostable bags, first class"],
            ("Read our story", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        wholesale_band(),
        journal_row(),
        newsletter(),
    ])


def wholesale_band():
    inner = "\n".join([
        eyebrow("Wholesale", color="overlay"),
        heading("Serving it somewhere?", level=2, size="huge", color="overlay"),
        para("We supply about forty cafes, restaurants and offices. That comes with a machine setup, training for your staff and a standing order you can change any week.",
             color="overlay", size="large"),
        buttons(button("Talk to us about wholesale", "{{page:wholesale}}", bg="overlay", color="dark")),
    ])
    # The text sits on the left, so the photograph is darkened from the left.
    # A scrim that darkens from the middle down left the eyebrow at 3.4:1 on the
    # bar room, which is bright exactly where that word lands.
    return section(cover(group(group(inner, layout="default", cls="tyche-hero__content"), align="wide", layout="default"),
                         "promo-1", min_height=420, position="center left", cls="tyche-promo",
                         align="wide", gradient=SCRIM_SIDE), pad=("0", "70"))


def journal_row():
    body = section_head("From the roastery", kicker="Journal", link_text="Read the journal", link_href="{{page:journal}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def newsletter():
    return cta(
        "Subscriptions",
        "Coffee that arrives before you run out",
        "Tell us how much you drink and we will send it every week, fortnight or month. Change the coffee, skip a delivery or stop it entirely from your account.",
        ["Ten per cent off every bag", "Free delivery, always", "Skip or stop whenever you like"],
        ("Create an account", "{{account}}"),
        ("Shop coffee", "{{shop}}"),
        "contact-1")

def brew_guides():
    ratios = [
        ("Pour-over", "60 g per litre, medium grind, 3 minutes"),
        ("Cafetiere", "60 g per litre, coarse grind, 4 minutes, then plunge"),
        ("Espresso", "18 g in, 36 g out, 28 seconds, fine grind"),
        ("Moka pot", "Fill the basket level, medium-fine, off the heat when it gurgles"),
        ("Cold brew", "80 g per litre, coarse, 16 hours in the fridge"),
    ]
    return "\n\n".join([
        section(page_intro("Brew guides", "How to brew what we roast",
                           "Coffee is a ratio, a grind and a time. Get those three right and the rest is preference."),
                pad=("70", "60")),
        section(image("brew-1", IMAGES["brew-1"], ratio="21/9", align="wide"), pad=("0", "70")),
        numbered_steps(BREW_STEPS, "A pour-over, step by step", kicker="Filter"),
        spec_rows(ratios, "Ratios for everything else", kicker="Cheat sheet"),
        section(group("\n".join([
            heading("Still not right?", level=2, align="center"),
            para("Bitter usually means too fine or too long. Sour usually means too coarse or too quick. Change one thing at a time.",
                 align="center", color="muted"),
            buttons(button("Ask us", "{{page:contact}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30")),
    ])


def wholesale():
    offers = [
        ("Coffee", "Any coffee we roast, in 1 kg bags, at trade prices that fall as the standing order grows."),
        ("Equipment", "Grinders, brewers and scales at cost, on loan or bought outright."),
        ("Training", "A day in the roastery for your staff, then a visit whenever you hire someone new."),
        ("Support", "A number that reaches a person, and a standing order you can change until Monday morning."),
    ]
    return "\n\n".join([
        section(page_intro("Wholesale", "Coffee for cafes, restaurants and offices",
                           "We supply about forty places within a morning's drive. Here is what that looks like."),
                pad=("70", "60")),
        story_split(
            "How it works",
            "One roast date, forty deliveries",
            "Tell us what you serve and how much of it. We roast on Tuesday, deliver on Wednesday and Thursday, and invoice monthly. Most cafes start with one blend and add a single origin for filter once their staff have tasted a few.",
            ["Trade prices from 5 kg a week",
             "Free delivery within the county, next day",
             "Machine setup, dialling in and staff training included"],
            ("Send us a message", "{{page:contact}}"),
            "promo-1", IMAGES["promo-1"]),
        spec_rows(offers, "What comes with it", kicker="Wholesale"),
        section(group("\n".join([
            heading("Start with a sample box", level=2, align="center"),
            para("Three kilos, chosen for what you serve, with no commitment. Tell us your machine and your milk and we will put it together.",
                 align="center", color="muted"),
            buttons(button("Request a sample box", "{{page:contact}}"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def about():
    return "\n\n".join([
        section(page_intro("Our story", "A railway arch, a drum roaster and a lot of notebooks",
                           "We buy coffee we can trace, roast it in small batches and sell it while it is fresh. That is the whole business."),
                pad=("70", "60")),
        section(image("about-1", IMAGES["about-1"], ratio="21/9", align="wide"), pad=("0", "70")),
        story_split(
            "2019",
            "It started because nobody would sell us a kilo",
            "Two of us wanted good coffee at home and could only buy it by the cup. We bought a second-hand twelve-kilo roaster, put it in a railway arch, and spent a year making bad coffee until we stopped.",
            ["Twelve-kilo batches, roasted to order",
             "Every bag carries its roast date, not a best-before",
             "Compostable bags, posted first class"],
            ("Shop this week's coffee", "{{shop}}"),
            "story-2", IMAGES["story-2"]),
        numbered_steps([
            ("Buy", "Through importers who publish what they paid the farm. If they will not say, we do not buy."),
            ("Sample", "Every lot is roasted small and tasted on a table with eight cups before we commit."),
            ("Roast", "Twelve kilos at a time, Tuesday, with the profile written down and kept."),
            ("Post", "Bagged Wednesday morning and in the post by noon."),
        ], "How a coffee gets here", kicker="Four steps"),
        spec_rows([
            ("Founded", "2019, in a railway arch that is still the roastery"),
            ("Roaster", "A 12 kg drum, rebuilt twice"),
            ("Roasted per week", "About 200 kg"),
            ("Cafes supplied", "Around 40"),
            ("People", "Six, four of whom roast"),
        ], "The roastery in numbers", kicker="About us"),
    ])


def contact():
    details = columns(*[
        column(group("\n".join([
            icon("tyche/" + name, cls="tyche-icon tyche-icon--large"),
            heading(title, level=2, size="large", family="figtree", cls="tyche-usp__title"),
            para(body, color="muted"),
        ]), layout="flex", orientation="vertical", gap="20", cls="tyche-usp"))
        for name, title, body in (
            ("headset", "Orders and coffee", "hello@example.com<br>We answer within one working day."),
            ("clock", "The counter", "Monday to Friday, 8am to 4pm<br>Saturday, 9am to 2pm"),
            ("map-pin", "The roastery", "Arch 12, Bridge Road<br>Open on Saturdays for bags and coffee"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Come and see where it is roasted",
                           "The arch is open on Saturday mornings. Bring a bag back and we will fill it."),
                pad=("70", "60")),
        section(details, pad=("0", "70")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "70")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Grinds, subscriptions, delivery and wholesale are all covered in the help pages.", align="center", color="muted"),
            buttons(button("Read the FAQ", "{{page:faq}}", style="tyche-outline"),
                    button("Delivery and returns", "{{page:delivery-returns}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Coffee", (
            ("How fresh is it?", "Everything is roasted on Tuesday and posted on Wednesday. The roast date is printed on the bag, not a best-before."),
            ("Which grind should I choose?", "Whole bean if you own a grinder, because coffee goes flat within an hour of grinding. Otherwise pick the way you brew: filter for a dripper or cafetiere, espresso for a machine."),
            ("How long does a bag last?", "Sealed, about three months. Open, about two weeks before you notice. Keep it in the bag, folded shut, out of the fridge."),
        )),
        ("Orders and subscriptions", (
            ("Can I change my subscription?", "Change the coffee, the size, the grind or the date from your account, up to the Monday before a roast."),
            ("Can I cancel?", "Yes, from your account, with no notice. Any coffee already roasted for you is sent."),
        )),
        ("Delivery", (
            ("When will it arrive?", "Orders placed before Monday evening are roasted Tuesday and posted Wednesday, first class. Most arrive Thursday."),
            ("Do you deliver abroad?", "To most of Europe. Costs appear at checkout once you enter an address."),
        )),
        ("Wholesale", (
            ("What is the minimum order?", "Five kilos a week for trade prices. Below that you are welcome to buy at the normal price."),
            ("Do you lend equipment?", "We lend grinders to wholesale customers and set them up on site."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "About the coffee, the subscriptions and how it reaches you."), pad=("70", "60")),
        section(body, pad=("0", "80")),
    ])


def delivery():
    rows = [
        ("Standard delivery", "$4.50, first class, two to three working days"),
        ("Free delivery", "On orders over $40, and on every subscription"),
        ("Roast day", "Tuesday. Order by Monday evening to be in that roast"),
        ("Collection", "Free from the arch on Saturday mornings"),
        ("Europe", "From $12, three to six working days"),
    ]
    return "\n\n".join([
        section(page_intro("Delivery and returns", "When it is roasted, and when it arrives",
                           "Coffee is posted the morning after it is roasted, so it reaches you within days of leaving the drum."),
                pad=("70", "60")),
        spec_rows(rows, "Delivery", kicker="What it costs", bg=None),
        section(group("\n\n".join([
            heading("Returns", level=2),
            para("Coffee is food, so we cannot resell a bag once it has left us. If something is wrong with it -- and sometimes something is -- tell us within thirty days and we will replace it or refund it. You do not need to send it back.",
                 color="muted"),
            heading("Equipment", level=2),
            para("Send equipment back unused within thirty days for a full refund. Anything faulty is covered for two years; write to us and we will collect it.",
                 color="muted"),
            heading("Damaged in the post", level=2),
            para("Send a photograph of the box and the bag. We will have another in that week's roast, at no cost.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def parts():
    """The header's promise and the footer's words belong to the starter."""
    return [
        {
            "slug": "header",
            "title": "Header",
            "area": "header",
            "content": header_part("Free delivery over $40 &middot; Roasted Tuesday, posted Wednesday",
                                   "Shop this week's coffee", "{{shop}}"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "A small coffee roastery in a railway arch. We buy what we can trace, roast it on Tuesdays and post it the morning after.",
                [
                    ("Shop", [("All coffee", "{{shop}}"), ("Single origin", "{{cat:single-origin}}"),
                              ("Blends", "{{cat:blends}}"), ("Equipment", "{{cat:equipment}}")]),
                    ("Learn", [("Brew guides", "{{page:brew-guides}}"), ("Journal", "{{page:journal}}"),
                               ("FAQ", "{{page:faq}}"), ("Delivery and returns", "{{page:delivery-returns}}")]),
                    ("Roastery", [("Our story", "{{page:about}}"), ("Wholesale", "{{page:wholesale}}"),
                                  ("Contact", "{{page:contact}}"), ("My account", "{{account}}")]),
                ],
                legal="Roasted and posted from the arch."),
        },
    ]


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("brew-guides", "Brew guides", brew_guides, "page-no-title"),
    ("wholesale", "Wholesale", wholesale, "page-no-title"),
    ("about", "Our story", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("delivery-returns", "Delivery and returns", delivery, "page-no-title"),
    ("journal", "Journal", None, ""),
]

# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------
POSTS = [
    ("dial-in-a-pour-over", "How to dial in a pour-over in three brews", "brew-guides", "journal-1", 6, [
        "A bag of coffee has about fifteen brews in it, and the first three are for learning. Here is the quickest way to spend them.",
        "Brew one: make it exactly as the bag says, 60 g per litre, and time it. If it took much less than three minutes the grind is too coarse; much more and it is too fine. Write down what happened.",
        "Brew two: change the grind and nothing else. Finer if it tasted thin, sour or salty. Coarser if it tasted bitter, dry or dull. One change, one brew.",
        "Brew three: now change the ratio, not the grind. More coffee if it still tastes weak, less if it is heavy. By the fourth cup you are drinking rather than measuring, which is the point.",
    ]),
    ("washed-and-natural", "What washed and natural mean on a coffee bag", "brew-guides", "journal-2", 13, [
        "Every bag we sell says washed, natural or wet hulled. It is the single most useful word on the label, and it describes what happened to the fruit around the seed.",
        "Washed coffee has the fruit removed within hours of picking and is fermented in tanks to clean the seed. It tastes clearer and more acidic: our Kenya and our Colombia are both washed.",
        "Natural coffee is dried whole, fruit and all, on raised beds for two or three weeks. The sugars work their way in, and the result is heavier and sweeter, sometimes close to jam. The Guji is natural.",
        "Wet hulled is an Indonesian method where the seed is hulled while still wet. It makes the cedar and the heaviness people recognise in Sumatra, and it is the reason that coffee divides a room.",
    ]),
    ("why-we-roast-on-tuesdays", "Why we roast on Tuesdays", "from-the-roastery", "journal-3", 24, [
        "Coffee is at its best between four and twenty days after roasting. Before that it is still letting go of carbon dioxide; after that it slowly flattens.",
        "So we roast everything on Tuesday, bag it on Wednesday morning and post it before noon. Order on Sunday and your coffee does not exist yet, which is deliberate.",
        "It also means the roastery runs on one rhythm. Green coffee is weighed on Monday, the drum runs all Tuesday, Wednesday is bags and post, and Thursday is for the cafes. Nothing sits in a warehouse waiting for an order.",
    ]),
]

MENU = [
    ("Shop", "{{shop}}", None),
    ("Single origin", "{{cat:single-origin}}", "cat:single-origin"),
    ("Blends", "{{cat:blends}}", "cat:blends"),
    ("Equipment", "{{cat:equipment}}", "cat:equipment"),
    ("Brew guides", "{{page:brew-guides}}", "page:brew-guides"),
    # Wholesale lives in the footer and in its own band on the homepage: seven
    # items and a centred logo wrap onto a second line at 1440px.
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


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------
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
    "journal": "What is on the roaster, where it came from, and how to get the best out of it at home.",
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

    posts = []
    for slug, title, category, photo, days, body in POSTS:
        posts.append({
            "slug": slug,
            "title": title,
            "content": paragraphs(*body),
            "excerpt": body[0],
            "categories": [category],
            "image": photo + ".webp",
            "days_ago": days,
        })

    terms = {
        "product_cat": [{"name": name, "slug": slug, "description": description}
                        for name, slug, description in CATEGORIES],
        "category": [{"name": name, "slug": slug, "description": description}
                     for name, slug, description in POST_CATEGORIES],
        "attributes": [
            {"name": "Size", "slug": "size", "type": "select", "order_by": "menu_order", "terms": SIZES},
            {"name": "Grind", "slug": "grind", "type": "select", "order_by": "menu_order", "terms": GRINDS},
            {"name": "Roast", "slug": "roast", "type": "select", "order_by": "menu_order", "terms": ROASTS},
        ],
    }

    products = coffee_products() + equipment_products()

    manifest = {
        "schema": 1,
        "slug": "roastery",
        "theme": {"slug": "tyche", "style": ["Roastery"]},
        "settings": {
            "title": "Roastery",
            "tagline": "Roasted Tuesday, posted Wednesday",
            "front_page": "home",
            "posts_page": "journal",
            "currency": "USD",
            "country": "US:OR",
            "shipping": {"country": "US", "flat_rate": "4.50", "free_over": "40"},
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

    variations = sum(len(p.get("variations", [])) for p in products)
    print("  %d products (%d variations), %d pages, %d posts, %d images"
          % (len(products), variations, len(pages), len(posts), len(IMAGES)))
    print("  " + ", ".join(written))


if __name__ == "__main__":
    main()
