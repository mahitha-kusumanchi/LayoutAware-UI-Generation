import json

def generate_prompt(layout_json):
    """
    Converts a layout JSON into a natural language prompt for Stable Diffusion.
    """
    if isinstance(layout_json, str):
        data = json.loads(layout_json)
    else:
        data = layout_json
        
    title = data.get("title", "A scene")
    objects = data.get("objects", [])
    
    if not objects:
        return title

    prompt_parts = [f"{title} featuring:"]
    
    for obj in objects:
        label = obj.get("label", "an object")
        x, y, w, h = obj.get("bbox", [0, 0, 0, 0])
        
        # Simple spatial description logic
        h_pos = "left" if x < 256 else "right" if x > 512 else "center"
        v_pos = "top" if y < 256 else "bottom" if y > 512 else "middle"
        
        prompt_parts.append(f"a {label} located at the {v_pos} {h_pos}")
        
    return ", ".join(prompt_parts) + "."

if __name__ == "__main__":
    # Test logic
    sample_data = {
        "title": "Forest",
        "objects": [{"label": "tree", "bbox": [10, 10, 50, 50]}]
    }
    print(generate_prompt(sample_data))
