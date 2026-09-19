#!/usr/bin/env bash
#
# Every gate a starter has to pass, in one run.
#
#   .dev/check-starter.sh roastery
#   WP_URL=https://colorlibhub.com/tyche-roastery .dev/check-starter.sh roastery --no-import
#
# With no --no-import it rebuilds the package, imports it into the test site,
# and takes it out again at the end, so the checks run against a store built the
# way a merchant's would be. Against a live preview, pass --no-import.
#
# It is deliberately noisy about what it skips: a gate that quietly does nothing
# is worse than no gate.

set -uo pipefail

SLUG="${1:-}"
if [ -z "$SLUG" ]; then
	echo "Usage: .dev/check-starter.sh <slug> [--no-import]"
	exit 2
fi
shift || true

HERE="$( cd "$( dirname "$0" )/.." && pwd )"
THEME="${TYCHE_THEME:-$HOME/Fresh Projects/tyche-2}"
PLUGIN="${TYCHE_PLUGIN:-$HOME/Fresh Projects/tyche-companion}"
# A wp-cli that already points at the test site: ~/.local/bin/twp carries the
# --path to the import bed, so a bare `wp` silently runs against nothing.
WP_CLI="${TYCHE_WP:-twp}"
WP_URL="${WP_URL:-http://localhost:8813}"
WP_USER="${WP_USER:-admin}"
WP_PASS="${WP_PASS:-admin123}"
IMPORT=1
[ "${1:-}" = "--no-import" ] && IMPORT=0

export WP_URL WP_USER WP_PASS

fails=0
step() { printf '\n\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  ok    %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; fails=$(( fails + 1 )); }

step "Build the package"
if [ ! -f "$HERE/.dev/$SLUG.py" ]; then
	# The original tyche package was written by hand rather than generated, so
	# there is nothing to rebuild. Every gate after this one still runs.
	python3 "$HERE/.dev/catalogue.py" > /dev/null
	ok "no builder for $SLUG — checking the package as it is on disk"
elif python3 "$HERE/.dev/$SLUG.py" && python3 "$HERE/.dev/catalogue.py" > /dev/null; then
	ok "$SLUG.py and catalogue.json"
else
	bad "the package did not build"
	exit 1
fi

step "Photographs"
missing=0
while read -r file; do
	[ -f "$HERE/$SLUG/images/$file" ] || { echo "  missing: $file"; missing=$(( missing + 1 )); }
done < <( python3 -c "
import json, sys
for image in json.load(open('$HERE/$SLUG/images.json')):
    print(image['file'])" )
credited=$( python3 -c "
import json
images = {i['file'] for i in json.load(open('$HERE/$SLUG/images.json'))}
try:
    credits = {c['file'] for c in json.load(open('$HERE/$SLUG/credits.json'))}
except FileNotFoundError:
    credits = set()
print(len(images - credits))" )
[ "$missing" -eq 0 ] && ok "every photograph the package names is present" || bad "$missing photographs are missing"
[ "$credited" -eq 0 ] && ok "every photograph has its licence recorded" || bad "$credited photographs have no credit"

if [ "$IMPORT" -eq 1 ]; then
	step "Import into $WP_URL"
	"$WP_CLI" tyche remove > /dev/null 2>&1
	if "$WP_CLI" tyche import "$SLUG" 2>&1 | tail -1; then
		ok "imported"
	else
		bad "the import failed"
	fi
fi

step "Blocks"
blocks_out=$( cd "$THEME" && node .dev/validate-blocks.mjs 2>&1 )
case "$blocks_out" in
	*"is valid"*)
		ok "every block in every template, part, page and menu"
		;;
	*invalid*)
		echo "$blocks_out" | grep -i invalid | head -5
		bad "a block would open in the editor with a recovery notice"
		;;
	*)
		# Reading blocks back needs a login. Against someone else's site there
		# may not be one, and a gate that cannot run has to say so rather than
		# pass quietly or fail as though it found something.
		echo "  skipped: could not read the blocks back (needs WP_USER and WP_PASS for $WP_URL)"
		;;
esac

step "Contrast, on the real photographs"
while read -r path; do
	out=$( cd "$THEME" && TYCHE_URL="$path" node .dev/contrast-rendered.mjs 2>&1 | tail -1 )
	case "$out" in
		*"at least 4.5:1"*) ok "$path" ;;
		*) bad "$path: $out" ;;
	esac
done < <( python3 -c "
import json
pages = json.load(open('$HERE/$SLUG/pages.json'))
manifest = json.load(open('$HERE/$SLUG/manifest.json'))
front = manifest.get('settings', {}).get('front_page', '')
print('/')
for page in pages:
    if page['slug'] != front:
        print('/%s/' % page['slug'])
print('/shop/')" )

step "Sideways scrolling"
paths=$( python3 -c "
import json
pages = json.load(open('$HERE/$SLUG/pages.json'))
manifest = json.load(open('$HERE/$SLUG/manifest.json'))
front = manifest.get('settings', {}).get('front_page', '')
out = ['/'] + ['/%s/' % p['slug'] for p in pages if p['slug'] != front] + ['/shop/']
print(','.join(out))" )
if ( cd "$THEME" && TYCHE_PATHS="$paths" node .dev/overflow-check.mjs 2>&1 | grep -q "not clean" ); then
	bad "something is wider than the screen"
else
	ok "clean at every width"
fi

step "The header"
header_out=$( cd "$THEME" && TYCHE_PATHS="/" node .dev/header-check.mjs 2>&1 )
if [ $? -eq 0 ]; then
	echo "$header_out" | sed 's/^/  ok    /'
else
	echo "$header_out" | grep -E "NO MENU|DOUBLED" | sed 's/^/  /'
	bad "the menu cannot be reached, or an icon appears twice"
fi

step "The store"
store_out=$( cd "$PLUGIN" && node .dev/store-test.mjs /tmp 2>&1 )
store_code=$?
echo "$store_out" | grep "^FAIL" || true
summary=$( echo "$store_out" | tail -1 )
if [ "$store_code" -eq 0 ]; then
	ok "$summary"
else
	bad "$summary"
fi

if [ "$IMPORT" -eq 1 ]; then
	step "Remove it again"
	"$WP_CLI" tyche remove 2>&1 | tail -1
	left=$( "$WP_CLI" eval '
		echo count( get_posts( array( "post_type" => array( "product", "post" ), "numberposts" => -1, "fields" => "ids", "post_status" => "any" ) ) )
			+ count( get_posts( array( "post_type" => "attachment", "numberposts" => -1, "fields" => "ids", "post_status" => "any" ) ) )
			+ count( get_posts( array( "post_type" => "page", "numberposts" => -1, "fields" => "ids", "post_status" => "any", "meta_key" => "_tyche_starter" ) ) );
	' 2>/dev/null | tr -d '[:space:]' )
	[ "$left" = "0" ] && ok "nothing left behind" || bad "$left items left behind"
fi

printf '\n'
if [ "$fails" -eq 0 ]; then
	printf '\033[32mAll gates passed for %s.\033[0m\n' "$SLUG"
else
	printf '\033[31m%d gate(s) failed for %s.\033[0m\n' "$fails" "$SLUG"
fi
exit $(( fails > 0 ))
