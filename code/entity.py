import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    """
    Base class for Player-class and Souleater-class. Provides basic methods for movement and collision detection.

    Parameters
    ----------
    groups : list[]
        determines the sprite groups the entity-object belongs to
    obstacle_sprites: sprite.Group()
        group of sprites the entity-object is able to collide with

    Attributes
    ----------
    obstacle_sprites : sprite.Group()
        group of sprites for collision detection with objects
    hitbox : pygame.Rect
        inflated Rect for environment interaction
    direction : pygame.math.Vector2()
        vector to shift entity-object for movement
    frame_index : int
        index of image to be displayed for animation
    animation_speed : float
        increment of frame_index to run animation
    """
    def __init__(self, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = None

        # movement
        self.direction = pygame.math.Vector2(0, 0)

        # animation
        self.frame_index = 0
        self.animation_speed = 0.15

    def move(self, speed):
        """
            Determines general movement of entity-object by multiplication of direction vector and speed. Therefore,
            direction vector has to be normalised. Checks for collisions in horizontal and vertical direction by calling
            sub-method collision().

            Parameters
            ----------
            speed : int
                speed of entity
        """
        if self.direction.magnitude() != 0:
            # normalize vector to length=1
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
            Sub-method for checking whether a collision with an obstacle_sprite-hitbox has occurred. Sets the entity-
            object back from obstacle_sprite-hitbox in according direction .

            Parameters
            ----------
            direction : pygame.math.Vector2()
                vector to shift entity-object for movement
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving right
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

