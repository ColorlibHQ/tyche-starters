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
    "hero-room": "A dining room with a long timber table and chairs in daylight",
    "hero-detail": "A close-up of a joint where a table leg meets the top",
    "cat-tables": "A timber dining table in an empty room",
    "cat-seating": "A wooden chair against a plain wall",
    "cat-storage": "A shelf unit holding books and ceramics",
    "cat-homeware": "A wool throw folded over the arm of a chair",
    "story-1": "A bench in a workshop with hand tools and shavings",
    "workshop-1": "A plane taking a shaving off a board",
    "materials-1": "Stacked oak boards seen end on",
    "showroom-1": "A room of furniture with daylight from one side",
    "delivery-1": "A finished piece wrapped in blankets",
    "contact-1": "A workshop door open onto a yard",
    "promo-1": "A close-up of an oiled timber surface",
    "journal-1": "A hand sanding an edge",
    "journal-2": "A room with a table and one chair",
    "journal-3": "Offcuts stacked beside a saw bench",
    "dining-table": "A long solid timber dining table",
    "extending-table": "A timber table with the leaf out",
    "desk": "A timber desk with two drawers",
    "bench": "A long timber bench",
    "dining-chair": "A timber dining chair seen from the front",
    "armchair": "A low armchair with a fabric seat",
    "stool": "A three-legged timber stool",
    "sideboard": "A long low sideboard with two doors",
    "shelf-unit": "An open shelf unit of timber boxes",
    "bookcase": "A tall bookcase against a white wall",
    "bedside-table": "A small bedside table with one drawer",
    "coffee-table": "A low timber coffee table",
    "mirror": "A round mirror in a timber frame",
    "wool-throw": "A folded wool throw",
    "linen-cushion": "A linen cushion on a chair",
    "ceramic-bowl": "A wide ceramic bowl on a table",
}

# slug, name, category, room, prices by finish or single, image, days ago,
# lead time, short line, long copy, spec rows
PIECES = [
    ("dining-table", "Linde Dining Table", "tables", "Dining", ("1480.00", "1780.00", "1620.00"),
     "dining-table", 4, "4–6 weeks",
     "A 200 cm table in solid timber, joined with drawbored mortise and tenon. Seats eight.",
     "The top is four boards, book-matched and held with breadboard ends so it can move with the seasons without splitting. The legs are drawbored into the rails, which is slower than a bolt and is the reason this outlives the room it goes in.",
     [("Size", "200 × 90 × 75 cm"), ("Weight", "62 kg"), ("Seats", "Eight, ten at a push"),
      ("Joint", "Drawbored mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("extending-table", "Linde Extending Table", "tables", "Dining", ("1780.00", "2080.00", "1920.00"),
     "extending-table", 11, "6–8 weeks",
     "The same table with a leaf that lives inside it. 180 cm, or 240 cm in about a minute.",
     "A single leaf on timber runners, stored under the top rather than in a cupboard, because the leaf nobody can find is the leaf nobody uses. Closed it is a table for six; open it takes ten.",
     [("Size", "180 or 240 × 90 × 75 cm"), ("Weight", "74 kg"), ("Seats", "Six, or ten open"),
      ("Joint", "Drawbored mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "6–8 weeks")]),
    ("desk", "Ash Desk", "tables", "Study", ("980.00", "1180.00", "1080.00"),
     "desk", 18, "4–6 weeks",
     "A desk at writing height with two drawers on timber runners and a cable slot at the back.",
     "Deep enough for a screen and a notebook at once, and high enough at 74 cm that a standard chair fits under it. The drawers run on waxed timber rather than metal slides, so they are silent and will still work in thirty years.",
     [("Size", "140 × 68 × 74 cm"), ("Weight", "38 kg"), ("Drawers", "Two, on waxed runners"),
      ("Joint", "Mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("bench", "Linde Bench", "seating", "Dining", ("520.00", "620.00", "570.00"),
     "bench", 25, "4–6 weeks",
     "A 180 cm bench in the same timber as the table, for the side against the wall.",
     "Benches seat more people than chairs and take up less room when they are pushed in, which is the whole argument for them. Solid throughout, so it can be stood on to reach a high shelf without anyone worrying.",
     [("Size", "180 × 35 × 45 cm"), ("Weight", "24 kg"), ("Seats", "Three adults"),
      ("Joint", "Mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("dining-chair", "Bow Chair", "seating", "Dining", ("340.00", "410.00", "375.00"),
     "dining-chair", 2, "4–6 weeks",
     "A steam-bent back, a shaped seat, and no fastening you can see.",
     "The back is one piece of timber bent over a form and left in it for a fortnight. The seat is scooped by hand, which takes an hour and is the difference between a chair you sit on for twenty minutes and one you sit on all evening.",
     [("Size", "46 × 52 × 82 cm"), ("Weight", "5.4 kg"), ("Seat height", "46 cm"),
      ("Joint", "Steam-bent back, wedged tenons"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("armchair", "Reading Chair", "seating", "Living", ("880.00", "1040.00", "960.00"),
     "armchair", 9, "6–8 weeks",
     "A low frame with a wool seat, for the corner with the lamp in it.",
     "Reclined a few degrees more than a dining chair, with arms at the height a book rests on. The cushions are wool over horsehair, and they can be recovered without touching the frame.",
     [("Size", "68 × 78 × 74 cm"), ("Weight", "14 kg"), ("Seat height", "40 cm"),
      ("Cushion", "Wool over horsehair, recoverable"), ("Finish", "Hardwax oil"), ("Lead time", "6–8 weeks")]),
    ("stool", "Workshop Stool", "seating", "Study", ("180.00", "220.00", "200.00"),
     "stool", 30, "2–3 weeks",
     "Three legs, a dished seat, and nothing else. It is the first thing every maker here builds.",
     "Three legs never rock on an uneven floor, which is why every workshop stool has three. The seat is dished with a travisher, and the legs are wedged from above so they tighten rather than loosen with use.",
     [("Size", "34 × 34 × 62 cm"), ("Weight", "3.8 kg"), ("Seat height", "62 cm"),
      ("Joint", "Wedged through-tenons"), ("Finish", "Hardwax oil"), ("Lead time", "2–3 weeks")]),
    ("sideboard", "Hollow Sideboard", "storage", "Living", ("1240.00", "1480.00", "1360.00"),
     "sideboard", 14, "6–8 weeks",
     "Two doors, one long shelf, and a back you would not mind seeing.",
     "Dovetailed at the corners and panelled at the back, because a piece that will be pulled out to hoover behind should look finished from every side. The doors are solid, so they are heavy: the hinges are rated for it.",
     [("Size", "160 × 45 × 78 cm"), ("Weight", "54 kg"), ("Inside", "One adjustable shelf"),
      ("Joint", "Hand-cut dovetails"), ("Finish", "Hardwax oil"), ("Lead time", "6–8 weeks")]),
    ("shelf-unit", "Stack Shelf", "storage", "Living", ("620.00", "740.00", "680.00"),
     "shelf-unit", 7, "4–6 weeks",
     "Four open boxes that stack, bolt together, or stand apart.",
     "Bought as four and arranged however the room needs: stacked in a column, in a row under a window, or split between two walls. Each box holds 25 kg, which is more books than you think.",
     [("Size", "40 × 34 × 40 cm each"), ("Weight", "7 kg each"), ("Load", "25 kg a box"),
      ("Joint", "Hand-cut dovetails"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("bookcase", "Tall Bookcase", "storage", "Study", ("980.00", "1180.00", "1080.00"),
     "bookcase", 21, "6–8 weeks",
     "Five shelves, 200 cm tall, with a wall fixing in the box.",
     "The shelves are 3 cm thick so they do not sag under a run of hardbacks, and they sit in housed joints rather than on pins. It comes with a bracket and the honest advice to use it.",
     [("Size", "90 × 32 × 200 cm"), ("Weight", "46 kg"), ("Shelves", "Five, housed"),
      ("Joint", "Housed and wedged"), ("Finish", "Hardwax oil"), ("Lead time", "6–8 weeks")]),
    ("bedside-table", "Bedside Table", "storage", "Bedroom", ("380.00", "460.00", "420.00"),
     "bedside-table", 28, "4–6 weeks",
     "One drawer, one shelf, and a top big enough for a lamp and a glass of water.",
     "Low enough to reach from a bed and narrow enough for the gap most bedrooms leave. The drawer is dovetailed and runs on waxed timber, so it opens quietly at two in the morning.",
     [("Size", "45 × 38 × 55 cm"), ("Weight", "11 kg"), ("Drawer", "One, dovetailed"),
      ("Joint", "Mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("coffee-table", "Low Table", "tables", "Living", ("640.00", "760.00", "700.00"),
     "coffee-table", 16, "4–6 weeks",
     "A 110 cm low table with a shelf underneath for the things that live on the floor.",
     "Sized against a three-seat sofa and set at 40 cm, which is the height a cup can be put down from without leaning. The lower shelf is slatted, so it holds magazines and not dust.",
     [("Size", "110 × 55 × 40 cm"), ("Weight", "18 kg"), ("Shelf", "Slatted, 8 cm clear"),
      ("Joint", "Mortise and tenon"), ("Finish", "Hardwax oil"), ("Lead time", "4–6 weeks")]),
    ("mirror", "Round Mirror", "homeware", "Bedroom", ("240.00",), "mirror", 12, "2–3 weeks",
     "A 60 cm mirror in a steam-bent frame, with the fixing already on the back.",
     "The frame is one length of timber bent into a ring, so there is no joint to open up in a steamy room. Hangs on a single screw and sits flat against the wall.",
     [("Size", "60 cm across, 4 cm deep"), ("Weight", "3.2 kg"), ("Glass", "4 mm, silvered"),
      ("Fixing", "Keyhole plate, screw included"), ("Lead time", "2–3 weeks")]),
    ("wool-throw", "Wool Throw", "homeware", "Living", ("95.00",), "wool-throw", 5, "In stock",
     "Undyed lambswool, woven in a mill that has been at it since 1856.",
     "Heavy enough to be worth having on a chair and soft enough to use. Undyed, so the colour is the sheep's rather than a dye lot, which means the next one will be close but not identical.",
     [("Size", "130 × 180 cm"), ("Weight", "1.1 kg"), ("Material", "100% lambswool, undyed"),
      ("Care", "Cool wool wash, dry flat"), ("Lead time", "In stock")]),
    ("linen-cushion", "Linen Cushion", "homeware", "Living", ("65.00",), "linen-cushion", 19, "In stock",
     "Washed linen with a feather insert and a button placket, not a zip.",
     "The cover comes off for washing and goes back on without a fight. Linen creases, and it is supposed to: it is the only upholstery fabric that looks better after a year.",
     [("Size", "50 × 50 cm"), ("Material", "Washed linen, feather insert"),
      ("Closure", "Four-button placket"), ("Care", "Machine wash cool"), ("Lead time", "In stock")]),
    ("ceramic-bowl", "Serving Bowl", "homeware", "Dining", ("78.00",), "ceramic-bowl", 23, "In stock",
     "A wide stoneware bowl, thrown by hand and glazed inside only.",
     "Big enough for a salad for six and heavy enough not to travel across the table. The outside is left unglazed, so it warms up in the hand the way a mug does.",
     [("Size", "28 cm across, 11 cm deep"), ("Weight", "1.4 kg"), ("Material", "Stoneware, glazed inside"),
      ("Care", "Dishwasher safe"), ("Lead time", "In stock")]),
]

FINISHES = ["Oak", "Walnut", "Blackened oak"]
ROOMS = ["Dining", "Living", "Bedroom", "Study"]

CATEGORIES = [
    ("Tables", "tables", "Dining, low and writing tables, from 110 cm to 240 cm."),
    ("Seating", "seating", "Chairs, benches and stools, shaped where it matters."),
    ("Storage", "storage", "Dovetailed boxes, shelves and sideboards that look finished from the back."),
    ("Homeware", "homeware", "The wool, linen and stoneware that go on top of the furniture."),
]

POST_CATEGORIES = [
    ("From the bench", "from-the-bench", "How a piece is made, and why it takes six weeks."),
    ("Living with it", "living-with-it", "Measuring, caring for and repairing solid timber."),
]

REVIEWS = {
    "dining-table": [
        ("Martha K.", 5, "Six weeks to the day, delivered by two people who put it together and took the packaging away. It is the first table I have owned that does not wobble."),
        ("Owen R.", 5, "The breadboard ends have moved a couple of millimetres over the winter, exactly as the care page said they would. No split."),
    ],
    "dining-chair": [
        ("Priya S.", 4, "Comfortable for a long dinner, which was the point. Four of them and only one had a mark, which they refinished without argument."),
    ],
    "wool-throw": [
        ("Jonas L.", 5, "Heavier than I expected and no smell of dye, because there is no dye."),
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
            "featured": slug in ("dining-table", "dining-chair", "shelf-unit", "sideboard",
                                 "wool-throw", "stool"),
            "attributes": [
                {"name": "Room", "slug": "room", "options": [room], "visible": True},
                {"name": "Lead time", "slug": "lead-time", "options": [lead], "visible": True},
            ],
            "reviews": [{"author": author, "rating": rating, "content": content}
                        for author, rating, content in REVIEWS.get(slug, [])],
        }
        if len(prices) == 1:
            product["type"] = "simple"
            product["price"] = prices[0]
        else:
            # One photograph, three finishes: say which one is in the picture
            # rather than letting a walnut buyer think they are looking at it.
            product["description"] = product["description"].replace(
                "</ul>", "<!-- wp:list-item -->\n<li>Photographed in: Oak</li>\n<!-- /wp:list-item -->\n</ul>")
            product["type"] = "variable"
            product["attributes"].insert(0, {"name": "Finish", "slug": "finish", "options": list(FINISHES),
                                             "visible": True, "variation": True})
            product["variations"] = [{"attributes": {"finish": finish}, "price": price,
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
        category_tiles([("tables", "Tables", "Dining, low and writing"),
                        ("seating", "Seating", "Chairs, benches, stools"),
                        ("storage", "Storage", "Boxes, shelves, sideboards"),
                        ("homeware", "Homeware", "Wool, linen and stoneware")],
                       "Shop by room", kicker="The catalogue", link=("See everything", "{{shop}}")),
        product_row("new-arrivals", "New", "Just off the bench", "Shop everything", "{{shop}}"),
        care_cards(PROMISES, "How we work", kicker="The basics", bg="surface"),
        spec_rows(
            [("Size", "200 × 90 × 75 cm"), ("Weight", "62 kg"), ("Seats", "Eight, ten at a push"),
             ("Timber", "European oak, walnut or blackened oak"), ("Joint", "Drawbored mortise and tenon"),
             ("Lead time", "4–6 weeks")],
            "Linde table, in short", kicker="This month's piece",
            photo="dining-table", alt=IMAGES["dining-table"]),
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
