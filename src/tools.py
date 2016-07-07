def collised(sprite1, sprite2):
    r1 = sprite1.get_rect()
    r2 = sprite2.get_rect()
    return r1.intersects(r2)

# def rect_of_sprite(sprite):
#     x, y = sprite.position
#     w, h = sprite.width, sprite.height
#     rect = x, y, w, h
#     return rect
