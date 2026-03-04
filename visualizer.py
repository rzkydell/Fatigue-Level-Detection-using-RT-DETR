import cv2

def draw_luxury_box(frame, box, label, color):
    x1, y1, x2, y2 = map(int, box)
    
    # 1. Bounding Box Dasar
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # 2. Sudut Siku Tebal
    length = int((x2 - x1) * 0.1)
    t = 5
    # Top Left
    cv2.line(frame, (x1, y1), (x1 + length, y1), color, t)
    cv2.line(frame, (x1, y1), (x1, y1 + length), color, t)
    # Top Right
    cv2.line(frame, (x2, y1), (x2 - length, y1), color, t)
    cv2.line(frame, (x2, y1), (x2, y1 + length), color, t)
    # Bottom Left
    cv2.line(frame, (x1, y2), (x1 + length, y2), color, t)
    cv2.line(frame, (x1, y2), (x1, y2 - length), color, t)
    # Bottom Right
    cv2.line(frame, (x2, y2), (x2 - length, y2), color, t)
    cv2.line(frame, (x2, y2), (x2, y2 - length), color, t)

    # 3. Label Background Solid
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 2
    (text_w, text_h), _ = cv2.getTextSize(label, font, font_scale, font_thickness)
    
    cv2.rectangle(frame, (x1, y1 - text_h - 15), (x1 + text_w + 10, y1), color, -1)
    cv2.putText(frame, label, (x1 + 5, y1 - 10), font, font_scale, (255, 255, 255), font_thickness)
    return frame