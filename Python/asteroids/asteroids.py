"""
File: asteroids.py
Original Author: Br. Burton
Completed by Vivian Ashton

This program implements the asteroids game.
"""
import arcade
import math
import random
from abc import ABC
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900

BULLET_RADIUS = 30/3
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 25 

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15*1.25

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5*2

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2*2


class Point:

    ### Initialize a Point object with default values
    def __init__(self):
        self.x = 0
        self.y = 0


class Velocity:

    ### Initialize a Velocity object with default values
    def __init__(self):
        self._dx = 0
        self._dy = 0

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        if dx > 30:
            self._dx = 30
        elif dx < -30:
            self._dx = -30
        else:
            self._dx = dx

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, dy):
        if dy > 30:
            self._dy = 30
        elif dy < -30:
            self._dy = -30
        else:
            self._dy = dy

# this if to put a cap on the ship's speed 
class Speed:

    ### Initialize a Velocity object with default values
    def __init__(self):
        self._dx = 0
        self._dy = 0

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, dx):
        if dx > 10:
            self._dx = 10
        elif dx < -10:
            self._dx = -10
        else:
            self._dx = dx

    @property
    def dy(self):
        return self._dy

    @dy.setter
    def dy(self, dy):
        if dy > 10:
            self._dy = 10
        elif dy < -10:
            self._dy = -10
        else:
            self._dy = dy
    
## make a Flying object class, -- getter and setter for the speed
class Flying_Object:

    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 30
        self.alive = True
        self.hits = 1
        
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    @abstractmethod
    def draw(self):
        pass

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):

        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.x < 0:
            self.center.x = SCREEN_WIDTH
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
        elif self.center.y < 0:
            self.center.y = SCREEN_HEIGHT

    def was_hit(self):
        self.hits -= 1
        self.alive = False

## make a bullets class -- 
class Bullet(Flying_Object):

    def __init__(self, angle, center_x, center_y, velocity_dx, velocity_dy):
        super().__init__()
        self.angle = angle + 90
        self.center.x = center_x
        self.center.y = center_y
        self.velocity.dx = velocity_dx
        self.velocity.dy = velocity_dy
        self.radius = BULLET_RADIUS
        self.alive = True
        self.frame_count = 0

    def fire(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def draw(self):
        texture = arcade.load_texture("laser.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle=self.angle)

    def advance(self):
        self.frame_count += 1
        super().advance()

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def was_hit(self):
        super().was_hit()

## make a ship class -- Getter setter for angle? -- 
class Ship(Flying_Object):

    def __init__(self, texture, place):
        super().__init__()
        self.angle = 0.1
        self.center.x = SCREEN_WIDTH*place 
        self.center.y = 100
        self.radius = SHIP_RADIUS
        self.speed = Speed()
        self.speed._dx = 0.02
        self.speed._dy = 0.02
        self.texture = texture
 
    def advance(self):
        self.center.x += self.speed.dx
        self.center.y += self.speed.dy
          
    def draw(self):
        if self.alive:
            texture = arcade.load_texture(self.texture)
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle=self.angle)

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
 
    def was_hit(self):
        super().was_hit()

## make an Asteroids -- make 3 sub classes for them --  
class Asteroids(Flying_Object):

    def __init__(self):
        super().__init__()
        self.angle = random.uniform(0, 360)

    @abstractmethod
    def draw(self):
        pass


class Small_Asteroid(Asteroids):
    
    def __init__(self, center_x, center_y, velocity_dx, velocity_dy):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.center.x = center_x
        self.center.y = center_y
        self.velocity.dx = velocity_dx
        self.velocity.dy = velocity_dy

    def draw(self):
        texture = arcade.load_texture("small.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle= self.angle)

    def advance(self):
        """
        Rotates at 5 degrees per frame
        """
        super().advance()
        self.angle += SMALL_ROCK_SPIN

    def was_hit(self):
        """
        When hit destroyed and removed from the game.
        Collision radius of 2
        """
        super().was_hit()

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)


class Medium_Asteroid(Asteroids):

    def __init__(self, center_x, center_y, velocity_dx, velocity_dy):
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.center.x = center_x
        self.center.y = center_y
        self.velocity.dx = velocity_dx
        self.velocity.dy = velocity_dy
        self.hits = 2
    
    def draw(self):
        texture = arcade.load_texture("medium.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle = self.angle)

    def advance(self):
        super().advance()
        self.angle += MEDIUM_ROCK_SPIN

    def was_hit(self):
        super().was_hit()

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)


class Large_Asteroids(Asteroids):

    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(10, SCREEN_WIDTH - 50)
        self.center.y = random.uniform(200, SCREEN_HEIGHT - 50)
        self.velocity.dx = math.cos(math.radians(self.angle)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.angle)) * BIG_ROCK_SPEED 
        self.radius = BIG_ROCK_RADIUS
        self.hits = 3

    def draw(self):
        texture = arcade.load_texture("big.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle = self.angle)

    def advance(self):
        """
        Moves at 1.5 pixels per frame at random initial direction,
        Rotates at 1 degree per frame-- maybe make this in a different functions
        """
        super().advance()
        self.angle += BIG_ROCK_SPIN
        
    def was_hit(self):
        """
        Breaks apart and becomes two medium asteroids and one small one
        First medium asteroid hass the same velocity as the original large one plus 2 pixel/frame in the down direction
        second medium asteroid has the same velocity as the original large one plus e pixel/frame in the down direction
        Small asteroid has the original velocity plus 5 pixel/fram to the right. 
        """
        super().was_hit()

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

## This is for the start menu
class Selector:
    
    def __init__(self , width, height):
        self.center = Point()
        self.center.x = width
        self.center.y = height
        self.change = 0
        self.texture = "ship.png"
        self.radius = 15
        self.angle = 0

    def draw(self):
        texture = arcade.load_texture(self.texture)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture, angle=self.angle)

    def move(self):
        self.center.x += self.change


class Start_Window(arcade.View):
    """
    Welcome  window asking if the game should be two player or one player 
    """
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.choose = "none"
        self.ship = Selector((SCREEN_WIDTH*1/5 - 25),(SCREEN_HEIGHT*1/3 + 10))
        self.held_keys = set()
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to My Asteroids Game!!", SCREEN_WIDTH*1/5, SCREEN_HEIGHT*2/3, arcade.color.WHITE)
        arcade.draw_text("Would you like to play as one player or two players?", SCREEN_WIDTH*1/4 + 10, SCREEN_HEIGHT*2/3 - 25, arcade.color.WHITE)
        arcade.draw_text("One Player", SCREEN_WIDTH*1/5, SCREEN_HEIGHT*1/3, arcade.color.WHITE)
        arcade.draw_text("Two Players", SCREEN_WIDTH*3/5, SCREEN_HEIGHT*1/3, arcade.color.WHITE)
        self.ship.draw()

    def update(self, delta_time):
        self.check_keys()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.center.x = SCREEN_WIDTH*1/5 - 25
            
        if arcade.key.RIGHT in self.held_keys:
            self.ship.center.x  = SCREEN_WIDTH*3/5 - 25

        if arcade.key.ENTER in self.held_keys:
        
            if self.ship.center.x  == SCREEN_WIDTH*3/5 - 25:
                
                intructions = Instructions_2_Player()
                self.window.show_view(intructions)

            elif self.ship.center.x == SCREEN_WIDTH*1/5 - 25:
    
                intructions = Instructions_1_Player()
                self.window.show_view(intructions)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        self.held_keys.add(key)
    
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


class Instructions_1_Player(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.held_keys = set()

    def draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, font_size=12, anchor_x="center")
        arcade.draw_text("Use the arrow keys to move your ship and the SPACE bar to shoot your lazer.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20, arcade.color.WHITE, font_size=12, anchor_x="center")
        arcade.draw_text("Hit Enter to Start", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 -40, arcade.color.WHITE, font_size=12, anchor_x="center")

    def update(self, delta_time):
        self.draw()
        self.check_keys()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.ENTER in self.held_keys:
            game = Game()
            self.window.show_view(game)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        self.held_keys.add(key)
    
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
    

class Instructions_2_Player(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.held_keys = set()

    def draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, font_size=12, anchor_x="center")
        arcade.draw_text("Player 1 will use the arrow keys to move their ship and the SPACE bar to shoot lazers", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-20, arcade.color.WHITE, font_size=12, anchor_x="center")
        arcade.draw_text("Player 2 Will use the A, W, D, and S, ship to move their an the C to shoot lazers", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-40, arcade.color.WHITE, font_size=12, anchor_x="center")
        arcade.draw_text("Hit Enter to Start", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-60, arcade.color.WHITE, font_size=12, anchor_x="center")

    def update(self, delta_time):
        self.draw()
        self.check_keys()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.ENTER in self.held_keys:
            game = Game2()
            self.window.show_view(game)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        self.held_keys.add(key)
    
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
        

class Game(arcade.View):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """
    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.held_keys = set()
        texture = "ship.png"
        self.ship = Ship(texture, 2/3)
        self.bullets = []
        self.asteroids = [Large_Asteroids(), Large_Asteroids(), Large_Asteroids(), Large_Asteroids(), Large_Asteroids()]

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()
        if self.ship.alive == False: 
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE)

        self.ship.draw()

        for bullet in self.bullets:
            bullet.draw()

        for asteroid in self.asteroids:
            asteroid.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_off_screen()
        self.ship.advance()
        self.check_for_colisions()

        for bullet in self.bullets:
            if bullet.frame_count == 60:
                self.bullets.remove(bullet)
            bullet.advance()

        for asteroid in self.asteroids:
            asteroid.advance()

    def check_off_screen(self):
        
        for bullet in self.bullets:
            bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        for asteroid in self.asteroids:
            asteroid.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def check_for_colisions(self):

        for bullet in self.bullets:
            for asteriod in self.asteroids:
                if bullet.alive and asteriod.alive:
                    too_close = bullet.radius + asteriod.radius
                    if (abs(bullet.center.x - asteriod.center.x) < too_close and abs(bullet.center.y - asteriod.center.y) < too_close):
                        bullet.was_hit()
                        self.clean_up_zombies()
                        
                        asteriod.was_hit()
                        if asteriod.hits == 2:

                            medAsteriod = Medium_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx , asteriod.velocity.dy + 2)

                            medAsteriod2 = Medium_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx, asteriod.velocity.dy - 2)

                            smolAsteriod = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx + 5, asteriod.velocity.dy)

                            self.asteroids.append(medAsteriod)
                            self.asteroids.append(medAsteriod2)
                            self.asteroids.append(smolAsteriod)

                        elif asteriod.hits == 1:

                            smolAsteriod = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx + 1.5, asteriod.velocity.dy + 1.5)
                            
                            smolAsteriod2 = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx - 1.5, asteriod.velocity.dy - 1.5)

                            self.asteroids.append(smolAsteriod)
                            self.asteroids.append(smolAsteriod2)


        for asteriod in self.asteroids:
            if asteriod.alive and self.ship.alive:
                too_close = self.ship.radius + asteriod.radius
                if (abs(self.ship.center.x - asteriod.center.x) < too_close and abs(self.ship.center.y - asteriod.center.y) < too_close):
                    self.ship.was_hit()

        self.clean_up_zombies()

    def clean_up_zombies(self):
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += SHIP_TURN_AMOUNT
            
        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= SHIP_TURN_AMOUNT
            
        if arcade.key.UP in self.held_keys:
            self.ship.speed.dx += math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.speed.dy += math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
        
        if arcade.key.DOWN in self.held_keys:
             self.ship.speed.dx -= math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
             self.ship.speed.dy -= math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            
        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:

                velocity_dx = (self.ship.speed.dx + math.cos(math.radians(self.ship.angle + 90)) * BULLET_SPEED)
                velocity_dy = self.ship.speed.dy + math.sin(math.radians(self.ship.angle + 90)) * BULLET_SPEED

                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y, velocity_dx, velocity_dy)
                bullet.fire()
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


class Game2(arcade.View):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """
    def __init__(self):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.held_keys = set()
        texture = "ship.png"
        self.ship2 = Ship(texture, 1/3)
        texture2 = "ship2.png"
        self.ship = Ship(texture2, 2/3)
        self.bullets = []
        self.asteroids = [Large_Asteroids(), Large_Asteroids(), Large_Asteroids(), Large_Asteroids(), Large_Asteroids()]
        self.score = 0

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()
        if self.ship.alive == False and self.ship2.alive == False:
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE)

        self.ship.draw()
        self.ship2.draw()

        for bullet in self.bullets:
            bullet.draw()

        for asteroid in self.asteroids:
            asteroid.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_off_screen()
        self.ship.advance()
        self.ship2.advance()
        self.check_for_colisions()

        for bullet in self.bullets:
            if bullet.frame_count == 60:
                self.bullets.remove(bullet)
            bullet.advance()

        for asteroid in self.asteroids:
            asteroid.advance()

    def check_off_screen(self):
        
        for bullet in self.bullets:
            bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ship2.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        for asteroid in self.asteroids:
            asteroid.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def check_for_colisions(self):

        for bullet in self.bullets:
            for asteriod in self.asteroids:
                if bullet.alive and asteriod.alive:
                    too_close = bullet.radius + asteriod.radius
                    if (abs(bullet.center.x - asteriod.center.x) < too_close and abs(bullet.center.y - asteriod.center.y) < too_close):
                        bullet.was_hit()
                        self.clean_up_zombies()
                        
                        asteriod.was_hit()
                        if asteriod.hits == 2:
                            
                            medAsteriod = Medium_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx , asteriod.velocity.dy + 2)

                            medAsteriod2 = Medium_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx, asteriod.velocity.dy - 2)

                            smolAsteriod = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx + 5, asteriod.velocity.dy)

                            self.asteroids.append(medAsteriod)
                            self.asteroids.append(medAsteriod2)
                            self.asteroids.append(smolAsteriod)

                        elif asteriod.hits == 1:

                            smolAsteriod = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx + 1.5, asteriod.velocity.dy + 1.5)
                            
                            smolAsteriod2 = Small_Asteroid(asteriod.center.x, asteriod.center.y, asteriod.velocity.dx - 1.5, asteriod.velocity.dy - 1.5)

                            self.asteroids.append(smolAsteriod)
                            self.asteroids.append(smolAsteriod2)


        for asteriod in self.asteroids:
            if asteriod.alive and self.ship.alive:
                too_close = self.ship.radius + asteriod.radius
                if (abs(self.ship.center.x - asteriod.center.x) < too_close and abs(self.ship.center.y - asteriod.center.y) < too_close):
                    self.ship.was_hit()

        ## for ship 2
        for asteriod in self.asteroids:
            if asteriod.alive and self.ship2.alive:
                too_close = self.ship2.radius + asteriod.radius
                if (abs(self.ship2.center.x - asteriod.center.x) < too_close and abs(self.ship2.center.y - asteriod.center.y) < too_close):
                    self.ship2.was_hit()

        ## if the ships run into each other they both die
        if self.ship.alive and self.ship2.alive:
            too_close = self.ship.radius + self.ship2.radius
            if (abs(self.ship2.center.x - self.ship.center.x) < too_close and abs(self.ship2.center.y - self.ship.center.y) < too_close):
                self.ship.was_hit()
                self.ship2.was_hit()

        ## if the ship gets shot down by a bullet

        self.clean_up_zombies()

    def clean_up_zombies(self):
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
                
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.angle += SHIP_TURN_AMOUNT
            
        if arcade.key.RIGHT in self.held_keys:
            self.ship.angle -= SHIP_TURN_AMOUNT
            
        if arcade.key.UP in self.held_keys:
            self.ship.speed.dx += math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship.speed.dy += math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
        
        if arcade.key.DOWN in self.held_keys:
             self.ship.speed.dx -= math.cos(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
             self.ship.speed.dy -= math.sin(math.radians(self.ship.angle + 90)) * SHIP_THRUST_AMOUNT
            
        ### For Ship Two            
        if arcade.key.W in self.held_keys:
            self.ship2.speed.dx += math.cos(math.radians(self.ship2.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship2.speed.dy += math.sin(math.radians(self.ship2.angle + 90)) * SHIP_THRUST_AMOUNT

        if arcade.key.A in self.held_keys:
            self.ship2.angle += SHIP_TURN_AMOUNT

        if arcade.key.D in self.held_keys:
            self.ship2.angle -= SHIP_TURN_AMOUNT
            
        if arcade.key.S in self.held_keys:
            self.ship2.speed.dx -= math.cos(math.radians(self.ship2.angle + 90)) * SHIP_THRUST_AMOUNT
            self.ship2.speed.dy -= math.sin(math.radians(self.ship2.angle + 90)) * SHIP_THRUST_AMOUNT
        

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:

                velocity_dx = (self.ship.speed.dx + math.cos(math.radians(self.ship.angle + 90)) * BULLET_SPEED)
                velocity_dy = self.ship.speed.dy + math.sin(math.radians(self.ship.angle + 90)) * BULLET_SPEED

                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y, velocity_dx, velocity_dy)
                bullet.fire()
                self.bullets.append(bullet)

        ## for ship 2
        if self.ship2.alive:
            self.held_keys.add(key)

            if key == arcade.key.C:
                
                velocity_dx = (self.ship2.speed.dx + math.cos(math.radians(self.ship2.angle + 90)) * BULLET_SPEED)
                velocity_dy = self.ship2.speed.dy + math.sin(math.radians(self.ship2.angle + 90)) * BULLET_SPEED

                bullet = Bullet(self.ship2.angle, self.ship2.center.x, self.ship2.center.y, velocity_dx, velocity_dy)
                bullet.fire()
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    start = Start_Window()
    window.show_view(start)
    arcade.run()

if __name__ == "__main__":
    main()