import pygame
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/character/move/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -30)

        self.player_win = False

        # collision
        self.obstacle_sprites = obstacle_sprites

        # player movement
        self.cooldown = 400
        self.light_on = True
        self.light_switch = False
        self.light_time = None

        # animation
        self.frames = import_folder('../graphics/character/move/')

        # stats
        self.stats = {'health': 100, 'coins': 0, 'speed': 5, 'visible_factor': 1, 'visible_radius': 220}
        self.health = self.stats['health']
        self.coins = self.stats['coins']
        self.speed = self.stats['speed']
        self.visible_factor = self.stats['visible_factor']
        self.visible_radius = self.stats['visible_radius'] * self.visible_factor

        # enemy interaction
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 400

        # sounds
        self.coin_sound = pygame.mixer.Sound('../audio/coin.mp3')
        self.coin_sound.set_volume(1)
        self.flower_sound = pygame.mixer.Sound('../audio/flower.wav')
        self.flower_sound.set_volume(0.2)


    def move(self, speed):
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
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.sprite_type == 'silver':
                    self.coin_sound.play()
                    self.coins += 100
                    sprite.kill()
                elif sprite.sprite_type == 'gold':
                    self.coin_sound.play()
                    self.coins += 500
                    sprite.kill()
                elif sprite.sprite_type == 'flower':
                    self.flower_sound.play()
                    self.visible_factor += 0.3
                    self.speed += 1
                    new_health = self.health + 25
                    if new_health >= 100:
                        self.health = 100
                    else:
                        self.health = new_health
                    sprite.kill()
                elif sprite.sprite_type == 'goal':
                    self.player_win = True

    def input(self):
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


    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.light_switch:
            if current_time - self.light_time >= self.cooldown:
                self.light_switch = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        # set the image
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.animate()
        self.move(self.speed)
