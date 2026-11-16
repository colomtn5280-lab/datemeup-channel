"""Export the DateMeUp 'Admit two' logo package for Hermes.
All artwork derives from canvas/logos.py so the package matches the approved board."""
import os, sys, subprocess, json, shutil
sys.path.insert(0, '/home/claude/vid/canvas')
from logos import admit2, NIGHT, CORAL, TEAL, TEALD, WHITE, INK, PAGE
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = '/home/claude/vid/brand/DateMeUp-logo'
shutil.rmtree(OUT, ignore_errors=True)
for d in ['svg', 'ios/AppIcon.appiconset', 'android/mipmap-anydpi-v26', 'android/play-store', 'web', 'lockups', 'social']:
    os.makedirs(f'{OUT}/{d}', exist_ok=True)

def write(path, text):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh: fh.write(text)
    os.replace(tmp, path)

def png(svg_path, png_path, w, h=None):
    h = h or w
    subprocess.run(['rsvg-convert', '-w', str(w), '-h', str(h), '-o', png_path + '.tmp.png', svg_path], check=True)
    os.replace(png_path + '.tmp.png', png_path)

def mark_svg(mode, scale, bg, rounded, size=1024, alpha=True):
    off = 50 * (1 - scale)
    frame = ''
    if bg:
        frame = f'<rect width="100" height="100" rx="{22.5 if rounded else 0}" fill="{bg}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<title>DateMeUp</title>{frame}<g transform="translate({off} {off}) scale({scale})">{admit2(mode)}</g></svg>')

# ---------- masters ----------
masters = {
    'mark-on-dark.svg': mark_svg('dark', 0.95, None, False),          # transparent, white ticket (use on navy)
    'mark-on-light.svg': mark_svg('light', 0.95, None, False),        # transparent, ink-outlined ticket
    'app-icon-ios-1024.svg': mark_svg('dark', 0.78, NIGHT, False),    # square, no rounding: iOS masks it
    'app-icon-rounded-preview.svg': mark_svg('dark', 0.78, NIGHT, True),
}
for n, s in masters.items():
    write(f'{OUT}/svg/{n}', s)

# ---------- iOS ----------
# Xcode 14+ single-size: one 1024 image, no alpha. Also emit legacy sizes for older targets / Expo.
ios_sizes = {'1024': 1024, '180': 180, '167': 167, '152': 152, '120': 120, '87': 87, '80': 80, '76': 76, '60': 60, '58': 58, '40': 40, '29': 29, '20': 20}
for k, px in ios_sizes.items():
    png(f'{OUT}/svg/app-icon-ios-1024.svg', f'{OUT}/ios/AppIcon.appiconset/icon-{k}.png', px)
# strip alpha (App Store rejects 1024 with alpha)
subprocess.run(['convert', f'{OUT}/ios/AppIcon.appiconset/icon-1024.png', '-background', NIGHT, '-alpha', 'remove', '-alpha', 'off',
                f'{OUT}/ios/AppIcon.appiconset/icon-1024.png'], check=True)
write(f'{OUT}/ios/AppIcon.appiconset/Contents.json', json.dumps({
    'images': [{'filename': 'icon-1024.png', 'idiom': 'universal', 'platform': 'ios', 'size': '1024x1024'}],
    'info': {'author': 'xcode', 'version': 1}}, indent=2))
# Expo: app.json "icon" -> ios/AppIcon.appiconset/icon-1024.png

# ---------- Android adaptive ----------
# 108dp canvas; safe zone is the centre 66dp circle => mark scale ~0.58 of the full layer.
write(f'{OUT}/svg/android-foreground.svg', mark_svg('dark', 0.61, None, False))
write(f'{OUT}/svg/android-background.svg',
      f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 100 100"><rect width="100" height="100" fill="{NIGHT}"/></svg>')
# monochrome (Android 13 themed icons): single colour silhouette, system tints it
mono = admit2('dark')
for c in [TEALD, CORAL, NIGHT, WHITE]:
    mono = mono.replace(f'"{c}"', '"#000000"' if c != NIGHT else '"#FFFFFF"')
mono_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 100 100">'
            f'<defs><mask id="m"><rect width="100" height="100" fill="#000"/>'
            f'<g transform="translate(19.5 19.5) scale(0.61)">'
            f'<path d="M14 22 H86 a5 5 0 0 1 5 5 V41 a8 8 0 0 0 0 16 V73 a5 5 0 0 1 -5 5 H14 a5 5 0 0 1 -5 -5 V57 a8 8 0 0 0 0 -16 V27 a5 5 0 0 1 5 -5 Z" fill="#fff"/>'
            f'<path d="M70 26 V74" stroke="#000" stroke-width="3" stroke-dasharray="4 4"/>'
            f'<circle cx="31" cy="42" r="8" fill="#000"/><path d="M18 74 A13 13 0 0 1 44 74 Z" fill="#000"/>'
            f'<circle cx="48" cy="44" r="10" fill="#fff"/><path d="M33 76 A15 15 0 0 1 63 76 Z" fill="#fff"/>'
            f'<circle cx="48" cy="44" r="8" fill="#000"/><path d="M35 76 A13 13 0 0 1 61 76 Z" fill="#000"/>'
            f'<path d="M77 44 v12 M83 44 v12" stroke="#000" stroke-width="3.5" stroke-linecap="round"/></g></mask></defs>'
            f'<rect width="100" height="100" fill="#000000" mask="url(#m)"/></svg>')
write(f'{OUT}/svg/android-monochrome.svg', mono_svg)
dens = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
legacy = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
write(f'{OUT}/svg/android-legacy-round.svg',
      f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="{NIGHT}"/>'
      f'<g transform="translate(16 16) scale(0.68)">{admit2("dark")}</g></svg>')
for d, px in dens.items():
    os.makedirs(f'{OUT}/android/mipmap-{d}', exist_ok=True)
    for layer in ['foreground', 'background', 'monochrome']:
        png(f'{OUT}/svg/android-{layer}.svg', f'{OUT}/android/mipmap-{d}/ic_launcher_{layer}.png', px)
    png(f'{OUT}/svg/app-icon-rounded-preview.svg', f'{OUT}/android/mipmap-{d}/ic_launcher.png', legacy[d])
    png(f'{OUT}/svg/android-legacy-round.svg', f'{OUT}/android/mipmap-{d}/ic_launcher_round.png', legacy[d])
adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
            '    <background android:drawable="@mipmap/ic_launcher_background" />\n'
            '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n'
            '    <monochrome android:drawable="@mipmap/ic_launcher_monochrome" />\n</adaptive-icon>\n')
write(f'{OUT}/android/mipmap-anydpi-v26/ic_launcher.xml', adaptive)
write(f'{OUT}/android/mipmap-anydpi-v26/ic_launcher_round.xml', adaptive)
png(f'{OUT}/svg/app-icon-ios-1024.svg', f'{OUT}/android/play-store/play-store-icon-512.png', 512)
# Expo equivalents
for layer in ['foreground', 'background', 'monochrome']:
    png(f'{OUT}/svg/android-{layer}.svg', f'{OUT}/android/expo-adaptive-{layer}-1024.png', 1024)

# ---------- outlined wordmark ----------
font = TTFont('/home/claude/vid/fonts/Bricolage-800.ttf')
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
upm = font['head'].unitsPerEm
def wordmark(text, color, track=-0.035):
    x, paths = 0, []
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        paths.append(pen.getCommands())
        x += hmtx[g][0] + track * upm
    return f'<path fill="{color}" d="{" ".join(paths)}"/>', x - track * upm
asc = font['OS/2'].sCapHeight or 700

def lockup(mode, bg):
    ink = WHITE if mode == 'dark' else INK
    wm, w = wordmark('DateMeUp', ink)
    # Ticket occupies x 9..91, y 22..78 of the 100-box (82 x 56). Crop to it.
    th = asc * 1.18                      # ticket height ~= cap height + a little (optically equal to the letters)
    sc = th / 56; tw = 82 * sc
    gap = asc * 0.30
    pad = asc * 0.45 if bg else asc * 0.04
    W = pad * 2 + tw + gap + w
    H = pad * 2 + max(th, asc * 1.32)    # room for the descender of the "p"
    ty = pad + th / 2 + asc / 2          # baseline so caps are centred on the ticket
    frame = f'<rect width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W/H*64:.0f}" height="64">'
            f'<title>DateMeUp</title>{frame}'
            f'<g transform="translate({pad - 9*sc:.1f} {pad - 22*sc:.1f}) scale({sc:.4f})">{admit2(mode)}</g>'
            f'<g transform="translate({pad + tw + gap:.1f} {ty:.1f})">{wm}</g></svg>'), W, H
for mode, bg, name in [('light', None, 'lockup-on-light'), ('dark', None, 'lockup-on-dark'),
                       ('light', PAGE, 'lockup-on-light-filled'), ('dark', NIGHT, 'lockup-on-dark-filled')]:
    s, W, H = lockup(mode, bg)
    write(f'{OUT}/lockups/{name}.svg', s)
    png(f'{OUT}/lockups/{name}.svg', f'{OUT}/lockups/{name}.png', int(W / H * 240), 240)
wm_l, ww = wordmark('DateMeUp', INK)
write(f'{OUT}/lockups/wordmark-ink.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-asc*1.05:.0f} {ww:.0f} {asc*1.3:.0f}"><title>DateMeUp</title>{wm_l}</svg>')
wm_w, _ = wordmark('DateMeUp', WHITE)
write(f'{OUT}/lockups/wordmark-white.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-asc*1.05:.0f} {ww:.0f} {asc*1.3:.0f}"><title>DateMeUp</title>{wm_w}</svg>')

# ---------- web ----------
write(f'{OUT}/web/favicon.svg',
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="{NIGHT}"/>'
      f'<g transform="translate(4 4) scale(0.92)">{admit2("dark")}</g></svg>')
for px in [16, 32, 48]:
    png(f'{OUT}/web/favicon.svg', f'{OUT}/web/fav-{px}.png', px)
subprocess.run(['convert', f'{OUT}/web/fav-16.png', f'{OUT}/web/fav-32.png', f'{OUT}/web/fav-48.png', f'{OUT}/web/favicon.ico'], check=True)
for px in [16, 32, 48]: os.remove(f'{OUT}/web/fav-{px}.png')
png(f'{OUT}/svg/app-icon-ios-1024.svg', f'{OUT}/web/apple-touch-icon.png', 180)
subprocess.run(['convert', f'{OUT}/web/apple-touch-icon.png', '-alpha', 'off', f'{OUT}/web/apple-touch-icon.png'], check=True)
png(f'{OUT}/svg/app-icon-rounded-preview.svg', f'{OUT}/web/icon-192.png', 192)
png(f'{OUT}/svg/app-icon-rounded-preview.svg', f'{OUT}/web/icon-512.png', 512)
write(f'{OUT}/web/icon-maskable.svg', mark_svg('dark', 0.6, NIGHT, False))
png(f'{OUT}/web/icon-maskable.svg', f'{OUT}/web/icon-maskable-512.png', 512)
write(f'{OUT}/web/manifest.webmanifest', json.dumps({
    'name': 'DateMeUp', 'short_name': 'DateMeUp', 'theme_color': NIGHT, 'background_color': '#F5F6FA', 'display': 'standalone',
    'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
              {'src': '/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}]}, indent=2))

# ---------- social / link preview 1200x630 ----------
wm_og, wwo = wordmark('DateMeUp', WHITE)
tag, tw = wordmark('Plan together. Go together.', CORAL, -0.02)
k = min(120 / asc, 700 / wwo); k2 = min(44 / asc, 700 / tw)
og = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
      f'<rect width="1200" height="630" fill="{NIGHT}"/>'
      f'<circle cx="1040" cy="120" r="54" fill="#FFE7B0"/><circle cx="1062" cy="104" r="50" fill="{NIGHT}"/>'
      + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#fff" opacity=".7"/>' for x, y in [(160, 80), (340, 140), (520, 60), (700, 120), (880, 70), (980, 240), (620, 220), (260, 230)])
      + f'<g transform="translate(96 160) scale(2.6)">{admit2("dark")}</g>'
      f'<g transform="translate(400 340) scale({k:.4f})">{wm_og}</g>'
      f'<g transform="translate(402 410) scale({k2:.4f})">{tag}</g>'
      f'<path d="M0 560 H1200 V630 H0 Z" fill="{CORAL}"/>'
      f'</svg>')
write(f'{OUT}/social/og-image.svg', og)
png(f'{OUT}/social/og-image.svg', f'{OUT}/social/og-image-1200x630.png', 1200, 630)
print('done')
