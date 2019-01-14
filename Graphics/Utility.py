__author__ = 'User'

import pygame

def rectangle_surface(width, height, color=(255,255,255), border_width = 0, border_color=(0,0,0)):
    rect = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw border
    rect.fill(border_color)

    # Draw inside
    rect.fill(color, rect=(border_width, border_width, width-2*border_width, height-2*border_width))

    return rect

def bar_surface(width, height, empty_amount, color_full=(255,255,255), color_empty=(255,255,255), border_width = 0, border_color=(0,0,0)):
    # First draw a full bar then we empty it
    full = rectangle_surface(width, height, color_full, border_width=border_width, border_color=border_color)

    # Get empty rectangle
    empty = rectangle_surface((width-border_width)*empty_amount, height-border_width*2, color_empty)

    full.blit(empty, (0,0))
    return full
