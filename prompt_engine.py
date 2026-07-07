"""
Prompt enhancement engine — purely rule-based, no API calls needed.
Appends quality boosting keywords that work well with Stable Diffusion models.
"""

QUALITY_SUFFIXES = [
    "highly detailed",
    "sharp focus",
    "8k resolution",
    "professional photography",
    "cinematic lighting",
    "vibrant colors",
    "masterpiece",
]

STYLE_MAP = {
    "portrait":     "portrait, bokeh background, soft lighting, shallow depth of field",
    "landscape":    "landscape, golden hour, dramatic sky, wide angle lens",
    "anime":        "anime style, cel shading, vibrant, Studio Ghibli inspired",
    "cartoon":      "cartoon style, flat design, bold outlines, colorful",
    "realistic":    "photorealistic, hyper-realistic, ultra detailed, DSLR quality",
    "painting":     "oil painting, impasto technique, rich textures, museum quality",
    "sketch":       "pencil sketch, graphite drawing, hatching, detailed linework",
    "fantasy":      "fantasy art, epic scene, magical atmosphere, concept art",
    "sci-fi":       "sci-fi, futuristic, neon lights, cyberpunk aesthetic",
    "watercolor":   "watercolor painting, soft washes, delicate, artistic",
}

NEGATIVE_PROMPTS_NOTE = (
    "blurry, low quality, deformed, ugly, bad anatomy, watermark, "
    "text, signature, jpeg artifacts, out of focus"
)


def enhance_prompt(prompt: str) -> str:
    """
    Enhance a raw user prompt with quality and style keywords.

    Strategy:
    1. Detect any style keywords the user already mentioned.
    2. Append matching style descriptors.
    3. Append universal quality suffixes.
    """
    prompt = prompt.strip()
    lower = prompt.lower()

    style_additions = []
    for keyword, descriptor in STYLE_MAP.items():
        if keyword in lower:
            style_additions.append(descriptor)

    # Build enhanced prompt
    parts = [prompt]
    if style_additions:
        parts.extend(style_additions)

    # Always add quality boosters
    parts.extend(QUALITY_SUFFIXES)

    enhanced = ", ".join(parts)
    return enhanced


def get_negative_prompt() -> str:
    """Return a standard negative prompt for Stable Diffusion."""
    return NEGATIVE_PROMPTS_NOTE
