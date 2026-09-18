#!/usr/bin/env python3
"""Build catalogue.json, the list the Starter sites screen reads.

    python3 .dev/catalogue.py

Counts come from each package rather than being typed here, so the screen can
never promise sixteen products and import fifteen. Everything else -- what the
starter is called, which niche it suits, whether it is free, where it can be
seen -- lives in STARTERS below.
"""

import datetime
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# slug, name, niche, tier, version, preview
STARTERS = [
    ("tyche", "Tyche", "Knitwear and basics", "free", "1.0.0",
     "https://colorlibhub.com/tyche-2/"),
    ("roastery", "Roastery", "Coffee roaster", "free", "1.0.0",
     "https://colorlibhub.com/tyche-roastery/"),
]


def counts(slug):
    """What the package actually contains."""
    def load(name):
        path = os.path.join(ROOT, slug, name)
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)

    pages = load("pages.json")
    manifest = load("manifest.json")
    posts_page = manifest.get("settings", {}).get("posts_page", "")

    return {
        "products": len(load("products.json")),
        # The journal is a page with no content of its own; it is not a page
        # anyone would count when deciding whether to import a starter.
        "pages": len([p for p in pages if p["slug"] != posts_page]),
        "posts": len(load("posts.json")),
        "images": len(load("images.json")),
        "variations": sum(len(p.get("variations", [])) for p in load("products.json")),
    }


def main():
    catalogue = {
        "schema": 1,
        "updated": datetime.date.today().isoformat(),
        "starters": [
            {
                "slug": slug,
                "name": name,
                "niche": niche,
                "tier": tier,
                "version": version,
                "thumbnail": "%s/thumbnail.webp" % slug,
                "preview": preview,
                "requires": {"theme": "tyche", "plugins": ["woocommerce"]},
                "counts": counts(slug),
            }
            for slug, name, niche, tier, version, preview in STARTERS
        ],
    }

    with open(os.path.join(ROOT, "catalogue.json"), "w", encoding="utf-8") as handle:
        json.dump(catalogue, handle, indent="\t", ensure_ascii=False)
        handle.write("\n")

    for starter in catalogue["starters"]:
        print("  %-10s %-22s %s" % (starter["slug"], starter["niche"],
                                    ", ".join("%s %s" % (v, k) for k, v in starter["counts"].items())))


if __name__ == "__main__":
    main()
