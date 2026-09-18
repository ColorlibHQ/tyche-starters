#!/usr/bin/env python3
"""Build the Dew starter: skincare from a small lab.

    python3 .dev/dew.py

A skincare shop is bought from by people who have been lied to, so the whole
store is built around saying less and proving it: one active per bottle, the
strength on the front, the date it was made on the back. What it exercises that
the others do not is a shop where the product photograph tells you almost
nothing -- one white bottle looks like another -- so the words, the ingredient
glossary and the routine have to carry the sale.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, care_cards, check_list, chips, column, columns, cta, footer_part, group,
    header_part, heading, image, numbered_steps, para, paragraphs, product_row, section,
    section_head, spec_list, spec_rows, spotlight_hero, story_split, eyebrow,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dew")

accordion = bp.accordion
page_intro = bp.page_intro

# ---------------------------------------------------------------------------
# The catalogue. Provisional until the photographs are in: a skincare shop can
# only sell what it can show, and an unbranded bottle is harder to find than an
# unbranded plant.
# ---------------------------------------------------------------------------
IMAGES = {
    "hero-1": "A frosted glass serum bottle with a dropper on a pale pink surface",
    "story-1": "Bottles being filled by hand at a bench",
    "routine-1": "A row of unlabelled bottles and jars along a bathroom shelf",
    "ingredients-1": "Oats, chamomile and a dish of clay on a pale surface",
    "about-1": "A small work bench with beakers and a set of scales",
    "contact-1": "A basin with a towel and two bottles beside it",
    "promo-1": "A hand holding a dropper over an open palm",
    "texture-1": "A smear of cream on a pale pink surface",
    "journal-1": "A palm with a drop of serum in it",
    "journal-2": "A bottle on a windowsill in morning light",
    "journal-3": "A jar of balm with the lid beside it",
    "barrier-serum": "A dropper bottle of clear serum",
    "hydrating-serum": "A dropper bottle beside a glass of water",
    "night-serum": "An amber dropper bottle on a dark surface",
    "exfoliating-toner": "A tall bottle of clear toner",
    "gel-cleanser": "A pump bottle of clear gel cleanser",
    "cream-cleanser": "A tube of cream cleanser",
    "gel-cream": "An open jar of light gel cream",
    "night-balm": "An open jar of thick balm",
    "squalane-oil": "A small bottle of clear oil",
    "daily-spf": "A white tube of sunscreen",
    "lip-balm": "A small tin of lip balm",
    "starter-set": "Three small bottles standing together",
}

# slug, name, category, prices (30 ml, 50 ml) or (single,), image, days ago,
# skin type, short line, long copy, spec rows
PRODUCTS = [
    ("barrier-serum", "Barrier Serum", "treat", ("24.00", "38.00"), "barrier-serum", 2,
     "All skin types",
     "Niacinamide at 10%, with zinc. For skin that is red, reactive, or breaking out.",
     "Ten per cent niacinamide and one per cent zinc, in water and glycerin, and nothing else worth naming. It is the one bottle most people should start with: it calms redness, it evens out tone over weeks rather than days, and it does not fight with anything else you use.",
     [("Active", "Niacinamide 10%, zinc 1%"), ("Texture", "Watery, absorbs in seconds"),
      ("Use", "Morning and evening, after cleansing"), ("Skin", "All, including sensitive"),
      ("pH", "5.5 to 6.0"), ("Size", "30 ml and 50 ml")]),
    ("hydrating-serum", "Hydrating Serum", "treat", ("22.00", "34.00"), "hydrating-serum", 9,
     "Dry skin",
     "Hyaluronic acid in three weights, for skin that feels tight by lunchtime.",
     "Three molecular weights, so it holds water at the surface and a little deeper rather than sitting on top. Put it on damp skin and follow it with a moisturiser, or it will take water from your face instead of giving it.",
     [("Active", "Hyaluronic acid 2%"), ("Texture", "Light gel"),
      ("Use", "On damp skin, then moisturise"), ("Skin", "Dry and dehydrated"),
      ("pH", "5.0 to 5.5"), ("Size", "30 ml and 50 ml")]),
    ("night-serum", "Night Serum", "treat", ("32.00", "48.00"), "night-serum", 16,
     "Combination skin",
     "Retinal at 0.05%, in an amber bottle because light ruins it.",
     "Retinal rather than retinol: fewer conversions in the skin, so a lower strength does the same work. Start twice a week, buffer it with moisturiser, and wear sunscreen in the morning or do not bother at all.",
     [("Active", "Retinal 0.05%"), ("Texture", "Light lotion"),
      ("Use", "Evening, twice a week to start"), ("Skin", "Not while pregnant"),
      ("pH", "5.5 to 6.0"), ("Size", "30 ml and 50 ml")]),
    ("exfoliating-toner", "Exfoliating Toner", "treat", ("20.00", "30.00"), "exfoliating-toner", 24,
     "Oily skin",
     "Salicylic acid at 2%, for blocked pores and the bumps that come with them.",
     "An oil-soluble acid, so it works inside a pore rather than on top of it. Twice a week is plenty for most people, and every night is how you end up with a stripped, shiny face that produces more oil than it did before.",
     [("Active", "Salicylic acid 2%"), ("Texture", "Water"),
      ("Use", "Evening, twice a week"), ("Skin", "Oily and congested"),
      ("pH", "3.5 to 4.0"), ("Size", "30 ml and 50 ml")]),
    ("gel-cleanser", "Gel Cleanser", "cleanse", ("18.00",), "gel-cleanser", 5,
     "Oily skin",
     "A low-foam gel that takes sunscreen off without stripping anything.",
     "Enough surfactant to shift a day of sunscreen and city air, and not so much that your face feels tight afterwards. If it squeaks, it was too strong: this one does not.",
     [("Use", "Morning and evening"), ("Texture", "Low-foam gel"),
      ("Skin", "Oily and combination"), ("pH", "5.0 to 5.5"), ("Size", "150 ml")]),
    ("cream-cleanser", "Cream Cleanser", "cleanse", ("18.00",), "cream-cleanser", 12,
     "Dry skin",
     "A milky cleanser for skin that hates foam.",
     "Takes make-up and sunscreen off with a flannel and warm water, and leaves the film your face actually needs. Winter, or dry skin, or any morning when washing hurts.",
     [("Use", "Evening, or morning in winter"), ("Texture", "Milky cream"),
      ("Skin", "Dry and sensitive"), ("pH", "5.5 to 6.0"), ("Size", "150 ml")]),
    ("gel-cream", "Gel Cream", "moisturise", ("26.00", "40.00"), "gel-cream", 7,
     "Combination skin",
     "A light moisturiser that disappears, for people who hate the feel of cream.",
     "Glycerin and squalane in a gel base: it holds water without the weight, and it sits under sunscreen without pilling, which is the only test most moisturisers fail.",
     [("Texture", "Gel cream"), ("Use", "Morning and evening"),
      ("Skin", "Combination and oily"), ("Under SPF", "Yes, it does not pill"),
      ("Size", "30 ml and 50 ml")]),
    ("night-balm", "Night Balm", "moisturise", ("32.00", "46.00"), "night-balm", 14,
     "Dry skin",
     "A thick occlusive balm for the last step of a winter evening.",
     "Shea, squalane and ceramides, thick enough to leave a sheen you will see on the pillow. It goes on last, over everything, and it is the difference between a serum working and a serum evaporating.",
     [("Texture", "Thick balm"), ("Use", "Evening, last step"),
      ("Skin", "Dry, or anyone in winter"), ("Ceramides", "3%"),
      ("Size", "30 ml and 50 ml")]),
    ("squalane-oil", "Squalane Oil", "moisturise", ("24.00", "36.00"), "squalane-oil", 21,
     "All skin types",
     "One ingredient, from olives. Two drops is the whole dose.",
     "Squalane and nothing else: no fragrance, no vitamin E, no botanical extract to make the label look busier. It is the safest oil for skin that reacts, and the least interesting to write about, which is rather the point.",
     [("Ingredients", "Squalane, 100%"), ("Texture", "Dry oil"),
      ("Use", "Evening, over moisturiser"), ("Skin", "All, including acne-prone"),
      ("Size", "30 ml and 50 ml")]),
    ("daily-spf", "Daily SPF 50", "protect", ("26.00",), "daily-spf", 3,
     "All skin types",
     "SPF 50, no white cast, no smell. The one step that does most of the work.",
     "A modern filter blend that does not leave a grey film or sting the eyes, in a tube big enough to use properly. Two fingers' length for a face and neck, every morning, or the rest of the shelf is decoration.",
     [("Protection", "SPF 50, UVA-PF 18"), ("Texture", "Light lotion"),
      ("Use", "Every morning, reapply at noon"), ("Skin", "All, including sensitive"),
      ("Size", "50 ml")]),
    ("lip-balm", "Lip Balm", "moisturise", ("9.00",), "lip-balm", 28,
     "All skin types",
     "Petrolatum and shea in a tin. It works, and it is nine dollars.",
     "There is no clever version of this. An occlusive, a wax and a tin that fits in a pocket, with nothing in it to make your lips tingle, because tingling is not a feature.",
     [("Ingredients", "Petrolatum, shea, beeswax"), ("Use", "Whenever"),
      ("Skin", "All"), ("Size", "15 ml tin")]),
    ("starter-set", "The Starter Set", "sets", ("58.00",), "starter-set", 1,
     "All skin types",
     "Cleanser, barrier serum and sunscreen. The three that matter, at a saving.",
     "If you are starting from nothing, this is the routine: wash, calm, protect. Full sizes of the gel cleanser, the barrier serum and the daily sunscreen, which is eight dollars less than buying them apart.",
     [("In the box", "Gel cleanser, barrier serum, SPF 50"), ("Saving", "$8 against buying apart"),
      ("Skin", "All"), ("Size", "Full sizes")]),
]

CATEGORIES = [
    ("Cleanse", "cleanse", "Two cleansers: a gel for oily skin and a cream for skin that hates foam."),
    ("Treat", "treat", "One active per bottle, at a strength that does something, with the number on the front."),
    ("Moisturise", "moisturise", "Gel, balm and oil, from lightest to heaviest. Pick by season rather than by skin type."),
    ("Protect", "protect", "The step that does most of the work, in a tube big enough to use properly."),
    ("Sets", "sets", "The routine in one box, for a few dollars less than buying it apart."),
]

POST_CATEGORIES = [
    ("Skin school", "skin-school", "How to use the things on the shelf, and how often."),
    ("From the lab", "from-the-lab", "How it is made, and why the label says what it says."),
]

SIZES = ["30 ml", "50 ml"]
SKIN_TYPES = ["All skin types", "Dry skin", "Oily skin", "Combination skin"]

REVIEWS = {
    "barrier-serum": [
        ("Dry skin, 34", 5, "Three weeks and the red patches around my nose have gone. No sting, no smell, nothing."),
        ("Combination skin, 27", 4, "Does what it says. The dropper is a bit stiff, which is my only complaint."),
    ],
    "daily-spf": [
        ("Oily skin, 41", 5, "The first sunscreen I have finished a whole tube of. No cast, no eye sting."),
    ],
    "night-balm": [
        ("Dry skin, 52", 5, "Winter face sorted. I use it over the serum and wake up without the tight feeling."),
    ],
}

PROMISES = [
    ("droplet", "Fragrance-free, all of it",
     "No perfume, no essential oils, nothing added to make it smell like anything. The most common reason a face reacts is the thing we left out."),
    ("shield-check", "One active per bottle",
     "If a bottle has niacinamide in it, that is what it is for. Five actives in one formula means nobody can tell you which one is working, or which one is stinging."),
    ("package", "A patch test in every box",
     "A 2 ml sachet of whatever you ordered, so you can try it behind your ear for three days before you put it on your face."),
]

ROUTINE_MORNING = [
    ("Wash, or just rinse", "If you cleansed last night, warm water is enough. Oily skin, use the gel."),
    ("Barrier serum", "Four drops, pressed in rather than rubbed. Give it a minute."),
    ("Moisturiser", "Gel cream in summer, balm in winter. Enough to stop the next step dragging."),
    ("Sunscreen", "Two fingers' length for face and neck. This is the step that pays for the others."),
]

ROUTINE_EVENING = [
    ("Take the day off", "Cleanse twice if you wore sunscreen: once to break it up, once to wash it off."),
    ("Treat, on the nights you treat", "Retinal twice a week, acid twice a week, never the same night."),
    ("Serum", "Barrier serum on the nights you are not treating. Hydrating serum on damp skin."),
    ("Seal it", "Balm last. If your skin is fine without it, skip it: it is not a moral failing."),
]

GLOSSARY = [
    ("Niacinamide", "Vitamin B3. At 10% it calms redness, helps the skin hold water and evens tone over a couple of months. It is the least glamorous active on the shelf and the one that suits the most faces."),
    ("Hyaluronic acid", "A humectant: it holds water. It needs water to hold, which is why it goes on damp skin and gets sealed with a moisturiser. On its own, in a dry room, it can make skin feel tighter."),
    ("Retinal", "A step closer to the active form than retinol, so a smaller number does the same work with less irritation. It is destroyed by light, which is why it is in an amber bottle and not a clear one."),
    ("Salicylic acid", "Oil-soluble, so it gets inside a pore rather than working on the surface. Good for blocked pores and the bumps that come with them, and easy to overdo."),
    ("Ceramides", "The mortar between skin cells. Skin that is flaky, tight or stinging when you put things on it is usually short of them."),
    ("Squalane", "An emollient from olives. One ingredient, no smell, no reaction in almost anyone, which is why it is in half the shelf and on its own in one bottle."),
    ("Glycerin", "The most boring, most useful humectant there is. It is near the top of most of these labels and it is not a filler."),
    ("Zinc oxide", "A mineral filter that sits on skin and reflects. In the serum it is there at 1% to help with oil, not for sun protection -- that is what the tube is for."),
]

LEFT_OUT = [
    "Fragrance, and the essential oils people use instead of admitting it is fragrance",
    "Denatured alcohol, which makes a serum feel fast and a face feel tight",
    "Colour, in anything",
    "Claims about cells, which we cannot prove and neither can anyone else",
]


def product_list():
    products = []
    for slug, name, category, prices, photo, days, skin, short, long_copy, spec in PRODUCTS:
        product = {
            "slug": slug,
            "name": name,
            "sku": "DW-" + slug[:3].upper(),
            "categories": [category],
            "image": photo + ".webp",
            "short_description": short,
            "description": paragraphs(long_copy) + "\n\n" + spec_list(spec),
            "days_ago": days,
            "stock_status": "instock",
            "featured": slug in ("barrier-serum", "daily-spf", "gel-cream", "squalane-oil",
                                 "gel-cleanser", "night-balm"),
            "attributes": [{"name": "Skin type", "slug": "skin-type", "options": [skin], "visible": True}],
            "reviews": [{"author": author, "rating": rating, "content": content}
                        for author, rating, content in REVIEWS.get(slug, [])],
        }
        if len(prices) == 1:
            product["type"] = "simple"
            product["price"] = prices[0]
        else:
            product["type"] = "variable"
            product["attributes"].insert(0, {"name": "Size", "slug": "size", "options": list(SIZES),
                                             "visible": True, "variation": True})
            product["variations"] = [{"attributes": {"size": size}, "price": price,
                                      "sku": "DW-%s-%s" % (slug[:3].upper(), size.split()[0])}
                                     for size, price in zip(SIZES, prices)]
        products.append(product)
    return products


def home():
    return "\n\n".join([
        spotlight_hero(
            "Niacinamide 10% + zinc 1%",
            "The serum that calms, then clears",
            "One active, at a strength that does something, in a bottle with the date it was made on the back. Nothing else in it.",
            ["Fragrance-free", "30 ml and 50 ml", "Patch test in every box"],
            ("Shop the serum", "{{product:barrier-serum}}"),
            ("Read the ingredients", "{{page:ingredients}}"),
            "hero-1", IMAGES["hero-1"]),
        product_row("new-arrivals", "New", "Just made", "Shop everything", "{{shop}}"),
        care_cards(PROMISES, "What comes in the box", kicker="The basics", bg="surface"),
        product_row("featured", "The shelf", "What most people buy", "Shop everything", "{{shop}}", carousel=True),
        spec_rows(
            [("Active", "Niacinamide 10%, zinc 1%"), ("Texture", "Watery, absorbs in seconds"),
             ("Use", "Morning and evening, after cleansing"), ("Skin", "All, including sensitive"),
             ("pH", "5.5 to 6.0"), ("Size", "30 ml and 50 ml")],
            "Barrier serum, in short", kicker="This month's bottle",
            photo="barrier-serum", alt=IMAGES["barrier-serum"]),
        numbered_steps(ROUTINE_MORNING, "A morning, in four steps", kicker="The routine"),
        story_split(
            "The lab",
            "Made in batches of four hundred",
            "Everything here is mixed, filled and labelled in one room in California, in batches small enough that a formula can be changed when it is wrong rather than when the stock runs out.",
            ["Every bottle dated on the back",
             "Formulas changed when they are wrong, not when the stock runs out",
             "Sixty days to send anything back, opened or not"],
            ("Read about the lab", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        journal_row(),
        cta(
            "Samples",
            "Tell us your skin, we will send three",
            "Skincare is bought blind and returned for the same reason. Make an account, say what your skin does, and the next order comes with three sachets chosen for it rather than three chosen for the warehouse.",
            ["Three sachets with every order",
             "A patch test of whatever you bought",
             "Sixty days to change your mind, opened or not"],
            ("Create an account", "{{account}}"),
            ("Read the routine", "{{page:routine}}"),
            "promo-1"),
    ])


def journal_row():
    body = section_head("From the lab", kicker="Journal", link_text="Read the journal", link_href="{{page:journal}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def ingredients():
    return "\n\n".join([
        section(page_intro("Ingredients", "What is in it, and what it does",
                           "Eight things worth knowing, written out in full. If a bottle has one of these in it, the number on the front is how much."),
                pad=("70", "50")),
        section(group(accordion(GLOSSARY, cls="tyche-faq"), layout="constrained", content_size="780px"),
                pad=("0", "60")),
        section(image("ingredients-1", IMAGES["ingredients-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n\n".join([
            heading("What we leave out", level=2),
            para("Not as a claim to virtue: each of these is left out for a reason we can say in one line.",
                 color="muted"),
            check_list(*LEFT_OUT),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def routine():
    return "\n\n".join([
        section(page_intro("The routine", "Four steps in the morning, four at night",
                           "Most of a routine is the order and the frequency. This is ours, and it is shorter than you expect."),
                pad=("70", "50")),
        numbered_steps(ROUTINE_MORNING, "Morning", kicker="Before the day"),
        numbered_steps(ROUTINE_EVENING, "Evening", kicker="After it"),
        spec_rows(
            [("Cleanser", "Twice a day, or once if your skin is dry"),
             ("Barrier serum", "Twice a day, every day"),
             ("Hydrating serum", "On damp skin, whenever it feels tight"),
             ("Retinal", "Twice a week to start, four times if it suits you"),
             ("Exfoliating toner", "Twice a week, never on a retinal night"),
             ("Sunscreen", "Every morning, all year, reapply at noon")],
            "How often", kicker="A rough guide", photo="routine-1", alt=IMAGES["routine-1"]),
        section(group("\n\n".join([
            heading("If you only do two things", level=2),
            para("Sunscreen in the morning and a moisturiser at night will do more than any serum on this shelf. Everything else is an improvement on a routine that already exists, which is why we would rather sell you a $26 tube than a $48 bottle.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def about():
    return "\n\n".join([
        section(page_intro("The lab", "A small room, a set of scales and a lot of dating labels",
                           "Dew is four people making a dozen products in California. Everything is mixed, filled and labelled here."),
                pad=("70", "50")),
        section(image("about-1", IMAGES["about-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        story_split(
            "How it is made",
            "Four hundred bottles at a time",
            "A batch of four hundred takes a morning. It also means a formula can be changed the week we learn something, instead of waiting out a year of stock, and that every bottle can carry the date it was filled rather than a best-before that means nothing.",
            ["Mixed, filled and labelled in one room",
             "Every bottle dated, not just batch-coded",
             "Nothing tested on animals, and nothing sold where that is required"],
            ("Read the ingredients", "{{page:ingredients}}"),
            "story-1", IMAGES["story-1"]),
        spec_rows([
            ("Products", "Twelve, and we would rather it stayed twelve"),
            ("Batch size", "400 bottles"),
            ("Ingredients in the serum", "Six, including the water"),
            ("Time from filling to shelf", "Eight days, most of it stability testing"),
            ("People", "Four"),
        ], "The lab in numbers", kicker="About us", photo="promo-1", alt=IMAGES["promo-1"]),
        section(group("\n\n".join([
            heading("What we will not say", level=2),
            para("That anything here repairs, renews or rebuilds. Skin is not a wall. These are well-made basics at strengths that have been studied, and the difference between a good routine and a bad one is mostly whether you use it.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def contact():
    details = columns(*[
        column(group("\n".join([
            bp.icon("tyche/" + name, cls="tyche-icon tyche-icon--large"),
            heading(title, level=2, size="large", cls="tyche-usp__title"),
            para(body, color="muted"),
        ]), layout="flex", orientation="vertical", gap="20", cls="tyche-usp"))
        for name, title, body in (
            ("headset", "Ask us anything", "hello@example.com<br>Tell us what your skin does and we will tell you what to skip."),
            ("clock", "When we reply", "Within a working day<br>Written by the people who make it"),
            ("map-pin", "The lab", "Not open to visitors<br>Returns go to the address on the packing slip"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Ask before you buy",
                           "We would rather talk you out of a bottle than have it come back. Say what your skin does and what you already use."),
                pad=("70", "50")),
        section(details, pad=("0", "60")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Strengths, order of use and what not to mix are all in the ingredients and routine pages.",
                 align="center", color="muted"),
            buttons(button("Read the ingredients", "{{page:ingredients}}", style="tyche-outline"),
                    button("Read the FAQ", "{{page:faq}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Choosing", (
            ("Where do I start?", "The barrier serum, a moisturiser and the sunscreen. That is a whole routine, and it is the one we would buy first."),
            ("Which cleanser?", "Gel if your face is oily or you wear sunscreen daily; cream if washing leaves your skin tight. If you are between the two, the gel."),
            ("Is any of it for sensitive skin?", "All of it is fragrance-free, which is the single biggest cause of reactions. The acid and the retinal are the two to introduce slowly."),
        )),
        ("Using it", (
            ("Can I use the retinal and the acid together?", "Not on the same night. Alternate them, and skip both if your skin is stinging."),
            ("How long before it works?", "The serum, about six weeks for tone. The acid, a fortnight for texture. Sunscreen works the day you start."),
            ("Does the sunscreen leave a white cast?", "No. It is a modern filter blend rather than a mineral one, which is also why it does not sting eyes."),
            ("What is the sachet in my box?", "A patch test of whatever you ordered. Behind the ear, three days, before it goes near your face."),
        )),
        ("Orders", (
            ("Can I return something I have opened?", "Yes, within sixty days. Skincare cannot be judged unopened, so a return policy that requires a seal is a policy against being used."),
            ("How long does it last once opened?", "Six months for the serums, twelve for the balm and the oil. The date on the back is when it was filled."),
            ("Do you ship outside the country?", "Not yet. The sunscreen is regulated differently almost everywhere, and shipping a partial routine seemed worse than waiting."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "What to start with, what not to mix, and what happens if it does not suit you."),
                pad=("70", "50")),
        section(body, pad=("0", "80")),
    ])


def delivery():
    rows = [
        ("Standard delivery", "$5, two to four working days"),
        ("Free delivery", "On orders over $45"),
        ("Express", "$12, next working day if ordered before noon"),
        ("Returns", "Sixty days, opened or not"),
        ("Samples", "Three sachets with every order"),
    ]
    return "\n\n".join([
        section(page_intro("Delivery and returns", "Sixty days, opened or not",
                           "Skincare cannot be judged through a seal, so a policy that requires one is a policy against trying it."),
                pad=("70", "50")),
        spec_rows(rows, "Delivery", kicker="What it costs", bg=None, photo="texture-1", alt=IMAGES["texture-1"]),
        section(group("\n\n".join([
            heading("Returns", level=2),
            para("Sixty days from delivery, whether or not it has been opened. Tell us what it did and we will refund it: a bottle that did not suit you is worth more to us as a sentence than as stock.",
                 color="muted"),
            heading("If it reacts", level=2),
            para("Stop using it, and email us before you throw it away. Nine times out of ten it is the acid or the retinal introduced too fast, and the fix is frequency rather than a different bottle.",
                 color="muted"),
            heading("Damaged in the post", level=2),
            para("Photograph the box within 48 hours and we will send another. Glass travels in a moulded insert, but couriers are couriers.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("ingredients", "Ingredients", ingredients, "page-no-title"),
    ("routine", "The routine", routine, "page-no-title"),
    ("about", "The lab", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("delivery-returns", "Delivery and returns", delivery, "page-no-title"),
    ("journal", "Journal", None, ""),
]

POSTS = [
    ("how-to-patch-test", "How to patch test, and why we insist", "skin-school", "journal-1", 4, [
        "A patch test is three days of nothing happening, which is why almost nobody does one. It is also the difference between losing a bottle and losing a week of your face.",
        "Behind the ear or on the inside of the forearm, twice a day for three days, the same amount you would use normally. Not a dab: a reaction to a dab tells you nothing about a face. If the skin is fine on the fourth morning, go ahead.",
        "The two worth testing properly are the retinal and the exfoliating toner. Everything else here is fragrance-free and unlikely to bother anyone, which is why the sachet in your box is whatever you actually ordered rather than a sample of something else.",
    ]),
    ("one-active-per-bottle", "Why there is only one active in each bottle", "from-the-lab", "journal-2", 15, [
        "It would be easy to put niacinamide, an acid and a retinoid in one bottle and call it a night treatment. It would sell better. It would also be useless the first time your skin reacted, because you would have no way of knowing which of the three did it.",
        "One active per bottle means you can introduce things one at a time, drop one without losing the rest, and use the strength that suits you rather than the strength that suited a marketing department.",
        "It also means fewer compromises in the formula: an acid wants a low pH, niacinamide does not, and the version of both that can live in the same bottle is a weaker version of each.",
    ]),
    ("spf-is-the-routine", "If you do one thing, do the sunscreen", "skin-school", "journal-3", 30, [
        "Every serum on this shelf is an improvement at the margin. Sunscreen is not: it is the step that decides what your skin looks like in ten years, and it is the one people skip in winter.",
        "The dose is the part nobody gets right. Two fingers' length for a face and neck, which is far more than it feels like, and again at noon if you are near a window all day.",
        "That is also why ours is a $26 tube of 50 ml rather than a $48 bottle of 30 ml. A sunscreen you are careful with is a sunscreen you are not using properly.",
    ]),
]

MENU = [
    ("Cleanse", "{{cat:cleanse}}", "cat:cleanse"),
    ("Treat", "{{cat:treat}}", "cat:treat"),
    ("Moisturise", "{{cat:moisturise}}", "cat:moisturise"),
    ("Protect", "{{cat:protect}}", "cat:protect"),
    ("Ingredients", "{{page:ingredients}}", "page:ingredients"),
    ("The routine", "{{page:routine}}", "page:routine"),
    ("Journal", "{{page:journal}}", "page:journal"),
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
            "content": header_part("Free samples with every order &middot; fragrance-free, always",
                                   "Read the ingredients", "{{page:ingredients}}",
                                   layout="header-minimal-no-announcement"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "A small lab making a dozen fragrance-free products, one active to a bottle, in batches of four hundred.",
                [
                    ("Shop", [("Cleanse", "{{cat:cleanse}}"), ("Treat", "{{cat:treat}}"),
                              ("Moisturise", "{{cat:moisturise}}"), ("Protect", "{{cat:protect}}")]),
                    ("Learn", [("Ingredients", "{{page:ingredients}}"), ("The routine", "{{page:routine}}"),
                               ("Journal", "{{page:journal}}"), ("FAQ", "{{page:faq}}")]),
                    ("Dew", [("The lab", "{{page:about}}"), ("Contact", "{{page:contact}}"),
                             ("My account", "{{account}}"), ("Delivery and returns", "{{page:delivery-returns}}")]),
                ],
                legal="Fragrance-free, and dated on the back."),
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
    "journal": "How to use it, how often, and why the label says what it says.",
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
            {"name": "Size", "slug": "size", "type": "select", "order_by": "menu_order", "terms": SIZES},
            {"name": "Skin type", "slug": "skin-type", "type": "select", "order_by": "menu_order",
             "terms": SKIN_TYPES},
        ],
    }

    products = product_list()

    manifest = {
        "schema": 1,
        "slug": "dew",
        "theme": {"slug": "tyche", "style": ["Dew"]},
        "settings": {
            "title": "Dew",
            "tagline": "Fragrance-free skincare, one active to a bottle",
            "front_page": "home",
            "posts_page": "journal",
            "currency": "USD",
            "country": "US:CA",
            "shipping": {"country": "US", "flat_rate": "5.00", "free_over": "45"},
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
