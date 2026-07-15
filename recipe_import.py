"""Recipe import: turn a recipe URL (or pasted text) into the app's draft
recipe shape for the add-recipe form to prefill.

URL path: fetch the page and read its schema.org/Recipe JSON-LD — virtually
every recipe site embeds one for Google search, so this is far more reliable
than scraping HTML. Text path: heuristic section/ingredient parsing, used
when a site can't be fetched (the free hosting tier only reaches whitelisted
domains) or the user just has text.

Everything returned is a DRAFT — the user reviews and saves via the normal
recipe form; nothing is written to the database here.
"""

import ipaddress
import json
import re
import socket
from html.parser import HTMLParser

import requests

FETCH_TIMEOUT = 10
MAX_BYTES = 3_000_000
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/126.0 Safari/537.36 StayReady/1.0')

UNITS = {
    'cup': 'cup', 'cups': 'cups', 'c': 'cup',
    'tablespoon': 'tbsp', 'tablespoons': 'tbsp', 'tbsp': 'tbsp', 'tbs': 'tbsp',
    'teaspoon': 'tsp', 'teaspoons': 'tsp', 'tsp': 'tsp',
    'ounce': 'oz', 'ounces': 'oz', 'oz': 'oz',
    'pound': 'lb', 'pounds': 'lb', 'lb': 'lb', 'lbs': 'lb',
    'gram': 'g', 'grams': 'g', 'g': 'g',
    'kilogram': 'kg', 'kilograms': 'kg', 'kg': 'kg',
    'milliliter': 'ml', 'milliliters': 'ml', 'ml': 'ml',
    'liter': 'l', 'liters': 'l', 'l': 'l',
    'clove': 'cloves', 'cloves': 'cloves',
    'can': 'can', 'cans': 'cans',
    'slice': 'slices', 'slices': 'slices',
    'stalk': 'stalks', 'stalks': 'stalks',
    'head': 'head', 'heads': 'head',
    'pinch': 'pinch', 'dash': 'dash',
    'package': 'pack', 'packages': 'packs', 'pack': 'pack', 'packs': 'packs',
}

FRACTIONS = {'½': 0.5, '⅓': 1 / 3, '⅔': 2 / 3, '¼': 0.25, '¾': 0.75,
             '⅕': 0.2, '⅖': 0.4, '⅗': 0.6, '⅘': 0.8, '⅙': 1 / 6, '⅚': 5 / 6,
             '⅐': 1 / 7, '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875}


class ImportError_(ValueError):
    """User-facing import failure message."""


# ---------------------------------------------------------------- fetching

def _assert_public_host(url):
    """SSRF guard: only http(s), and the host must not resolve to a private,
    loopback, or link-local address."""
    m = re.match(r'^(https?)://([^/:@]+)', url, re.I)
    if not m:
        raise ImportError_('That does not look like a web link (http/https)')
    host = m.group(2)
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        raise ImportError_('Could not find that website')
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise ImportError_('That address is not reachable')


def fetch_page(url):
    url = (url or '').strip()
    _assert_public_host(url)
    try:
        with requests.get(url, timeout=FETCH_TIMEOUT, stream=True,
                          headers={'User-Agent': USER_AGENT,
                                   'Accept': 'text/html,application/xhtml+xml'}) as resp:
            resp.raise_for_status()
            chunks, size = [], 0
            for chunk in resp.iter_content(65536):
                chunks.append(chunk)
                size += len(chunk)
                if size > MAX_BYTES:
                    break
            encoding = resp.encoding or 'utf-8'
            return b''.join(chunks).decode(encoding, errors='replace')
    except requests.exceptions.ProxyError:
        # PythonAnywhere free tier: outbound requests only reach an allowlist.
        raise ImportError_("This site can't be reached from the app's hosting "
                           'plan.  Paste the recipe text instead — that always works.')
    except requests.exceptions.RequestException:
        raise ImportError_("Couldn't load that page.  Check the link, or paste "
                           'the recipe text instead.')


# ---------------------------------------------------------- JSON-LD parsing

class _JsonLdCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._in_ldjson = False
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('type', '').lower().startswith('application/ld+json'):
            self._in_ldjson = True
            self.blocks.append('')

    def handle_endtag(self, tag):
        if tag == 'script':
            self._in_ldjson = False

    def handle_data(self, data):
        if self._in_ldjson:
            self.blocks[-1] += data


def _iter_jsonld_objects(html):
    collector = _JsonLdCollector()
    try:
        collector.feed(html)
    except Exception:
        pass
    for block in collector.blocks:
        try:
            data = json.loads(block.strip())
        except (ValueError, TypeError):
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, dict):
                yield node
                if '@graph' in node:
                    stack.append(node['@graph'])


def _is_recipe(node):
    t = node.get('@type')
    if isinstance(t, list):
        return any(str(x).lower() == 'recipe' for x in t)
    return str(t or '').lower() == 'recipe'


def _first_str(value):
    if isinstance(value, list):
        value = value[0] if value else ''
    if isinstance(value, dict):
        value = value.get('name') or value.get('@value') or ''
    return str(value or '').strip()


def _parse_iso_duration(value):
    """PT1H30M -> 90 minutes."""
    m = re.match(r'^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?', str(value or ''))
    if not m or not any(m.groups()):
        return 0
    days, hours, mins = (int(g or 0) for g in m.groups())
    return days * 24 * 60 + hours * 60 + mins


def _parse_yield(value):
    m = re.search(r'\d+', _first_str(value))
    return int(m.group()) if m else 0


def _num_from(value):
    m = re.search(r'[\d.]+', str(value or ''))
    try:
        return float(m.group()) if m else 0
    except ValueError:
        return 0


def _parse_instructions(value):
    """schema.org allows: string, [string], [HowToStep], [HowToSection]."""
    steps = []

    def add(node):
        if isinstance(node, str):
            text = node.strip()
            if text:
                steps.append(text)
        elif isinstance(node, dict):
            t = str(node.get('@type', '')).lower()
            if t == 'howtosection':
                for child in node.get('itemListElement') or []:
                    add(child)
            else:
                text = str(node.get('text') or node.get('name') or '').strip()
                if text:
                    steps.append(text)
        elif isinstance(node, list):
            for child in node:
                add(child)

    add(value)
    # One numbered step per line — the recipe form's convention.
    cleaned = []
    for s in steps:
        s = re.sub(r'^\s*(step\s*)?\d+[.:)]\s*', '', s, flags=re.I).strip()
        if s:
            cleaned.append(s)
    return '\n'.join(f'{i + 1}. {s}' for i, s in enumerate(cleaned))


def parse_ingredient_line(line):
    """'2 ½ cups jasmine rice' -> (name, quantity, unit). Best-effort.
    Order matters: mixed fraction ("2 1/2"), then plain fraction ("1/2"),
    then decimal/unicode ("2.5", "½", "2½", "2-3" -> low end)."""
    text = re.sub(r'\s+', ' ', str(line or '')).strip().strip('•-* ')
    if not text:
        return None
    qty = 0.0
    rest = text
    m = re.match(r'^(\d+)\s+(\d+)\s*/\s*(\d+)\s+', text)
    if m:
        qty = int(m.group(1)) + int(m.group(2)) / max(int(m.group(3)), 1)
        rest = text[m.end():]
    else:
        m = re.match(r'^(\d+)\s*/\s*(\d+)\s+', text)
        if m:
            qty = int(m.group(1)) / max(int(m.group(2)), 1)
            rest = text[m.end():]
        else:
            m = re.match(r'^(\d+(?:\.\d+)?)?\s*([' + ''.join(FRACTIONS) + r'])?'
                         r'(?:\s*(?:-|–|to)\s*\d+(?:\.\d+)?)?\s*', text)
            if m and (m.group(1) or m.group(2)):
                qty = float(m.group(1) or 0) + (FRACTIONS.get(m.group(2), 0))
                rest = text[m.end():]
    # Drop parentheticals BEFORE unit detection: "1 (14 oz) can ..." -> "1 can ..."
    rest = re.sub(r'\s*\([^)]*\)\s*', ' ', rest).strip()
    words = rest.split(' ')
    unit = ''
    if words:
        candidate = words[0].lower().strip('.,')
        if candidate in UNITS:
            unit = UNITS[candidate]
            words = words[1:]
    name = ' '.join(words).strip(' ,.-')
    if not name:
        name, unit = (unit or text), ''
    return {'name': name[:60], 'quantity': round(qty, 3), 'unit': unit}


def _draft_from_jsonld(recipe, source_url):
    nutrition = recipe.get('nutrition') or {}
    total_min = (_parse_iso_duration(recipe.get('totalTime'))
                 or _parse_iso_duration(recipe.get('cookTime'))
                 + _parse_iso_duration(recipe.get('prepTime')))
    ingredients = []
    for line in recipe.get('recipeIngredient') or recipe.get('ingredients') or []:
        parsed = parse_ingredient_line(line)
        if parsed:
            ingredients.append(parsed)
    return {
        'name': _first_str(recipe.get('name'))[:80] or 'Imported recipe',
        'description': _first_str(recipe.get('description'))[:200],
        'meal_type': 'dinner',
        'time_minutes': total_min or 30,
        'servings': _parse_yield(recipe.get('recipeYield')) or 4,
        'cost_total': 0,
        'calories': int(_num_from(nutrition.get('calories'))),
        'protein_g': _num_from(nutrition.get('proteinContent')),
        'carbs_g': _num_from(nutrition.get('carbohydrateContent')),
        'fat_g': _num_from(nutrition.get('fatContent')),
        'fiber_g': _num_from(nutrition.get('fiberContent')),
        'sugar_g': _num_from(nutrition.get('sugarContent')),
        'sodium_mg': int(_num_from(nutrition.get('sodiumContent'))),
        'ingredients': ingredients,
        'instructions': _parse_instructions(recipe.get('recipeInstructions')),
        'source_url': source_url,
    }


# ------------------------------------------------------------- text parsing

_ING_HEADER = re.compile(r'^\s*ingredients?\b', re.I)
_STEP_HEADER = re.compile(r'^\s*(instructions?|directions?|method|steps?|preparation)\b', re.I)
_QTY_START = re.compile(r'^\s*(\d|[' + ''.join(FRACTIONS) + r']|•|-|\*)')


def draft_from_text(text):
    """Heuristic parse of pasted recipe text: first non-empty line = name;
    'Ingredients'/'Instructions' headers split sections; otherwise short
    quantity-looking lines are ingredients, sentences are steps."""
    lines = [ln.strip() for ln in (text or '').splitlines()]
    lines = [ln for ln in lines if ln]
    if len(lines) < 2:
        raise ImportError_('Paste the whole recipe — name, ingredients, and steps')
    name = lines[0][:80]
    body = lines[1:]

    ingredients, steps = [], []
    section = None
    for ln in body:
        if _ING_HEADER.match(ln):
            section = 'ing'
            continue
        if _STEP_HEADER.match(ln):
            section = 'step'
            continue
        target = section
        if target is None:
            # No headers: guess per line. Quantity-ish and short -> ingredient.
            target = 'ing' if (_QTY_START.match(ln) and len(ln) < 80
                               and not re.match(r'^\d+[.:)]\s+\w+\s+\w+\s+\w+\s+\w+', ln)) else 'step'
        if target == 'ing':
            parsed = parse_ingredient_line(ln)
            if parsed:
                ingredients.append(parsed)
        else:
            cleaned = re.sub(r'^\s*(step\s*)?\d+[.:)]\s*', '', ln, flags=re.I).strip()
            if cleaned:
                steps.append(cleaned)

    if not ingredients and not steps:
        raise ImportError_("Couldn't find ingredients or steps in that text")
    return {
        'name': name, 'description': '', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 4, 'cost_total': 0,
        'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0,
        'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 0,
        'ingredients': ingredients,
        'instructions': '\n'.join(f'{i + 1}. {s}' for i, s in enumerate(steps)),
        'source_url': '',
    }


def draft_from_url(url):
    html = fetch_page(url)
    for node in _iter_jsonld_objects(html):
        if _is_recipe(node):
            return _draft_from_jsonld(node, url)
    raise ImportError_("That page doesn't have machine-readable recipe data.  "
                       'Copy the recipe text from the page and paste it instead.')
