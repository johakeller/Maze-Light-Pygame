import pygame

from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    """
    A class to create a particle effect when player is attacked by enemy. A PaticleEffect-object has its own animate()
    and update() methods.

    Attributes
    ----------
    frame_index : int
        index of the image to be displayed
    animation_speed : float
        increment of the frame_index-value
    animations : list
        images from folder to be displayed
    image : python.Surface
        current image being displayed on surface
    rect : python.Rect
        rect for the image for positioning
    """

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = import_folder('../graphics/particles/')
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Method to display particle animation, plays content of animations list and destroys the object afterwards to
        make the particles appear only once.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.kill()
        else:
            self.image = self.animations[int(self.frame_index)]

    def update(self):
        """
        Method to update particle object. Calls animate().
        """
        self.animate()
