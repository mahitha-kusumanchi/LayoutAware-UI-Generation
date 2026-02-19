import json

# -------- Step 1: Sample JSON Layout --------

layout_json = '''
{
  "header": {"x": 0, "y": 0, "width": 100, "height": 15},
  "image": {"x": 0, "y": 15, "width": 50, "height": 50},
  "text": {"x": 50, "y": 15, "width": 50, "height": 50},
  "button": {"x": 40, "y": 70, "width": 20, "height": 10}
}
'''

# Convert string to Python dictionary
layout = json.loads(layout_json)

# -------- Step 2: Function to Convert Layout to Prompt --------

def generate_prompt(layout_data):

    prompt = "Generate a modern website UI screenshot.\n"

    for element in layout_data:

        data = layout_data[element]
        x = data["x"]
        y = data["y"]
        width = data["width"]

        # HEADER LOGIC
        if element == "header":
            prompt += "Top full-width header section.\n"

        # IMAGE LOGIC
        elif element == "image":
            if x == 0 and width == 50:
                prompt += "Left side image section in a two-column layout.\n"

        # TEXT LOGIC
        elif element == "text":
            if x == 50:
                prompt += "Right side text content area.\n"

        # BUTTON LOGIC
        elif element == "button":
            if y >= 60:
                prompt += "Bottom centered call-to-action button.\n"

    prompt += "Clean layout, professional design, realistic screenshot."

    return prompt

# -------- Step 3: Generate Prompt --------

final_prompt = generate_prompt(layout)

print("Generated Prompt:\n")
print(final_prompt)
