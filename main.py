import pygame, random, copy

pygame.init()
wordList = ["Patriotism", "Independence", "Peace", "Mahatma", "Gandhi",
            "Tricolor", "Freedom", "Unity", "Diversity", "Jai Hind", "Saffron",
            "White", "Green", "Ashoka", "Chakra", "Satyameva", "Jayate",
            "Nationalism", "Non-violence", "Respect", "Constitution", "Sacrifice",
            "INA", "Martyr", "Revolution", "Liberation", "Swaraj",
            "Courage", "Tolerance", "Tiranga", "Motherland", "Inspirational",
            "Equality", "Bharat Mata", "Himalayas", "boycott", "swadeshi", "swaraj",
            "constitution", "Bose", "Congress", "INC", "INU", "Drafting", "Commitee", "harijan"]
"""
import nltk 
nltk.download('words')
from nltk.corpus import words
wordList = words.words()
"""
len_indexes = []
length =1


#sorting for length as per levels 
wordList.sort(key=len)
for i in range(len(wordList)):
    if len(wordList[i]) > length:
        length +=1
        len_indexes.append(i)
len_indexes.append(len(wordList))


#game initialization things
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Typing Racer!')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60
#game variables
level = 1
active_string = 'test string'
score =0
high_score=1
submit = ''
lives=5
paused = False
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
           'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]
word_objects =[]
new_level = True
#2 letter to 8 letter choices as boolean options
choices = [True, True, True, True, True, True, True, True, True, True,]



#sfx and music and font
header_font =  pygame.font.Font('fonts/Square.ttf', 45)
pause_font = pygame.font.Font('fonts/1up.ttf', 38)
banner_font = pygame.font.Font('fonts/1up.ttf', 28)
font = pygame.font.Font('fonts/AldotheApache.ttf', 48)


class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text

    def draw(self):
        color = 'black'
        screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= self.speed

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.clicked = clicked
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45,89,135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190,35,35), (self.x_pos, self.y_pos), 35)
                self.clicled = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        cir = pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos -25))



def draw_screen():
    #screen oytlines wagerah
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0,0,WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (250, HEIGHT-100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT-100), (700, HEIGHT-100), 2)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT-100), 2)

    #text for showing current level, player current input, highscore, score, lives, pause

    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (10, HEIGHT-75))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (270, HEIGHT - 75))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    screen.blit(banner_font.render(f'Score:  {score}', True, 'black'), (250, 10))
    screen.blit(banner_font.render(f'Best:  {high_score}', True, 'black'), (550, 10))
    screen.blit(banner_font.render(f'Lives:  {lives}', True, 'black'), (10, 10))
    return pause_btn.clicked


def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0,0,0,100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    # define buttons for pause menu
    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()

    screen.blit(surface, (0,0))


def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text)/3)
            scor += int(points)
            word_objects.remove(wrd)
            #play successful entry sfx here
    return scor

def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i+1]))
    for i in range(level):
        speed = random.randint(2,3)
        y_pos = random.randint(10 + (i*vertical_spacing), (i+1)*vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordList[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word)


    return word_objs


run = True
while run:
    screen.fill('gray')
    timer.tick(fps)
    #draw bg status pause status
    pause_butt = draw_screen()
    if paused:
        draw_pause()
    if new_level and not paused:
        word_objects = generate_level()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos <-200:
                word_objects.remove(w)
                lives -=1
    if len(word_objects) <= 0 and not paused:
        level += 1
        new_level = True

    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            #play wrong entry sound
            pass



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''

    if pause_butt:
        paused = True



    pygame.display.flip()
pygame.quit()
