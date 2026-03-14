import json

def calculate_overlap_ratio(layout):
    """
    Computes the percentage of components that overlap with each other.
    Lower is better. (Rubric 11: Quantitative Evaluation)
    """
    objects = layout.get("objects", [])
    if not objects: return 0
    
    overlaps = 0
    for i, obj1 in enumerate(objects):
        x1, y1, w1, h1 = obj1["bbox"]
        for j, obj2 in enumerate(objects):
            if i == j: continue
            x2, y2, w2, h2 = obj2["bbox"]
            
            # Check overlap
            if not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1):
                overlaps += 1
                break
                
    return (overlaps / len(objects)) * 100

def calculate_alignment_score(layout, grid=8):
    """
    Measures how well components are aligned to an 8px grid.
    Higher is better.
    """
    objects = layout.get("objects", [])
    if not objects: return 100
    
    off_grid = 0
    for obj in objects:
        x, y, w, h = obj["bbox"]
        if x % grid != 0 or y % grid != 0:
            off_grid += 1
            
    return (1 - (off_grid / len(objects))) * 100

if __name__ == "__main__":
    sample = {
        "objects": [
            {"label": "btn", "bbox": [10, 10, 50, 50]},
            {"label": "img", "bbox": [15, 15, 100, 100]} # Overlaps
        ]
    }
    
    print(f"Overlap Ratio: {calculate_overlap_ratio(sample):.2f}%")
    print(f"Alignment Score: {calculate_alignment_score(sample):.2f}%")
    
    # After optimization
    from layout_optimizer import optimize_layout
    optimized = optimize_layout(sample)
    print("\n--- After Optimization ---")
    print(f"Overlap Ratio: {calculate_overlap_ratio(optimized):.2f}%")
    print(f"Alignment Score: {calculate_alignment_score(optimized, grid=8):.2f}%")
