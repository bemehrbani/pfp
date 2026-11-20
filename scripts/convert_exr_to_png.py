"""Convert the painted-plaster EXR maps to 8-bit PNG for the WebGL build.

Run through Blender's bundled Python, because it ships the OpenImageIO/OpenEXR
reader that CPython does not:

    blender --background --factory-startup --python scripts/convert_exr_to_png.py -- \
        --src painted_plaster_wall_1k.blend/textures \
        --out PFP_Platform/web/public/textures/plaster

The normal and roughness maps are non-colour data, so the PNG bytes must hold
the shader's sampled values unchanged. Decoding through bpy and writing the PNG
here keeps every value on the linear-to-8-bit path; bpy's own save would push
the buffer through the image colourspace and shift the normals.

Relative paths resolve against the repository root.
"""

import argparse
import os
import struct
import sys
import zlib

import bpy  # noqa: F401  (available only inside Blender)
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve(path):
    """Treat relative paths as repository-relative, not as Blender-CWD-relative."""
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(REPO_ROOT, path))


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", required=True, help="Directory holding the .exr files")
    parser.add_argument("--out", required=True, help="Directory for the 8-bit PNG files")
    parser.add_argument(
        "--normal-min",
        type=float,
        default=-0.01,
        help="Buffer minimum below which the red channel is treated as a signed vector",
    )
    return parser.parse_args(argv)


def load_float_rgb(path):
    """Return an H x W x 3 float32 array, flipped to PNG's top-down row order."""
    img = bpy.data.images.load(path, check_existing=False)
    width, height = img.size
    if width == 0 or height == 0:
        raise RuntimeError(f"{path}: decoded to an empty image")
    rgba = np.empty(width * height * 4, dtype=np.float32)
    img.pixels.foreach_get(rgba)
    bpy.data.images.remove(img)
    # Blender stores rows bottom-up; every image format we write is top-down.
    return rgba.reshape(height, width, 4)[::-1, :, :3].copy()


def write_png(path, rgb):
    """Write 8-bit truecolour PNG from an H x W x 3 uint8 array."""
    height, width, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[y].tobytes() for y in range(height))

    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as fh:
        fh.write(png)


def convert(src_path, dst_path, normal_min):
    rgb = load_float_rgb(src_path)
    name = os.path.basename(src_path)
    is_normal = "_nor_" in name

    if is_normal and rgb.min() < normal_min:
        # Some exporters store the unit vector itself (-1..1) instead of an
        # encoded map; the shader expects the encoded 0..1 form.
        rgb = rgb * 0.5 + 0.5
        print(f"{name}: signed vector detected, remapped to 0..1")

    out = np.clip(np.rint(rgb * 255.0), 0, 255).astype(np.uint8)
    write_png(dst_path, out)

    stats = ", ".join(
        f"{ch} min {out[..., i].min():3d} max {out[..., i].max():3d} mean {out[..., i].mean():6.1f}"
        for i, ch in enumerate("RGB")
    )
    print(f"{name} -> {os.path.basename(dst_path)}  {out.shape[1]}x{out.shape[0]}  {stats}")


def main():
    args = parse_args()
    src_dir = resolve(args.src)
    out_dir = resolve(args.out)
    os.makedirs(out_dir, exist_ok=True)

    exrs = sorted(f for f in os.listdir(src_dir) if f.lower().endswith(".exr"))
    if not exrs:
        sys.exit(f"no .exr files in {src_dir}")

    for name in exrs:
        stem = os.path.splitext(name)[0]
        convert(os.path.join(src_dir, name), os.path.join(out_dir, stem + ".png"), args.normal_min)

    print(f"wrote {len(exrs)} PNG files to {out_dir}")


if __name__ == "__main__":
    main()
