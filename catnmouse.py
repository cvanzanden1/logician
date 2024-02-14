import pygame
import random

# Initialize Pygame
pygame.init()

# Set the width and height of the window
width = 1100
height = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cat, Mouse, and Cheese: A Love Story")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# classes for the mouse, cat, and cheese sprites
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, width), random.randint(0, height))
        self.speed = 2
        self.target_cheese = None

    def update(self):
        if not self.target_cheese or not self.target_cheese.alive():
            # Find the nearest cheese
            self.target_cheese = self.find_nearest_cheese()

        if self.target_cheese:
            # Move towards the target cheese
            target_x = self.target_cheese.rect.centerx
            target_y = self.target_cheese.rect.centery

            if self.rect.centerx < target_x:
                self.rect.x += self.speed
            elif self.rect.centerx > target_x:
                self.rect.x -= self.speed

            if self.rect.centery < target_y:
                self.rect.y += self.speed
            elif self.rect.centery > target_y:
                self.rect.y -= self.speed

        # Check if the mouse touched any cheese
        collided_cheese = pygame.sprite.spritecollide(self, cheese_group, True)
        for cheese in collided_cheese:
            score.increment()
            self.target_cheese = None

        # Keep the mouse within the screen bounds
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def find_nearest_cheese(self):
        min_distance = float('inf')
        nearest_cheese = None

        for cheese in cheese_group:
            distance = self.calculate_distance(cheese.rect.center, self.rect.center)
            if distance < min_distance:
                min_distance = distance
                nearest_cheese = cheese

        return nearest_cheese

    @staticmethod
    def calculate_distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

class Cat(pygame.sprite.Sprite):
    def __init__(self, mouse):
        super().__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, width), random.randint(0, height))
        self.speed = 1
        self.mouse = mouse

    def update(self):
        target_x = self.mouse.rect.centerx
        target_y = self.mouse.rect.centery

        if self.rect.centerx < target_x:
            self.rect.x += self.speed
        elif self.rect.centerx > target_x:
            self.rect.x -= self.speed

        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

        # Check if the cat touched the mouse
        if pygame.sprite.collide_rect(self, self.mouse):
            game_over()

        # Keep the cat within the screen bounds
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

class Cheese(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(None, 36)

    def increment(self):
        self.value += 1

    def draw(self):
        text = self.font.render("Score: " + str(self.value), True, GREEN)
        screen.blit(text, (10, 10))

# Game over function
def game_over():
    reset_game()
    screen.fill(WHITE)
    game_over_text = score.font.render("Game Over", True, RED)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Delay for 2 seconds

# Reset game function
def reset_game():
    all_sprites.empty()
    cheese_group.empty()
    score.value = 0

    mouse = Mouse()
    cat = Cat(mouse)

    all_sprites.add(mouse, cat)

    # Create cheese squares
    for _ in range(7):
        pos = (random.randint(0, width), random.randint(0, height))
        cheese = Cheese(pos)
        cheese_group.add(cheese)
        all_sprites.add(cheese)

# Create sprite groups
all_sprites = pygame.sprite.Group()
cheese_group = pygame.sprite.Group()

# Create the mouse and cat
mouse = Mouse()
cat = Cat(mouse)



# Create cheese squares
for _ in range(7):
    pos = (random.randint(0, width), random.randint(0, height))
    cheese = Cheese(pos)
    cheese_group.add(cheese)
    all_sprites.add(cheese)

# Add the mouse, cat, and score to the sprite group
all_sprites.add(mouse, cat)

# Create the score
score = Score()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Check if all cheese is collected
    if len(cheese_group) == 0:
        reset_game()
        screen.fill(WHITE)
        win_text = score.font.render("You Win!", True, GREEN)
        screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Delay for 2 seconds

    # Render the screen
    screen.fill(WHITE)
    all_sprites.draw(screen)
    score.draw()
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
