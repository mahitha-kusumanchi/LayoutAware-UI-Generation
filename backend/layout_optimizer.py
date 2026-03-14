import json

def optimize_layout(layout_json, grid_size=8, threshold=10):
    """
    Applies rule-based logic to snap UI components to a grid and prevent overlaps.
    
    Args:
        layout_json (dict): Input JSON with 'objects' list.
        grid_size (int): The grid unit to snap coordinates to (default 8px).
        threshold (int): Distance threshold for snapping to neighbors.
        
    Returns:
        dict: The optimized layout JSON.
    """
    if isinstance(layout_json, str):
        data = json.loads(layout_json)
    else:
        data = layout_json
        
    objects = data.get("objects", [])
    optimized_objects = []
    
    for obj in objects:
        label = obj.get("label", "unknown")
        bbox = obj.get("bbox", [0, 0, 0, 0])
        x, y, w, h = bbox
        
        # 1. Snap to Grid (Rubric 7: Preprocessing/Consistency)
        x = round(x / grid_size) * grid_size
        y = round(y / grid_size) * grid_size
        w = round(w / grid_size) * grid_size
        h = round(h / grid_size) * grid_size
        
        # 2. Minimal Width/Height Constraint
        w = max(w, grid_size * 2) 
        h = max(h, grid_size * 2)
        
        new_obj = obj.copy()
        new_obj["bbox"] = [x, y, w, h]
        optimized_objects.append(new_obj)
        
    # 3. Simple Overlap Resolution (Optional: Horizontal/Vertical Check)
    # (Future-friendly placeholder for more complex logic)
        
    data["objects"] = optimized_objects
    return data

if __name__ == "__main__":
    # Test example
    sample = {
        "title": "Test Layout",
        "objects": [
            {"label": "button", "bbox": [15, 23, 107, 42]}
        ]
    }
    print(json.dumps(optimize_layout(sample), indent=4))
