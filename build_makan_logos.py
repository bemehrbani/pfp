import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_circular_seal_png(face_stencil_path, out_png, is_dark=True):
    size = 1024
    im = Image.new('RGBA', (size, size), (7, 12, 24, 255) if is_dark else (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Colors
    gold = (201, 168, 76, 255) if is_dark else (148, 115, 30, 255)
    gold_light = (232, 212, 139, 255) if is_dark else (100, 75, 15, 255)
    white = (248, 250, 252, 255) if is_dark else (17, 24, 39, 255)

    # Outer decorative rings
    center = size // 2
    r_outer = 480
    r_inner = 450
    r_core = 330

    # Draw outer ring
    draw.ellipse([center - r_outer, center - r_outer, center + r_outer, center + r_outer], outline=gold, width=4)
    draw.ellipse([center - (r_outer - 12), center - (r_outer - 12), center + (r_outer - 12), center + (r_outer - 12)], outline=gold, width=1)
    draw.ellipse([center - r_inner, center - r_inner, center + r_inner, center + r_inner], outline=gold, width=3)
    draw.ellipse([center - r_core, center - r_core, center + r_core, center + r_core], outline=gold, width=2)

    # Decorative dots on inner ring
    for angle in range(0, 360, 10):
        rad = np.radians(angle)
        dx = int(center + (r_outer - 6) * np.cos(rad))
        dy = int(center + (r_outer - 6) * np.sin(rad))
        draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=gold)

    # Load and tint face stencil
    stencil = Image.open(face_stencil_path).convert('L')
    # Bounding crop
    np_s = np.array(stencil)
    coords = cv2.findNonZero(np_s)
    x, y, w, h = cv2.boundingRect(coords)
    stencil_cropped = stencil.crop((x, y, x + w, y + h))

    # Resize face to fit in central circle (radius 310 -> max height 460)
    target_h = 440
    aspect = stencil_cropped.width / stencil_cropped.height
    target_w = int(target_h * aspect)
    stencil_resized = stencil_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Create tinted face layer
    face_layer = Image.new('RGBA', (target_w, target_h), gold_light)
    face_layer.putalpha(stencil_resized)

    # Paste face in center
    paste_x = center - (target_w // 2)
    paste_y = center - (target_h // 2) - 10
    im.paste(face_layer, (paste_x, paste_y), face_layer)

    # Save
    im.save(out_png)
    print(f"Saved: {out_png}")

def create_wreath_emblem_png(face_stencil_path, out_png, is_dark=True):
    size = 1024
    im = Image.new('RGBA', (size, size), (7, 12, 24, 255) if is_dark else (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    gold = (201, 168, 76, 255) if is_dark else (148, 115, 30, 255)
    gold_light = (232, 212, 139, 255) if is_dark else (110, 85, 20, 255)
    center = size // 2

    # Draw stylized olive wreath arcs
    r_wreath = 360
    # Left wreath arc
    draw.arc([center - r_wreath, center - r_wreath, center + r_wreath, center + r_wreath], start=90, end=270, fill=gold, width=3)
    # Right wreath arc
    draw.arc([center - r_wreath, center - r_wreath, center + r_wreath, center + r_wreath], start=270, end=90, fill=gold, width=3)

    # Draw stylized leaves along arcs
    for angle in range(105, 255, 18):
        rad = np.radians(angle)
        lx = center + r_wreath * np.cos(rad)
        ly = center + r_wreath * np.sin(rad)
        # Leaf oval
        draw.ellipse([lx - 12, ly - 6, lx + 12, ly + 6], outline=gold, width=2)

    for angle in range(-75, 75, 18):
        rad = np.radians(angle)
        rx = center + r_wreath * np.cos(rad)
        ry = center + r_wreath * np.sin(rad)
        draw.ellipse([rx - 12, ry - 6, rx + 12, ry + 6], outline=gold, width=2)

    # Load and place face
    stencil = Image.open(face_stencil_path).convert('L')
    np_s = np.array(stencil)
    coords = cv2.findNonZero(np_s)
    x, y, w, h = cv2.boundingRect(coords)
    stencil_cropped = stencil.crop((x, y, x + w, y + h))

    target_h = 420
    aspect = stencil_cropped.width / stencil_cropped.height
    target_w = int(target_h * aspect)
    stencil_resized = stencil_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    face_layer = Image.new('RGBA', (target_w, target_h), gold_light)
    face_layer.putalpha(stencil_resized)

    im.paste(face_layer, (center - target_w // 2, center - target_h // 2 - 30), face_layer)

    im.save(out_png)
    print(f"Saved: {out_png}")

def create_svg_seal(face_paths_svg, out_svg):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <!-- Radial gradient for seal background -->
    <radialGradient id="sealBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0f1a30" />
      <stop offset="100%" stop-color="#070c18" />
    </radialGradient>
    
    <!-- Metallic Gold Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e8d48b" />
      <stop offset="35%" stop-color="#c9a84c" />
      <stop offset="70%" stop-color="#f3e5ab" />
      <stop offset="100%" stop-color="#94731e" />
    </linearGradient>

    <path id="upperArc" d="M 120 500 A 380 380 0 0 1 880 500" fill="none" />
    <path id="lowerArc" d="M 880 500 A 380 380 0 0 1 120 500" fill="none" />
  </defs>

  <!-- Background -->
  <rect width="1000" height="1000" rx="30" fill="url(#sealBg)" />

  <!-- Outer Rings -->
  <circle cx="500" cy="500" r="470" fill="none" stroke="url(#goldGrad)" stroke-width="4" />
  <circle cx="500" cy="500" r="456" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" stroke-dasharray="4,6" />
  <circle cx="500" cy="500" r="440" fill="none" stroke="url(#goldGrad)" stroke-width="3" />
  <circle cx="500" cy="500" r="320" fill="none" stroke="url(#goldGrad)" stroke-width="2" />
  <circle cx="500" cy="500" r="312" fill="none" stroke="url(#goldGrad)" stroke-width="1" stroke-dasharray="3,5" />

  <!-- Stars on side -->
  <g fill="url(#goldGrad)">
    <polygon points="105,500 113,506 110,515 118,509 126,515 123,506 131,500 121,500 118,490 115,500" />
    <polygon points="870,500 878,506 875,515 883,509 891,515 888,506 896,500 886,500 883,490 880,500" />
  </g>

  <!-- Circular Text -->
  <text font-family="'DM Sans', 'Segoe UI', sans-serif" font-size="29" font-weight="700" fill="url(#goldGrad)" letter-spacing="7">
    <textPath href="#upperArc" startOffset="50%" text-anchor="middle">
      MAKAN RY · HELSINKI · EST. 2026
    </textPath>
  </text>

  <text font-family="'Vazirmatn', 'Segoe UI', Tahoma" font-size="28" font-weight="700" fill="url(#goldGrad)" letter-spacing="3">
    <textPath href="#lowerArc" startOffset="50%" text-anchor="middle">
      انجمن ماکان · عدالت، صلح و استقلال ملت‌ها
    </textPath>
  </text>

  <!-- Centered Face Stencil Vector -->
  <g transform="translate(365, 275) scale(0.65)" fill="url(#goldGrad)">
'''
    # Insert paths
    for p in face_paths_svg:
        svg += f'    <path d="{p}" fill-rule="evenodd" />\n'

    svg += '''  </g>

  <!-- Subtitle Ribbon -->
  <text x="500" y="775" font-family="'DM Sans', sans-serif" font-size="16" font-weight="600" fill="#94a3b8" letter-spacing="4" text-anchor="middle">
    PEACE · ACCOUNTABILITY · SOVEREIGNTY
  </text>
</svg>'''
    with open(out_svg, 'w') as f:
        f.write(svg)
    print(f"Saved: {out_svg}")

def create_svg_olive_wreath(face_paths_svg, out_svg):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <radialGradient id="wreathBg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0e172a" />
      <stop offset="100%" stop-color="#070c18" />
    </radialGradient>
    <linearGradient id="goldGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f3e5ab" />
      <stop offset="50%" stop-color="#c9a84c" />
      <stop offset="100%" stop-color="#a37e2c" />
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" rx="30" fill="url(#wreathBg)" />

  <!-- Symmetrical Olive Branches -->
  <g stroke="url(#goldGrad2)" stroke-width="3" fill="none">
    <!-- Left Stem -->
    <path d="M 500 780 C 260 760 180 500 240 320 C 270 250 340 180 430 150" />
    <!-- Right Stem -->
    <path d="M 500 780 C 740 760 820 500 760 320 C 730 250 660 180 570 150" />
  </g>

  <!-- Olive Leaves Left -->
  <g fill="url(#goldGrad2)" opacity="0.9">
    <path d="M 240 320 Q 210 300 230 280 Q 250 300 240 320 Z" />
    <path d="M 200 400 Q 165 390 180 365 Q 210 380 200 400 Z" />
    <path d="M 180 480 Q 140 480 155 450 Q 190 460 180 480 Z" />
    <path d="M 195 570 Q 160 590 170 615 Q 205 595 195 570 Z" />
    <path d="M 240 660 Q 215 690 235 710 Q 260 680 240 660 Z" />
    <path d="M 330 735 Q 310 770 340 780 Q 360 745 330 735 Z" />
    <path d="M 430 775 Q 430 810 460 805 Q 460 775 430 775 Z" />

    <!-- Olive Leaves Right -->
    <path d="M 760 320 Q 790 300 770 280 Q 750 300 760 320 Z" />
    <path d="M 800 400 Q 835 390 820 365 Q 790 380 800 400 Z" />
    <path d="M 820 480 Q 860 480 845 450 Q 810 460 820 480 Z" />
    <path d="M 805 570 Q 840 590 830 615 Q 795 595 805 570 Z" />
    <path d="M 760 660 Q 785 690 765 710 Q 740 680 760 660 Z" />
    <path d="M 670 735 Q 690 770 660 780 Q 640 745 670 735 Z" />
    <path d="M 570 775 Q 570 810 540 805 Q 540 775 570 775 Z" />
  </g>

  <!-- Centered Face Stencil Vector -->
  <g transform="translate(365, 230) scale(0.65)" fill="url(#goldGrad2)">
'''
    for p in face_paths_svg:
        svg += f'    <path d="{p}" fill-rule="evenodd" />\n'

    svg += '''  </g>

  <!-- Typography -->
  <text x="500" y="860" font-family="'Playfair Display', Georgia, serif" font-size="44" font-weight="800" fill="url(#goldGrad2)" letter-spacing="12" text-anchor="middle">
    MAKAN RY
  </text>
  <text x="500" y="905" font-family="'Vazirmatn', sans-serif" font-size="24" font-weight="600" fill="#94a3b8" letter-spacing="4" text-anchor="middle">
    انجمن ماکان · صدای کودکان بی‌گناه و دادخواهی صلح
  </text>
</svg>'''
    with open(out_svg, 'w') as f:
        f.write(svg)
    print(f"Saved: {out_svg}")

def create_svg_minimal_modern(face_paths_svg, out_svg):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="1000" height="500">
  <defs>
    <linearGradient id="goldH" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f3e5ab" />
      <stop offset="60%" stop-color="#c9a84c" />
      <stop offset="100%" stop-color="#94731e" />
    </linearGradient>
  </defs>

  <rect width="1000" height="500" rx="20" fill="#070c18" />

  <!-- Left Side: Face in soft circle -->
  <circle cx="260" cy="250" r="180" fill="#0f172a" stroke="url(#goldH)" stroke-width="2" />
  
  <g transform="translate(145, 100) scale(0.53)" fill="url(#goldH)">
'''
    for p in face_paths_svg:
        svg += f'    <path d="{p}" fill-rule="evenodd" />\n'

    svg += '''  </g>

  <!-- Right Side: Brand Typography -->
  <text x="500" y="210" font-family="'DM Sans', -apple-system, sans-serif" font-size="52" font-weight="800" fill="url(#goldH)" letter-spacing="6">
    MAKAN RY
  </text>
  <text x="500" y="265" font-family="'Vazirmatn', sans-serif" font-size="34" font-weight="700" fill="#ffffff" letter-spacing="1">
    انجمن ماکان
  </text>
  <line x1="500" y1="290" x2="880" y2="290" stroke="url(#goldH)" stroke-width="2" opacity="0.6" />
  <text x="500" y="330" font-family="'DM Sans', sans-serif" font-size="18" font-weight="500" fill="#94a3b8" letter-spacing="3">
    PEACE &amp; JUSTICE ASSOCIATION · FINLAND
  </text>
  <text x="500" y="365" font-family="'Vazirmatn', sans-serif" font-size="16" font-weight="400" fill="#64748b" letter-spacing="1">
    نهاد مستقل، صلح‌طلب و مدافع حقوق انسانی و استقلال ملت‌ها
  </text>
</svg>'''
    with open(out_svg, 'w') as f:
        f.write(svg)
    print(f"Saved: {out_svg}")

def main():
    face_stencil = 'Makan_Ry/makan_stencil_clean.png'

    # Extract contours
    img = cv2.imread(face_stencil, cv2.IMREAD_GRAYSCALE)
    points = cv2.findNonZero(img)
    x, y, w, h = cv2.boundingRect(points)
    cropped = img[y:y+h, x:x+w]

    contours, hierarchy = cv2.findContours(cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    face_paths = []
    for cnt in contours:
        if cv2.contourArea(cnt) < 15:
            continue
        epsilon = 0.002 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) < 3:
            continue
        pts = approx.reshape(-1, 2)
        d = f'M {pts[0][0]},{pts[0][1]} ' + ' '.join([f'L {p[0]},{p[1]}' for p in pts[1:]]) + ' Z'
        face_paths.append(d)

    out_dirs = [
        'Makan_Ry/logos',
        'PFP_Platform/web/public/legal/makan/logos'
    ]

    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        # 1. Circular Seal
        create_circular_seal_png(face_stencil, os.path.join(d, '01_makan_seal_dark.png'), is_dark=True)
        create_circular_seal_png(face_stencil, os.path.join(d, '01_makan_seal_light.png'), is_dark=False)
        create_svg_seal(face_paths, os.path.join(d, '01_makan_seal_official.svg'))

        # 2. Olive Wreath Emblem
        create_wreath_emblem_png(face_stencil, os.path.join(d, '02_makan_wreath_dark.png'), is_dark=True)
        create_wreath_emblem_png(face_stencil, os.path.join(d, '02_makan_wreath_light.png'), is_dark=False)
        create_svg_olive_wreath(face_paths, os.path.join(d, '02_makan_wreath_emblem.svg'))

        # 3. Modern Horizontal
        create_svg_minimal_modern(face_paths, os.path.join(d, '03_makan_brandmark_horizontal.svg'))

        # Copy original reference
        cv2.imwrite(os.path.join(d, '00_makan_original_portrait.png'), cv2.imread('Makan_Ry/makan_clean_portrait.png'))
        cv2.imwrite(os.path.join(d, '00_makan_stencil_clean.png'), cv2.imread('Makan_Ry/makan_stencil_clean.png'))

if __name__ == '__main__':
    main()
