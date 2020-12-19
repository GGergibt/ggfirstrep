from typing import List

import pygame
import random


pygame.init()

display_width = 800
display_height = 600

clock = pygame.time.Clock()

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Беги, Дино, которым управляют")

icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)

cactus_img = [
    pygame.image.load("Cactus0.png"),
    pygame.image.load("Cactus1.png"),
    pygame.image.load("Cactus2.png"),
]
cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load("Stone0.png"), pygame.image.load("Stone1.png")]
cloud_img = [pygame.image.load("Cloud0.png"), pygame.image.load("Cloud1.png")]
dino_img = [
    pygame.image.load("Dino0.png"),
    pygame.image.load("Dino1.png"),
    pygame.image.load("Dino2.png"),
    pygame.image.load("Dino3.png"),
    pygame.image.load("Dino4.png"),
]
dino_img2 = [
    pygame.image.load("Dino2_0.png"),
    pygame.image.load("Dino2_1.png"),
    pygame.image.load("Dino2_2.png"),
    pygame.image.load("Dino2_3.png"),
    pygame.image.load("Dino2_4.png"),
]


bird_img = [
    pygame.image.load("Bird0.png"),
    pygame.image.load("Bird1.png"),
    pygame.image.load("Bird2.png"),
    pygame.image.load("Bird3.png"),
    pygame.image.load("Bird4.png"),
]


jump_sound = pygame.mixer.Sound("Rrr.wav")
fall_sound = pygame.mixer.Sound("Bdish.wav")
loss_sound = pygame.mixer.Sound("loss.wav")
heart_plus_sound = pygame.mixer.Sound("hp+.wav")
button_sound = pygame.mixer.Sound("button.wav")
bullet_sound = pygame.mixer.Sound("shot1.wav")

bullet_img = pygame.image.load("shot.png")
bullet_img = pygame.transform.scale(bullet_img, (30, 9))
all_ms_bullets = []



class Bird:
    global all_ms_bullets
    def __init__(self,  away_y):
        self.x = random.randrange(550, 730)
        self.y  = away_y
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * random.randrange(20, 70)
        self.width = 105
        self.height = 55

        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False
        self.cd_shoot = 0
        self.all_bullets =[]



    def draw(self):

        if self.img_cnt == 60:
            self.img_cnt = 0

        display.blit(bird_img[self.img_cnt // 12], (self.x, self.y))
        self.img_cnt += 1
        if self.come and self.cd_hide == 0:
            return 1

        elif self.go_away:
            return 2



        elif self.cd_hide > 0:
            self.cd_hide -= 1

        return 0

    def hide(self):
        if self.y > self.dest_y:
            self.y -= self.speed
        else:
            self.come = True
            self.go_away = False
            self.x = random.randrange(550, 730)

            self.dest_y = self.speed * random.randrange(20, 70)
            self.cd_hide = 80

    def show(self):
        if self.y < self.dest_y:
            self.y += self.speed
        else:
            self.come = False

            self.dest_y = self.ay

    def check_dmg(self, bullet):

        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= self.y + self.height:
                self.go_away = True
    def shoot(self):
        if not self.cd_shoot:
            pygame.mixer.Sound.play(bullet_sound)
            new_bullet = Bullet(self.x, self.y)
            new_bullet.find_path(usr_x + usr_width // 2, usr_y + usr_height // 2)

            self.all_bullets.append(new_bullet)
            self.cd_shoot = 200

        else:
            self.cd_shoot -= 1

        for bullet in self.all_bullets:
            if not bullet.move_to(self, reverse=True):
                self.all_bullets.remove(bullet)



                


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed_x = 8
        self.speed_y = 0
        self.dest_x = 0
        self.dest_y = 0

    def move(self):
        self.x += self.speed_x
        if self.x <= display_width:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False


    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

        delta_x = dest_x - self.x
        count_up = delta_x // self.speed_x

        if self.y >= dest_y:
            delta_y = self.y - dest_y
            self.speed_y = delta_y / count_up

        else:
            delta_y = dest_y - self.y
            self.speed_y = -(delta_y / count_up)


    def move_to(self, bird, reverse=False):




        if not reverse:
            if bird.y <= self.y <= bird.y + bird.height:

                if bird.x <= self.x <= bird.x + bird.width:
                    bird.hide()

                    return False
            self.x += self.speed_x
            self.y -= self.speed_y
        else:
            self.x -= self.speed_x
            self.y += self.speed_y
        if self.x <= display_width and self.y >= 0 and not reverse:    # and self.y >= self.dest_y:

            display.blit(bullet_img, (self.x, self.y))
            return True
        elif self.x >= 0 and reverse:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False




    def move_false(self):
        return False





class Object:
    def __init__(self, x, y, width, image, speed):
        """

        :type x: object
        """
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.image = image

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 100 + random.randrange(-90, -30)
            return False

    def return_self(self, radius, y, width, image):
        """
        radius
        y = 0
        image
        """
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

class Button:
    def __init__(
        self,
        width,
        height,
    ):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 50)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(
                display, self.active_color, (x, y, self.width, self.height)
            )

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit

                    else:
                        action()

        else:
            pygame.draw.rect(
                display, self.inactive_color, (x, y, self.width, self.height)
            )
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


class Dinosaur:
    def __init__(self):

        self.x = display_width // 3
        self.y = display_height - usr_height - 100
        self.width = 60
        self.height = 100
        make_jump = False
        health = 2
        jump_counter = 30
        img_counter = 0
        emeralds = 2
        cooldown = 0






cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100


scores = 0
health_img = pygame.image.load("heart.png")


# above_cactus = False
max_scores = 0
max_above = 0
x = 20
health_img = pygame.transform.scale(health_img, (30, 30))

emerald_img = pygame.image.load("Emerald.png")
emerald_img = pygame.transform.scale(emerald_img, (30, 30))
start_button = Button(288, 70)
quit_button = Button(120, 70)
start_button2 = Button(288, 70)

def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:

        # pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -30:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 2
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False





def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

# def check_bullet_collision(energy):
#     global barrier, cactus_options, barrier_x, barrier_y, barrier_width, barrier_height
#     for barrier in cactus_options:
#         print(barrier)
#           # little cactus
#         if not make_jump:
#                 #if barrier_x <= energy.x + energy.width - 35 <= barrier_x + barrier_width:
#             object_return(cactus_options, barrier)
#             return True

def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:  # little cactus
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():

                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        if check_health():

                            object_return(barriers, barrier)
                            return False
                        else:
                            return True

        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                    if check_health():
                        object_return(barriers, barrier)

                        return False
                    else:
                        return True
            elif jump_counter >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
                else:
                    if usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
                            if check_health():
                                object_return(barriers, barrier)
                                return False
                            else:
                                return True



def game_over():
    global scores, max_scores, health, cooldown, emeralds
    game_restart = Button(288, 70)
    game_stop = Button(120, 70)
    game_restart1 = Button(288, 70)
    if scores > max_scores:
        max_scores = scores

    stopped = True
    while stopped:
        pygame.mixer.music.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Game over", 340, 120)

        game_restart.draw(270, 200, " hero  1 ", new_start1, 50)
        game_restart1.draw(270, 300, " hero  2 ", new_start, 50)
        game_stop.draw(350, 400, "quit", quit, 50)
        print_text("max scores: " + str(max_scores), 320, 500)
        scores = 0
        health = 120
        cooldown = 0
        emeralds = 120

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(65)


def check_birds_damage(bullets, birds):
        for bird in birds:
            for bullet in bullets:
                bird.check_dmg(bullet)




def draw_birds(birds):
    for bird in birds:
        action = bird.draw()
        if action == 1:
            bird.show()
        elif action == 2:
            bird.hide()
        else:
            bird.shoot()



def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 450)
    return radius

def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)
            # radius = find_radius(array)
            #
            # choice = random.randrange(0, 3)
            # img = cactus_img[choice]
            # width = cactus_options[choice * 2]
            # height = cactus_options[choice * 2 + 1]
            # cactus.return_self(radius, height, width, img)

def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)
    return stone, cloud

def show_menu():
    global start_button, quit_button, start_button2
    menu_backgr = pygame.image.load("Menu.jpg")
    pygame.mixer.music.load("Big_Slinker.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    start_btn2 = Button(288, 70)
    show = True
    while show:



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(menu_backgr, (0, 0))

        start_button.draw(270, 200, "hero one", new_start1, 50)
        start_btn2.draw(270, 300, "hero two", new_start, 50)
        # start_button2.draw(270, 300, "hero two", choose_hero(), 50)
        quit_button.draw(350, 400, "quit", quit, 50)

        pygame.display.update()
        clock.tick(60)

def new_start():
    game_cycle2()

def new_start1():
    game_cycle()

def draw_dino():
    global img_counter

    if img_counter == 25:
        img_counter = 0
    xxx = dino_img[img_counter // 5]
    display.blit(xxx, (usr_x, usr_y))

    img_counter += 1

def draw_dino2():
    global img_counter

    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img2[img_counter // 5], (usr_x, usr_y))
    img_counter += 1

def start_game():
    global scores, make_jump, jump_counter, usr_y, health, land

    while game_cycle():
        scores = 0
        make_jump = False
        jump_counter = 30
        usr_y = display_height - usr_height - 100
        health = 2
        display.blit(land, (0, 0))
        clock.tick(60)

def print_text(message, x, y, font_color=(0, 0, 0), font_type="PingPong.ttf", font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))

def pause():

    paused = True
    while paused:
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("paused. press enter to continue", 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)
        pygame.mixer.music.unpause()

def count_scores(barriers):
    global scores, max_above
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_height - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                    max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0

def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(
            display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone
        )

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(
            display_width, random.randrange(10, 80), cloud.width, img_of_cloud
        )

def show_health():
    global health, energy
    show = 0
    x = 20
    while show != health :
        display.blit(health_img, (x, 20))
        x += 40
        show += 1




def check_damage_user():


def show_health2():
    global emeralds
    show = 0
    x = 20
    while show != emeralds:
        display.blit(emerald_img, (x, 60))
        x += 40
        show += 1

def check_health():
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play(loss_sound)
        game_over()
    else:
        pygame.mixer.Sound.play(fall_sound)
        return True

def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)

def hearts_plus(heart):
    global health, usr_x, usr_y, usr_width, usr_height
    if usr_x <= heart.x <= usr_x + usr_width:

        if usr_y <= heart.y <= usr_y + usr_height and health < 5:

            pygame.mixer.Sound.play(heart_plus_sound)

            if health < 5:
                health += 1

                radius = display_width + random.randrange(500, 1700)
                homework = heart.y + random.randrange(10, 15)
                print(homework)

                heart.return_self(radius, homework, heart.width, heart.image)
                heart.y = 280

def hearts_plus2(energy):
    global health, usr_x, usr_y, usr_width, usr_height, emeralds
    if usr_x <= energy.x <= usr_x + usr_width:

        if usr_y <= energy.y <= usr_y + usr_height and emeralds < 10:
            if emeralds < 10:
                emeralds += 1

                pygame.mixer.Sound.play(heart_plus_sound)
                radius = display_width + random.randrange(500, 1700)
                homework = energy.y + random.randrange(10, 15)


                energy.return_self(radius, homework, energy.width, emerald_img)
                energy.y = 280


def game_cycle():
    """ Запуск игры"""
    global make_jump, stone, cloud, usr_x, usr_y, usr_width, cooldown, emeralds
    pygame.mixer.music.load("background.ogg")
    pygame.mixer.music.set_volume(0.5)

    pygame.mixer.music.play(-1)

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r"Land.jpg")
    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, health_img, 4)
    energy = Object(display_width, 280, 50, emerald_img, 4)
    bird1 = Bird(-80)
    bird2 = Bird(-120)

    all_birds = (bird1,)

    all_btn_bullets = []
    all_ms_bullets = []


    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()

        display.blit(land, (0, 0))  # рисуем экран
        draw_array(cactus_arr)
        move_objects(stone, cloud)
        print_text("Scores: " + str(scores), 600, 10)
        count_scores(cactus_arr)
        if keys[pygame.K_ESCAPE]:
            pause()
        heart.move()
        hearts_plus(heart)
        hearts_plus2(energy)
        energy.move()
        bird2.draw()

        if check_collision(cactus_arr):
            game = False
        show_health()
        show_health2()
        draw_birds(all_birds)
        check_birds_damage(all_ms_bullets, all_birds)

        if emeralds > 0:

            if not cooldown:

                # if keys[pygame.K_x]:
                #     all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y + 28))
                #          # b = pygame.time.get_ticks()
                #     cooldown = 50
                #     pygame.mixer.Sound.play(bullet_sound)
                #     emeralds -= 1

                if click[0]:
                    pygame.mixer.Sound.play(bullet_sound)
                    add_bullet = Bullet(usr_x + usr_width, usr_y + 20)
                    add_bullet.find_path(mouse[0], mouse[1])

                    all_ms_bullets.append(add_bullet)
                    cooldown = 50
                    emeralds -= 1






            else:
                cooldown -= 1
                print_text("max time" + str(cooldown), 482, 40)

        for bullet in all_btn_bullets:
            if not bullet.move(bird1):
                all_btn_bullets.remove(bullet)

        for bullet in all_ms_bullets:
            if not bullet.move_to(bird1):
                all_ms_bullets.remove(bullet)
                # bird1.hide()



        # for bullet in all_ms_bullets:
        #     if not bullet.move_to(bird2):
        #         all_ms_bullets.remove(bullet)
        # bird2.hide()

        # for bullet in all_ms_bullets:
        #     if bird1.x <= bullet.x <= bird1.x + bird1.width:
        #         if bird1.y <= bullet.y <= bird1.y + bird1.height:
        #             #check_birds_damage(bullet, bird1)
        #             bird1.hide()
        #
        #             all_ms_bullets.remove(bullet)
        #
        # for bullet in all_ms_bullets:
        #     if bird2.x <= bullet.x <= bird2.x + bird2.width:
        #         if bird2.y <= bullet.y <= bird2.y + bird2.height:
        #             bird2.hide()
        #
        #             all_ms_bullets.remove(bullet)

        draw_dino()

        pygame.display.update()

        clock.tick(70)

    return game_over()


def game_cycle2():
    """ Запуск игры"""
    global make_jump, stone, cloud, usr_x, usr_y, usr_width, cooldown, emeralds
    pygame.mixer.music.load("background.ogg")
    pygame.mixer.music.set_volume(0.5)

    pygame.mixer.music.play(-1)

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r"Land.jpg")
    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, health_img, 4)
    energy = Object(display_width, 280, 50, emerald_img, 4)
    bird1 = Bird(-80)
    bird2 = Bird(-120)

    all_birds = (bird1,)

    all_btn_bullets = []
    all_ms_bullets = []

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()

        display.blit(land, (0, 0))  # рисуем экран
        draw_array(cactus_arr)
        move_objects(stone, cloud)
        print_text("Scores: " + str(scores), 600, 10)
        count_scores(cactus_arr)
        if keys[pygame.K_ESCAPE]:
            pause()
        heart.move()
        hearts_plus(heart)
        hearts_plus2(energy)
        energy.move()
        bird2.draw()

        if check_collision(cactus_arr):
            game = False
        show_health()
        show_health2()
        draw_birds(all_birds)
        check_birds_damage(all_ms_bullets, all_birds)

        if emeralds > 0:

            if not cooldown:

                # if keys[pygame.K_x]:
                #     all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y + 28))
                #          # b = pygame.time.get_ticks()
                #     cooldown = 50
                #     pygame.mixer.Sound.play(bullet_sound)
                #     emeralds -= 1

                if click[0]:
                    pygame.mixer.Sound.play(bullet_sound)
                    add_bullet = Bullet(usr_x + usr_width, usr_y + 20)
                    add_bullet.find_path(mouse[0], mouse[1])

                    all_ms_bullets.append(add_bullet)
                    cooldown = 50
                    emeralds -= 1






            else:
                cooldown -= 1
                print_text("max time" + str(cooldown), 482, 40)

        for bullet in all_btn_bullets:
            if not bullet.move(bird1):
                all_btn_bullets.remove(bullet)

        for bullet in all_ms_bullets:
            if not bullet.move_to(bird1):
                all_ms_bullets.remove(bullet)
                # bird1.hide()

        # for bullet in all_ms_bullets:
        #     if not bullet.move_to(bird2):
        #         all_ms_bullets.remove(bullet)
        # bird2.hide()

        # for bullet in all_ms_bullets:
        #     if bird1.x <= bullet.x <= bird1.x + bird1.width:
        #         if bird1.y <= bullet.y <= bird1.y + bird1.height:
        #             #check_birds_damage(bullet, bird1)
        #             bird1.hide()
        #
        #             all_ms_bullets.remove(bullet)
        #
        # for bullet in all_ms_bullets:
        #     if bird2.x <= bullet.x <= bird2.x + bird2.width:
        #         if bird2.y <= bullet.y <= bird2.y + bird2.height:
        #             bird2.hide()
        #
        #             all_ms_bullets.remove(bullet)

        draw_dino2()

        pygame.display.update()

        clock.tick(70)

    return game_over()

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(r"Land.jpg")
    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, health_img, 4)
    energy = Object(display_width, 280, 50, emerald_img, 4)
    bird1 = Bird(-80)
    bird2 = Bird(-75)

    all_birds = (bird1, bird2)

    all_btn_bullets = []
    all_ms_bullets = []


    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            make_jump = True
        if make_jump:
            jump()

        display.blit(land, (0, 0)) #рисуем экран
        draw_array(cactus_arr)
        move_objects(stone, cloud)
        print_text("Scores: " + str(scores), 600, 10)
        count_scores(cactus_arr)
        if keys[pygame.K_ESCAPE]:
            pause()
        heart.move()
        hearts_plus(heart)
        hearts_plus2(energy)
        energy.move()
        bird1.draw()



        if check_collision(cactus_arr):
            game = False
        show_health()
        show_health2()
        draw_birds(all_birds)
        #check_birds_damage(all_ms_bullets, all_birds)



        if emeralds > 0:

            if  not cooldown:




                    if keys[pygame.K_x]:
                        all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y + 28))
                             # b = pygame.time.get_ticks()
                        cooldown = 50
                        pygame.mixer.Sound.play(bullet_sound)
                        emeralds -= 1

                    elif click[0]:
                        pygame.mixer.Sound.play(bullet_sound)
                        add_bullet = Bullet(usr_x + usr_width, usr_y + 20)
                        add_bullet.find_path(mouse[0], mouse[1])

                        all_ms_bullets.append(add_bullet)
                        cooldown = 50
                        emeralds -= 1





            else:
                cooldown -= 1
                print_text("max time" + str(cooldown), 482, 40)

        for bullet in all_btn_bullets:
            if not bullet.move():
                all_btn_bullets.remove(bullet)


        for bullet in all_ms_bullets:
            if not bullet.move_to():
                all_ms_bullets.remove(bullet)
        for bird in all_birds:
            for bullet in all_ms_bullets:
                if  bird.check_dmg(bullet):
                    bullet.move_false()





        draw_dino2()

        pygame.display.update()

        clock.tick(70)

    return game_over()




show_menu()
# while game_cycle():

# scores = 0
# make_jump = False
# jump_counter = 30
# usr_y = display_height - usr_height - 100
# health = 2


pygame.quit()
quit()
