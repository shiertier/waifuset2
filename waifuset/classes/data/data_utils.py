from pathlib import Path
from typing import List, Literal
from .caption import tagging


def read_attrs(fp, types: List[Literal['txt', 'danbooru']] = None):
    if isinstance(types, str):
        types = [types]
    elif types is None:
        types = ['txt', 'danbooru']
    fp = Path(fp)
    if 'txt' in types and (txt_cap_path := fp.with_suffix('.txt')).is_file():
        caption = txt_cap_path.read_text(encoding='utf-8')
        attrs_dict = {'caption': caption}
        return attrs_dict

    if 'danbooru' in types:
        import json
        if (waifuc_md_path := fp.with_name(f".{fp.stem}_meta.json")).is_file():  # waifuc naming format
            with open(waifuc_md_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            attrs_dict = parse_danbooru_metadata(metadata['danbooru'])
            attrs_dict = convert_danbooru_metadata(attrs_dict)
            return attrs_dict
        elif (gallery_dl_md_path := fp.with_name(f"{fp.name}.json")).is_file():
            with open(gallery_dl_md_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            attrs_dict = parse_danbooru_metadata(metadata)
            attrs_dict = convert_danbooru_metadata(attrs_dict)
            return attrs_dict

    return None


def parse_danbooru_metadata(metadata):
    tags = metadata['tag_string']
    artist_tags = metadata['tag_string_artist']
    character_tags = metadata['tag_string_character']
    copyright_tags = metadata['tag_string_copyright']
    meta_tags = metadata['tag_string_meta']

    safety_tag = {
        'g': 'general',
        's': 'sensitive',
        'q': 'questionable',
        'e': 'explicit',
    }[metadata['rating']]
    date = metadata['created_at'].split('T')[0]
    original_size = f"{metadata['image_width']}x{metadata['image_height']}"
    return {
        'caption': tags,
        'artist': artist_tags,
        'character': character_tags,
        'copyright': copyright_tags,
        'meta': meta_tags,
        'safety': safety_tag,
        'original_size': original_size,
        'date': date,
    }


def convert_danbooru_metadata(metadata):
    metadata['caption'] = ', '.join([tagging.fmt2train(tag) for tag in metadata['caption'].split(' ')])
    for attr in ('artist', 'character', 'copyright', 'meta'):
        metadata[attr] = ', '.join([tagging.fmt2danbooru(tag) for tag in metadata[attr].split(' ')])
    return metadata
