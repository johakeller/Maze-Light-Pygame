from entity import Entity
from support import *


class Souleater(Entity):
    """
    A class to create an enemy-object as opponent to the player. Class inherits from Entity, allows control over enemy-
    object via general statistics, movement and behaviour control and player interaction.

    Parameters
    ----------
    pos : (x,y)
        determines position of the enemy-sprite
    groups : list
        determines the sprite groups the enemy-object belongs to
    obstacle_sprites: pygame.sprite.Group()
        group of sprites the enemy is able to collide with
    damage_player : def
        function which determines damage for player-object

    Attributes
    ----------
    sprite_type : str
        type of sprite object
    animations : dict
        dictionary of status and lists of images for animation
    import_graphics() : method call
        method coll to set up enemy graphics
    status : str
        status for behavior determination
    image : str
        selection of image for animation frame
    rect : pygame.Rect
        determines position of frames
    hitbox : pygame.Rect
        inflated Rect for environment interaction
    obstacle_sprites : sprite.Group()
        group of collide able sprites
    stats : dict
        dictionary of enemy attributes
            self.attack_damage = self.stats['attack_damage']
    speed : int
        speed of enemy
    attack_radius : int
        radius in which attack on player is possible
    can_attack : boolean
        determines whether enemy is able to attack player
    attack_time : int
        time of attack for timer
    attack_cooldown : int
        time for cooldown after attack
    damage_player : def
        function which determines damage for player-object
    last_player_pos : (x,y)
        last position of player before light was switched off
    current_player_pos : (x,y)
        current position of player-object
    can_remember : boolean
         ability of enemy to remember new player position
    remember_time : int
        time of remember player position
    remember_cooldown : int
        cooldown for remembering player position
    """

    def __init__(self, pos, groups, obstacle_sprites, damage_player):
        # general setup
        super().__init__(groups, obstacle_sprites)
        self.sprite_type = 'souleater'

        # graphic setup
        self.animations = {'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [],
                           'left_attack': [], 'right_attack': []}
        self.import_graphics()
        self.status = 'left_idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(center=(pos[0] + (TILE_SIZE / 2), pos[1] + (TILE_SIZE / 2)))
        self.hitbox = self.rect.inflate(0, -10)

        # statistics
        self.stats = {'attack_damage': 34, 'attack_sound': '../audio/claw.wav', 'speed': 5,
                      'attack_radius': 30, 'notice_radius': 400}
        self.attack_damage = self.stats['attack_damage']
        self.speed = self.stats['speed']
        self.attack_radius = self.stats['attack_radius']

        # enemy-player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 800
        self.damage_player = damage_player
        self.last_player_pos = None
        self.current_player_pos = None
        self.can_remember = True
        self.remember_time = None
        self.remember_cooldown = 800

        # sound
        self.enemy_sound = pygame.mixer.Sound('../audio/souleater_walk.mp3')
        self.enemy_sound.set_volume(0.01)

    def import_graphics(self):
        """
        Import graphics for animation
        """
        enemy_path = '../graphics/souleater/'

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player_pos):
        """
        Retrieves vector comprising distance and direction to player

        Parameters
        ----------
        player_pos : (x,y)
            assumed position of player object

        Returns
        -------
        (float, float)
            distance and direction of player-object
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player_pos)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:

            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return (distance, direction)

    def get_status(self, player):
        """
        Determines whether in visible radius of player, if yes, changing status to move status ('left' or 'right').When
        player is close enough for attack, changes to 'attack' status. If distance is larger than visible radius of
        player: status is 'idle'

        Parameters
        ----------
        player : Player
            player object
        """
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
        """
        Determines whether in visible radius of player, if yes, changing status to move status ('left' or 'right').When
        player is close enough for attack, changes to 'attack' status. If distance is larger than visible radius of
        player: status is 'idle'

        Parameters
        ----------
        player : Player
            player object
        """
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'left' or self.status == 'right':
            pygame.mixer.find_channel(True).play(self.enemy_sound)
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
        """
        Chooses path for animation accordingly to status and fills animations with images from path. Loops over frame
        index and restarts animation after finished. By setting can_attack to False in case of attack, attack can be
        only played once in range of timer.
        """
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = False
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        """
        Cooldown timer for can_attack. After enemy attacked player, attack_time is saved. If passed time is greater than
        cooldown time, can_attack is set back to True. Same functionality for can_remember to guarantee, last player
        position is only remembered once, once light is turned off.
        """
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.can_remember:
            if current_time - self.remember_time >= self.remember_cooldown:
                self.can_remember = True

    def update(self):
        """
        Update method to run current movement, animation and cooldown for souleater-object. Calls move(), animate() and
        cooldown().
        """
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        """
        Update method to get current player position, status and determine actions. Is called in class Level run()
        method.
        """
        self.current_player_pos = player.rect.center
        self.get_status(player)
        self.actions(player)
