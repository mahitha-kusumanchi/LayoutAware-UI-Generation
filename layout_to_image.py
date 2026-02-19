import json
from PIL import Image, ImageDraw


def load_layout(json_path):
    """
    Load layout from JSON file
    """
    with open(json_path, "r") as file:
        layout_data = json.load(file)
    return layout_data


def generate_layout_image(layout_data, output_path="layout.png"):
    """
    Convert layout JSON into a visual layout sketch image
    """

    # Create blank white image
    image_size = 512
    img = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(img)

    # Scale factor (JSON uses 0–100 system)
    scale = image_size / 100

    for element in layout_data:

        data = layout_data[element]

        x = data["x"] * scale
        y = data["y"] * scale
        width = data["width"] * scale
        height = data["height"] * scale

        # Draw rectangle
        draw.rectangle(
            [x, y, x + width, y + height],
            outline="black",
            width=3
        )

        # Write element name inside box
        draw.text((x + 5, y + 5), element, fill="black")

    # Save image
    img.save(output_path)
    print(f"Layout image saved as {output_path}")


# Run directly
if __name__ == "__main__":
    layout = load_layout("layout.json")
    generate_layout_image(layout)
