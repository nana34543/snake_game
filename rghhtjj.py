import random
import sys


import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
FPS = 20

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    def __init__(
        self,
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=None,
    ):
        self.position = position
        self.body_color = body_color
    def draw(self, surface):

        pass
class Apple(GameObject):

    def __init__(self):

        super().__init__(body_color=RED)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):

        occupied = set(snake_positions or [])
        free_cells = [
            (x * CELL_SIZE, y * CELL_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * CELL_SIZE, y * CELL_SIZE) not in occupied
        ]

        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = (
                random.randrange(GRID_WIDTH) * CELL_SIZE,
                random.randrange(GRID_HEIGHT) * CELL_SIZE,
            )

    def draw(self, surface):

        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):


    def __init__(self):

        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=GREEN,
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None
        self.last_tail = None

    def update_direction(self):
        if self.next_direction is None:
            return

        dx, dy = self.next_direction
        current_dx, current_dy = self.direction

        if (dx, dy) != (-current_dx, -current_dy) and (dx, dy) != (0, 0):
            self.direction = self.next_direction

        self.next_direction = None

    def move(self):

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx) % SCREEN_WIDTH,
            (head_y + dy) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.last_tail = self.positions.pop()
        else:
            self.last_tail = None

    def draw(self, surface):

        if self.last_tail is not None:
            tail_rect = pygame.Rect(self.last_tail, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, BLACK, tail_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):

        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.position = self.positions[0]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None
        self.last_tail = None


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (CELL_SIZE, 0)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()