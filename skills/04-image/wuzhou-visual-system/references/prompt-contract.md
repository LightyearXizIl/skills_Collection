# Midjourney 输出规范

## Required format

Return a Chinese title followed by one concise English prompt that can be pasted directly into Midjourney.

Example structure:

```text
登基正殿全景

Grand wide establishing shot of ... no posing, ultra realistic, no CGI --ar 16:9 --style raw --no ...
```

Do not put Chinese instructions inside the MJ prompt. Do not append “调用SKILL.”

## Prompt order

Use this order unless the user's correction requires the existing structure to remain unchanged:

1. Shot type and camera angle.
2. Era, exact place, time, and weather.
3. Main subject, life stage, status, makeup, expression, and pose.
4. Costume and complete headdress.
5. One primary action and its relationship to nearby people or objects.
6. Foreground, midground, background, scale, symmetry, and negative space.
7. Architecture and historically useful props.
8. Transparent natural light, low-saturation Eastern palette, realistic skin and materials.
9. Lens and historical-film realism.
10. Parameters and concise negatives.

## Default rendering phrase

Use or adapt:

`transparent natural light, controlled warm highlights and cool shadows, low-saturation Eastern palette, realistic translucent skin texture, tactile silk brocade wood stone and bronze, gentle cinematic contrast, 35mm historical documentary photography, no posing, ultra realistic, no CGI`

Choose 50mm for balanced character scenes and 85mm for close portraits. Do not stack all lenses.

## Default ending

Use:

`--ar 16:9 --style raw`

Do not add `--chaos` or an explicit stylize value unless the user requests it.

## Negative vocabulary

Choose only what fits the shot:

`--no modern objects, modern architecture, modern makeup, Ming dynasty, Qing dynasty, Manchu clothing, fantasy armor, fairy costume, anime, CGI, plastic skin, oversaturated colors, heavy orange filter, excessive bloom, readable text, subtitles, watermark, logo, extra fingers, malformed hands`

Do not use a long negative list to compensate for an unclear positive prompt.

## Complexity limits

- One dominant action per prompt.
- Do not assign individual actions to a large cast.
- Keep the environment restrained enough that the subject and story function remain readable.
- State critical composition constraints early: `close-up`, `chest-up`, `direct overhead bird's-eye view`, `grand wide establishing shot`, `over-the-shoulder reverse shot`.
- State exclusions positively when possible: `the throne immediately behind her, no ministers visible behind her`.

## Targeted revision protocol

When asked to change a single element:

1. Copy the current approved prompt.
2. Locate the smallest clause that controls the requested element.
3. Replace only that clause.
4. Preserve all other wording, order, camera, light, negatives, and parameters.
5. Return only the revised item unless the user asks for the full set.

## Static/video boundary

This skill creates and reviews still-image assets. It may name the intended transition function, but it must not assign seconds, dialogue timing, camera trajectories, sound effects, or a 30-second edit. Use `$universal-30s-image-to-video` after the images are approved.

