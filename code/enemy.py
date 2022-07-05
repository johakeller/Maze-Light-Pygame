import pygame
from settings import *
from support import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphic setup
        self.import_graphics()
        self.status = 'left_idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        offset_x = pos[0] + (TILE_SIZE / 2)
        offset_y = pos[1] + (TILE_SIZE / 2)
        self.rect = self.image.get_rect(center=(offset_x, offset_y))
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # collision
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {'attack_damage': 34, 'attack_sound': '../audio/claw.wav', 'speed': 5,
                      'attack_radius': 30, 'notice_radius': 400}
        self.attack_damage = self.stats['attack_damage']
        self.speed = self.stats['speed']
        self.attack_radius = self.stats['attack_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 800
        self.damage_player = damage_player
        self.last_player_pos = None
        self.current_player_pos = None
        self.trigger_death_particles = trigger_death_particles
        self.can_remember = True
        self.remember_time = None
        self.remember_cooldown = 800

        # sound
        self.enemy_attack_sound = pygame.mixer.Sound('../audio/spider_attack.wav')
        self.enemy_attack_sound.set_volume(0.1)

    def import_graphics(self):
        enemy_path = '../graphics/enemy/'
        self.animations = {'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [],
                           'left_attack': [], 'right_attack': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player_pos):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(self.current_player_pos)[0]
        direction = self.get_player_distance_direction(self.current_player_pos)[1]

        if distance <= self.attack_radius and self.can_attack:
            if not 'attack' in self.status:
                self.frame_index = 0
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status = self.status + '_attack'
        elif distance <= player.visible_radius:
            if direction.x > 0:  # right
                self.status = 'right'
            elif direction.x < 0:  # left
                self.status = 'left'
        else:
            if not 'idle' in self.status:
                if 'attack' in self.status:
                    self.frame_index = 0
                    self.status = self.status.replace('attack', 'idle')
                else:
                    self.status = self.status + '_idle'

    def actions(self, player):
        if 'attack' in self.status:
            self.enemy_attack_sound.play()
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'left' or self.status == 'right':
            if player.light_on:
                self.direction = self.get_player_distance_direction(self.current_player_pos)[1]
            else:
                if player.light_switch and self.can_remember:
                    self.last_player_pos = player.rect.center
                    self.direction = self.get_player_distance_direction(self.last_player_pos)[1]
                    self.remember_time = pygame.time.get_ticks()
                    self.can_remember = False
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            # stop attack after animation
            if 'attack' in self.status:
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.can_remember:
            if current_time - self.remember_time >= self.remember_cooldown:
                self.can_remember = True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.current_player_pos = player.rect.center
        self.get_status(player)
        self.actions(player)
