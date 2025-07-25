import pygame

class Player:
    def __init__(self, WIDTH, HEIGHT, assets):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.PLAYER_WIDTH = 72
        self.PLAYER_HEIGHT = 97
        self.PLAYER_CROUCH_HEIGHT = 64
        self.x = WIDTH // 2 - self.PLAYER_WIDTH // 2
        self.y = HEIGHT - self.PLAYER_HEIGHT - 50
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 7
        self.jump_power = 18
        self.gravity = 1
        self.on_ground = True
        self.crouching = False
        self.assets = assets
        # Animation
        self.walk_frames = assets.get('player_walk', [])
        self.walk_frame_idx = 0
        self.walk_anim_timer = 0
        self.walk_anim_speed = 6  # frames per animation update
        self.facing_right = True

    def get_current_sprite(self):
        if not self.on_ground and self.assets['player_jump']:
            return self.assets['player_jump']
        elif self.crouching and self.assets['player_crouch']:
            return self.assets['player_crouch']
        elif self.on_ground and self.vel_x != 0 and self.walk_frames:
            return self.walk_frames[self.walk_frame_idx]
        elif self.assets['player']:
            return self.assets['player']
        return None

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True

    def update(self):
        prev_y = self.y
        self.x += self.vel_x
        self.y += self.vel_y
        if not self.on_ground:
            self.vel_y += self.gravity
        # Animation update
        if self.on_ground and not self.crouching and self.vel_x != 0 and self.walk_frames:
            self.walk_anim_timer += 1
            if self.walk_anim_timer >= self.walk_anim_speed:
                self.walk_anim_timer = 0
                self.walk_frame_idx = (self.walk_frame_idx + 1) % len(self.walk_frames)
        else:
            self.walk_frame_idx = 0
            self.walk_anim_timer = 0
        # Ground collision
        # Only align feet to ground when on ground (not jumping)
        ground_y = self.HEIGHT - 50
        if self.y + self.get_sprite_height() >= ground_y:
            self.y = ground_y - self.get_sprite_height()
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        # Keep player in screen bounds
        if self.x < 0:
            self.x = 0
        if self.x > self.WIDTH - self.PLAYER_WIDTH:
            self.x = self.WIDTH - self.PLAYER_WIDTH
        # When on ground, always align feet to ground for current sprite
        if self.on_ground:
            sprite = self.get_current_sprite()
            if sprite:
                sprite_height = sprite.get_height()
                self.y = ground_y - sprite_height

    def get_sprite_height(self):
        sprite = self.get_current_sprite()
        if sprite:
            return sprite.get_height()
        return self.PLAYER_HEIGHT

    def draw(self, screen):
        img = self.get_current_sprite()
        if img:
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (50, 50, 200), (self.x, self.y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT))

    def jump(self):
        self.vel_y = -self.jump_power
        self.on_ground = False

    def reset(self):
        self.x = self.WIDTH // 2 - self.PLAYER_WIDTH // 2
        self.y = self.HEIGHT - self.PLAYER_HEIGHT - 50
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.crouching = False
        self.walk_frame_idx = 0
        self.walk_anim_timer = 0
        self.facing_right = True 