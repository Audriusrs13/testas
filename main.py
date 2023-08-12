import pygame
import sys
import random
import pygame_menu
import pygame_menu.font
from config import *
from snake_block import SnakeBlock


pygame.init()
bg_image = pygame.image.load("background.jpg")

labels = None
table = None
total = 0
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake_v.0.1")
timer = pygame.time.Clock()
digital_font = pygame_menu.font.get_font(pygame_menu.font.FONT_DIGITAL, 28)


def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


def on_play_button_click():
    start_the_game()


def read_scores_from_file(file_name):
    scores = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                scores.append(line.strip())
    except FileNotFoundError:
        pass
    return scores


def remove_scores_table():
    global table

    menu.remove_widget(table)


def game_over_label():
    global labels
    # global SOUND

    if labels is not None:
        for label in labels:
            menu.remove_widget(label)

    labels = menu.add.label(f'GAME OVER \n your score : {total}',
                            font_background_color=(255, 5, 5), font_size=30, font_color=(5, 5, 5))


def update_scores_table():
    global table

    table = menu.add.table(table_id='my_table', font_size=12)
    table.default_cell_padding = 1
    table.default_row_background_color = L_YELLOW
    scores = read_scores_from_file('scores.txt')
    table.add_row(['HIGH SCORES'], cell_font=pygame_menu.font.FONT_8BIT, cell_font_color=(5, 5, 5))
    for score in scores:
        table.add_row([score], cell_font=pygame_menu.font.FONT_NEVIS, cell_font_color=(39, 78, 19))


def save_score():
    player_name = input_field.get_value()
    new_score = f'{player_name}: {total}'

    if not is_duplicate_score(new_score):
        scores = read_scores_from_file('scores.txt')

        if len(scores) < MAX_SCORES:
            scores.append(new_score)
        else:
            if total > int(scores[-1].split(': ')[-1]):
                scores.pop()
                scores.append(new_score)

        sorted_scores = sorted(scores, key=lambda score2: int(score2.split(': ')[-1]), reverse=True)

        with open('scores.txt', 'w') as f:
            for score in sorted_scores:
                f.write(f'{score}\n')


def is_duplicate_score(new_score):
    with open('scores.txt', 'r') as f:
        for line in f:
            if line.strip() == new_score.strip():
                return True
    return False


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK, SIZE_BLOCK])


def start_the_game():
    global total

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = 0
    d_col = 1
    speed = 1
    total = 0

    while True:

        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                print("exit")
                pygame.quit()
                sys.exit()
            elif game_event.type == pygame.KEYDOWN:
                if game_event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif game_event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif game_event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif game_event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(GREEN)
        pygame.draw.rect(screen, L_GREEN, [0, 0, size[0], HEADER_MARGIN])

        text_total = digital_font.render(f'SCORE: {total}', 0, (39, 78, 19))
        text_speed = digital_font.render(f'SPEED: {speed}', 0, (39, 78, 19))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = L_GREEN
                else:
                    color = L_YELLOW

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print("game_over, hit_to_the_wall")
            print(total, 'score')
            play_sound("Sounds/hit.wav")
            game_over_label()
            save_score()
            remove_scores_table()
            update_scores_table()

            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(BROWN, block.x, block.y)

        pygame.display.flip()

        if apple == head:
            total += 1
            speed = total//5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()
            play_sound("Sounds/tap.wav")

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print("game_over, yourself")
            print(total, 'score')
            play_sound("Sounds/hit.wav")
            game_over_label()
            save_score()
            remove_scores_table()
            update_scores_table()

            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(3+speed)
        play_sound("Sounds/step.wav")


main_theme = pygame_menu.themes.THEME_GREEN.copy()
main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
main_theme.set_background_color_opacity(0)
menu = pygame_menu.Menu('', 220, 360, theme=main_theme)
main_theme.widget_font = pygame_menu.font.FONT_FRANCHISE
main_theme.widget_font_size = 30
main_theme.widget_font_color = (5, 5, 5)
main_theme.widget_font_background_color = (39, 78, 19)
main_theme.border_color = (0, 255, 5)
main_theme.widget_border_width = 0
input_field = menu.add.text_input('', maxwidth=20, maxchar=12, default="Your Name")
menu.add.button('Play', on_play_button_click, align=pygame_menu.locals.ALIGN_CENTER)
menu.add.button('Quit', pygame_menu.events.EXIT, align=pygame_menu.locals.ALIGN_CENTER)
update_scores_table()


while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
