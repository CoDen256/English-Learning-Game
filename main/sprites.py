import pygame
import pygame.gfxdraw
import random
from functions import *

class Mouse(pygame.sprite.Sprite):
    """ Класс Mouse использован для более простой обработки событий при наведении курсора на объект. """
    def __init__(self):
        super(Mouse, self).__init__()

        self.img = pygame.Surface((1,1))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

        self.pressed = False

        self.connected_object = None

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Collidable(pygame.sprite.Sprite):
    """ General Sprites """
    def __init__(self, surface, pos, size, color, text, text_size, text_color):
        super(Collidable, self).__init__()
        self.surface = surface
        self.pos = pos
        self.size = self.w, self.h = size
        self.color = color

        self.text = text
        self.text_color = text_color
        self.text_size = text_size

        self.img = pygame.Surface(size)
        self.img.fill(color)
        self.image = self.img
        self.rect = self.image.get_rect()

        self.rect.center = pos


    def update(self):
        pass

    def hover(self, mouse):
        return pygame.sprite.collide_rect(mouse, self)



class Static(Collidable):
    """ Static objects """
    def __init__(self, surface, pos, size, color, word, allowed, text_size, text_color):
        super(Static, self).__init__(surface=surface,
                                     pos=pos,
                                     size=size,
                                     color=color,
                                     text=word,
                                     text_size=text_size,
                                     text_color=text_color)
        self.allowed = allowed

        self.correct = 0
        self.incorrect = 0
        self.wait = 0

        self.positive_color = None
        self.negative_color = None
        self.neutral_color = None
        self.result_color = None

    def receive(self, dynamic):
        if self.allowed in dynamic.words:

            self.correct += 1
            self.wait = 10
            self.result_color = self.positive_color

            self.action(1)

        else:

            self.incorrect += 1
            self.wait = 10
            self.result_color = self.negative_color

            self.action(0)

        dynamic.kill()
        dynamic.__class__.drag = False

    def action(self, point):
        pass


class Dynamic(Collidable):
    """ Dynamic objects """

    drag = False

    def __init__(self, surface, pos, size, color, word, forms, hover_color, velocity, text_size, text_color):
        super(Dynamic, self).__init__(surface=surface,
                                     pos=pos,
                                     size=size,
                                     color=color,
                                     text=word,
                                     text_size=text_size,
                                     text_color=text_color)

        self.word = word
        self.words = forms
        self.hover_color = hover_color

        self.dx, self.dy = self.velocity = velocity
        self.drag = False

    def check_border_overlapping(self, borders, parent_class=None):
        bx, by, bw, bh = borders
        if not self.drag:
            if not(bx <= self.rect.left <= bx + bw - self.w):
                self.dx = - self.dx
            if not(by <= self.rect.top <= by + bh - self.h):
                self.dy = - self.dy

            if by >= self.rect.top+5 or by+bh <= self.rect.bottom-5 \
               or bx >= self.rect.left+5 or bx+bw <= self.rect.right-5:

                if not parent_class:
                    self.rect.center = (bx+bw)//2, (by+bh)//2
                else:
                    is_collide = lambda x,y: self.radius+parent_class.radius >= ((x-parent_class.rect.center[0])**2+(y-parent_class.rect.center[1])**2)**0.5
                    ran_pos = lambda: (random.randint(self.radius, bw-self.radius), random.randint(self.radius, bh-self.radius))
                    xr,yr = ran_pos()
                    while is_collide(xr,yr):
                        xr,yr = ran_pos()
                    self.rect.center = xr, yr


    def check_mouse_pressing(self, mouse):
        if mouse.pressed and not self.__class__.drag and mouse.connected_object == None:
            self.drag = True
            self.__class__.drag = True
            mouse.connected_object = self

        if not mouse.pressed:
            self.drag = False
            self.__class__.drag = False
            mouse.connected_object = None

    def follow_mouse(self, mouse):
        self.rect.center = mouse.rect.center



class Button(Collidable):
    """ Общий класс для использования обработки нажатий мышки и дальнейшего выполнения действий """

    def __init__(self, surface, pos, size, color, text, text_color=(25,25,25), text_size=30, action=None, id=0):
        super(Button, self).__init__(surface=surface,
                                     pos=pos,
                                     size=size,
                                     color=color,
                                     text=text,
                                     text_size=text_size,
                                     text_color=text_color)


        self.action = action
        self.active = False
        self.id = id

    def update(self, mouse):

        self.img.fill(self.color)
        self.draw_border(mouse)

        add_message(self.img, self.text, self.text_size, self.text_color, self.w/2, self.h/2)

        if self.hover(mouse):
            self.check_pressing(mouse)

    def check_pressing(self, mouse):
        if mouse.pressed:
            if self.action:
                self.action()
            self.active = True
            mouse.pressed = False

    def draw_border(self, mouse):
        if self.hover(mouse):
            pygame.draw.rect(self.img, (250, 250, 250), [1.5, 1.5, self.w-1.5, self.h-1.5], 3)
        else:
            pygame.draw.rect(self.img, (50, 50, 50), [0, 0, self.w, self.h], 3)


######################   Game 1 - Irregular Verbs ######################

class TenseGroup(Static):
    """ TenseGroup which can allow or not allow Verb"""
    total_incorrect = 0
    def __init__(self, surface, pos, size, text, allowed, color=(175,175,175), text_color=(25,25,25), text_size=25):
        super(TenseGroup, self).__init__(surface=surface,
                                     pos=pos,
                                     size=size,
                                     color=color,
                                     word=text,
                                     allowed=allowed,
                                     text_size=text_size,
                                     text_color=text_color)

        self.result_color = self.color

        self.positive_color = (125,225,100)
        self.negative_color = (225,125,100)

        self.neutral_color = self.color
        self.positive_result = (180,220,175)
        self.negative_result = (220,180,175)



    def update(self, mouse):
        if self.wait > 0:
            self.wait -= 1

        if not self.wait:
            self.result_color = self.current_color()

        self.img.fill(self.result_color)

        if self.hover(mouse):

            if Verb.drag:
                self.receive(mouse.connected_object)

            pygame.draw.rect(self.img, (250, 250, 250), [1.5, -5, self.w-1.5, self.h-1.5+5], 5)

        else:
            pygame.draw.rect(self.img, (25, 25, 25), [0, 0, self.w, self.h], 5)

        add_message(self.img, self.text, self.text_size, self.text_color, self.w//2, self.h//2,)
        add_message(self.img, "Correct: "+str(self.correct), 12, self.text_color, self.w//4, 4*self.h//5)
        add_message(self.img, "Incorrect: "+str(self.incorrect), 12, self.text_color, 3*self.w//4, 4*self.h//5)

    def current_color(self):
        if self.incorrect == self.correct:
            return self.neutral_color
        if self.incorrect > self.correct:
            return self.negative_result
        if self.correct > self.incorrect:
            return self.positive_result

    def action(self, point):
        TenseGroup.total_incorrect += not point

class Verb(Dynamic):
    """ Word that has priority of 1,2 or 3(for forms of verbs)"""

    def __init__(self, surface, pos, size, text, forms, velocity, text_size, color=(225,125,100), hover_color=(250,250,250), text_color=(25,25,25)):
        super(Verb, self).__init__(surface=surface,
                                        pos=pos,
                                        size=size,
                                        color=color,
                                        word=text,
                                        forms=forms,
                                        hover_color=hover_color,
                                        velocity=velocity,
                                        text_size=text_size,
                                        text_color=text_color)

    def update(self, mouse, border):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.hover(mouse):
            self.img.fill(self.hover_color)
            self.check_mouse_pressing(mouse)
        else:
            self.img.fill(self.color)

        if self.drag:
            self.follow_mouse(mouse)

        self.check_border_overlapping(border)


        pygame.draw.rect(self.img, (25, 25, 25), [0, 0, self.w, self.h], 3)
        add_message(self.img, self.text, self.text_size, self.text_color, self.w//2, self.h//2)



######################   Game 2 - Translation    ######################
class MainWord(Static):
    """ Main word that has to be translated """

    def __init__(self, surface, pos, radius, word, translation, color=(97, 143, 182), border_color=(250,250,250), border_width=4,
                                                                                      text_color=(250,250,250), text_size=40):
        super(MainWord, self).__init__(surface=surface,
                                       pos=pos,
                                       size=(radius*2,radius*2),
                                       color=color,
                                       word=word,
                                       allowed=translation,
                                       text_size=text_size,
                                       text_color=text_color)




        self.border_width = border_width
        self.border_color = border_color

        self.radius = radius

        self.result_color = None
        self.neutral_color = self.color
        self.positive_color = (56, 171, 146)
        self.negative_color = (243, 70, 84)

        self.time_left = 0
        self.delay = 0

    def update(self, mouse):
        if self.wait > 0:
            self.wait -= 1
            self.color = self.result_color

        if self.wait == 0:
            self.color = self.neutral_color
            self.result_color = None

        self.draw_circle()


        add_message(self.img, self.text, self.font_size(self.text), self.text_color, self.radius, self.radius)

        add_message(self.img, "Correct: "+str(self.correct), 15, (240,240,240), int(self.radius*2/4), int(self.radius*2/3)*2)
        add_message(self.img, "Incorrect: "+str(self.incorrect), 15, (240,240,240), int(self.radius*2/4)*3, int(self.radius*2/3)*2)

        add_message(self.img, str(self.time_left), 40, (25,25,25), self.radius, int(self.radius*2/4))
        #add_message(self.img, str(self.allowed), 40, (25,25,25), self.radius, int(self.radius*2/4))

        if self.hover(mouse):
            if Translation.drag:
                self.receive(mouse.connected_object)

    def draw_circle(self):
        self.img.fill((255,255,255))
        self.img.set_colorkey((255,255,255))

        pygame.gfxdraw.aacircle(self.img, self.radius+1, self.radius+1, self.radius-2, self.border_color)

        if self.border_width:
            pygame.gfxdraw.filled_circle(self.img, self.radius+1, self.radius+1, (self.radius-2)-int(.3*self.border_width), self.color)

    def action(self, point):
        self.delay = self.delay + 2 if point else self.delay - 2

    def font_size(self, word):
        if len(word) >= 10:
            return self.text_size-(len(word))
        else:
            return self.text_size

class Translation(Dynamic):
    """ Words that are translation of MainWord"""
    def __init__(self, surface, pos, radius, word, velocity, color=(32, 144, 189), hover_color=(243, 70, 84), border_color=(250,250,250), border_width=4,
                                                                                                              text_color=(250,250,250), text_size=25):
        super(Translation, self).__init__(surface=surface,
                                              pos=pos,
                                              size=(radius*2,radius*2),
                                              color=color,
                                              word=word,
                                              forms=[word],
                                              hover_color=hover_color,
                                              velocity=velocity,
                                              text_size=text_size,
                                              text_color=text_color)
        self.radius = radius

        self.neutral_color = color

        self.border_color = border_color
        self.border_width = border_width


    def update(self, surface, mouse, main_circle):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.hover(mouse):
            self.color = self.hover_color
            self.check_mouse_pressing(mouse)
        else:
            self.color = self.neutral_color

        if self.drag:
            self.follow_mouse(mouse)

        self.draw_circle()

        self.check_border_overlapping((0, 0, surface.get_width(), surface.get_height()), main_circle)
        self.check_circle_overlapping(main_circle)

        add_message(self.img, self.text, self.font_size(self.text), self.text_color, self.radius, self.radius)

    def draw_circle(self):
        self.img.fill((255,255,255))
        self.img.set_colorkey((255,255,255))

        pygame.gfxdraw.aacircle(self.img, self.radius+1, self.radius+1, self.radius-2, self.border_color)

        if self.border_width:
            pygame.gfxdraw.filled_circle(self.img, self.radius+1, self.radius+1, (self.radius-2)-int(.3*self.border_width), self.color)

    def font_size(self, word):
        if len(word) >= 8:
            return 18-len(word)+10
        else:
            return self.text_size

    def check_circle_overlapping(self, circle):
        if pygame.sprite.collide_circle(self, circle):
            self.dx = - self.dx
            self.dy = - self.dy