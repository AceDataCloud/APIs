#!/usr/bin/env python3
"""Copy Studio/public service logos without publisher badges or new artwork."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps, ImageChops

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true', help='Refresh official source assets')
    args = parser.parse_args()
    sources = json.loads((ROOT / 'catalog/official-icons.json').read_text())
    overrides_path = ROOT / 'catalog/icon-overrides.json'
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    originals = ROOT / 'icons/official'
    originals.mkdir(parents=True, exist_ok=True)

    def render(item):
        key, source = item
        custom = overrides.get(key)
        original = ROOT / custom['file'] if custom else originals / f'{key}.asset'
        if not custom and (args.refresh or not original.exists()):
            with urlopen(Request(source['url'], headers={'User-Agent': 'CozeCatalogAssetBuilder/1.0'}), timeout=30) as response:
                data = response.read()
            original.write_bytes(data)
        data = original.read_bytes()
        if b'<svg' in data[:2000]:
            import cairosvg
            data = cairosvg.svg2png(bytestring=data, output_width=512, output_height=512)
        with Image.open(io.BytesIO(data)) as image:
            image = ImageOps.exif_transpose(image).convert('RGBA')
            if key in {'gemini','veo','glm'}:
                flat=Image.new('RGBA',image.size,'white');flat.alpha_composite(image)
                mask=ImageChops.difference(flat.convert('RGB'),Image.new('RGB',image.size,'white')).convert('L').point(lambda value:255 if value>16 else 0)
                box=mask.getbbox()
                if box:
                    side=min(max(box[2]-box[0],box[3]-box[1])*1.15,min(image.size))
                    cx=(box[0]+box[2])/2;cy=(box[1]+box[3])/2
                    left=max(0,min(cx-side/2,image.width-side));top=max(0,min(cy-side/2,image.height-side))
                    image=image.crop((round(left),round(top),round(left+side),round(top+side)))
            image = ImageOps.contain(image, (512, 512), Image.Resampling.LANCZOS)
            canvas = Image.new('RGBA', (512, 512), 'white')
            canvas.alpha_composite(image, ((512-image.width)//2, (512-image.height)//2))
            canvas.convert('RGB').save(ROOT / 'icons' / f'{key}.png', optimize=True)
            canvas.convert('RGB').save(ROOT / 'icons' / f'{key}.jpg', quality=96)
        return key, {'sha256': hashlib.sha256(original.read_bytes()).hexdigest(), 'source_url': None if custom else source['url'], 'source': custom['source'] if custom else source['source']}

    with ThreadPoolExecutor(max_workers=8) as pool:
        manifest = dict(pool.map(render, sorted(sources.items())))
    (ROOT / 'catalog/official-icon-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    tile = 128
    sheet = Image.new('RGB', (tile*7, tile*math.ceil(len(sources)/7)), '#eef2f6')
    for i,key in enumerate(sorted(sources)):
        with Image.open(ROOT/'icons'/f'{key}.png') as image:
            sheet.paste(image.resize((tile,tile)),((i%7)*tile,(i//7)*tile))
    sheet.save(ROOT/'catalog/icon-contact-sheet.png')
    print(f'Prepared {len(sources)} full-frame icons ({len(overrides)} custom GPT Image utility icons).')


if __name__ == '__main__':
    main()
