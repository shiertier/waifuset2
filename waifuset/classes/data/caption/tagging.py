import re
import json
import os
from typing import Literal
from ....const import ROOT


def search_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    return None


TAG_TYPES = ('artist', 'character', 'style', 'quality', 'aesthetic', 'copyright', 'meta', 'safety')
CUSTOM_TAG_PATH = search_file('custom_tags.json', ROOT)
PRIORITY_TABLE_PATH = search_file('priority_table.json', ROOT)
OVERLAP_TABLE_PATH = search_file('overlap_tags.json', ROOT)
FEATURE_TABLE_PATH = search_file('feature_table.json', ROOT)
ARTIST_TAGS_PATH = search_file('artist_tags.json', ROOT)
CHARACTER_TAGS_PATH = search_file('character_tags.json', ROOT)
COPYRIGHT_TAGS_PATH = search_file('copyright_tags.json', ROOT)
META_TAGS_PATH = search_file('meta_tags.json', ROOT)

if not CUSTOM_TAG_PATH:
    print(f'custom tag config not found in root: {ROOT}')
if not PRIORITY_TABLE_PATH:
    print(f'priority table not found in root: {ROOT}')
if not OVERLAP_TABLE_PATH:
    print(f'overlap table not found in root: {ROOT}')
if not FEATURE_TABLE_PATH:
    print(f'feature table not found in root: {ROOT}')

if not ARTIST_TAGS_PATH:
    print(f'artist tags not found in root: {ROOT}')
if not CHARACTER_TAGS_PATH:
    print(f'character tags not found in root: {ROOT}')
if not COPYRIGHT_TAGS_PATH:
    print(f'copyright tags not found in root: {ROOT}')
if not META_TAGS_PATH:
    print(f'meta tags not found in root: {ROOT}')

PATTERN_ARTIST_TAG = r"(?:^|,\s)(by[\s_]([\w\d][\w_\-.\s()\\]*))"  # match `by xxx`
PATTERN_QUALITY_TAG = r'\b((amazing|best|high|normal|low|worst|horrible)([\s_]quality))\b'  # match `xxx quality`
PATTERN_UNESCAPED_BRACKET = r"(?<!\\)([\(\)\[\]\{\}])"  # match `(` and `)`
PATTERN_ESCAPED_BRACKET = r"\\([\(\)\[\]\{\}])"  # match `\(` and `\)`
PATTERN_WEIGHTED_CAPTION = r"[^\\]\((.+?)(?::([\d\.]+))?[^\\]\)"  # match `(xxx:yyy)`

REGEX_ARTIST_TAG = re.compile(PATTERN_ARTIST_TAG)
REGEX_UNESCAPED_BRACKET = re.compile(PATTERN_UNESCAPED_BRACKET)
REGEX_ESCAPED_BRACKET = re.compile(PATTERN_ESCAPED_BRACKET)
REGEX_WEIGHTED_CAPTION = re.compile(PATTERN_WEIGHTED_CAPTION)
REGEX_QUALITY_TAG = re.compile(PATTERN_QUALITY_TAG)

PATTERN_CHARACTER = r"((character:[\s_]*)([^,]+))"
PATTERN_ARTIST = r"((artist:[\s_]*)([^,]+))"
PATTERN_STYLE = r"((style:[\s_]*)([^,]+))"
PATTERN_COPYRIGHT = r"((copyright:[\s_]*)([^,]+))"
PATTERN_META = r"((meta:[\s_]*)([^,]+))"

REGEX_CHARACTER = re.compile(PATTERN_CHARACTER)
REGEX_ARTIST = re.compile(PATTERN_ARTIST)
REGEX_STYLE = re.compile(PATTERN_STYLE)
REGEX_COPYRIGHT = re.compile(PATTERN_COPYRIGHT)
REGEX_META = re.compile(PATTERN_META)

CUSTOM_TAGS = None
QUALITY_TAGS = None
AESTHETIC_TAGS = None
STYLE_TAGS = None


def init_custom_tags(path=CUSTOM_TAG_PATH):
    global CUSTOM_TAGS, QUALITY_TAGS, AESTHETIC_TAGS, STYLE_TAGS
    if CUSTOM_TAGS is not None:
        return True
    try:
        with open(path, 'r') as f:
            custom_tag_table = json.load(f)
        custom_tag_table = {k: set(v) for k, v in custom_tag_table.items()}
        QUALITY_TAGS = custom_tag_table.get('quality', set())
        AESTHETIC_TAGS = custom_tag_table.get('aesthetic', set())
        STYLE_TAGS = custom_tag_table.get('style', set())
        CUSTOM_TAGS = QUALITY_TAGS | AESTHETIC_TAGS | STYLE_TAGS
        return True
    except Exception as e:
        CUSTOM_TAGS = None
        return False


def get_aesthetic_tags():
    return AESTHETIC_TAGS if init_custom_tags() else None


def get_style_tags():
    return STYLE_TAGS if init_custom_tags() else None


def get_quality_tags():
    return QUALITY_TAGS if init_custom_tags() else None


def get_custom_tags():
    return CUSTOM_TAGS if init_custom_tags() else None


def encode_tag(tag: str):
    tag = re.escape(tag)
    tag = REGEX_UNESCAPED_BRACKET.sub(r'\\\?\\\1', tag)
    tag = tag.replace('\ ', r'[\s_]')  # support space
    tag = tag.replace('_', r'[\s_]')  # support underscore
    return tag


def compile_or_regex(tags):
    return '(' + '|'.join([encode_tag(tag) for tag in tags]) + ')' if tags else ''

# PATTERN_CHARACTER_TAGS = '(' + '|'.join(
#     [encode_tag(tag) for tag in CHARACTER_TAGS]
# ) + ')'
# REGEX_CHARACTER_TAGS = re.compile(PATTERN_CHARACTER_TAGS)


TAG_TABLE = None
OVERLAP_TABLE = None
FEATURE_TABLE = None
PRIORITY_TABLE = None

ARTIST_TAGS = None
CHARACTER_TAGS = None
COPYRIGHT_TAGS = None
META_TAGS = None
# QUALITY_TAGS = {'amazing_quality', 'best_quality', 'high_quality', 'normal_quality', 'low_quality', 'worst_quality', 'horrible_quality'}

SAFE_LEVEL2TAG = {
    'g': 'general',
    's': 'sensitive',
    'q': 'questionable',
    'e': 'explicit',
}


def init_artist_tags(path=ARTIST_TAGS_PATH):
    global ARTIST_TAGS
    if ARTIST_TAGS is not None:
        return True
    try:
        with open(path, 'r') as f:
            ARTIST_TAGS = set(json.load(f))
    except Exception as e:
        ARTIST_TAGS = None
        return False
    return True


def get_artist_tags():
    return ARTIST_TAGS if init_artist_tags() else None


def init_character_tags(path=CHARACTER_TAGS_PATH):
    global CHARACTER_TAGS
    if CHARACTER_TAGS is not None:
        return True
    try:
        with open(path, 'r') as f:
            CHARACTER_TAGS = set(json.load(f))
    except Exception as e:
        CHARACTER_TAGS = None
        return False
    return True


def init_meta_tags(path=META_TAGS_PATH):
    global META_TAGS
    if META_TAGS is not None:
        return True
    try:
        with open(path, 'r') as f:
            META_TAGS = set(json.load(f))
    except Exception as e:
        META_TAGS = None
        return False
    return True


def get_meta_tags():
    return META_TAGS if init_meta_tags() else None


def get_character_tags():
    return CHARACTER_TAGS if init_character_tags() else None


def init_copyright_tags(path=COPYRIGHT_TAGS_PATH):
    global COPYRIGHT_TAGS
    if COPYRIGHT_TAGS is not None:
        return True
    try:
        with open(path, 'r') as f:
            COPYRIGHT_TAGS = set(json.load(f))
    except Exception as e:
        COPYRIGHT_TAGS = None
        return False
    return True


def get_copyright_tags():
    return COPYRIGHT_TAGS if init_copyright_tags() else None


def init_overlap_table(table_path=OVERLAP_TABLE_PATH):
    global OVERLAP_TABLE
    if OVERLAP_TABLE is not None:
        return True
    try:
        import json
        with open(table_path, 'r') as f:
            table = json.load(f)
        table = {entry['query']: (set(entry.get("has_overlap") or []), set(entry.get("overlap_tags") or [])) for entry in table}
        table = {k: v for k, v in table.items() if len(v[0]) > 0 or len(v[1]) > 0}
        OVERLAP_TABLE = table
        return True
    except Exception as e:
        OVERLAP_TABLE = None
        print(f'failed to read overlap table: {e}')
        return False


def get_overlap_table():
    return OVERLAP_TABLE if init_overlap_table() else None


def init_priority_table(table_path=PRIORITY_TABLE_PATH):
    global PRIORITY_TABLE
    if PRIORITY_TABLE is not None:
        return True
    try:
        with open(table_path, 'r') as f:
            PRIORITY_TABLE = json.load(f)
    except Exception as e:
        PRIORITY_TABLE = None
        return False
    return True


def get_priority_table():
    return PRIORITY_TABLE if init_priority_table() else None


def init_feature_table(table_path=FEATURE_TABLE_PATH, freq_thres=0.3, count_thres=1, least_sample_size=50):
    global FEATURE_TABLE
    if FEATURE_TABLE is not None:
        if not (freq_thres == FEATURE_TABLE.freq_thres and count_thres == FEATURE_TABLE.count_thres and least_sample_size == FEATURE_TABLE.least_sample_size):
            FEATURE_TABLE = None
            return init_feature_table(table_path, freq_thres, count_thres, least_sample_size)  # remake the table
        else:
            return True
    try:
        from .table import FeatureTable
        FEATURE_TABLE = FeatureTable(table_path, freq_thres=freq_thres, count_thres=count_thres, least_sample_size=least_sample_size)
    except Exception as e:
        FEATURE_TABLE = None
        return False
    return True


def get_feature_table():
    return FEATURE_TABLE if init_feature_table() else None


PRIORITY, PRIORITY_REGEX = None, None


def init_priority_tags():
    global PRIORITY, PRIORITY_REGEX
    if PRIORITY and PRIORITY_REGEX:
        return True

    if init_custom_tags():
        PATTERN_STYLE_TAGS = compile_or_regex(STYLE_TAGS)
    else:
        PATTERN_STYLE_TAGS = r''

    # ! spacing captions only.
    PRIORITY = {
        # Role
        'role': [r'\d?\+?(?:boy|girl|other)s?', r'multiple (boys|girls|others)', 'no humans'],
        # Character
        'character': [PATTERN_CHARACTER, 'cosplay'],
        # Copyright
        'copyright': [compile_or_regex(COPYRIGHT_TAGS)],
        'race': [r'(furry|fox|pig|wolf|elf|oni|horse|cat|dog|arthropod|shark|mouse|lion|slime|tiger|raccoon|bird|squirrel|cow|animal|maid|sheep|bear|monster|mermaid|angel|demon|dark-skinned|mature|spider|fish|plant|goat|inkling|octoling) (female|male|girl|boy)s?',
                 'maid', 'nun', 'androgynous', 'demon', 'oni', 'giant', 'loli', 'angel', 'monster', 'office lady'],
        'solo': ['solo'],
        # Subject
        'subject': ['portrait', 'scenery', 'out-of-frame'],
        # Theme
        'theme': [r'.*\b(theme)\b.*', 'science fiction', 'fantasy'],
        # Safety
        'safety': [r'\b(safety:\s*)?(general|sensitive|questionable|explicit)\b'],
        # Environment
        'environment': ['nature', 'indoors', 'outdoors'],
        # Background
        'background': [r'.*\bbackground\b.*'],
        # Angle
        'angle': [r'from (side|behind|above|below)', r'(full|upper|lower) body', r'.*\b(focus)\b.*', 'cowboy shot', 'close-up', 'dutch angle', 'wide shot', 'multiple views', r'.*\b(out of frame)\b.*', 'selfie'],

        # Actions
        'action': [r'.*\b(sitting|lying|soaked|outstretched|standing|masturbation|kneeling|crouching|squatting|stretching|bespectacled|leaning|looking|kissing|sex|sewing|facing|carrying|licking|floating|wading|aiming|reaching|drinking|drawing|fidgeting|covering|tying|walking|running|jumping|protecting|fighting|inkling|grabing|eating|trembling|sleeping|crying|straddling|pointing|drooling)\b.*',
                   'flying', 'falling', 'diving', 'holding', "jack-o' challenge", r'(hand|arm|keg|thigh)s? (up|down)', 'heart hands', 'cowgirl position', 'lifted by self', 'hetero', 'paw pose'],
        'additional_action': ['on back', 'on stomach'],

        # Expressions
        'expression': [r'.*\b(happy|sad|angry|grin|surprised|scared|embarrassed|shy|smiling|smile|frowning|crying|laughing|blushing|sweating|blush|:3|:o|expression|expressionless)\b.*'],

        # Skin
        'skin': [r'dark-skinned (?:female|male)', r'.*\b(tan|figure|skin)\b.*'],

        # Features
        'face_feature': [r'.*\b(ear|horn|tail|mouth|lip|teeth|tongue|fang|saliva|kemonomimi mode|mustache|beard|sweatdrop)s?\b.*'],

        # Eyes
        'eye': [r'.*\beyes\b.*', 'heterochromia'],
        'eye_feature': [r'.*\b(eyelashes|eyeshadow|eyebrow|eye|pupil)s?\b.*'],
        'eye_accessory': [r'.*\b(eyepatch|glasses|sunglassess|eyewear|goggles|makeup)\b.*'],

        # Hair
        'hair': [r'[\w\-\s]+ hair'],
        'hairstyle': [r'.*\b(hair|ponytail|twintail|hairbun|bun|bob cut|braid|bang|ahoge)s?\b.*', 'ringlets', 'sidelocks', 'fringe', 'forelock', 'two side up'],
        # Hair ornaments
        'hair_ornament': [r'.*\b(hairclip|haircut|hairband|hair ornament)s?\b.*'],

        'figure': ['plump',],

        # Breast
        'breast': [r'.*\b(huge|large|medium|small|flat) (breasts|chest)\b'],
        'breast_feature': [r'.*\b(breast|chest)s?\b.*', r'(side|inner|under)boob', 'cleavage'],
        'nipple': [r'.*\b(nipple|areola|areolae)s?\b.*'],

        # Pussy
        'pussy': [r'.*\b(pussy|vaginal|penis|anus)\b.*'],
        'mosaic': [r'.*\b(uncensor|censor)(ed|ing)?\b.*'],

        # Bodies
        'body': [r'.*\b(ass|butt|booty|rear|navel|groin|armpit|hip|thigh|leg|feet|foot)s?\b.*', 'barefoot'],
        'body_feature': [r'.*\b(mole|tattoo|scar|bandaid|bandage|blood|sweat|tear)s?\b.*', 'freckles', 'body freckles', 'collarbone', 'navel', 'belly button', 'piercing', 'birthmark', 'wound', 'bruise'],

        # Suit
        'suit': [r'.*\b(enmaided|plugsuit|nude)\b.*'],
        # Clothing
        'clothes': [r'.*\b(clothes|outfit|suit|capelet|headwear|maid|apron|vest|cloak|kneehighs|petticoat|legwear|serafuku|dress|sweater|hoodie|uniform|armor|veil|footwear|thighhigh|clothing|garment|attire|robe|kimono|shirt|skirt|pants|shorts|shoes|boots|gloves|socks|stockings|pantyhose|bra|panties|underwear|lingerie|swimsuit|bikini|bodysuit|leotard|tights|coat|jacket|cape|scarf|hat|cap|glasses|sunglasses|mask|helmet|headphones)s?\b.*',
                    'bottomless', 'topless', 'official alternate costume', 'alternate costume', r'.*\bnaked.*\b'],
        # Clothing Features
        'clothes_accessory': [r'.*\b(center opening|pelvic curtain|high heels|choker|zettai ryouiki|tassel|bow|sleeve|necktie|neckline|skindentation|highleg|gown|halterneck|turtleneck|collar|bowtie|fishnets|cutout|ribbon|sleeveless|crossdressing|hood|shoulder|belt|frills|halo|jewelry)s?\b.*'],

        # Fingers
        'digit': [r'.*\b(digit|finger|toe)s?\b.*', 'v', r'.*\b(gesture)\b.*'],
        'nail': [r'.*\b(fingernail|toenail|nail)s?\b.*'],

        # Items
        'item': [r'.*\b(weapon|tool|katana|instrument|gadget|device|equipment|item|object|artifact|accessory|prop|earrings|necklace|bracelet|ring|watch|bag|backpack|purse|umbrella|parasol|cane|spear|sword|knife|gun|pistol|revolver|shotgun|rifle|gun|cannon|rocket launcher|grenade|bomb|shield|wing|hoove|antler)s?\b.*'],

        # Artist
        'artist': [PATTERN_ARTIST_TAG, PATTERN_ARTIST],
        # Style
        'style': [PATTERN_STYLE_TAGS, PATTERN_STYLE],
        # Artistic
        'aesthetic': [compile_or_regex(AESTHETIC_TAGS)],
        # Quality
        'quality': [r'\b(amazing|best|high|normal|low|worst|horrible) quality\b'],
        # Meta
        'meta': [compile_or_regex(META_TAGS)],
    }

    PRIORITY_REGEX = [re.compile('|'.join([pattern for pattern in patterns if pattern.strip() != '']).replace(' ', r'[\s_]')) for patterns in PRIORITY.values()]

    return True


PATTERN_CHARACTER_FEATURES, REGEX_CHARACTER_FEATURES = None, None


def init_character_features():
    global PATTERN_CHARACTER_FEATURES, REGEX_CHARACTER_FEATURES
    if PATTERN_CHARACTER_FEATURES and REGEX_CHARACTER_FEATURES:
        return True

    PATTERN_CHARACTER_FEATURES = [
        r".*\b(hair|bang|braid|ahoge|eye|eyeshadow|eyelash|forehead|eyeliner|fang|eyebrow|pupil|tongue|makeup|lip|mole|ear|horn|nose|mole|tail|wing|breast|chest|tattoo|pussy|penis|fur|arm|leg|thigh|skin|freckle|leg|thigh|foot|feet|toe|finger)s?\b.*",
        r".*\b(twintails|ponytail|hairbun|double bun|hime cut|bob cut|sidelocks|loli|tan|eyelashes|halo)\b.*",
        r"\b(furry|fox|pig|wolf|elf|oni|horse|cat|dog|arthropod|shark|mouse|lion|slime|goblin|tiger|dragon|raccoon|bird|squirrel|cow|animal|maid|frog|sheep|bear|monster|mermaid|angel|demon|dark-skinned|mature|spider|fish|plant|goat|inkling|octoling|jiangshi)([\s_](girl|boy|other|male|female))?\b",
    ]
    REGEX_CHARACTER_FEATURES = [re.compile(pattern.replace(' ', r'[\s_]')) for pattern in PATTERN_CHARACTER_FEATURES]

    return True


def get_priority_index_of_tagtype(key):
    if not PRIORITY:
        init_priority_tags()
    return list(PRIORITY.keys()).index(key)


def fmt2unescape(tag):
    return re.sub(r'(\\+)([\(\)])', r'\2', tag)


def fmt2escape(tag):
    return re.sub(r'(?<!\\)(\()(.*)(?<!\\)(\))', r'\\\1\2\\\3', tag)  # negative lookbehind


def fmt2danbooru(tag):
    tag = tag.lower().replace(' ', '_').strip('_')
    tag = re.sub(r'(_+)', '_', tag)
    tag = tag.replace(':_', ':')
    tag = fmt2unescape(tag)
    return tag


def fmt2train(tag):
    tag = fmt2danbooru(tag)
    tag = tag.replace('_', ' ')
    return tag


def fmt2prompt(tag):
    tag = tag.replace('_', ' ').strip()
    tag = fmt2escape(tag)
    tag = tag.replace(': ', ':')
    return tag


def fmt2awa(tag):
    tag = fmt2prompt(tag)
    if (tagtype := get_tagtype_from_tag(tag)):
        prefix, tag = tag.split(":", 1)
        if prefix == 'artist':
            return f"by {tag}"
        elif prefix == 'character':
            return f"1 {tag}"
        elif prefix == 'style':
            return f"{tag} style"
        elif prefix == 'quality':
            return f"{tag} quality" if not tag.endswith(' quality') else tag
        elif prefix == 'safety':
            return tag
    return tag


def match(pattern, tag):
    if isinstance(pattern, str):
        return tag == pattern
    elif isinstance(pattern, re.Pattern):
        return re.match(pattern, tag)


def tag2priority(tag):
    LOWEST_PRIORITY = 999
    if ':' in tag and any(tag.startswith(tagtype + ':') for tagtype in TAG_TYPES):
        return get_priority_index_of_tagtype(tag.split(':', 1)[0])
    elif tag.endswith('quality'):
        return get_priority_index_of_tagtype('quality')
    elif init_custom_tags() and tag in AESTHETIC_TAGS:
        return get_priority_index_of_tagtype('aesthetic')
    elif init_priority_table():
        dan_tag = fmt2danbooru(tag)
        if dan_tag in PRIORITY_TABLE:
            return PRIORITY_TABLE[dan_tag]
        else:
            return LOWEST_PRIORITY
    elif init_priority_tags():
        for i, regex in enumerate(PRIORITY_REGEX):
            if regex.match(tag):
                return i
        return LOWEST_PRIORITY
    else:
        return LOWEST_PRIORITY


def get_tagset_from_tagtype(tagtype: Literal['artist', 'character', 'style', 'aesthetic', 'copyright', 'quality']):
    r"""
    Get specific tagset.
    """
    if tagtype == 'artist':
        return get_artist_tags()
    elif tagtype == 'character':
        return get_character_tags()
    elif tagtype == 'style':
        return get_style_tags()
    elif tagtype == 'aesthetic':
        return get_aesthetic_tags()
    elif tagtype == 'copyright':
        return get_copyright_tags()
    elif tagtype == 'quality':
        return get_quality_tags()
    elif tagtype == 'meta':
        return get_meta_tags()
    else:
        raise ValueError(f'invalid tagtype: {tagtype}')


def get_tagtype_from_tag(tag: str):
    if ':' in tag:
        for tagtype in TAG_TYPES:
            if tag.startswith(tagtype + ':'):
                return tagtype
    return None


def get_tagtype_from_ref(tag: str):
    dan_tag = fmt2danbooru(tag)
    if init_artist_tags() and dan_tag in ARTIST_TAGS:
        return 'artist'
    elif init_character_tags() and dan_tag in CHARACTER_TAGS:
        return 'character'
    elif init_custom_tags() and dan_tag in STYLE_TAGS:
        return 'style'
    elif init_copyright_tags() and dan_tag in COPYRIGHT_TAGS:
        return 'copyright'
    elif init_meta_tags() and dan_tag in META_TAGS:
        return 'meta'
    elif dan_tag in QUALITY_TAGS:
        return 'quality'
    else:
        return None


def tag2type(tag: str):
    return get_tagtype_from_tag(tag) or get_tagtype_from_ref(tag)


def uncomment(tag: str, tagtype=None):
    tagtype = tagtype or get_tagtype_from_tag(tag)
    return tag[len(tagtype) + 1:] if tagtype else tag


def comment(tag: str, tagtype=None):
    return f'{tagtype}:{tag}' if tagtype else tag
