import json

def extract_objects(data):
    """Recursively extract objects from nested Android UI layouts."""
    extracted = []
    
    # Check if this node is an "object" itself
    label = data.get("componentLabel") or data.get("label") or data.get("class", "").split(".")[-1]
    bounds = data.get("bounds") or data.get("bbox")
    
    if label:
        if bounds:
            # Convert [x1, y1, x2, y2] to [x, y, w, h] if necessary
            if len(bounds) == 4:
                x, y, x2, y2 = bounds
                if x2 > x and y2 > y: # likely [x1, y1, x2, y2]
                    w, h = x2 - x, y2 - y
                else: # likely already [x, y, w, h]
                    w, h = x2, y2
                extracted.append({"label": label, "bbox": [x, y, w, h]})
        elif "x" in data and "y" in data and "width" in data and "height" in data:
            # Handle normalized fractional coordinates or explicit x,y,w,h keys
            extracted.append({
                "label": label, 
                "bbox": [data["x"], data["y"], data["width"], data["height"]],
                "normalized": isinstance(data["x"], float) and data["x"] <= 1.0
            })
            
    # Recurse into children
    children = data.get("children", [])
    for child in children:
        extracted.extend(extract_objects(child))
        
    return extracted

def generate_prompt(layout_json):
    """
    Converts a layout JSON (flat or nested) into a natural language prompt.
    """
    if isinstance(layout_json, str):
        data = json.loads(layout_json)
    else:
        data = layout_json
        
    # Same extraction logic as layout_to_image
    objects = []
    for obj_data in data.get("objects", []):
        if "label" not in obj_data: continue
        
        if "bbox" in obj_data:
            objects.append(obj_data)
        elif "x" in obj_data and "y" in obj_data and "width" in obj_data and "height" in obj_data:
            objects.append({
                "label": obj_data.get("label"), 
                "bbox": [obj_data["x"], obj_data["y"], obj_data["width"], obj_data["height"]],
                "normalized": isinstance(obj_data["x"], float) and obj_data["x"] <= 1.0
            })
            
    if not objects:
        objects = extract_objects(data)
    
    title = data.get("title") or data.get("scene")
    if not title:
        title = "A Mobile App UI" if "children" in data or "class" in data else "A scene"
    
    if not objects:
        return title

    prompt_parts = [f"{title} featuring:"]
    
    for obj in objects:
        label = obj.get("label", "an object")
        bbox = obj.get("bbox", [0, 0, 0, 0])
        x, y, w, h = bbox
        
        # Simple spatial description logic
        normalized = obj.get("normalized", False)
        if not normalized and max(w, h, x, y) <= 1.0:
            normalized = True
        
        if normalized:
            # Coordinates are [0.0, 1.0]
            h_pos = "left" if x < 0.33 else "right" if x > 0.66 else "center"
            v_pos = "top" if y < 0.33 else "bottom" if y > 0.66 else "middle"
        else:
            # Assuming 1440x2560 or similar for UI
            h_pos = "left" if x < 400 else "right" if x > 1000 else "center"
            v_pos = "top" if y < 800 else "bottom" if y > 1800 else "middle"
        
        prompt_parts.append(f"a {label} {v_pos} {h_pos}")
        
    return ", ".join(prompt_parts) + "."
