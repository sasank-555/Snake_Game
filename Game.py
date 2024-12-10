import pygame as pg
import random
import collections

class SnakeGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((600, 400))
        self.snake = collections.deque([(100, 50), (90, 50), (80, 50)])
        self.direction = "RIGHT"
        self.font = pg.font.Font(None, 36)
        self.score = 0
        self.clock = pg.time.Clock()
        self.dmap = {"RIGHT": (10, 0), "LEFT": (-10, 0), "UP": (0, -10), "DOWN": (0, 10)}
        self.food = self.get_food()
        self.difficulty = "Medium"
        self.difficulty_mapping = {
            "Easy": 10,
            "Medium": 15,
            "Hard": 20
        }

    def display_text(self, text, color, position):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def get_food(self):
        return random.randrange(0, 600, 10), random.randrange(0, 400, 10)

    def draw_borders(self):
        pg.draw.rect(self.screen, "Black", (0, 0, 600, 10))  
        pg.draw.rect(self.screen, "Black", (0, 0, 10, 400))  
        pg.draw.rect(self.screen, "Black", (590, 0, 10, 400))  
        pg.draw.rect(self.screen, "Black", (0, 390, 600, 10))  

    def menu(self):
        self.screen.fill("purple") 
        self.draw_borders()  
        menu_running = True
        while menu_running:
            self.display_text("Snake Game", "White", (225, 50))
            self.display_text("Select Difficulty", "White", (200, 100))
            self.display_text("1. Easy", "White", (250, 150))
            self.display_text("2. Medium", "White", (250, 200))
            self.display_text("3. Hard", "White", (250, 250))
            self.display_text("Press 1, 2, or 3 to select", "White", (150, 300))

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_1:
                        self.difficulty = "Easy"
                        menu_running = False
                    if e.key == pg.K_2:
                        self.difficulty = "Medium"
                        menu_running = False
                    if e.key == pg.K_3:
                        self.difficulty = "Hard"
                        menu_running = False
            pg.display.update()
            self.clock.tick(30)

    def game_over(self):
        self.screen.fill("purple")  
        self.draw_borders()  
        self.display_text("Game Over!", "Red", (220, 110))
        self.display_text(f"Final Score: {self.score}", "White", (210, 160))
        self.display_text("Press 'Q' to Quit or 'R' to Restart", "White", (110, 210))
        pg.display.update()
        waiting_for_input = True
        while waiting_for_input:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_q:
                        pg.quit()
                        quit()
                    if e.key == pg.K_r:
                        self.__init__()
                        self.run()
                        waiting_for_input = False

    def update_snake(self):
        hx, hy = self.snake[0]
        dx, dy = self.dmap[self.direction]
        nx, ny = hx + dx, hy + dy
        if not (10 <= nx <= 590 and 10 <= ny <= 390) or (nx, ny) in self.snake:
            self.game_over()
        ok = False
        if (nx, ny) == self.food:
            ok = True
            self.food = self.get_food()
            self.score += 1
        self.snake.appendleft((nx, ny))
        if not ok:
            self.snake.pop()

    def display_snake(self):
        for s in self.snake:
            pg.draw.rect(self.screen, "green", (*s, 10, 10))

    def display_food(self):
        pg.draw.rect(self.screen, "red", (*self.food, 10, 10))

    def run(self):
        self.menu()
        while True:
            self.screen.fill("purple")  
            self.draw_borders()  
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    quit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    if e.key == pg.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    if e.key == pg.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    if e.key == pg.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
            self.update_snake()
            self.display_food()
            self.display_snake()
            score_text = self.font.render(f"Score: {self.score}", True, "White")
            self.screen.blit(score_text, (10, 10))
            pg.display.update()
            self.clock.tick(self.difficulty_mapping[self.difficulty])

game = SnakeGame()
game.run()
