from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Dict

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "assets" / "hero.yml"
OUTPUT_PATH = ROOT / "assets" / "hero.svg"

DEFAULT_CONFIG: Dict[str, Any] = {
    "name": "0MollyMan0",
    "subtitle": "Low-Level Development • Graphics • Cybersecurity",
    "canvas": {
        "width": 1200,
        "height": 380,
    },
    "panel": {
        "width": 900,
        "height": 168,
        "radius": 34,
    },
    "colors": {
        "background_top": "#24163E",
        "background_bottom": "#101827",
        "blob_lavender": "#C8A8FF",
        "blob_blue": "#96BFFF",
        "blob_periwinkle": "#B6A1FF",
        "glass_fill": "#FFFFFF",
        "glass_fill_opacity": 0.11,
        "glass_stroke": "#FFFFFF",
        "glass_stroke_opacity": 0.22,
        "text_primary": "#F8F8FF",
        "text_secondary": "#E4E9FF",
    },
    "fonts": {
        "name_size": 70,
        "subtitle_size": 30,
        "name_weight": 700,
        "subtitle_weight": 500,
    },
    "animation": {
        "drift_1": "52s",
        "drift_2": "64s",
        "drift_3": "58s",
        "drift_4": "70s",
    },
}


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    else:
        raw = {}
    return deep_merge(DEFAULT_CONFIG, raw)


def normalize_duration(value: Any) -> str:
    text = str(value).strip()
    return text if text.endswith("s") else f"{text}s"


def blob_group(
    *,
    name: str,
    cx: int,
    cy: int,
    rx: int,
    ry: int,
    fill_id: str,
    opacity: float,
    drift_x_1: int,
    drift_y_1: int,
    drift_x_2: int,
    drift_y_2: int,
    duration: str,
) -> str:
    return f"""
    <g opacity="{opacity:.2f}" filter="url(#blobBlur)" transform="translate({cx},{cy})">
      <ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="url(#{fill_id})">
        <animateTransform
          attributeName="transform"
          type="translate"
          values="0 0; {drift_x_1} {drift_y_1}; {drift_x_2} {drift_y_2}; 0 0"
          keyTimes="0; 0.35; 0.7; 1"
          dur="{duration}"
          repeatCount="indefinite"
        />
      </ellipse>
    </g>
    """


def main() -> None:
    cfg = load_config()

    canvas = cfg["canvas"]
    panel = cfg["panel"]
    colors = cfg["colors"]
    fonts = cfg["fonts"]
    animation = cfg["animation"]

    width = int(canvas["width"])
    height = int(canvas["height"])

    panel_w = int(panel["width"])
    panel_h = int(panel["height"])
    panel_r = int(panel["radius"])

    name = escape(str(cfg["name"]))
    subtitle = escape(str(cfg["subtitle"]))

    name_size = int(fonts["name_size"])
    subtitle_size = int(fonts["subtitle_size"])
    name_weight = int(fonts["name_weight"])
    subtitle_weight = int(fonts["subtitle_weight"])

    duration_1 = normalize_duration(animation["drift_1"])
    duration_2 = normalize_duration(animation["drift_2"])
    duration_3 = normalize_duration(animation["drift_3"])
    duration_4 = normalize_duration(animation["drift_4"])

    panel_x = (width - panel_w) / 2
    panel_y = (height - panel_h) / 2
    center_x = width / 2

    blobs = [
        blob_group(
            name="blobA",
            cx=-120,
            cy=70,
            rx=300,
            ry=220,
            fill_id="blobLavender",
            opacity=0.42,
            drift_x_1=18,
            drift_y_1=8,
            drift_x_2=8,
            drift_y_2=-10,
            duration=duration_1,
        ),
        blob_group(
            name="blobB",
            cx=145,
            cy=390,
            rx=260,
            ry=190,
            fill_id="blobBlue",
            opacity=0.36,
            drift_x_1=-14,
            drift_y_1=-10,
            drift_x_2=-4,
            drift_y_2=8,
            duration=duration_2,
        ),
        blob_group(
            name="blobC",
            cx=1045,
            cy=55,
            rx=250,
            ry=180,
            fill_id="blobPeriwinkle",
            opacity=0.40,
            drift_x_1=-10,
            drift_y_1=10,
            drift_x_2=-18,
            drift_y_2=2,
            duration=duration_3,
        ),
        blob_group(
            name="blobD",
            cx=1280,
            cy=320,
            rx=240,
            ry=175,
            fill_id="blobLavender",
            opacity=0.30,
            drift_x_1=10,
            drift_y_1=-8,
            drift_x_2=18,
            drift_y_2=-2,
            duration=duration_4,
        ),
    ]

    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
  width="{width}"
  height="{height}"
  viewBox="0 0 {width} {height}"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label="{name} profile header"
  preserveAspectRatio="xMidYMid meet"
>
  <defs>
    <clipPath id="roundedClip">
      <rect width="{width}" height="{height}" rx="36" ry="36" />
    </clipPath>

    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{colors['background_top']}" />
      <stop offset="100%" stop-color="{colors['background_bottom']}" />
    </linearGradient>

    <radialGradient id="blobLavender" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{colors['blob_lavender']}" stop-opacity="0.95" />
      <stop offset="55%" stop-color="{colors['blob_lavender']}" stop-opacity="0.35" />
      <stop offset="100%" stop-color="{colors['blob_lavender']}" stop-opacity="0.00" />
    </radialGradient>

    <radialGradient id="blobBlue" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{colors['blob_blue']}" stop-opacity="0.95" />
      <stop offset="55%" stop-color="{colors['blob_blue']}" stop-opacity="0.30" />
      <stop offset="100%" stop-color="{colors['blob_blue']}" stop-opacity="0.00" />
    </radialGradient>

    <radialGradient id="blobPeriwinkle" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="{colors['blob_periwinkle']}" stop-opacity="0.95" />
      <stop offset="55%" stop-color="{colors['blob_periwinkle']}" stop-opacity="0.32" />
      <stop offset="100%" stop-color="{colors['blob_periwinkle']}" stop-opacity="0.00" />
    </radialGradient>

    <linearGradient id="panelGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{colors['glass_fill']}" stop-opacity="{float(colors['glass_fill_opacity']) + 0.04}" />
      <stop offset="100%" stop-color="{colors['glass_fill']}" stop-opacity="{colors['glass_fill_opacity']}" />
    </linearGradient>

    <filter id="blobBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="28" />
    </filter>

    <filter id="panelShadow" x="-20%" y="-30%" width="140%" height="180%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="{colors['blob_lavender']}" flood-opacity="0.14" />
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#FFFFFF" flood-opacity="0.06" />
    </filter>

    <style>
      .title {{
        font-family: Inter, Segoe UI, Helvetica Neue, Arial, sans-serif;
        font-size: {name_size}px;
        font-weight: {name_weight};
        letter-spacing: 3px;
        fill: {colors['text_primary']};
      }}

      .subtitle {{
        font-family: Inter, Segoe UI, Helvetica Neue, Arial, sans-serif;
        font-size: {subtitle_size}px;
        font-weight: {subtitle_weight};
        letter-spacing: 1.6px;
        fill: {colors['text_secondary']};
      }}
    </style>
  </defs>

<g clip-path="url(#roundedClip)">

  <rect width="{width}" height="{height}" fill="url(#bgGradient)" />

  {''.join(blobs)}

  <g filter="url(#panelShadow)">
    <rect
      x="{panel_x}"
      y="{panel_y}"
      width="{panel_w}"
      height="{panel_h}"
      rx="{panel_r}"
      fill="url(#panelGradient)"
      stroke="{colors['glass_stroke']}"
      stroke-opacity="{colors['glass_stroke_opacity']}"
      stroke-width="1.2"
    />

    <text
      x="{center_x}"
      y="{panel_y + 70}"
      text-anchor="middle"
      class="title"
    >{name}</text>

    <text
      x="{center_x}"
      y="{panel_y + 118}"
      text-anchor="middle"
      class="subtitle"
    >{subtitle}</text>
  </g>

</g>
</svg>
"""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()