import pygame
import pygame.gfxdraw
import random
from datetime import datetime as dt
from datetime import timedelta as td
from functions import *
from sprites import *
from localization import l

SIZE = 720, 640
icon = pygame.image.load('icon.png')

window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('English Learning Game')
pygame.display.set_icon(icon)


W, H = MAIN_SIZE = window.get_size()

language = 'RU'
lan = None




def menu(current_player):
    global language, lan

    lan = 1 if language == 'RU' else 0
    surface = pygame.image.load("pict2.jpg")

    button_1 = Button(surface, (W/2, 3*H/7), (255, 60), (118, 200, 200), l["Играть"][lan])
    button_2 = Button(surface, (W/2, 5*H/7), (255, 60), (118, 200, 200), l["Выход"][lan], action=quit_game)
    button_3 = Button(surface, (3*W/4, 3*H/7), (60, 60), (118, 200, 200), language)
    button_4 = Button(surface, (W/2, H/5), (290,60), (118, 200, 200), 'Сменить пользователя')
    mouse = Mouse()

    surface_sprites = pygame.sprite.Group()
    buttons = [button_1, button_2, button_3, button_4]
    surface_sprites.add(buttons)

    mainloop = True
    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    quit_game()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0, 0))

        add_message(surface, ' - '.join(current_player), 50, (0,0,0), W/2, H/10)

        surface_sprites.draw(surface)

        mouse.update()
        for button in buttons:
            button.update(mouse)


        if button_1.active:
            mainloop = False
            choice(current_player)

        if button_3.active:
            if language == 'RU':
                language = 'UA'
            else:
                language = 'RU'

            mainloop = False
            menu(current_player)
            button_3.active = False

        if button_4.active:
            mainloop = False
            choose_user()

        lan = 1 if language == 'RU' else 0

        pygame.display.flip()

def choice(current_player):

    surface = pygame.Surface(MAIN_SIZE)

    button_0 = Button(surface, (W/2, H-H/5), (255, 60), (118, 150, 150), l["Назад в меню"][lan], text_size=25)
    button_1 = Button(surface, (W/2, H/5), (255, 60), (118, 200, 200), l["Неправильные глаголы"][lan], text_size=25)
    button_2 = Button(surface, (W/2, 2*H/5), (255, 60), (118, 200, 200), l["Перевод слов"][lan], text_size=25)

    mouse = Mouse()

    buttons = [button_0, button_1, button_2]
    surface_sprites = pygame.sprite.Group()
    surface_sprites.add(buttons)

    mainloop = True
    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    quit_game()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0, 0))
        surface.fill((100, 150, 175))

        surface_sprites.draw(surface)

        add_message(surface, l["Темы"][lan]+':', 50, (50,50,50), W/2, H/10)

        mouse.update()
        for button in buttons:
            button.update(mouse)

        if button_0.active:
            mainloop = False
            menu(current_player)

        if button_1.active:
            mainloop = False
            game1(current_player)

        if button_2.active:
            mainloop = False
            game2(current_player)

        pygame.display.flip()

def game1(current_player):
    TenseGroup.total_incorrect = 0


    verbs = load_data("irregular_verbs.txt", '\t')
    fps = 100

    surface = pygame.Surface(MAIN_SIZE)
    border = border_x, border_y, border_w, border_h = 10, H//8+10, W-20, 7*H//8-20

    all_sprites = pygame.sprite.Group()
    tense_groups = []
    verb_objects = []

    columns = ["Infinitive", "Past Simple", "Past Participle"]
    for i in range(3):
        group = TenseGroup(surface, ((i)*W/3+(W/6), 40), (160, 60), columns[i], i)
        tense_groups.append(group)

    for i in range(15):
        verb = gen_Verb(border, verbs, surface)
        verb_objects.append(verb)

    mouse = Mouse()
    mouse.pressed = False

    all_sprites.add(tense_groups, verb_objects)

    mainloop = True
    clock = pygame.time.Clock()
    while mainloop:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if pause(surface):
                        mainloop = False
                        menu()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0,0))
        surface.fill((150,200,150))

        all_sprites.draw(surface)

        mouse.update()
        for group in tense_groups:
            group.update(mouse)
        for verb in verb_objects:
            verb.update(mouse, border)

            if not verb.alive():
                verb_objects.remove(verb)

                new_verb = gen_Verb(border, verbs, surface)
                verb_objects.append(new_verb)
                all_sprites.add(new_verb)

        pygame.draw.rect(surface, (50, 50, 50), [border_x, border_y, border_w, border_h], 5)

        if TenseGroup.total_incorrect >= 10:
            result = fail_message(surface, l["Вы ошиблись "][lan]+str(10)+l[" раз"][lan])
            if result == 0:
                mainloop = False
                game1(current_player)
            if result == 1:
                mainloop = False
                menu(current_player)


        pygame.display.flip()
        clock.tick(fps)



def game2(current_player):
    surface = pygame.Surface(MAIN_SIZE)

    words = load_data("definition.txt", "-")

    mouse = Mouse()

    all_sprites = pygame.sprite.Group()
    t_words = []

    main_word = MainWord(surface, (W//2, H//2), 100, None, None)
    t_words = gen_Translation(main_word, words, 10, t_words)

    all_sprites.add(main_word, t_words)

    end_dt = dt.now() + td(minutes=1)
    mouse.pressed = False
    mainloop = True
    clock = pygame.time.Clock()
    while mainloop:

        cur_dt = dt.now()
        left = dt_format(end_dt-cur_dt)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if pause(surface):
                        mainloop = False
                        menu(current_player)
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False


        window.blit(surface, (0,0))
        surface.fill((100,150,200))

        all_sprites.draw(surface)

        main_word.time_left = int(left) + main_word.delay

        mouse.update()
        main_word.update(mouse)

        for t_word in t_words:
            t_word.update(surface, mouse, main_word)

            if not t_word.alive():
                t_words.remove(t_word)

                new_words = gen_Translation(main_word, words, 0, t_words)

                t_words += new_words
                all_sprites.add(new_words)

        if main_word.time_left <= 0:
            result = fail_message(surface, l["Время вышло"][lan])
            if result == 0:
                mainloop = False
                game2(current_player)
            if result == 1:
                mainloop = False
                menu(current_player)

        clock.tick(60)
        pygame.display.flip()

def choose_user():
    surface = pygame.Surface(MAIN_SIZE)
    scores = init_score("score.txt")

    mouse = Mouse()

    sprites = pygame.sprite.Group()
    buttons = []
    for i in range(len(scores)):
        name, score = scores[i]
        if not name and not score:
            name, score = "Create new user +", '-1'

        new_button = Button(surface,(W/2, (90*(i)+120)), (400,60), (118,200,200), name + (" - "+ score)*(score!='-1'), id=i)
        buttons.append(new_button)

    sprites.add(buttons)

    mouse.pressed = False
    mainloop = True

    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0,0))
        surface.fill((100,150,200))

        sprites.draw(surface)

        add_message(surface, "Выберите пользователя", 50, (50,50,50), W/2, H/10)

        mouse.update()
        for button in buttons:
            button.update(mouse)
            if button.active and button.text == "Create new user +":
                scores = create_new_user(button.id)
                mainloop = False

                menu(scores[button.id])
            elif button.active:
                mainloop = False

                menu((tuple(button.text.split(' - '))))


        pygame.display.flip()


def pause(surface):

    mouse = Mouse()

    button_0 = Button(surface, (W/2, H/4), (255, 60), (118, 200, 200), l["Вернуться в игру"][lan])
    button_1 = Button(surface, (W/2, H/2), (255, 60), (118, 200, 200), l["Вернуться в меню"][lan])
    button_2 = Button(surface, (W/2, H-H/6), (255, 60), (118, 150, 150), l["Завершить игру"][lan], action=quit_game)


    sprites = pygame.sprite.Group()
    buttons = [button_0, button_1, button_2]
    sprites.add(buttons)

    mouse.pressed = False
    mainloop = True
    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0,0))

        sprites.draw(surface)

        mouse.update()
        for button in buttons:
            button.update(mouse)

        if button_0.active:
            mainloop = False

        if button_1.active:
            mainloop = False
            return 1

        pygame.display.flip()

def fail_message(surface, message):

    mouse = Mouse()

    button_0 = Button(surface, (W/2, 2*H/5), (255, 60), (118, 200, 200), l["Попробовать еще раз"][lan], text_size=25)
    button_1 = Button(surface, (W/2, 3*H/5), (255, 60), (118, 200, 200), l["Вернуться в меню"][lan], text_size=25)
    button_2 = Button(surface, (W/2, 4*H/5), (255, 60), (118, 150, 150), l["Завершить игру"][lan], text_size=25, action=quit_game)


    sprites = pygame.sprite.Group()
    buttons = [button_0, button_1, button_2]
    sprites.add(buttons)

    mouse.pressed = False
    mainloop = True
    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True
            if e.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False

        window.blit(surface, (0,0))

        add_message(surface, l["Игра окончена"][lan]+". "+message, 45, (250,250,250), W/2, H/5)

        sprites.draw(surface)

        mouse.update()
        for button in buttons:
            button.update(mouse)

        if button_0.active:
            mainloop = False
            return 0

        if button_1.active:
            mainloop = False
            return 1

        pygame.display.flip()

def gen_Verb(border, verbs, surface):
    border_x, border_y, border_w, border_h = border
    verb_width, verb_height = 100, 40

    verb_x = random.randint(border_x+(verb_width/2), border_x+border_w-(verb_width/2))
    verb_y = random.randint(border_y+(verb_height/2), border_y+border_h-(verb_height/2))
    verb_pos = verb_x, verb_y

    velocity = random.randint(1, 3)*random.choice([1,-1]), random.randint(1, 3)*random.choice([1,-1])

    words = random.choice(verbs)

    form = random.randint(0,2)
    forms = [form,]

    for i in range(len(words)):
        if i != form and words[i] == words[form]:
            forms.append(i)

    word = words[form]

    if len(word) >= 8:
        text_size = 18-(len(word)-10)
    else:
        text_size = 25

    return Verb(surface, verb_pos, (verb_width, verb_height), word, forms, velocity, text_size)

def gen_Translation(main_circle, vocabulary, n, current_objects):
    objects = []
    radius = 50


    ran_vel = lambda: (random.randint(1, 2)*random.choice([1,-1]), random.randint(1, 2)*random.choice([1,-1]))
    ran_pos = lambda: (random.randint(radius, W-radius), random.randint(radius, H-radius))
    ran_data = lambda: tuple(random.choice(vocabulary))
    is_collide = lambda x,y: radius+main_circle.radius >= ((x-main_circle.rect.center[0])**2+(y-main_circle.rect.center[1])**2)**0.5


    ### Data for random key-object
    k_translation, *word_uaru  = ran_data()
    while len(k_translation) >= 12:
        k_translation, *word_uaru  = ran_data()
    k_word = word_uaru[not lan]

    main_circle.allowed, main_circle.text = k_translation, k_word # Changing current value of MainWord


    ###### Creating list of randomly generated words ######
    for i in range(n+1):
        x,y = W/2, H/2
        velocity = ran_vel()

        while is_collide(x,y):
            x,y = ran_pos()

        objects.append(Translation(main_circle.surface, (x, y), radius, None, velocity))

    ###### Changing value of word for each and initializating key object
    key_object = random.choice(current_objects+objects)
    for t_object in (current_objects+objects):
        x,y = W/2, H/2

        translation = ran_data()[0]
        while len(translation) >= 12:
            translation = ran_data()[0]

        t_object.text = translation if t_object != key_object else k_translation
        t_object.words = [t_object.text]

    #### List of ol Translation uncluding (n) objects + object-key to main circle ####
    return objects
def create_new_user(id):
    scores = init_score('scores.txt')
    scores[id] = input_name(), '0'
    return scores

def input_name(surface):

choose_user()
#menu()
#choice()
#game1()
#game2()
#game3()


# todo: добавить словарь из слов необходимых именно для зно
# todo: измененную базу данных
# todo: систему очков, при входе в игру запрашивается какой пользователь играет сейчас, добавляется возможность создать пользователя нового,
# добавить кнопку смены пользователя в меню? лимит пользователей за одним компьютером - 6, функцию записи очков по окончанию игры
# todo: dt_format()
# todo: распределение очков между играми отностильено игор

# + добавлена функция init_score()
# + присваивается перменной scores значение списка очков каждого пользователя
# +
# +
# +
# +
# +
# +
# +
# +
# +
# +
# +
# +
# +

