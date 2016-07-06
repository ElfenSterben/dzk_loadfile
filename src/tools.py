def collision(sprite1, sprite2):
    rect1 = rect_of_sprite(sprite1)
    rect2 = rect_of_sprite(sprite2)
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    if abs(x1 - x2) < (w1 + w2) / 2 and abs(y1 - y2) < (h1 + h2) / 2:
        return True
    return False


def rect_of_sprite(sprite):
    x, y = sprite.position
    w, h = sprite.width, sprite.height
    rect = x, y, w, h
    return rect
