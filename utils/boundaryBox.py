def getCenterOfBoundaryBox(bbox):
    x1,y1,x2,y2 = bbox
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    return int(x), int(y)

def getBoundaryBoxWidth(bbox):
    return bbox[2] - bbox[0]