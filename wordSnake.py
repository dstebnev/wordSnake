import sys, pygame, math, random, time

config = {
    "WIDTH": 800,
    "HEIGHT" : 600,
    "BACKGROUND_COLOR" : (0, 0, 0),
    "GRID_SIZE" : 50,
    "GRID_WIDTH" : 800,
    "GRID_HEIGHT" : 600, 
}


class SnakeNode():
    def __init__(self, letter, x, y):
        self.x = x
        self.y = y
        self.letter = letter
    
    def update_position(self, x, y):
        self.x = x
        self.y = y
        

class Snake():
    def __init__(self, body, direction="r"):
        self.body = body
        self.direction = direction
    
    def update_position(self, next_x, next_y):        
        # node - SnakeNode
        for node in self.body:
            temp_x = node.x
            temp_y = node.y
            node.update_position(next_x, next_y)
            next_x = temp_x
            next_y = temp_y
        pass
    
    def check_collision(self, feeds):
        for feed in feeds:
            if self.body[0].x == feed.x and self.body[0].y == feed.y and feed.show:
                self.body.append(feed.become_node())
                feed.delete_feed()
        
    def set_diraction(self, d):
        self.direction = d
    
    def add_letter(self, letter):
        self.body = self.body + letter

class Feed():
    def __init__(self, letter, x=0, y=0):
        self.letter = letter
        self.x = x
        self.y = y
        self.show = True   
        
    def update_coord(self, x, y):
        self.x = x
        self.y = y
        
    def delete_feed(self):
        self.show = False
        
    def become_node(self):
        return SnakeNode(self.letter, self.x, self.y)


def choose_random_word():
    """Return a random word for the game."""
    words = ["ATE", "PYTHON", "HELLO", "WORLD", "GAMES"]
    return random.choice(words).upper()

def init_feeds(word, config):
    letters = list(word)
    feeds = []

    for l in letters:
        f = Feed(l)
        f.update_coord(
            random.randint(2, config['WIDTH'] // config['GRID_SIZE'] - 1),
            random.randint(2, config['HEIGHT'] // config['GRID_SIZE'] - 1)
        )
        feeds.append(f)

    return feeds


def check_letter_collision(snake, feeds, word, index):
    """Check if snake collides with the expected letter."""
    for feed in feeds:
        if feed.show and snake.body[0].x == feed.x and snake.body[0].y == feed.y:
            if feed.letter == word[index]:
                snake.body.append(feed.become_node())
                feed.delete_feed()
                return index + 1, True
            return index, False
    return index, True

def show_feeds(screen, font, feeds, config):
    for feed in feeds:
        text = font.render(feed.letter, True, (0,245,0))
        if feed.show:
            screen.blit(text, (feed.x*config['GRID_SIZE'],feed.y*config['GRID_SIZE']))
                
def start_game(config):
    pygame.init()
    screen = pygame.display.set_mode((config['WIDTH'],config['HEIGHT']))
    pygame.display.set_caption("WordSnake")
    screen.fill(config['BACKGROUND_COLOR'])
    
    word = choose_random_word()
    first_letter = word[0]
    letter_size = 50
    step = 1
    pause = False
    head_x = 1
    head_y = 1
    head = SnakeNode(first_letter, head_x, head_y)
    snake = Snake([head])
    feeds = init_feeds(word, config)
    current_index = 0

    font = pygame.font.Font(None, letter_size)
    head_position = (head_x * config['GRID_SIZE'], head_y * config['GRID_SIZE'])
    text = font.render(head.letter, True, (0,245,0))
    screen.blit(text, head_position)

    show_feeds(screen, font, feeds, config)
    
    
    clock = pygame.time.Clock()
    FPS = 7
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and not pause:
                    snake.set_diraction("u")
                if keys[pygame.K_DOWN] and not pause:
                    snake.set_diraction("d")
                if keys[pygame.K_LEFT] and not pause:
                    snake.set_diraction("l")
                if keys[pygame.K_RIGHT] and not pause:
                    snake.set_diraction("r")
                if event.key == pygame.K_SPACE:
                    pause = not pause
        
        screen.fill(config['BACKGROUND_COLOR'])
        
        if not pause:
            if snake.direction == "r":
                head_x+=step
                if head_x > config['WIDTH']/config['GRID_SIZE']-1:
                    head_x = 0
            elif snake.direction == "l":
                head_x-=step
                if head_x < 0:
                    head_x = config['WIDTH']/config['GRID_SIZE']-1
            elif snake.direction == "u":
                head_y-=step
                if head_y < 0:
                    head_y = config['HEIGHT']/config['GRID_SIZE']-1
            elif snake.direction == "d":
                head_y+=step
                if head_y > config['HEIGHT']/config['GRID_SIZE']-1:
                    head_y = 0
            
            snake.update_position(head_x, head_y)
            for snake_node in snake.body:
                node_position = (snake_node.x * config['GRID_SIZE'], snake_node.y * config['GRID_SIZE'])
                node_letter = font.render(snake_node.letter, True, (0,245,0))
                screen.blit(node_letter, node_position)

            
            show_feeds(screen, font, feeds, config)

            if current_index < len(word):
                current_index, correct = check_letter_collision(
                    snake, feeds, word, current_index
                )
                if not correct:
                    print("Wrong letter collected! Game Over.")
                    pygame.time.wait(1000)
                    pygame.quit()
                    return
                if current_index == len(word):
                    print("Word completed!")
                    pygame.time.wait(1000)
                    pygame.quit()
                    return
                
            pygame.display.flip()
            pygame.display.update()
            
        clock.tick(FPS)

if __name__ == "__main__":
    start_game(config)

