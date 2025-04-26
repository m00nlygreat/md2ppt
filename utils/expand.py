def expand(shapes, idx, p):

    def coordinatify(shape):
        return {
            **shape,
            "right": shape["left"] + shape["width"],
            "bottom": shape["top"] + shape["height"],
            "tl": (shape["top"], shape["left"]),
            "tr": (shape["top"], shape["left"] + shape["width"]),
            "bl": (shape["top"] + shape["height"], shape["left"]),
            "br": (shape["top"] + shape["height"], shape["left"] + shape["width"]),
        }

    def are_related(foo, bar, direction):
        if direction == "left":
            # bar가 foo의 왼쪽에 있고, 세로(y축) 범위가 겹치는지
            return bar["left"] + bar["width"] <= foo["left"] and \
                max(foo["top"], bar["top"]) <= min(foo["top"] + foo["height"], bar["top"] + bar["height"])

        elif direction == "right":
            # bar가 foo의 오른쪽에 있고, 세로(y축) 범위가 겹치는지
            return bar["left"] >= foo["left"] + foo["width"] and \
                max(foo["top"], bar["top"]) <= min(foo["top"] + foo["height"], bar["top"] + bar["height"])

        elif direction == "above":
            # bar가 foo의 위에 있고, 가로(x축) 범위가 겹치는지
            return bar["top"] + bar["height"] <= foo["top"] and \
                max(foo["left"], bar["left"]) <= min(foo["left"] + foo["width"], bar["left"] + bar["width"])

        elif direction == "below":
            # bar가 foo의 아래에 있고, 가로(x축) 범위가 겹치는지
            return bar["top"] >= foo["top"] + foo["height"] and \
                max(foo["left"], bar["left"]) <= min(foo["left"] + foo["width"], bar["left"] + bar["width"])

    def find_canvas(shapes):
        top = min([shape["top"] for shape in shapes])
        left = min([shape["left"] for shape in shapes])
        width = max([shape["left"] + shape["width"] for shape in shapes]) - left
        height = max([shape["top"] + shape["height"] for shape in shapes]) - top
        s = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
        }
        return coordinatify(s)
    
    def greater_margin(foo, bar):
        def emu(val):
            return int(val * 914400)
        f = foo.get("margin",0)
        b = bar.get("margin",0)
        return emu(f) if  f > b else emu(b)
    
    canvas = find_canvas(shapes)
    sphs = [coordinatify(shape) for shape in shapes]
    dir = {
        "d" : ("left", "right", "above", "below"),
        "left": ("left", "right"),
        "right": ("right", "left"),
        "above": ("top", "bottom"),
        "below": ("bottom", "top")
    }
    
    foo = sphs.pop(idx)
    bars = sphs
    
    deltas = {
        'left' : 0,
        'right' : 0,
        'above' : 0,
        'below' : 0,
    }
    
    for d in dir['d']:
        related = [s for s in bars if are_related(foo, s, d)]
        if bool(related):
            most_close = min(abs(foo[dir[d][0]]-bar[dir[d][1]]) - greater_margin(foo,bar) for bar in related)
            deltas.update({d: most_close})
        else:
            reaching_canvas = abs(foo[dir[d][0]]-canvas[dir[d][0]])
            deltas.update({d: reaching_canvas})

    return deltas