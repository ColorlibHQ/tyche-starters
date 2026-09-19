#!/usr/bin/env python3
"""Build the Pantry starter: a grocery that delivers tomorrow.

    python3 .dev/pantry.py

A grocery is the opposite of the other starters: forty-odd cheap things rather
than a dozen considered ones, bought weekly rather than once, and searched
rather than browsed. So this one exercises what none of the others do -- a
search-first header with aisles under it, weight options with a price per kilo,
a delivery slot rather than a shipping class, and a basket people fill before
they think about it.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starterlib import (  # noqa: E402
    bp, buttons, button, care_cards, check_list, chips, column, columns, cta, footer_part, group,
    header_part, heading, image, numbered_steps, para, paragraphs, product_row, section,
    section_head, spec_list, spec_rows, story_split, tiles_hero,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pantry")

accordion = bp.accordion
page_intro = bp.page_intro

# ---------------------------------------------------------------------------
# The catalogue. Provisional until the photographs are in: a grocery can only
# sell what it can show, and the last three starters were all rewritten to
# match the photographs rather than the other way round.
# ---------------------------------------------------------------------------
IMAGES = {
    # Sections
    "cat-produce": "Crates of vegetables on a market stall",
    "cat-bakery": "Loaves of bread cooling on a rack",
    "cat-dairy": "Eggs and a jug of milk on a pale surface",
    "hero-1": "A box of vegetables packed ready for delivery",
    "story-1": "A market stall being set out in the morning",
    "delivery-1": "A paper bag of groceries on a doorstep",
    "about-1": "A greengrocer weighing produce on a scale",
    "contact-1": "A chalk price board above a crate of apples",
    "promo-1": "A basket of mixed vegetables seen from above",
    "offers-1": "A crate of seconds, marked down",
    "journal-1": "Vegetables being chopped on a board",
    "journal-2": "A bowl of soup beside a torn loaf",
    "journal-3": "Herbs and lemons on a worktop",
    # The shelves
    "tomatoes": "Ripe tomatoes on the vine",
    "potatoes": "New potatoes with soil still on them",
    "carrots": "A bunch of carrots with their tops",
    "onions": "Brown onions in a wooden crate",
    "apples": "Apples in a crate at a market",
    "citrus": "Lemons and oranges in a bowl",
    "leaves": "A head of leafy salad",
    "mushrooms": "Chestnut mushrooms in a paper bag",
    "squash": "A butternut squash on a bench",
    "berries": "Strawberries in a punnet",
    "herbs": "A bunch of flat-leaf parsley",
    "sourdough": "A round sourdough loaf, cut",
    "baguette": "Two baguettes in a paper wrap",
    "croissants": "Croissants on a tray",
    "rye": "A dark rye loaf on a board",
    "eggs": "Half a dozen eggs in a box",
    "milk": "A glass bottle of milk",
    "butter": "A block of butter on paper",
    "cheese": "A wedge of hard cheese on a board",
    "yoghurt": "A jar of yoghurt with a spoon",
    "pasta": "Dried pasta in a glass jar",
    "rice": "Rice in a cloth sack",
    "lentils": "Green lentils in a bowl",
    "oats": "Rolled oats in a jar",
    "olive-oil": "A bottle of olive oil beside olives",
    "honey": "A jar of honey with a dipper",
    "coffee-beans": "Coffee beans in a scoop",
    "juice": "A bottle of cloudy apple juice",
}

# slug, name, aisle, prices by size, image, days ago, diet, unit price line,
# short line, long copy, spec rows
GOODS = [
    ("tomatoes", "Vine Tomatoes", "produce", ("4.20", "7.60"), "tomatoes", 2, "Organic",
     "$8.40 a kg",
     "Grown twenty miles away and picked on the vine, which is why they smell of something.",
     "Sold on the vine in 500 g and 1 kg boxes. They keep better out of the fridge, on a windowsill, and they are worth eating within the week rather than storing.",
     [("Size", "500 g or 1 kg"), ("Price per kg", "$8.40"), ("Grown", "Twenty miles away"),
      ("Keep", "Out of the fridge, a week"), ("Diet", "Organic")]),
    ("potatoes", "New Potatoes", "produce", ("3.10", "6.80"), "potatoes", 9, "Organic",
     "$2.72 a kg",
     "Earthy, thin-skinned and worth scrubbing rather than peeling.",
     "Lifted young, so the skins rub off under a tap and the insides stay waxy. Boil them whole and they will not fall apart; roast them and they crisp without flour.",
     [("Size", "1 kg or 2.5 kg"), ("Price per kg", "$2.72"), ("Skin", "Thin, no need to peel"),
      ("Keep", "Somewhere dark, two weeks"), ("Diet", "Organic")]),
    ("carrots", "Bunched Carrots", "produce", ("2.80",), "carrots", 16, "Organic",
     "$5.60 a kg",
     "Sold with their tops on, which is how you tell how long ago they were pulled.",
     "The tops go limp days before the carrot does, so they are an honest label. Take them off when you get home or they draw moisture out of the root.",
     [("Size", "500 g bunch"), ("Price per kg", "$5.60"), ("Tops", "On, and edible"),
      ("Keep", "Fridge, ten days"), ("Diet", "Organic")]),
    ("onions", "Brown Onions", "produce", ("2.40", "4.50"), "onions", 23, "",
     "$2.40 a kg",
     "The one thing in the shop that goes in almost everything else.",
     "Firm, dry-skinned and stored properly, which is the difference between an onion that lasts a month and one that sprouts in a fortnight.",
     [("Size", "1 kg or 2 kg"), ("Price per kg", "$2.40"), ("Keep", "Dark and dry, a month"),
      ("Diet", "Not organic, and cheaper for it")]),
    ("apples", "Eating Apples", "produce", ("3.60", "6.40"), "apples", 5, "",
     "$4.80 a kg",
     "This week's variety, picked at the orchard on Tuesday.",
     "We buy whatever is good that week rather than the same apple all year, so the variety on the label changes and the price does not. Ask if you want the sharp ones.",
     [("Size", "750 g or 1.5 kg"), ("Price per kg", "$4.80"), ("Variety", "Changes weekly"),
      ("Keep", "Fridge, three weeks")]),
    ("citrus", "Lemons", "produce", ("2.90",), "citrus", 30, "",
     "$7.25 a kg",
     "Unwaxed, so the zest is worth using.",
     "Most lemons are waxed to make them shine and last, which is fine until you want the peel. These are not, so they look duller and they do not keep as long.",
     [("Size", "Four, about 400 g"), ("Price per kg", "$7.25"), ("Peel", "Unwaxed"),
      ("Keep", "Fridge, two weeks")]),
    ("leaves", "Salad Leaves", "produce", ("3.20",), "leaves", 3, "Organic",
     "$16.00 a kg",
     "Cut the morning they are delivered, which is the only way salad is worth buying.",
     "Loose leaves rather than a bag of air: they last three days, not ten, because nothing has been done to them. Wash them when you use them, not before.",
     [("Size", "200 g"), ("Price per kg", "$16.00"), ("Cut", "The morning of delivery"),
      ("Keep", "Fridge, three days"), ("Diet", "Organic")]),
    ("mushrooms", "Chestnut Mushrooms", "produce", ("3.40",), "mushrooms", 12, "Vegan",
     "$11.30 a kg",
     "In a paper bag, because plastic makes them sweat.",
     "Darker and firmer than a white mushroom and worth the extra sixty cents. Keep them in the paper they came in and brush the soil off rather than washing them.",
     [("Size", "300 g"), ("Price per kg", "$11.30"), ("Bag", "Paper, on purpose"),
      ("Keep", "Fridge, five days"), ("Diet", "Vegan")]),
    ("squash", "Butternut Squash", "produce", ("3.80",), "squash", 26, "Vegan",
     "$2.53 a kg",
     "One squash, about a kilo and a half, and it will keep until you get round to it.",
     "The most forgiving thing in the shop: it sits in a bowl for a month without complaint, and it roasts into something worth eating with almost no work.",
     [("Size", "About 1.5 kg"), ("Price per kg", "$2.53"), ("Keep", "Room temperature, a month"),
      ("Diet", "Vegan")]),
    ("berries", "Strawberries", "produce", ("4.50",), "berries", 1, "",
     "$18.00 a kg",
     "In season and local, or not on the shelf at all.",
     "We do not fly them in out of season, so there are months when this listing is empty. When it is not, they were picked within a day of being delivered.",
     [("Size", "250 g punnet"), ("Price per kg", "$18.00"), ("Season", "June to September"),
      ("Keep", "Fridge, two days")]),
    ("herbs", "Flat-leaf Parsley", "produce", ("1.80",), "herbs", 19, "Organic",
     "$36.00 a kg",
     "A proper bunch rather than the supermarket's sprig in a sleeve.",
     "Fifty grams, which is more than most recipes ask for and less than it looks. Stand it in water like flowers and it will last the week.",
     [("Size", "50 g bunch"), ("Price per kg", "$36.00"), ("Keep", "In water, a week"),
      ("Diet", "Organic")]),
    ("sourdough", "Sourdough Loaf", "bakery", ("6.50",), "sourdough", 1, "Vegan",
     "$8.13 a kg",
     "Baked at four, delivered at nine, and worth eating the same day.",
     "Slow-fermented for eighteen hours, which is why it keeps four days rather than two and why the crust cracks when you press it. Cut from the middle and stand the halves face down.",
     [("Size", "800 g"), ("Price per kg", "$8.13"), ("Baked", "The morning of delivery"),
      ("Keep", "Cut side down, four days"), ("Diet", "Vegan")]),
    ("baguette", "Baguettes, 2", "bakery", ("4.20",), "baguette", 7, "Vegan",
     "$10.50 a kg",
     "Two, because one is never enough and they are stale by tomorrow.",
     "A proper thin crust, which means they are past their best in six hours and excellent in the meantime. Anything left goes in the oven for two minutes or into breadcrumbs.",
     [("Size", "Two, 200 g each"), ("Price per kg", "$10.50"), ("Best", "Within six hours"),
      ("Diet", "Vegan")]),
    ("croissants", "Croissants, 4", "bakery", ("6.80",), "croissants", 4, "",
     "Butter, and a lot of it.",
     "All butter, laminated by hand, and delivered on Saturday morning.",
     "Twenty-seven layers, made with a butter block rather than a margarine sheet, which you can tell by the way they shatter. We bake them for Saturday and Sunday only.",
     [("Size", "Four"), ("Butter", "All, 28% of the dough"), ("Delivered", "Saturday and Sunday"),
      ("Keep", "The day they arrive")]),
    ("rye", "Dark Rye", "bakery", ("5.40",), "rye", 14, "Vegan",
     "$6.75 a kg",
     "Dense, sour and it keeps for a week, which sourdough does not.",
     "Ninety per cent rye, so it is closer to a cake than a loaf and wants to be cut thin. It improves for two days after baking, which is the opposite of every other bread here.",
     [("Size", "800 g"), ("Price per kg", "$6.75"), ("Rye", "90%"),
      ("Keep", "Wrapped, a week"), ("Diet", "Vegan")]),
    ("eggs", "Eggs, 12", "dairy", ("5.40",), "eggs", 2, "",
     "45 cents an egg",
     "From a farm with four hundred hens rather than forty thousand.",
     "Laid within three days of delivery and stamped with the date rather than a best-before worked out from one. Keep them out of the fridge unless your kitchen is hot.",
     [("Size", "Twelve, medium to large"), ("Each", "45 cents"), ("Farm", "400 hens, twelve miles"),
      ("Keep", "Cool, three weeks")]),
    ("milk", "Whole Milk, 1 L", "dairy", ("2.20",), "milk", 2, "",
     "$2.20 a litre",
     "In glass, and we take the bottle back.",
     "Non-homogenised, so the cream sits on top and you shake it. The bottle is worth forty cents on return, which is why they come back and plastic never does.",
     [("Size", "1 litre, glass"), ("Deposit", "40 cents, refunded"), ("Cream", "On top, shake it"),
      ("Keep", "Fridge, five days")]),
    ("butter", "Salted Butter", "dairy", ("4.60",), "butter", 11, "",
     "$18.40 a kg",
     "Churned weekly, salted properly, wrapped in paper.",
     "Cultured for a day before churning, which is where the flavour comes from, and salted at 2% rather than the 1.5% most dairies use. It browns beautifully.",
     [("Size", "250 g"), ("Price per kg", "$18.40"), ("Salt", "2%"),
      ("Keep", "Fridge, three weeks")]),
    ("cheese", "Farmhouse Cheddar", "dairy", ("7.20", "13.40"), "cheese", 18, "",
     "$28.80 a kg",
     "Eighteen months old, cut from the wheel on the day it goes out.",
     "Made on one farm with one herd, so it tastes of a place rather than of cheddar in general. Cut to order in 250 g and 500 g pieces, waxed paper, no plastic.",
     [("Size", "250 g or 500 g"), ("Price per kg", "$28.80"), ("Age", "18 months"),
      ("Cut", "To order, on the day"), ("Keep", "Fridge, a month")]),
    ("yoghurt", "Natural Yoghurt", "dairy", ("3.80",), "yoghurt", 6, "",
     "$7.60 a kg",
     "Set in the jar, and the jar comes back like the milk bottles.",
     "Nothing in it but milk and cultures: no thickener, no powder, no sugar. It separates a little, which is what yoghurt does when nobody has stabilised it.",
     [("Size", "500 g jar"), ("Price per kg", "$7.60"), ("Deposit", "40 cents, refunded"),
      ("Keep", "Fridge, two weeks")]),
    ("pasta", "Bronze-cut Pasta", "pantry", ("3.40",), "pasta", 21, "Vegan",
     "$6.80 a kg",
     "Rough enough to hold a sauce, which the shiny sort is not.",
     "Extruded through bronze rather than teflon, so the surface is chalky and sauce clings to it. Dried slowly at a low temperature, which is why it takes eleven minutes rather than seven.",
     [("Size", "500 g"), ("Price per kg", "$6.80"), ("Cut", "Bronze"),
      ("Cook", "11 minutes"), ("Diet", "Vegan")]),
    ("rice", "Short-grain Rice", "pantry", ("4.20", "9.60"), "rice", 28, "Vegan",
     "$4.20 a kg",
     "For risotto, rice pudding and anything else that wants to be creamy.",
     "Starchy enough to thicken what it is cooked in, which is the whole point and the reason it is not interchangeable with a long grain.",
     [("Size", "1 kg or 2.5 kg"), ("Price per kg", "$4.20"), ("Grain", "Short"),
      ("Diet", "Vegan")]),
    ("lentils", "Green Lentils", "pantry", ("2.90",), "lentils", 33, "Vegan",
     "$5.80 a kg",
     "They hold their shape, so they are worth the extra minute over the split sort.",
     "No soaking, twenty-five minutes, and they stay whole rather than collapsing into soup unless you want them to. The cheapest protein in the shop by a distance.",
     [("Size", "500 g"), ("Price per kg", "$5.80"), ("Soak", "Not needed"),
      ("Cook", "25 minutes"), ("Diet", "Vegan")]),
    ("oats", "Rolled Oats", "pantry", ("2.60", "5.80"), "oats", 40, "Vegan",
     "$2.60 a kg",
     "Rolled, not instant, which is the difference between porridge and wallpaper paste.",
     "Whole oats rolled thick, so they take ten minutes and keep some texture. Milled two counties away from a grain grown in this country.",
     [("Size", "1 kg or 2.5 kg"), ("Price per kg", "$2.60"), ("Cut", "Rolled thick"),
      ("Cook", "10 minutes"), ("Diet", "Vegan")]),
    ("olive-oil", "Olive Oil, 500 ml", "pantry", ("11.50",), "olive-oil", 24, "Vegan",
     "$23.00 a litre",
     "Single estate, this year's harvest, in a tin that keeps the light out.",
     "Pressed within a day of picking and dated on the tin, because olive oil is a fruit juice and it goes stale. Peppery at the back of the throat, which is the polyphenols and a good sign.",
     [("Size", "500 ml tin"), ("Price per litre", "$23.00"), ("Harvest", "Dated on the tin"),
      ("Keep", "Dark cupboard, a year"), ("Diet", "Vegan")]),
    ("honey", "Local Honey", "pantry", ("8.40",), "honey", 35, "",
     "$18.67 a kg",
     "From hives within ten miles, and it sets, because real honey does.",
     "Unfiltered and unheated, so it crystallises in a month or two. Stand the jar in warm water if you want it runny again; anything that stays clear for a year has been treated.",
     [("Size", "450 g jar"), ("Price per kg", "$18.67"), ("Hives", "Within ten miles"),
      ("Sets", "Yes, that is the point")]),
    ("coffee-beans", "Coffee Beans, 250 g", "pantry", ("9.80",), "coffee-beans", 8, "Vegan",
     "$39.20 a kg",
     "Roasted on Tuesday by the roaster two streets away.",
     "A medium roast that suits a cafetiere and a moka pot equally, which is what most kitchens actually have. Whole beans only: ground coffee is stale in a week.",
     [("Size", "250 g"), ("Price per kg", "$39.20"), ("Roasted", "Tuesdays"),
      ("Grind", "Whole bean"), ("Diet", "Vegan")]),
    ("juice", "Cloudy Apple Juice", "drinks", ("3.60",), "juice", 15, "Vegan",
     "$4.80 a litre",
     "Pressed from the apples that are too ugly to sell whole.",
     "One ingredient, and the sediment at the bottom is apple. Pressed at the orchard from the same fruit as the eating apples, sold in glass with the same deposit as the milk.",
     [("Size", "750 ml, glass"), ("Price per litre", "$4.80"), ("Deposit", "40 cents, refunded"),
      ("Keep", "Fridge once opened, five days"), ("Diet", "Vegan")]),
]

AISLES = [
    ("Produce", "produce", "Fruit and vegetables, bought from three farms within twenty miles."),
    ("Bakery", "bakery", "Baked the morning it is delivered, by a bakery that starts at four."),
    ("Dairy and eggs", "dairy", "Milk in glass, butter in paper, eggs stamped with the day they were laid."),
    ("Pantry", "pantry", "The dry things: pasta, rice, pulses, oil, honey and coffee."),
    ("Drinks", "drinks", "Juice pressed from our own seconds, in bottles that come back."),
]

POST_CATEGORIES = [
    ("What to cook", "what-to-cook", "Three ingredients and half an hour, mostly."),
    ("From the market", "from-the-market", "What is good this week, and why the price moved."),
]

SIZES_BY_SLUG = {
    "tomatoes": ["500 g", "1 kg"],
    "potatoes": ["1 kg", "2.5 kg"],
    "onions": ["1 kg", "2 kg"],
    "apples": ["750 g", "1.5 kg"],
    "cheese": ["250 g", "500 g"],
    "rice": ["1 kg", "2.5 kg"],
    "oats": ["1 kg", "2.5 kg"],
}

DIETS = ["Organic", "Vegan"]

SALE = {"squash": "2.80", "oats": "2.10"}
SOLD_OUT = {"berries"}

REVIEWS = {
    "sourdough": [
        ("Ffion T.", 5, "Ordered at ten at night, on the doorstep by eight. Still warm, which I did not expect."),
        ("Dan H.", 5, "Four days on and it is still worth eating, which no supermarket loaf manages."),
    ],
    "eggs": [
        ("Mira S.", 5, "Dated rather than best-before, and the yolks stand up in the pan."),
    ],
    "milk": [
        ("Tom A.", 4, "Glass is heavier to carry in but the milk tastes of something. The deposit is easy enough."),
    ],
}

PROMISES = [
    ("truck-delivery", "Order by ten, delivered tomorrow",
     "A two-hour slot you choose at checkout, in a refrigerated van, driven by someone who works here."),
    ("ruler-measure", "A price per kilo on everything",
     "Because a 300 g bag at $3.40 and a 500 g bag at $5.10 are not comparable at a glance, and shops know it."),
    ("recycle", "Glass comes back",
     "Milk, yoghurt and juice carry a forty-cent deposit. Leave the empties out on your next delivery and it comes off the bill."),
]

ORDER_STEPS = [
    ("Fill the basket", "Search for what you want, or work down the aisles. Prices are per kilo as well as per pack."),
    ("Choose a slot", "Two-hour slots, 7am to 9pm, seven days. Tomorrow if you order before ten tonight."),
    ("We pack it", "Into paper and crates, chilled things last, in the order they will be unpacked."),
    ("Leave the empties", "Bottles and jars go back to the driver, and the deposit comes off the next bill."),
]

DELIVERY_ROWS = [
    ("Delivery", "$4.50, free over $60"),
    ("Slots", "Two hours, 7am to 9pm, seven days"),
    ("Cut-off", "10pm for next-day delivery"),
    ("Area", "Within fifteen miles of the market"),
    ("Substitutions", "Only if you allow them, and always cheaper or the same"),
    ("Deposit", "40 cents a glass bottle or jar, refunded on return"),
]


def pantry_products():
    products = []
    for (slug, name, aisle, prices, photo, days, diet, unit,
         short, long_copy, spec) in GOODS:
        categories = [aisle] + (["offers"] if slug in SALE else [])
        product = {
            "slug": slug,
            "name": name,
            "sku": "PN-" + slug[:4].upper(),
            "categories": categories,
            "image": photo + ".webp",
            "short_description": short,
            "description": paragraphs(long_copy) + "\n\n" + spec_list(spec),
            "days_ago": days,
            "stock_status": "outofstock" if slug in SOLD_OUT else "instock",
            "featured": slug in ("sourdough", "tomatoes", "eggs", "milk", "olive-oil", "coffee-beans"),
            "attributes": [],
            "reviews": [{"author": author, "rating": rating, "content": content}
                        for author, rating, content in REVIEWS.get(slug, [])],
        }
        if diet:
            product["attributes"].append({"name": "Diet", "slug": "diet", "options": [diet], "visible": True})

        sizes = SIZES_BY_SLUG.get(slug)
        if sizes and len(prices) == len(sizes):
            product["type"] = "variable"
            product["attributes"].insert(0, {"name": "Size", "slug": "size", "options": list(sizes),
                                             "visible": True, "variation": True})
            product["variations"] = [{"attributes": {"size": size}, "regular_price": price,
                                      "stock_status": "instock",
                                      "sku": "PN-%s-%s" % (slug[:4].upper(), size.split()[0])}
                                     for size, price in zip(sizes, prices)]
        else:
            product["type"] = "simple"
            product["regular_price"] = prices[0]
            if slug in SALE:
                product["sale_price"] = SALE[slug]
        products.append(product)
    return products


def home():
    return "\n\n".join([
        tiles_hero(
            "From farms within twenty miles",
            "Order tonight, eat it tomorrow",
            "A greengrocer, a bakery and a dairy in one basket, delivered in a two-hour slot you choose. Prices per kilo, so you can tell what anything actually costs.",
            ("Start a basket", "{{shop}}"),
            ("How delivery works", "{{page:delivery}}"),
            [("produce", "Produce", "Three farms, twenty miles, picked this week"),
             ("bakery", "Bakery", "Baked at four, with you by nine"),
             ("dairy", "Dairy and eggs", "Milk in glass, eggs stamped by date")]),
        product_row("new-arrivals", "Just in", "On the stall this week", "See every aisle", "{{shop}}"),
        care_cards(PROMISES, "How it works", kicker="The basics", bg="surface"),
        product_row("featured", "The regulars", "What goes in most baskets", "Shop everything", "{{shop}}", carousel=True),
        spec_rows(
            [("Size", "800 g"), ("Price per kg", "$8.13"), ("Baked", "The morning of delivery"),
             ("Fermented", "Eighteen hours"), ("Keep", "Cut side down, four days"), ("Diet", "Vegan")],
            "Sourdough, in short", kicker="This week's loaf",
            photo="sourdough", alt=IMAGES["sourdough"]),
        numbered_steps(ORDER_STEPS, "From basket to doorstep", kicker="Four steps"),
        story_split(
            "The market",
            "A stall, then a van, now a website",
            "We started with one stall and a chalk board. The website is the same shop: the same three farms, the same bakery, the same prices written where you can see them.",
            ["Three farms within twenty miles",
             "A price per kilo on every shelf",
             "Glass back, deposit refunded"],
            ("Read about the market", "{{page:about}}"),
            "story-1", IMAGES["story-1"], flip=True),
        journal_row(),
        cta(
            "The weekly box",
            "Let us choose, and it is cheaper",
            "Twelve to fifteen items of whatever is best that week, packed on Thursday. It costs about a fifth less than picking the same things yourself, because we buy what the farms have rather than what a list demands.",
            ["Twelve to fifteen items, about $34",
             "Skip any week, cancel whenever",
             "Tell us what you never want and we leave it out"],
            ("Create an account", "{{account}}"),
            ("See this week's box", "{{page:delivery}}"),
            "promo-1"),
    ])


def journal_row():
    body = section_head("What to cook", kicker="Recipes", link_text="Read the recipes", link_href="{{page:recipes}}")
    body += "\n\n" + bp.post_grid(inherit=False, per_page=3, cols=3, pagination=False)
    return section(body)


def delivery():
    return "\n\n".join([
        section(page_intro("Delivery", "Two hours, chosen by you",
                           "Order before ten tonight and it is with you tomorrow, in a slot you pick at checkout rather than a day-long window."),
                pad=("70", "50")),
        spec_rows(DELIVERY_ROWS, "What it costs", kicker="Delivery", photo="delivery-1",
                  alt=IMAGES["delivery-1"]),
        numbered_steps(ORDER_STEPS, "How an order runs", kicker="Four steps"),
        section(group("\n\n".join([
            heading("Substitutions", level=2),
            para("Only if you say so, and only ever for something cheaper or the same price. If we cannot match it we leave it out and refund it, because a swap nobody wanted is worse than a gap.",
                 color="muted"),
            heading("If something is wrong", level=2),
            para("Tell the driver, or email us the same day. Anything that arrives bruised, short or late is refunded without an argument and without asking for it back.",
                 color="muted"),
            heading("The deposit", level=2),
            para("Glass bottles and jars carry forty cents. Leave them out on your next delivery and it comes off the bill. There is no limit and no time on it.",
                 color="muted"),
        ]), layout="constrained", content_size="720px", gap="30"), bg="surface"),
    ])


def about():
    return "\n\n".join([
        section(page_intro("The market", "One stall, three farms, a refrigerated van",
                           "We buy from the people who grow it, sell it at a price with the kilo written next to it, and deliver it ourselves."),
                pad=("70", "50")),
        section(image("about-1", IMAGES["about-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        story_split(
            "How we buy",
            "What is good this week, not what is on a list",
            "A supermarket decides in January what it will sell in June and makes the growing fit. We buy on Monday what came out of the ground on Sunday, which is why the apple variety changes and why strawberries disappear in October.",
            ["Three farms within twenty miles",
             "Bread from one bakery, baked the morning of delivery",
             "Nothing flown in to keep a shelf full"],
            ("See what is in the aisles", "{{shop}}"),
            "story-1", IMAGES["story-1"]),
        spec_rows([
            ("Farms", "Three, all within twenty miles"),
            ("Deliveries a week", "About 600"),
            ("Van", "One, refrigerated, electric since March"),
            ("Glass returned", "84% of what goes out"),
            ("Food to the food bank", "Everything unsold, twice a week"),
        ], "The market in numbers", kicker="About us", photo="promo-1", alt=IMAGES["promo-1"]),
        section(group("\n\n".join([
            heading("On price", level=2),
            para("We are not cheaper than a supermarket on everything and we will not pretend to be. We are cheaper on vegetables, about the same on dry goods, and dearer on dairy, which is what happens when the farm is paid properly. Every shelf shows a price per kilo so you can check rather than take our word for it.",
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
            ("headset", "Something wrong with an order", "hello@example.com<br>Same day, and refunded without asking for it back."),
            ("clock", "The stall", "Tuesday to Saturday, 7am to 2pm<br>Deliveries seven days"),
            ("map-pin", "Where", "Market Row, under the arches<br>Collection from the stall is free"),
        )
    ], align="wide", gap="50")
    return "\n\n".join([
        section(page_intro("Contact", "Ask before you order",
                           "What is good this week, whether something is really in season, or what to do with a squash."),
                pad=("70", "50")),
        section(details, pad=("0", "60")),
        section(image("contact-1", IMAGES["contact-1"], ratio="21/9", align="wide"), pad=("0", "60")),
        section(group("\n".join([
            heading("Looking for a quick answer?", level=2, align="center"),
            para("Slots, substitutions, the deposit and what happens when something is out of stock are all on the delivery page.",
                 align="center", color="muted"),
            buttons(button("How delivery works", "{{page:delivery}}", style="tyche-outline"),
                    button("Read the FAQ", "{{page:faq}}", style="tyche-outline"), justify="center"),
        ]), layout="constrained", content_size="620px", gap="30"), bg="surface"),
    ])


def faq():
    topics = (
        ("Ordering", (
            ("When do I have to order by?", "Ten at night for delivery tomorrow. After that the next free slot is the day after, because the van is packed overnight."),
            ("Is there a minimum order?", "Twenty dollars. Below that the delivery costs more than the margin on the shopping, and we would rather say so than pad the basket."),
            ("Can I change an order after placing it?", "Until ten the night before. After that it is packed and on the van."),
        )),
        ("Delivery", (
            ("How do the slots work?", "Two hours, between 7am and 9pm, seven days a week. You choose at checkout and the driver texts when they are twenty minutes away."),
            ("What if I am out?", "Tell us somewhere safe and we will leave it, chilled things in a cool bag. Otherwise the driver takes it back and we refund the perishables."),
            ("How far do you deliver?", "Fifteen miles from the market. The checkout will tell you before you get attached to a basket."),
        )),
        ("The shopping", (
            ("What happens if something is out of stock?", "We leave it out and refund it, unless you have allowed substitutions, in which case you get something the same or cheaper and never dearer."),
            ("Why is there a deposit on the glass?", "Because it comes back. Forty cents a bottle or jar, off your next bill, and about five in six come home."),
            ("Is everything organic?", "No, and we say which is which. Some of it is grown by people who farm well and cannot afford the certificate, and the onions are neither and cheaper for it."),
            ("Why do prices change week to week?", "Because they do at the farm. We put the price per kilo on the shelf so a change is visible rather than hidden in a smaller bag."),
        )),
    )
    blocks = []
    for title, qa in topics:
        blocks.append(heading(title, level=2, size="xx-large"))
        blocks.append(accordion(list(qa), cls="tyche-faq"))
    body = group("\n\n".join(blocks), layout="constrained", content_size="780px", gap="40")
    return "\n\n".join([
        section(page_intro("Help", "Questions we are asked most",
                           "Slots, substitutions, the deposit, and why the price of apples moved."),
                pad=("70", "50")),
        section(body, pad=("0", "80")),
    ])


PAGES = [
    ("home", "Home", home, "page-no-title"),
    ("delivery", "Delivery", delivery, "page-no-title"),
    ("about", "The market", about, "page-no-title"),
    ("contact", "Contact", contact, "page-no-title"),
    ("faq", "FAQ", faq, "page-no-title"),
    ("recipes", "Recipes", None, ""),
]

POSTS = [
    ("what-to-do-with-a-squash", "What to do with a squash, four ways", "what-to-cook", "journal-1", 5, [
        "A butternut is the most forgiving thing in the shop and the one most often left in the bowl until it is too late. It keeps a month, which is exactly why nobody gets round to it.",
        "Roast it in wedges with the skin on at 200°C for forty minutes: the skin softens and there is no peeling. Or cube it and let it collapse into a soup with onions and stock, which takes twenty-five minutes and freezes well.",
        "The seeds are worth keeping. Rinse them, dry them, toss them in oil and salt and give them ten minutes in the same oven as the squash.",
    ]),
    ("why-the-apples-changed", "Why the apples changed this week", "from-the-market", "journal-3", 12, [
        "The label said Discovery last week and Worcester this week, and the price did not move. That is not a mistake: we buy whatever is picked and good rather than the same variety all year.",
        "A supermarket sells one apple for eleven months by storing it in a controlled atmosphere, which works and is why the texture is always the same and the flavour never is.",
        "If you want the sharp ones for cooking, ask the driver or put a note on the order. There is usually a crate of something too ugly to sell whole, and that is what the juice is pressed from.",
    ]),
    ("bread-keeps-better-out-of-the-fridge", "Bread keeps better out of the fridge", "what-to-cook", "journal-2", 24, [
        "A fridge is the worst place for a loaf. Cold speeds up the staling — the starch recrystallises fastest just above freezing — so refrigerated bread goes stale in a day where a bread bin gives you three.",
        "Cut from the middle and stand the two halves face down on the board. The crust becomes the wrapper and the crumb keeps its moisture, which is how bakeries have always done it.",
        "Anything past its best is not waste: a dry loaf is breadcrumbs, croutons, or panzanella. The freezer works too, but slice it first, because nobody saws a frozen loaf twice.",
    ]),
]

MENU = [
    ("Produce", "{{cat:produce}}", "cat:produce"),
    ("Bakery", "{{cat:bakery}}", "cat:bakery"),
    ("Dairy and eggs", "{{cat:dairy}}", "cat:dairy"),
    ("Pantry", "{{cat:pantry}}", "cat:pantry"),
    ("Drinks", "{{cat:drinks}}", "cat:drinks"),
    ("Offers", "{{cat:offers}}", "cat:offers"),
    ("Delivery", "{{page:delivery}}", "page:delivery"),
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
            "content": header_part("Order by 10pm &middot; delivered tomorrow in a two-hour slot",
                                   "How delivery works", "{{page:delivery}}",
                                   layout="header-search-no-announcement"),
        },
        {
            "slug": "footer",
            "title": "Footer",
            "area": "footer",
            "content": footer_part(
                "A greengrocer, a bakery and a dairy in one basket, from three farms within twenty miles, delivered in a two-hour slot.",
                [
                    ("Aisles", [("Produce", "{{cat:produce}}"), ("Bakery", "{{cat:bakery}}"),
                                ("Dairy and eggs", "{{cat:dairy}}"), ("Pantry", "{{cat:pantry}}")]),
                    ("Shopping", [("Delivery", "{{page:delivery}}"), ("Offers", "{{cat:offers}}"),
                                  ("Recipes", "{{page:recipes}}"), ("FAQ", "{{page:faq}}")]),
                    ("The market", [("About us", "{{page:about}}"), ("Contact", "{{page:contact}}"),
                                    ("My account", "{{account}}"), ("Everything", "{{shop}}")]),
                ],
                legal="Prices per kilo on every shelf."),
        },
    ]


def write(name, data):
    path = os.path.join(OUT, name)
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent="\t", ensure_ascii=False)
        handle.write("\n")
    return name


INTROS = {
    "recipes": "What is good this week, and what to do with it when it arrives.",
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

    all_sizes = []
    for sizes in SIZES_BY_SLUG.values():
        for size in sizes:
            if size not in all_sizes:
                all_sizes.append(size)

    terms = {
        "product_cat": [{"name": n, "slug": s, "description": d} for n, s, d in AISLES] +
                       [{"name": "Offers", "slug": "offers",
                         "description": "Marked down because there is a lot of it, or because it wants eating."}],
        "category": [{"name": n, "slug": s, "description": d} for n, s, d in POST_CATEGORIES],
        "attributes": [
            {"name": "Size", "slug": "size", "type": "select", "order_by": "menu_order", "terms": all_sizes},
            {"name": "Diet", "slug": "diet", "type": "select", "order_by": "menu_order", "terms": DIETS},
        ],
    }

    products = pantry_products()

    manifest = {
        "schema": 1,
        "slug": "pantry",
        "theme": {"slug": "tyche", "style": ["Pantry"]},
        "settings": {
            "title": "Pantry",
            "tagline": "Order tonight, eat it tomorrow",
            "front_page": "home",
            "posts_page": "recipes",
            "currency": "USD",
            "country": "US:MA",
            "shipping": {"country": "US", "flat_rate": "4.50", "free_over": "60"},
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
