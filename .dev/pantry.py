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
    "cat-produce": "Crates of fruit and vegetables along the front of a market stall",
    "cat-bakery": "A bread stall with a chalk sign reading fresh bread",
    "cat-dairy": "A bowl of brown and white eggs beside a whisk",
    "story-1": "A hand choosing produce from a market crate",
    "about-1": "A greengrocer's shopfront with crates lining the pavement",
    "delivery-1": "A woven basket of shopping carried through a market",
    "contact-1": "A crate of pumpkins with a handwritten dollar price card",
    "promo-1": "A wooden crate of lemons on a stall",
    "journal-1": "A close crop of a broccoli head with a water droplet",
    "journal-2": "Slices of grapefruit, orange and lime in water",
    "journal-3": "The veins of a savoy cabbage leaf, close",
    # Produce
    "vine-tomatoes": "Tomatoes on the vine in a white bowl",
    "cherry-tomatoes": "Red, orange and yellow cherry tomatoes in a bowl",
    "carrots": "A bunch of carrots with their tops on",
    "beetroot": "Beetroot with leafy tops in an enamel pot",
    "radishes": "Radishes with their tops in a bowl",
    "mushrooms": "A cluster of pale oyster mushrooms",
    "garlic": "Bulbs of garlic with their roots still on",
    "peppers": "Three bell peppers, red, yellow and orange",
    "squash": "Three butternut squash on grey cloth",
    "apples": "Apples in a wooden bowl",
    "pears": "Slices of pear fanned on a white plate",
    "figs": "Figs cut in half, showing the pink inside",
    "asparagus": "A bundle of asparagus spears standing upright",
    "kale": "Curly kale in a black bowl",
    "leeks": "Leeks and greens in a wooden crate at a market",
    "lemons": "Lemons and limes, halved and whole, on a white plate",
    "strawberries": "Strawberries piled close",
    "blueberries": "Blueberries piled close",
    # Bakery
    "sourdough": "A round sourdough loaf on a wooden board",
    "seeded-loaf": "A dark seeded loaf, sliced, with olives beside it",
    "baguettes": "Baguettes standing in a basket",
    "rolls": "Bread rolls in a basket",
    "croissants": "Croissants piled on a red cloth",
    "bagels": "Sesame bagels, close",
    # Dairy
    "eggs": "White eggs in a cardboard box, seen from above",
    "cheese": "A wheel of cheese with a wedge cut out of it",
    "blue-cheese": "A wedge of blue cheese with raspberries and almonds",
    "milk": "A glass bottle of milk on a dark table",
    # Pantry
    "beans": "Jars of white, kidney and black beans with bowls",
    "olive-oil": "A bottle of olive oil with olives and herbs",
    "sea-salt": "Coarse salt crystals scattered on wood",
    "pasta": "Dried pasta spilling from a glass jar",
    "spices": "A row of spice tins with handwritten chalk labels",
    "pistachios": "A glass bowl of pistachios",
    "coffee": "Roasted coffee beans filling the frame",
    # Drinks
    "orange-juice": "A glass of orange juice on a wooden table",
    "green-juice": "A bottle of green juice with glasses and citrus",
    "iced-tea": "Two jars of iced lemon tea with straws, outdoors",
}

# slug, name, aisle, prices by size, image, days ago, diet,
# short line, long copy, spec rows. The price per kilo is a spec row, because
# that is where someone comparing two bags will look for it.
GOODS = [
    # Produce
    ("vine-tomatoes", "Vine Tomatoes", "produce", ("4.20", "7.60"), "vine-tomatoes", 2, "Organic",
     "Grown twenty miles away and picked on the vine, which is why they smell of something.",
     "Sold still on the vine, in 500 g and 1 kg boxes. Keep them out of the fridge on a windowsill: cold flattens the flavour and they are worth eating within the week anyway.",
     [("Size", "500 g or 1 kg"), ("Price per kg", "$8.40"), ("Grown", "Twenty miles away"),
      ("Keep", "Out of the fridge, a week"), ("Diet", "Organic")]),
    ("cherry-tomatoes", "Mixed Cherry Tomatoes", "produce", ("3.80",), "cherry-tomatoes", 6, "Organic",
     "Red, orange and yellow in one box, because the yellow ones are the sweet ones.",
     "A mixed punnet from the same grower as the vine tomatoes, picked small. The pale ones are riper than they look, which is the usual reason people leave them.",
     [("Size", "400 g"), ("Price per kg", "$9.50"), ("Colours", "Red, orange, yellow"),
      ("Keep", "Out of the fridge, five days"), ("Diet", "Organic")]),
    ("carrots", "Bunched Carrots", "produce", ("2.80",), "carrots", 16, "Organic",
     "Sold with their tops on, which is how you tell how long ago they were pulled.",
     "The tops wilt days before the carrot does, so they are an honest label rather than decoration. Twist them off when you get home or they draw moisture out of the root.",
     [("Size", "500 g bunch"), ("Price per kg", "$5.60"), ("Tops", "On, and edible"),
      ("Keep", "Fridge, ten days"), ("Diet", "Organic")]),
    ("beetroot", "Beetroot", "produce", ("2.60",), "beetroot", 21, "Organic",
     "With the leaves on, which are worth cooking like chard rather than binning.",
     "Roast them in their skins and they slip off afterwards; boil them and half the colour ends up in the water. The leaves wilt in a pan in two minutes.",
     [("Size", "500 g bunch"), ("Price per kg", "$5.20"), ("Leaves", "On, and edible"),
      ("Keep", "Fridge, two weeks"), ("Diet", "Organic")]),
    ("radishes", "Radishes", "produce", ("2.20",), "radishes", 11, "Organic",
     "Peppery, crunchy and best on the day, which is why they come in small bunches.",
     "Eat them with butter and salt and you will understand why the French bother. They go soft within three days, so we sell them in bunches rather than bags.",
     [("Size", "250 g bunch"), ("Price per kg", "$8.80"), ("Keep", "Fridge, three days"),
      ("Diet", "Organic")]),
    ("mushrooms", "Oyster Mushrooms", "produce", ("3.40",), "mushrooms", 12, "Vegan",
     "In a paper bag, because plastic makes them sweat.",
     "Grown on straw an hour from here and picked in clusters, which is how they are sold. Tear rather than slice them, and cook them hotter and drier than you think.",
     [("Size", "250 g"), ("Price per kg", "$13.60"), ("Bag", "Paper, on purpose"),
      ("Keep", "Fridge, four days"), ("Diet", "Vegan")]),
    ("garlic", "New Season Garlic", "produce", ("2.40",), "garlic", 27, "Vegan",
     "Fresh rather than stored, so the cloves are juicy and the skins still cling.",
     "Harvested this season and dried for three weeks, not the year-old stuff that has gone papery. It is milder raw and it does not have the green shoot in the middle.",
     [("Size", "Three bulbs"), ("Price per kg", "$9.60"), ("Season", "Summer and autumn"),
      ("Keep", "Somewhere dry, a month"), ("Diet", "Vegan")]),
    ("peppers", "Bell Peppers", "produce", ("3.60",), "peppers", 18, "",
     "Three, one of each colour, which is all most recipes ask for.",
     "Red, orange and yellow, which are the same pepper at three stages of ripening and the reason the green ones taste sharper. Grown under glass forty miles away.",
     [("Size", "Three, about 450 g"), ("Price per kg", "$8.00"), ("Colours", "Red, orange, yellow"),
      ("Keep", "Fridge, a week")]),
    ("squash", "Butternut Squash", "produce", ("3.80",), "squash", 26, "Vegan",
     "One squash, about a kilo and a half, and it keeps until you get round to it.",
     "The most forgiving thing in the shop: it sits in a bowl for a month without complaint and roasts into something worth eating with almost no work. The seeds are worth keeping.",
     [("Size", "About 1.5 kg"), ("Price per kg", "$2.53"), ("Keep", "Room temperature, a month"),
      ("Diet", "Vegan")]),
    ("apples", "Eating Apples", "produce", ("3.60", "6.40"), "apples", 5, "",
     "This week's variety, picked at the orchard on Tuesday.",
     "We buy whatever is good that week rather than the same apple all year, so the variety on the label changes and the price does not. Ask if you want the sharp ones for cooking.",
     [("Size", "750 g or 1.5 kg"), ("Price per kg", "$4.80"), ("Variety", "Changes weekly"),
      ("Keep", "Fridge, three weeks")]),
    ("pears", "Pears", "produce", ("3.40",), "pears", 33, "",
     "Bought hard, because a pear ripe in the shop is a pear bruised by the time it is home.",
     "Leave them in a bowl for two or three days and press the neck, not the belly, to tell when they are ready. They go from perfect to woolly in about a day, which is the whole problem with pears.",
     [("Size", "Four, about 600 g"), ("Price per kg", "$5.67"), ("Ripen", "Two or three days in a bowl"),
      ("Keep", "Fridge once ripe, four days")]),
    ("figs", "Figs", "produce", ("4.80",), "figs", 8, "Vegan",
     "In season for six weeks, and worth the wait rather than the airfreight.",
     "Ripe when they droop and split a little, which is also when they will not survive a lorry, so these come from the closest grower we can find and only when the season is on.",
     [("Size", "Six"), ("Price per kg", "$16.00"), ("Season", "August and September"),
      ("Keep", "Two days, room temperature"), ("Diet", "Vegan")]),
    ("asparagus", "Asparagus", "produce", ("4.60",), "asparagus", 4, "Vegan",
     "Eight weeks a year, cut the morning it is delivered.",
     "Asparagus starts turning to sugar-free fibre the moment it is cut, so a spear that has flown in is a different vegetable. Stand the bundle in an inch of water like flowers.",
     [("Size", "500 g bundle"), ("Price per kg", "$9.20"), ("Season", "Late April to June"),
      ("Keep", "Standing in water, three days"), ("Diet", "Vegan")]),
    ("kale", "Curly Kale", "produce", ("2.60",), "kale", 14, "Organic",
     "Cut this morning, and it improves after a frost rather than before it.",
     "Strip the leaves off the stalks with your hands and keep the stalks for stock. It wants either two minutes or twenty, and nothing in between is any good.",
     [("Size", "300 g"), ("Price per kg", "$8.67"), ("Keep", "Fridge, five days"),
      ("Diet", "Organic")]),
    ("leeks", "Leeks", "produce", ("3.20",), "leeks", 29, "Vegan",
     "Grit and all, because a washed leek is a leek that has started to rot.",
     "Split them down the middle and run water between the layers: that is where the soil is. The dark green tops are for stock rather than the bin.",
     [("Size", "Three, about 700 g"), ("Price per kg", "$4.57"), ("Keep", "Fridge, ten days"),
      ("Diet", "Vegan")]),
    ("lemons", "Lemons and Limes", "produce", ("3.40",), "lemons", 22, "Vegan",
     "Unwaxed, so the zest is worth using.",
     "Most citrus is waxed to make it shine and last, which is fine until you want the peel. These are not, so they look duller and they keep two weeks rather than six.",
     [("Size", "Four lemons, two limes"), ("Price per kg", "$7.25"), ("Peel", "Unwaxed"),
      ("Keep", "Fridge, two weeks"), ("Diet", "Vegan")]),
    ("strawberries", "Strawberries", "produce", ("4.50",), "strawberries", 1, "",
     "In season and local, or not on the shelf at all.",
     "We do not fly them in out of season, so there are months when this listing is empty. When it is not, they were picked within a day of being delivered to you.",
     [("Size", "400 g punnet"), ("Price per kg", "$11.25"), ("Season", "June to September"),
      ("Keep", "Fridge, two days")]),
    ("blueberries", "Blueberries", "produce", ("4.20",), "blueberries", 7, "Vegan",
     "The one berry that travels well, so these are good for longer than the rest.",
     "Firm, dry and unwashed, which is how they keep a week rather than three days. The dusty bloom on the skin is a sign of freshness, not dirt.",
     [("Size", "300 g"), ("Price per kg", "$14.00"), ("Keep", "Fridge, a week"),
      ("Diet", "Vegan")]),
    # Bakery
    ("sourdough", "Sourdough Loaf", "bakery", ("6.50",), "sourdough", 1, "Vegan",
     "Baked at four, delivered at nine, and worth eating the same day.",
     "Slow-fermented for eighteen hours, which is why it keeps four days rather than two and why the crust cracks when you press it. Cut from the middle and stand the halves face down.",
     [("Size", "800 g"), ("Price per kg", "$8.13"), ("Baked", "The morning of delivery"),
      ("Keep", "Cut side down, four days"), ("Diet", "Vegan")]),
    ("seeded-loaf", "Seeded Dark Loaf", "bakery", ("5.80",), "seeded-loaf", 13, "Vegan",
     "Dense, sour and it keeps a week, which sourdough does not.",
     "Rye and wheat with sunflower and linseed through it, so it is closer to a cake than a loaf and wants cutting thin. It improves for two days after baking, unlike everything else here.",
     [("Size", "750 g"), ("Price per kg", "$7.73"), ("Seeds", "Sunflower and linseed"),
      ("Keep", "Wrapped, a week"), ("Diet", "Vegan")]),
    ("baguettes", "Baguettes, 2", "bakery", ("4.20",), "baguettes", 3, "Vegan",
     "Two, because one is never enough and they are stale by tomorrow.",
     "A proper thin crust, which means they are past their best in six hours and excellent in the meantime. Anything left goes in the oven for two minutes or into breadcrumbs.",
     [("Size", "Two, 200 g each"), ("Price per kg", "$10.50"), ("Best", "Within six hours"),
      ("Diet", "Vegan")]),
    ("rolls", "Bread Rolls, 6", "bakery", ("4.60",), "rolls", 19, "Vegan",
     "Six soft rolls, baked with the morning's bread.",
     "The same dough as the white loaf, shaped small and baked hotter, so there is more crust for the size. They freeze better than anything else on this shelf.",
     [("Size", "Six, 80 g each"), ("Price per kg", "$9.58"), ("Freeze", "Yes, on the day"),
      ("Keep", "Two days"), ("Diet", "Vegan")]),
    ("croissants", "Croissants, 4", "bakery", ("6.80",), "croissants", 2, "",
     "All butter, laminated by hand, delivered Saturday and Sunday only.",
     "Twenty-seven layers, made with a butter block rather than a margarine sheet, which you can tell by the way they shatter rather than squash. We only bake them for the weekend.",
     [("Size", "Four"), ("Butter", "28% of the dough"), ("Delivered", "Saturday and Sunday"),
      ("Keep", "The day they arrive")]),
    ("bagels", "Sesame Bagels, 6", "bakery", ("5.40",), "bagels", 25, "Vegan",
     "Boiled before they are baked, which is the whole difference.",
     "A minute in boiling water sets the crust and gives the inside its chew. Anything sold as a bagel that has not been boiled is a bread roll with a hole in it.",
     [("Size", "Six"), ("Price per kg", "$9.00"), ("Boiled", "One minute, then baked"),
      ("Keep", "Two days, or freeze"), ("Diet", "Vegan")]),
    # Dairy
    ("eggs", "Eggs, 12", "dairy", ("5.40",), "eggs", 2, "",
     "From a farm with four hundred hens rather than forty thousand.",
     "Laid within three days of delivery and stamped with the date rather than a best-before worked out from one. Keep them out of the fridge unless the kitchen is hot.",
     [("Size", "Twelve, medium to large"), ("Each", "45 cents"), ("Farm", "400 hens, twelve miles"),
      ("Keep", "Cool, three weeks")]),
    ("cheese", "Farmhouse Cheddar", "dairy", ("7.20", "13.40"), "cheese", 18, "",
     "Eighteen months old, cut from the wheel on the day it goes out.",
     "Made on one farm with one herd, so it tastes of a place rather than of cheddar in general. Cut to order, wrapped in waxed paper, never plastic.",
     [("Size", "250 g or 500 g"), ("Price per kg", "$28.80"), ("Age", "18 months"),
      ("Cut", "To order, on the day"), ("Keep", "Fridge, a month")]),
    ("blue-cheese", "Blue Cheese", "dairy", ("8.60",), "blue-cheese", 31, "",
     "Sharp, crumbly and made forty miles away in a cave that used to be a railway tunnel.",
     "Nine weeks in the tunnel, turned by hand. Take it out of the fridge an hour before you eat it or you are tasting cold fat rather than cheese.",
     [("Size", "200 g"), ("Price per kg", "$43.00"), ("Age", "Nine weeks"),
      ("Serve", "An hour out of the fridge"), ("Keep", "Fridge, three weeks")]),
    ("milk", "Whole Milk, 1 L", "dairy", ("2.20",), "milk", 2, "",
     "In glass, and we take the bottle back.",
     "Non-homogenised, so the cream sits on top and you shake it. The bottle is worth forty cents on return, which is why they come back and plastic never does.",
     [("Size", "1 litre, glass"), ("Deposit", "40 cents, refunded"), ("Cream", "On top, shake it"),
      ("Keep", "Fridge, five days")]),
    # Pantry
    ("beans", "Dried Beans, 3 Jars", "pantry", ("9.80",), "beans", 24, "Vegan",
     "White, kidney and black, in jars that are worth keeping.",
     "Dried beans are a fifth the price of tinned and twice the flavour, at the cost of remembering the night before. Soak, then simmer with a bay leaf and no salt until the end.",
     [("Size", "Three 400 g jars"), ("Price per kg", "$8.17"), ("Soak", "Overnight"),
      ("Keep", "Two years, sealed"), ("Diet", "Vegan")]),
    ("olive-oil", "Olive Oil", "pantry", ("11.50", "20.40"), "olive-oil", 20, "Vegan",
     "Single estate, this year's harvest, dated on the label.",
     "Pressed within a day of picking, because olive oil is a fruit juice and it goes stale. Peppery at the back of the throat, which is the polyphenols and a good sign.",
     [("Size", "500 ml"), ("Price per litre", "$23.00"), ("Harvest", "Dated on the label"),
      ("Keep", "Dark cupboard, a year"), ("Diet", "Vegan")]),
    ("sea-salt", "Coarse Sea Salt", "pantry", ("4.20",), "sea-salt", 35, "Vegan",
     "Dried in pans on the coast, and coarse enough to feel between your fingers.",
     "Worth having beside the hob in a bowl rather than a grinder: you season better when you can see how much you have picked up. Nothing added to stop it clumping, so it clumps.",
     [("Size", "500 g"), ("Price per kg", "$8.40"), ("Dried", "In pans, on the coast"),
      ("Additives", "None, so it clumps"), ("Diet", "Vegan")]),
    ("pasta", "Bronze-cut Pasta", "pantry", ("3.40",), "pasta", 28, "Vegan",
     "Rough enough to hold a sauce, which the shiny sort is not.",
     "Extruded through bronze rather than teflon, so the surface is chalky and sauce clings to it. Dried slowly at a low temperature, which is why it takes eleven minutes rather than seven.",
     [("Size", "500 g"), ("Price per kg", "$6.80"), ("Cut", "Bronze"),
      ("Cook", "11 minutes"), ("Diet", "Vegan")]),
    ("spices", "Spice Tins, 6", "pantry", ("18.40",), "spices", 38, "Vegan",
     "Six tins, refillable, labelled in chalk because the contents change.",
     "Cayenne, chipotle, curry, cumin, smoked paprika and cinnamon, ground within the month. Ground spice is stale in six months whatever the jar says, so these come in small tins on purpose.",
     [("Size", "Six 40 g tins"), ("Refills", "$2.20 a tin"), ("Ground", "Within the month"),
      ("Keep", "Six months, then refill"), ("Diet", "Vegan")]),
    ("pistachios", "Pistachios", "pantry", ("7.60",), "pistachios", 16, "Vegan",
     "Roasted and salted in their shells, which slows everyone down.",
     "Sold in the shell because shelled nuts go soft and because the shells are the only thing stopping you eating the bag in one go. Roasted here, weekly.",
     [("Size", "300 g"), ("Price per kg", "$25.33"), ("Roasted", "Weekly"),
      ("Keep", "A month, sealed"), ("Diet", "Vegan")]),
    ("coffee", "Coffee Beans", "pantry", ("9.80", "17.60"), "coffee", 9, "Vegan",
     "Roasted on Tuesday by the roaster two streets away.",
     "A medium roast that suits a cafetiere and a moka pot equally, which is what most kitchens actually have. Whole beans only: ground coffee is stale within a week.",
     [("Size", "250 g"), ("Price per kg", "$39.20"), ("Roasted", "Tuesdays"),
      ("Grind", "Whole bean"), ("Diet", "Vegan")]),
    # Drinks
    ("orange-juice", "Orange Juice, 750 ml", "drinks", ("3.90",), "orange-juice", 5, "Vegan",
     "Squeezed on Wednesday from the oranges that were too ugly to sell whole.",
     "One ingredient. It separates in the bottle because nothing has been added to stop it, so turn it over before you pour. Glass, with the same deposit as the milk.",
     [("Size", "750 ml, glass"), ("Price per litre", "$5.20"), ("Deposit", "40 cents, refunded"),
      ("Keep", "Fridge, four days"), ("Diet", "Vegan")]),
    ("green-juice", "Green Juice, 500 ml", "drinks", ("4.60",), "green-juice", 15, "Vegan",
     "Cucumber, apple, spinach and lime. No banana, no apple concentrate, no sugar.",
     "Cold-pressed on the morning of delivery, which is the only way it is worth what it costs. Three days in the fridge and no longer, because there is nothing in it to make it last.",
     [("Size", "500 ml, glass"), ("Price per litre", "$9.20"), ("Deposit", "40 cents, refunded"),
      ("Keep", "Fridge, three days"), ("Diet", "Vegan")]),
    ("iced-tea", "Iced Lemon Tea, 2", "drinks", ("5.20",), "iced-tea", 34, "Vegan",
     "Brewed, cooled and barely sweetened, in jars that come back.",
     "Real tea brewed strong and left to cool rather than a syrup diluted with water, so it tastes of tea and lemon and very little else. Half the sugar of anything on a supermarket shelf.",
     [("Size", "Two 330 ml jars"), ("Price per litre", "$7.88"), ("Sugar", "3.1 g per 100 ml"),
      ("Deposit", "40 cents a jar"), ("Diet", "Vegan")]),
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
    "vine-tomatoes": ["500 g", "1 kg"],
    "apples": ["750 g", "1.5 kg"],
    "cheese": ["250 g", "500 g"],
    "coffee": ["250 g", "500 g"],
    "olive-oil": ["500 ml", "1 litre"],
}

DIETS = ["Organic", "Vegan"]

# A grocery marks things down because there is a glut or because they want
# eating, and it runs out of the seasonal things. Both states belong in a demo.
SALE = {"squash": "2.80", "pears": "2.60"}
SOLD_OUT = {"strawberries"}

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
    for (slug, name, aisle, prices, photo, days, diet,
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
            product["attributes"].append({"name": "Diet", "slug": "diet", "taxonomy": True,
                                          "options": [diet], "visible": True})

        sizes = SIZES_BY_SLUG.get(slug)
        if sizes and len(prices) == len(sizes):
            product["type"] = "variable"
            product["attributes"].insert(0, {"name": "Size", "slug": "size", "taxonomy": True,
                                             "options": list(sizes), "visible": True,
                                             "variation": True})
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
