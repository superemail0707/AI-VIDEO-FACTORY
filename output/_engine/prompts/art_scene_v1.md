You are generating ONE illustration for the 2D chibi animation channel "Ngang Một Tí". Owner policy D-029 authorizes this generation.

TASK
1. Look at the reference images (character / style sheets) before generating:
{references}
2. Use your built-in ImageGen tool to generate EXACTLY ONE new image from the scene prompt below.
   - Portrait orientation, the tallest available portrait size (9:16 preferred; if only 2:3 is available, keep every character and important prop inside the CENTRAL 84% of the width, because the sides will be cropped to 9:16).
   - Full-bleed: no panel borders, no frames, no white or cream margins.
3. Save the generated image as a PNG file at exactly this path (create folders if needed, do NOT overwrite any other file):
   {target}
4. Do not create, edit, move or delete any other file. Do not run other commands. Do not generate more than one image.
5. Reply with ONLY this JSON (no other text):
   {{"saved": "<absolute path of the PNG you saved>", "source": "<path where ImageGen originally wrote the image, if different>", "width": <int>, "height": <int>}}

LAYOUT RULES (mandatory, from previous failures)
- Keep ALL characters in the UPPER TWO-THIRDS of the image. The bottom third must be a LARGE EMPTY foreground (floor, mat, ground) with no faces, hands, feet or props — subtitles are drawn there.
- Character heads must not touch the top edge; keep the top 12% of the image as background.
- Draw ONLY the characters named in the scene's CAST line, in exactly the state the ACTION describes (awake/asleep, holding/not). Every face at least 12% from the left/right edges; top of every head (and cat ears) at least 13% below the top edge.
- NO text, NO letters, NO numbers, NO speech bubbles with words, NO watermark, NO logo.
- Mimi is a brown tabby cat (dark stripes, green eyes, cream muzzle, white paws, pink inner ears); she never speaks.
- Do not repeat or vary a previous scene; this is a new, independent composition.
{fix_note}
SCENE PROMPT
<<<
{scene_prompt}
>>>
