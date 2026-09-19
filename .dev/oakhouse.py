#!/usr/bin/env python3
"""Build the Oakhouse starter: solid timber furniture, made to order.

    python3 .dev/oakhouse.py

Furniture is the slowest thing a small shop sells: nothing is in stock, every
piece is a six-week wait, and the questions are dimensions, timber and whether
it will fit up the stairs. So this store is built around answering those before
anyone asks -- millimetres, kilos, species and lead time on every page -- and it
exercises what the others do not: a catalogue where the variation is a finish
rather than a size, and where delivery is a conversation rather than a box.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, care_cards, category_tiles, check_list, collage_hero, column, columns,
    cta, footer_part, group, header_part, heading, image, numbered_steps, para, paragraphs,
    product_row, section, section_head, spec_list, spec_rows, story_split,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "oakhouse")

accordion = bp.accordion
page_intro = bp.page_intro

# ---------------------------------------------------------------------------
# The catalogue. Provisional until the photographs are in: this shop can only
# sell the pieces it can show, and the last starter was rewritten twice to
# match what the library actually had.
# ---------------------------------------------------------------------------
IMAGES = {
    # Sections
    "hero-room": "A rustic timber table and stools on a balcony above a wooded valley",
    "hero-detail": "Curved strips of bent timber, lit warm and close",
    "story-1": "A workshop pegboard hung with chisels, clamps and saws",
    "workshop-1": "Old hand tools laid out in rows on a dark bench",
    "materials-1": "The end grain of a sawn trunk, rings running out from the centre",
    "timber-1": "A close-up of warm brown plank grain",
    "showroom-1": "A living room with a green sofa, a round table and a lamp",
    "delivery-1": "A pale ash plank with the grain running across it",
    "contact-1": "A maker in an apron working at a bench, hands only",
    "promo-1": "A bench with a compass and a leather mat, tools to hand",
    "journal-1": "A hammer and a scatter of nails on a plain ground",
    "journal-2": "A bedroom lined in pale timber, plain bed, one window",
    "journal-3": "A sawn trunk end, rings and cracks running out from the middle",
    # The pieces
    "linde-table": "A long farmhouse table and bench against a green panelled wall",
    "round-table": "A round walnut table with a chair drawn up to it",
    "low-table": "A hexagonal oak coffee table with books on it",
    "bow-chair": "A pale timber chair with a bentwood back, alone against a plain wall",
    "porch-rocker": "A painted rocking chair on a covered porch",
    "painted-stool": "A small green painted stool with a fern on it",
    "sideboard": "A low cabinet on tapered legs in an empty room",
    "tall-vase": "A frosted grey vase holding pink flowers",
    "stem-vase": "A small white vase with a few yellow stems",
    "water-jug": "A white ceramic jug on a timber table",
    "teapot": "A green ceramic teapot with two cups and a bowl",
    "cup-set": "Two stacked cups and saucers in black and deep red",
    "coasters": "A stack of round timber coasters cut from a branch",
}

# slug, name, category, room, prices by finish or single, image, days ago,
# lead time, short line, long copy, spec rows
PIECES = [
    ("linde-table", "Linde Dining Table", "tables", "Dining", ("1480.00", "1780.00", "1620.00"),
     "linde-table", 52, "4–6 weeks",
     "A 200 cm table in solid timber, joined with drawbored mortise and tenon. Seats eight.",
     "The top is four boards, book-matched and held with breadboard ends so it can move with the seasons without splitting. The legs are drawbored into the rails, which is slower than a bolt and is the reason this outlives the room it goes in.",
     [("Size", "200 × 90 × 75 cm"), ("Weight", "62 kg"), ("Seats", "Eight, ten at a push"),
      ("Joint", "Drawbored mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("round-table", "Round Table", "tables", "Dining", ("1180.00", "1420.00", "1290.00"),
     "round-table", 96, "4–6 weeks",
     "A 120 cm round table on a single turned column. Four people, and no corner to walk into.",
     "A round top seats four in less floor than a rectangle needs, and nobody sits at an end. The column is turned from one piece and the top is buttoned on, so it can move without the joint opening.",
     [("Size", "120 cm across, 75 cm high"), ("Weight", "41 kg"), ("Seats", "Four"),
      ("Joint", "Turned column, buttoned top"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("low-table", "Low Table", "tables", "Living", ("640.00", "760.00", "700.00"),
     "low-table", 9, "4–6 weeks",
     "A six-sided top on tapered legs, at the height a cup can be put down from.",
     "Hexagonal, because a low table with corners you pass every day should have blunt ones. Set at 40 cm against a three-seat sofa, with the grain run across the width so the top reads as one board.",
     [("Size", "95 cm across, 40 cm high"), ("Weight", "16 kg"), ("Top", "Six-sided, one board"),
      ("Joint", "Tapered legs, wedged tenons"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("bow-chair", "Bow Chair", "seating", "Dining", ("340.00", "410.00", "375.00"),
     "bow-chair", 3, "4–6 weeks",
     "A steam-bent back, a shaped seat, and no fastening you can see.",
     "The back is one piece of timber bent over a form and left in it for a fortnight. The seat is scooped by hand, which takes an hour and is the difference between a chair you sit on for twenty minutes and one you sit on all evening.",
     [("Size", "46 × 52 × 82 cm"), ("Weight", "5.4 kg"), ("Seat height", "46 cm"),
      ("Joint", "Steam-bent back, wedged tenons"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("porch-rocker", "Porch Rocker", "seating", "Living", ("520.00",), "porch-rocker", 9, "6–8 weeks",
     "A slatted rocker, painted rather than oiled, for a porch or a bright hallway.",
     "The only piece here that leaves painted: four coats of eggshell over primed ash, because a chair that lives near a door gets scuffed and paint is the finish you can put right in an afternoon. Rockers are cut to one radius, tested on a flat floor before it goes out.",
     [("Size", "62 × 88 × 104 cm"), ("Weight", "9 kg"), ("Seat height", "42 cm"),
      ("Finish", "Eggshell over primed ash"), ("Colour", "Sage, off-white or charcoal"),
      ("Lead time", "6–8 weeks")]),
    ("painted-stool", "Painted Stool", "seating", "Study", ("180.00",), "painted-stool", 30, "2–3 weeks",
     "Three legs, a dished seat, painted. The first thing every maker here builds.",
     "Three legs never rock on an uneven floor, which is why every workshop stool has three. The seat is dished with a travisher and the legs are wedged from above, so they tighten rather than loosen with use.",
     [("Size", "34 × 34 × 45 cm"), ("Weight", "3.8 kg"), ("Seat height", "45 cm"),
      ("Joint", "Wedged through-tenons"), ("Finish", "Eggshell, any of three colours"),
      ("Lead time", "2–3 weeks")]),
    ("sideboard", "Hollow Sideboard", "storage", "Living", ("1240.00", "1480.00", "1360.00"),
     "sideboard", 61, "6–8 weeks",
     "Two doors, one long shelf, tapered legs, and a back you would not mind seeing.",
     "Dovetailed at the corners and panelled at the back, because a piece that gets pulled out to hoover behind should look finished from every side. The doors are solid, so they are heavy: the hinges are rated for it.",
     [("Size", "160 × 45 × 78 cm"), ("Weight", "54 kg"), ("Inside", "One adjustable shelf"),
      ("Joint", "Hand-cut dovetails"), ("Finish", "Hardwax oil"), ("Lead time", "6–8 weeks")]),
    ("coasters", "Branch Coasters, 6", "homeware", "Dining", ("24.00",), "coasters", 7, "In stock",
     "Six coasters cut across a branch, from the offcuts of everything else.",
     "Cut from the ends of the boards that become tables, so no two runs match and the bark edge is left on. Waxed rather than oiled, which is what stops a hot cup marking them.",
     [("Size", "9 to 11 cm across"), ("Material", "Offcut oak or walnut, as available"),
      ("Finish", "Hard wax"), ("Care", "Wipe, do not soak"), ("Lead time", "In stock")]),
    ("tall-vase", "Tall Vase", "homeware", "Living", ("48.00",), "tall-vase", 5, "In stock",
     "A frosted stoneware vase, thrown by the potter two doors down.",
     "Wide enough at the base to hold a full head of flowers without tipping and narrow enough at the neck to hold three stems upright. Matte outside, glazed inside, so it holds water and warms in the hand.",
     [("Size", "24 cm high, 12 cm across"), ("Material", "Stoneware, matte outside"),
      ("Made by", "Ilse, two doors down"), ("Care", "Rinse by hand"), ("Lead time", "In stock")]),
    ("stem-vase", "Stem Vase", "homeware", "Dining", ("28.00",), "stem-vase", 19, "In stock",
     "A small white vase for the three stems left over from a bunch.",
     "The one vase most people actually use: small enough for a windowsill, heavy enough not to go over, and the right neck for whatever is left when the big arrangement has been made.",
     [("Size", "14 cm high, 7 cm across"), ("Material", "Stoneware, satin white"),
      ("Made by", "Ilse, two doors down"), ("Care", "Rinse by hand"), ("Lead time", "In stock")]),
    ("water-jug", "Water Jug", "homeware", "Dining", ("64.00",), "water-jug", 23, "In stock",
     "A litre and a half, with a lip that does not drip.",
     "Thrown heavy so it sits still on a laid table, and pulled to a proper lip rather than a pinched one, which is the whole difference between a jug and a vase with ambitions.",
     [("Size", "1.5 litres, 22 cm high"), ("Material", "Stoneware, glazed"),
      ("Made by", "Ilse, two doors down"), ("Care", "Dishwasher safe"), ("Lead time", "In stock")]),
    ("teapot", "Teapot and Two Cups", "homeware", "Dining", ("78.00",), "teapot", 12, "In stock",
     "A 700 ml pot and two cups, glazed deep green.",
     "Enough for two people twice, with a cane handle that stays cool and a strainer built into the spout. The cups are deliberately small: tea goes cold in a big one.",
     [("Size", "700 ml pot, 180 ml cups"), ("Material", "Stoneware, cane handle"),
      ("Made by", "Ilse, two doors down"), ("Care", "Hand wash the handle"), ("Lead time", "In stock")]),
    ("cup-set", "Cups and Saucers, 2", "homeware", "Dining", ("34.00",), "cup-set", 27, "In stock",
     "Two cups and saucers, one black and one oxblood.",
     "Stacked, they are the two colours the kiln does best. The saucer is deep enough to be a small dish, which is what most of them end up as.",
     [("Size", "200 ml cups, 14 cm saucers"), ("Material", "Stoneware, gloss glaze"),
      ("Made by", "Ilse, two doors down"), ("Care", "Dishwasher safe"), ("Lead time", "In stock")]),
]

FINISHES = ["Oak", "Walnut", "Blackened oak"]

# A workshop that makes to order rarely discounts, but it does retire a glaze
# and it does run out of a batch, and a shopper should meet both states.
SALE = {"cup-set": "26.00"}

# How long ago each piece was listed. A workshop that has made the same chair
# for years should not have a New badge on every product in the shop.
DAYS = {
    "bow-chair": 3, "low-table": 9, "coasters": 17, "tall-vase": 41,
    "linde-table": 52, "sideboard": 61, "teapot": 66, "porch-rocker": 74,
    "round-table": 96, "stem-vase": 88, "water-jug": 112, "painted-stool": 130,
    "cup-set": 145,
}
SOLD_OUT = {"porch-rocker"}
ROOMS = ["Dining", "Living", "Bedroom", "Study"]

CATEGORIES = [
    ("Tables", "tables", "Three tables: one long, one round, one low."),
    ("Seating", "seating", "A chair, a rocker and a stool, shaped where it matters."),
    ("Storage", "storage", "One cabinet, dovetailed, and finished at the back."),
    ("Homeware", "homeware", "Stoneware from the potter two doors down, and coasters from our own offcuts."),
]

POST_CATEGORIES = [
    ("From the bench", "from-the-bench", "How a piece is made, and why it takes six weeks."),
    ("Living with it", "living-with-it", "Measuring, caring for and repairing solid timber."),
]

REVIEWS = {
    "linde-table": [
        ("Martha K.", 5, "Six weeks to the day, delivered by two people who put it together and took the packaging away. It is the first table I have owned that does not wobble."),
        ("Owen R.", 5, "The breadboard ends have moved a couple of millimetres over the winter, exactly as the care page said they would. No split."),
    ],
    "bow-chair": [
        ("Priya S.", 4, "Comfortable for a long dinner, which was the point. Four of them and only one had a mark, which they refinished without argument."),
    ],
    "teapot": [
        ("Jonas L.", 5, "The cane handle stays cool and the spout does not dribble, which is two more than my last teapot managed."),
    ],
    "coasters": [
        ("Elin M.", 5, "Bark still on the edge and no two the same. Cheaper than I expected for something cut from a table."),
    ],
}

PROMISES = [
    ("ruler-measure", "Every dimension, before you ask",
     "Width, depth, height, weight and seat height on every page, in centimetres and kilos. If it will not go up your stairs we would both rather know now."),
    ("shield-check", "Joints, not fastenings",
     "Mortise and tenon, dovetails and wedges. There is no bolt holding any of this together, which is why the guarantee on the joints runs to ten years."),
    ("truck-delivery", "Two people, into the room",
     "Delivered by the two people who made it, carried to the room it is for, assembled, and the blankets taken away again."),
]

ORDER_STEPS = [
    ("Choose the finish", "Oak, walnut or blackened oak. Samples are free and take two days."),
    ("We cut", "Boards are chosen for the piece and left a fortnight in the workshop to settle."),
    ("We join", "Cut, fitted, glued and oiled by hand. This is the part that takes the weeks."),
    ("We deliver", "Two people, into the room, assembled. We take the packaging away."),
]

TIMBERS = [
    ("European oak", "Pale, hard, and the one that will still look right in thirty years. It darkens slightly and evenly."),
    ("American walnut", "Darker, with more figure. It lightens in sunlight rather than darkening, which surprises people."),
    ("Blackened oak", "Oak, ebonised with an iron solution that reacts with the tannin in the timber rather than sitting on top of it as a paint would."),
]

CARE_ROWS = [
    ("Every day", "A dry cloth. Water rings lift with a damp one if you get to them the same day."),
    ("Twice a year", "A coat of hardwax oil on the top, rubbed in and wiped off. Twenty minutes."),
    ("Marks", "Sand along the grain with 240 grit and re-oil the area. It will blend within a month."),
    ("Heat", "Use a mat. Hardwax oil is not lacquer and a hot pan will leave a pale ring."),
    ("Humidity", "Solid timber moves. A few millimetres across a season is the piece working, not failing."),
]


def piece_products():
    products = []
    for (slug, name, category, room, prices, photo, days, lead,
         short, long_copy, spec) in PIECES:
        days = DAYS.get(slug, days)
        product = {
            "slug": slug,
            "name": name,
            "sku": "OH-" + slug[:3].upper(),
            "categories": [category],
            "image": photo + ".webp",
            "short_description": short,
            "description": paragraphs(long_copy) + "\n\n" + spec_list(spec),
            "days_ago": days,
            "stock_status": "instock",
            "featured": slug in ("linde-table", "bow-chair", "low-table", "sideboard",
                                 "teapot", "tall-vase"),
            "attributes": [
                {"name": "Room", "slug": "room", "taxonomy": True, "options": [room], "visible": True},
                {"name": "Lead time", "slug": "lead-time", "taxonomy": True, "options": [lead],
                 "visible": True},
            ],
            "reviews": [{"author": author, "rating": rating, "content": content}
                        for author, rating, content in REVIEWS.get(slug, [])],
        }
        if len(prices) == 1:
            product["type"] = "simple"
            product["regular_price"] = prices[0]
            if slug in SALE:
                product["sale_price"] = SALE[slug]
            if slug in SOLD_OUT:
                product["stock_status"] = "outofstock"
        else:
            # One photograph, three finishes: say which one is in the picture
            # rather than letting a walnut buyer think they are looking at it.
            product["description"] = product["description"].replace(
                "</ul>", "<!-- wp:list-item -->\n<li>Photographed in: Oak</li>\n<!-- /wp:list-item -->\n</ul>")
            product["type"] = "variable"
            product["attributes"].insert(0, {"name": "Finish", "slug": "finish", "taxonomy": True,
                                             "options": list(FINISHES), "visible": True,
                                             "variation": True})
            product["variations"] = [{"attributes": {"finish": finish}, "regular_price": price,
                                      "stock_status": "instock",
                                      "sku": "OH-%s-%s" % (slug[:3].upper(), finish[:3].upper())}
                                     for finish, price in zip(FINISHES, prices)]
        products.append(product)
    return products


def home():
    return "\n\n".join([
        collage_hero(
            "Made to order &middot; 4–6 weeks",
            "Solid oak, joined by hand",
            "Nothing here is in stock, and that is the point: every piece is cut for the room it is going into, in timber you chose, by the two people who will deliver it.",
            ("Shop dining", "{{cat:tables}}"),
            ("See the workshop", "{{page:about}}"),
            "hero-room", IMAGES["hero-room"], "hero-detail", IMAGES["hero-detail"]),
        product_row("new-arrivals", "New", "Just off the bench", "Shop everything", "{{shop}}"),
        care_cards(PROMISES, "How we work", kicker="The basics", bg="surface"),
        spec_rows(
            [("Size", "200 × 90 × 75 cm"), ("Weight", "62 kg"), ("Seats", "Eight, ten at a push"),
             ("Timber", "European oak, walnut or blackened oak"), ("Joint", "Drawbored mortise and tenon"),
             ("Lead time", "4–6 weeks")],
            "Linde table, in short", kicker="This month's piece",
            photo="materials-1", alt=IMAGES["materials-1"]),
        product_row("featured", "The range", "What we make most of", "Shop everything", "{{shop}}", carousel=True),
        numbered_steps(ORDER_STEPS, "How an order is made", kicker="Six weeks, roughly"),
        story_split(
            "The workshop",
            "Four benches, and nothing on a shelf",
            "We do not hold stock. A piece is cut when it is ordered, from boards chosen for it, which is slower and is the only way to let someone pick a timber and a size and still get a joint that fits.",
            ["Every joint cut and fitted by hand",
             "Timber from managed European forests, with the mill named on request",
             "Ten years on the joints, for as long as you own it"],
            ("Read about the workshop", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        journal_row(),
        cta(
            "For the trade",
            "Specifying for a project?",
            "Architects, interior designers and hotels buy differently: drawings, samples, staged deliveries and a contract price. The trade programme covers all four, and the lead time is the same six weeks.",
            ["Trade pricing from the first order",
             "CAD drawings and finish samples on request",
             "Staged delivery, held in our store at no charge"],
            ("Apply for a trade account", "{{page:trade}}"),
            ("Book a showroom visit", "{{page:showroom}}"),
            "promo-1"),
    ])


def journal_row():
    body = section_head("From the bench", kicker="Journal", link_text="Read the journal", link_href="{{page:journal}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def materials():
    timber_rows = [(name, note) for name, note in TIMBERS]
    return "\n\n".join([
        section(page_intro("Materials and care", "Three timbers, one finish, no lacquer",
                           "What each timber does over time, and the twenty minutes a year that keeps it looking like it did on the first day."),
                pad=("70", "50")),
        spec_rows(timber_rows, "The timbers", kicker="What we cut", photo="materials-1", alt=IMAGES["materials-1"]),
        section(group("\n\n".join([
            heading("The finish", level=2),
            para("Everything leaves here under hardwax oil: a penetrating finish that sits in the timber rather than on it. It is less waterproof than lacquer and infinitely easier to repair, because a scratch is sanded and re-oiled in an afternoon instead of being sent back to a sprayer.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), pad=("0", "60")),
        section(image("timber-1", IMAGES["timber-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        spec_rows(CARE_ROWS, "Looking after it", kicker="Care", bg="surface",
                  photo="promo-1", alt=IMAGES["promo-1"]),
        section(group("\n\n".join([
            heading("What solid timber does", level=2),
            para("It moves. A table top is a little wider in a damp August than in a dry February, which is why the tops here have breadboard ends and the panels sit in grooves rather than being glued down. Movement is the piece working. A split is not, and that is what the guarantee is for.",
                 color="muted"),
            check_list(
                "A few millimetres of seasonal movement across a top is normal",
                "Oak darkens slightly and evenly; walnut lightens in sunlight",
                "Ten years on every joint, for as long as you own the piece"),
        ]), layout="constrained", content_size="720px", gap="30"), pad=("0", "80")),
    ])


def trade():
    return "\n\n".join([
        section(page_intro("Trade", "For architects, designers and hotels",
                           "Trade pricing from the first order, drawings and samples when you are still specifying, and delivery staged to a site programme."),
                pad=("70", "50")),
        spec_rows([
            ("Trade discount", "20% from the first order, 25% over $20,000 a year"),
            ("Drawings", "DWG and PDF for every piece, dimensioned"),
            ("Samples", "Free finish samples, two working days"),
            ("Lead time", "Six weeks, the same as anyone else"),
            ("Staged delivery", "Held in our store at no charge for up to twelve weeks"),
            ("Bespoke", "Sizes changed to the millimetre, from $250"),
        ], "What a trade account gets", kicker="The terms", photo="showroom-1", alt=IMAGES["showroom-1"]),
        section(group("\n\n".join([
            heading("Applying", level=2),
            para("Email the practice name, a project and a rough schedule of what you are specifying. Accounts are opened within a working day and there is no minimum order.",
                 color="muted"),
            buttons(button("Email the trade desk", "{{page:contact}}"),
                    button("Book a showroom visit", "{{page:showroom}}", style="tyche-outline")),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def showroom():
    return "\n\n".join([
        section(page_intro("The showroom", "Sit on it before you buy it",
                           "Everything we make, in one room above the workshop. No appointment for browsing; book an hour if you want someone with you."),
                pad=("70", "50")),
        section(image("showroom-1", IMAGES["showroom-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        spec_rows([
            ("Open", "Thursday to Saturday, 10am to 5pm"),
            ("Where", "Above the workshop, on the yard behind the mill"),
            ("Parking", "In the yard, and the door is at ground level"),
            ("On display", "Every piece in the catalogue, in all three finishes"),
            ("Bring", "Your measurements, and a photograph of the room"),
        ], "Visiting", kicker="Practical", bg=None, photo="contact-1", alt=IMAGES["contact-1"]),
        section(group("\n".join([
            heading("Want an hour with someone?", level=2, align="center"),
            para("Book ahead and one of the makers will walk the room with you, take your measurements and price a bespoke size while you are there.",
                 align="center", color="muted"),
            buttons(button("Book a visit", "{{page:contact}}"),
                    button("Read the FAQ", "{{page:faq}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def contact():
    details = columns(*[
        column(group("\n".join([
            bp.icon("tyche/" + name, cls="tyche-icon tyche-icon--large"),
            heading(title, level=2, size="large", cls="tyche-usp__title"),
            para(body, color="muted"),
        ]), layout="flex", orientation="vertical", gap="20", cls="tyche-usp"))
        for name, title, body in (
            ("headset", "Ask a maker", "hello@example.com<br>Questions about size, timber or a bespoke change."),
            ("clock", "Workshop hours", "Monday to Friday, 8am to 4pm<br>Showroom Thursday to Saturday"),
            ("map-pin", "Where we are", "The Old Mill Yard<br>Deliveries and collections at the yard gate"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Measure twice, then ask us",
                           "Send the dimensions of the room and what has to fit in it. We would rather change a size now than take a table back later."),
                pad=("70", "50")),
        section(details, pad=("0", "60")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Timbers, finishes, lead times and what to do about a water ring are all on the materials page.",
                 align="center", color="muted"),
            buttons(button("Materials and care", "{{page:materials}}", style="tyche-outline"),
                    button("Read the FAQ", "{{page:faq}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Ordering", (
            ("Why six weeks?", "Because nothing is in stock. Boards are chosen for your piece, left to settle in the workshop for a fortnight, then cut, fitted, glued and oiled. The waiting is mostly timber acclimatising and oil curing."),
            ("Can I change a size?", "Usually. A different length or height is from $250 and adds a fortnight. A different design is a commission, and we will say so."),
            ("Can I see the timber first?", "Finish samples are free and take two days. For a table we will send photographs of the actual boards before we cut."),
        )),
        ("Delivery", (
            ("Who delivers it?", "Two of the people who made it, in our own van, to the room it is for. They assemble it and take the packaging away."),
            ("What if it will not fit?", "Tell us the narrowest point before you order and we will measure the piece against it. Tables come apart; sideboards do not."),
            ("Do you deliver outside the country?", "Not yet. A table that arrives damaged by a freight company is a table nobody can repair on the doorstep."),
        )),
        ("Afterwards", (
            ("Something has a mark. Can it be fixed?", "Almost always, by you, in an afternoon: sand along the grain and re-oil. Send a photograph if you would rather we did it."),
            ("The top has moved. Is that a fault?", "No. A few millimetres across a season is solid timber doing what it does, which is why the tops are built to allow it. A split is a fault, and it is covered."),
            ("What does the guarantee cover?", "Every joint, for ten years, for as long as you own the piece. It does not cover a finish worn through by use, which is a repair rather than a failure."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "Lead times, sizes, stairs, and what to do when something gets marked."),
                pad=("70", "50")),
        section(body, pad=("0", "80")),
    ])


def about():
    return "\n\n".join([
        section(page_intro("The workshop", "Four benches behind a mill",
                           "Oakhouse is six people making furniture to order in one room, with a showroom above it and nothing on a shelf."),
                pad=("70", "50")),
        section(image("workshop-1", IMAGES["workshop-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        story_split(
            "How we got here",
            "Nothing in stock, on purpose",
            "Holding stock means guessing sizes and finishes a year ahead, and then discounting whatever you guessed wrong. Cutting to order means six weeks, and it means the piece that arrives is the one that was wanted.",
            ["Six people, four benches, one showroom",
             "Timber from managed European forests",
             "Offcuts go to a furniture-making course down the road"],
            ("Read about the timbers", "{{page:materials}}"),
            "story-1", IMAGES["story-1"]),
        spec_rows([
            ("Pieces a year", "About 400"),
            ("People", "Six, four of them at benches"),
            ("Lead time", "Four to eight weeks, depending on the piece"),
            ("Guarantee", "Ten years on every joint"),
            ("Waste", "Offcuts to a local course; shavings to a farm"),
        ], "The workshop in numbers", kicker="About us", photo="journal-3", alt=IMAGES["journal-3"]),
        section(group("\n\n".join([
            heading("What we will not do", level=2),
            para("Veneer over chipboard, cam-lock fittings, or a finish that cannot be repaired in a room. None of those are wrong for every piece of furniture; they are wrong for furniture meant to be passed on, which is the only kind worth waiting six weeks for.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def delivery():
    rows = [
        ("Two-person delivery", "$90, into the room, assembled"),
        ("Free delivery", "On orders over $1,200"),
        ("Homeware only", "$8, sent by post"),
        ("Collection", "Free, from the yard, Thursday to Saturday"),
        ("Returns", "Fourteen days on stock items; made-to-order is made for you"),
    ]
    return "\n\n".join([
        section(page_intro("Delivery and returns", "Carried in, put together, packaging taken away",
                           "Furniture delivered to a doorstep is furniture you now have to move. Ours comes into the room it is for."),
                pad=("70", "50")),
        spec_rows(rows, "Delivery", kicker="What it costs", bg=None, photo="delivery-1", alt=IMAGES["delivery-1"]),
        section(group("\n\n".join([
            heading("Before it leaves", level=2),
            para("We call to agree a day, and we ask about stairs, lifts, corners and parking. A table that will not turn a landing is the one problem we cannot solve on the doorstep, so we would rather find it on the phone.",
                 color="muted"),
            heading("Returns", level=2),
            para("Homeware and stock items come back within fourteen days, unused. Made-to-order pieces are made to your size and finish, so they cannot: that is what the samples, the drawings and the phone call are for.",
                 color="muted"),
            heading("If it arrives damaged", level=2),
            para("It will not have been couriered, so this is rare. If it happens, the two people who delivered it will take it back the same day and it is repaired or remade.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("materials", "Materials and care", materials, "page-no-title"),
    ("trade", "Trade", trade, "page-no-title"),
    ("showroom", "Showroom", showroom, "page-no-title"),
    ("about", "The workshop", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("delivery-returns", "Delivery and returns", delivery, "page-no-title"),
    ("journal", "Journal", None, ""),
]

POSTS = [
    ("how-to-measure-for-a-table", "How to measure for a table, properly", "living-with-it", "journal-2", 6, [
        "The mistake is measuring the room. What matters is the space around the table: 90 cm from the edge to the nearest wall or radiator, or nobody can get past a pulled-out chair.",
        "Work backwards from that. A 200 cm table needs a room 380 cm long to be comfortable, and 340 cm to be usable. If the numbers do not work, a bench down one side buys you 30 cm, because a bench pushes in.",
        "Then measure the route in: the front door, the turn at the bottom of the stairs, the landing. Tables come apart and sideboards do not, and we would rather know before we cut.",
    ]),
    ("why-six-weeks", "Why it takes six weeks", "from-the-bench", "journal-1", 17, [
        "A fortnight of that is the timber sitting in the workshop doing nothing. Boards come out of a kiln at a lower moisture content than a house, and a table cut the day the wood arrives is a table that moves in its first winter.",
        "Then the joints. A drawbored mortise and tenon takes an hour a leg, against a minute for a bolt. It is also the reason a hundred-year-old table is still tight and a ten-year-old flat-pack is not.",
        "The last week is oil. Hardwax oil goes on thin, three coats, and each one wants a day. Rushing it gives you a surface that marks in a month, and we have tried.",
    ]),
    ("living-with-solid-timber", "Living with something that moves", "living-with-it", "journal-3", 34, [
        "A solid top is a little wider in August than in February. On a 90 cm table that is about two millimetres, and you will only notice it as a fractional overhang at the breadboard end.",
        "That movement is designed for. The tops are not glued across their width, the panels sit loose in their grooves, and the ends are pegged rather than fixed. Stop the wood moving and it splits instead.",
        "What you can do: keep it out of the path of a radiator or a wood burner, and do not stand it in front of a south-facing window for a year and expect the colour to be even. Both are heat, and heat is what solid timber minds.",
    ]),
]

MENU = [
    ("Tables", "{{cat:tables}}", "cat:tables"),
    ("Seating", "{{cat:seating}}", "cat:seating"),
    ("Storage", "{{cat:storage}}", "cat:storage"),
    ("Homeware", "{{cat:homeware}}", "cat:homeware"),
    ("Materials", "{{page:materials}}", "page:materials"),
    ("Showroom", "{{page:showroom}}", "page:showroom"),
    ("Trade", "{{page:trade}}", "page:trade"),
]


def menu():
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
            "content": header_part("Made to order in four to eight weeks &middot; delivered into the room",
                                   "See the lead times", "{{page:delivery-returns}}",
                                   layout="header-left-no-announcement"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "Six people making solid timber furniture to order, behind a mill. Nothing in stock, ten years on every joint.",
                [
                    ("Shop", [("Tables", "{{cat:tables}}"), ("Seating", "{{cat:seating}}"),
                              ("Storage", "{{cat:storage}}"), ("Homeware", "{{cat:homeware}}")]),
                    ("Learn", [("Materials and care", "{{page:materials}}"), ("Journal", "{{page:journal}}"),
                               ("FAQ", "{{page:faq}}"), ("Delivery and returns", "{{page:delivery-returns}}")]),
                    ("Oakhouse", [("The workshop", "{{page:about}}"), ("Showroom", "{{page:showroom}}"),
                                  ("Trade", "{{page:trade}}"), ("My account", "{{account}}")]),
                ],
                legal="Timber from managed European forests."),
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
    "journal": "How a piece is made, how to measure for one, and how to live with something that moves.",
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
            {"name": "Finish", "slug": "finish", "type": "select", "order_by": "menu_order", "terms": FINISHES},
            {"name": "Room", "slug": "room", "type": "select", "order_by": "menu_order", "terms": ROOMS},
            {"name": "Lead time", "slug": "lead-time", "type": "select", "order_by": "menu_order",
             "terms": ["In stock", "2–3 weeks", "4–6 weeks", "6–8 weeks"]},
        ],
    }

    products = piece_products()

    manifest = {
        "schema": 1,
        "slug": "oakhouse",
        "theme": {"slug": "tyche", "style": ["Oakhouse"]},
        "settings": {
            "title": "Oakhouse",
            "tagline": "Solid timber furniture, made to order",
            "front_page": "home",
            "posts_page": "journal",
            "currency": "USD",
            "country": "US:VT",
            "shipping": {"country": "US", "flat_rate": "90.00", "free_over": "1200"},
        },
        "counts": {"products": len(products), "pages": len(pages) - 1, "posts": len(posts), "images": len(IMAGES)},
    }

    written = [
        write("manifest.json", manifest),
        write("terms.json", terms),
        write("products.json", products),
        write("pages.json", pages),
        write("posts.json", posts),
        write("menus.json", [{"slug": "primary", "title": "Primary", "content": menu()}]),
        write("parts.json", parts()),
        write("images.json", [{"file": slug + ".webp", "alt": alt} for slug, alt in sorted(IMAGES.items())]),
    ]

    variations = sum(len(p.get("variations", [])) for p in products)
    print("  %d products (%d variations), %d pages, %d posts, %d images"
          % (len(products), variations, len(pages), len(posts), len(IMAGES)))
    print("  " + ", ".join(written))


if __name__ == "__main__":
    main()
