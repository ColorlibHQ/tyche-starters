# Tyche starter sites

The library behind **Appearance > Starter sites** in the Tyche Companion plugin.
Each starter is a complete store: products with real options, pages, journal
posts, photographs and a look.

    catalogue.json        what the Starter sites screen lists
    <slug>/manifest.json  the store's settings, and which style it uses
    <slug>/terms.json     product categories, post categories, attributes
    <slug>/products.json  products, variations and reviews
    <slug>/pages.json     pages, as block markup
    <slug>/posts.json     journal posts
    <slug>/menus.json     the menu, as block markup
    <slug>/parts.json     header and footer changes, when a starter has any
    <slug>/images.json    every photograph, with its alt text
    <slug>/images/        the photographs themselves, WebP, CC0
    <slug>/credits.json   where each photograph came from, and its licence

Nothing here is code. The plugin reads these files and builds the store with
WordPress and WooCommerce's own functions.

## Placeholders

A package never contains a URL or an ID from the store it was made on. Instead:

| Placeholder | Becomes |
| --- | --- |
| `{{theme}}` | the active theme's directory URL |
| `{{img:file.webp}}` / `{{imgid:file.webp}}` | the photograph's URL / attachment ID |
| `{{page:slug}}` / `{{pageid:slug}}` | that page's URL / ID |
| `{{post:slug}}` / `{{postid:slug}}` | that journal post's URL / ID |
| `{{product:slug}}` | that product's URL |
| `{{cat:slug}}` / `{{catid:slug}}` | that product category's URL / ID |
| `{{term:slug}}` / `{{termid:slug}}` | that post category's URL / ID |
| `{{shop}}` `{{cart}}` `{{checkout}}` `{{account}}` `{{home}}` | the store's own pages |

Anything the importing store has no match for falls back to the shop or the home
page, so a starter imported "look only" onto someone else's catalogue still has
working links.

## Making a starter

A starter is designed by building a real store and exporting it:

    wp eval-file export-starter.php <slug> <out-dir> --url=https://the-store/

`export-starter.php` lives in the Tyche Companion repository, under `.dev/`. The
photographs are converted to WebP by hand and kept here; the exporter only
records their names and alt text.

## Testing one

    wp tyche import <slug>     # imports it
    wp tyche remove            # takes it out again

Point a development site at this directory with:

    define( 'TYCHE_COMPANION_STARTER_DIR', '/path/to/tyche-starters/' );

## Licences

Every photograph is CC0. `credits.json` records the source and the licence for
each one, and those credits travel with the package so a store that imports it
knows what it has.
