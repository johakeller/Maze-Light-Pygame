import pygame

from entity import Entity
from support import import_folder


class Player(Entity):
    """
    A class to create the player object. Allows for player control via keyboard input and determines general statistics,
    movement and environment interaction like coin collection etc.

    Parameters
    ----------
    pos : (x,y)
        determines position of the player-sprite
    groups : list
        determines the sprite groups the player belongs to
    obstacle_sprites : pygame.sprite.Group()
        group of sprites the player is able to collide with

    Attributes
    ----------
    image : str
        selection of image for animation frame
    rect : pygame.Rect
        determines position of frames
    hitbox : pygame.Rect
        inflated Rect for environment interaction
    player_win : bool
        True if player-hit_box collides with goal-sprite
    obstacle_sprites : sprite.Group()
        group of collide able environment-sprites
    cooldown : int
        value for input timer regulation
    light_on : bool
        light is on: player can see and is visible for enemies
    light_switch : bool
        player has switched light off/on
    light_time : float
        timer since last light switch
    animations : str
        path to folder with images for animation
    stats : dict
        dictionary of player attributes
    health : int
        health of player
    coins : int
        coins collected for score
    speed : int
        speed of player movement
    visible_factor : float
        factor by which visibility-radius of player is multiplied
    visible_radius : int
        radius in which player is able to see and to be seen by enemies
    vulnerable : bool
        if true enemy can attack player and cause damage
    hurt_time : float
        time of attack by enemy
    invulnerability_duration : int
        duration in which player is not able to be attacked
    """

    def __init__(self, pos, groups, obstacle_sprites):
        # general setup
        super().__init__(groups, obstacle_sprites)
        self.image = pygame.image.load('../graphics/player/move/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -30)
        self.player_win = False

        # player movement
        self.cooldown = 400
        self.light_on = True
        self.light_switch = False
        self.light_time = None

        # animation
        self.animations = import_folder('../graphics/player/move/')

        # statistics
        self.stats = {'health': 100, 'coins': 0, 'speed': 5, 'visible_factor': 1, 'visible_radius': 220}
        self.health = self.stats['health']
        self.coins = self.stats['coins']
        self.speed = self.stats['speed']
        self.visible_factor = self.stats['visible_factor']
        self.visible_radius = self.stats['visible_radius'] * self.visible_factor

        # souleater interaction
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 400

        # sounds
        self.coin_sound = pygame.mixer.Sound('../audio/coin.mp3')
        self.coin_sound.set_volume(1)
        self.flower_sound = pygame.mixer.Sound('../audio/flower.wav')
        self.flower_sound.set_volume(0.2)

    def move(self, speed):
        """
        Determines movement of player by keyboard input via direction vector * speed. Therefore, direction vector
        has to be normalised. Checks for collisions in horizontal and vertical direction by calling sub-methods
        item_collection() and collision().

        Parameters
        ----------
        speed : int
            speed of player
        """
        if self.direction.magnitude() != 0:
            # normalize vector to length=1
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.item_collection()
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.item_collection()
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def item_collection(self):
        """
        Determines movement of player by keyboard input via direction vector * speed. Therefore, direction vector
        has to be normalised. Checks for collisions in horizontal and vertical direction by calling sub-methods
        item_collection() and collision().
        """
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                # silver coin collection
                if sprite.sprite_type == 'silver':
                    pygame.mixer.find_channel(True).play(self.coin_sound)
                    self.coins += 100
                    sprite.kill()
                # gold coin collection
                elif sprite.sprite_type == 'gold':
                    pygame.mixer.find_channel(True).play(self.coin_sound)
                    self.coins += 500
                    sprite.kill()
                # flower collection
                elif sprite.sprite_type == 'flower':
                    pygame.mixer.find_channel(True).play(self.flower_sound)
                    self.visible_factor += 0.3
                    self.speed += 1
                    new_health = self.health + 25
                    if new_health >= 100:
                        self.health = 100
                    else:
                        self.health = new_health
                    sprite.kill()
                # win condition
                elif sprite.sprite_type == 'goal':
                    self.player_win = True

    def input(self):
        """
        Retrieves input from keyboard to move up, down, left right and activates light switch (including light
        switch timer)via space-button.
        """
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # light input
        if keys[pygame.K_SPACE] and not self.light_switch:
            self.light_switch = True
            self.light_time = pygame.time.get_ticks()
            if self.light_on:
                self.light_on = False
            else:
                self.light_on = True

    def check_cooldown(self):
        """
        Retrieves input from keyboard to move up, down, left right and activates light switch (including light
        switch timer)via space-button.
        """
        current_time = pygame.time.get_ticks()
        # light switch cooldown
        if self.light_switch:
            if current_time - self.light_time >= self.cooldown:
                self.light_switch = False
        # vulnerability cooldown
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        """
        Method to display player animation, loops over animations list and is displaying the image in self.image.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        self.image = self.animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        """
        Method to update player object.
        """
        self.input()
        self.check_cooldown()
        self.animate()
        self.move(self.speed)
