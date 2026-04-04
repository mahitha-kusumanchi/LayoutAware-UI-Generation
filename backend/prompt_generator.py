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
            cx, cy = data["x"], data["y"]
            w, h = data["width"], data["height"]
            extracted.append({
                "label": label, 
                "bbox": [cx - w/2.0, cy - h/2.0, w, h],
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
            cx, cy = obj_data["x"], obj_data["y"]
            w, h = obj_data["width"], obj_data["height"]
            objects.append({
                "label": obj_data.get("label"), 
                "bbox": [cx - w/2.0, cy - h/2.0, w, h],
                "normalized": isinstance(obj_data["x"], float) and obj_data["x"] <= 1.0
            })
            
    if not objects:
        objects = extract_objects(data)
    
    title = data.get("title") or data.get("scene")
    if not title:
        title = "A Mobile App UI" if "children" in data or "class" in data else "A scene"
    
    if not objects:
        return title

    # Calculate actual scene bounds to describe elements relative to the layout itself
    valid_x_coords = []
    valid_y_coords = []
    
    for obj in objects:
        bbox = obj.get("bbox", [0, 0, 0, 0])
        if len(bbox) == 4:
            x, y, w, h = bbox
            valid_x_coords.extend([x, x + w])
            valid_y_coords.extend([y, y + h])
            
    if not valid_x_coords:
        return title
        
    min_x, max_x = min(valid_x_coords), max(valid_x_coords)
    min_y, max_y = min(valid_y_coords), max(valid_y_coords)
    
    scene_w = max_x - min_x if max_x > min_x else 1
    scene_h = max_y - min_y if max_y > min_y else 1
    
    # Map technical names to SD-friendly concepts
    semantic_map = {
        "popupdecorview": "popup dialog",
        "modal": "modal window",
        "textview": "text blocks",
        "imageview": "image",
        "button": "button",
        "icon": "icon",
        "text": "text block"
    }

    descriptions = []
    
    for obj in objects:
        raw_label = obj.get("label", "object").split('$')[-1].split('.')[-1].lower()
        label = semantic_map.get(raw_label, raw_label)
        
        bbox = obj.get("bbox", [0, 0, 0, 0])
        x, y, w, h = bbox
            
        cx = x + w / 2.0
        cy = y + h / 2.0
        
        # Calculate relative position within the layout bounds
        rel_x = (cx - min_x) / scene_w
        rel_y = (cy - min_y) / scene_h
        
        # Using 45% and 55% thresholds to strictly divide the UI into left/right columns, leaving a small center deadzone.
        h_pos = "left" if rel_x < 0.45 else "right" if rel_x > 0.55 else "center"
        v_pos = "top" if rel_y < 0.35 else "bottom" if rel_y > 0.65 else "middle"
        
        # Store as tuple for proper pluralization later
        descriptions.append((label, v_pos, h_pos))
        
    # Group duplicates to make the prompt cleaner
    from collections import Counter
    desc_counts = Counter(descriptions)
    
    
    prompt_items = []
    for (label, v_pos, h_pos), count in desc_counts.items():
        if count > 1:
            plural_label = label + "s" if not label.endswith("s") else label
            prompt_items.append(f"{count} {plural_label} {v_pos} {h_pos}")
        else:
            article = "an" if label[0].lower() in 'aeiou' else "a"
            prompt_items.append(f"{article} {label} {v_pos} {h_pos}")
            
    return f"{title} featuring: " + ", ".join(prompt_items) + "."
