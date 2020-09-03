"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Chelci Lee cl868 Ada Luo al2342
# 2019.12.12
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _count: the number of aliens alive
    #Invariant: _count is a int >= 0

    # Attribute _direction: the direction the ship is moving
    #Invariant: _direction is a string

    #Attribute _lose: if the aliens the defensive line or if the lives are 0
    #Invariant: _lose is a bool

    #Attribute _win: if the player wins, this is True
    #Invariant: _win is a bool

    #Attribute _pbolt: if there is a player bolt, this is True
    #Invariant: _pbolt is a bool

    #Attribute _random: a random number of steps before an alien fires a bolt.
    #Invariant: _random is an in between 1 and BOLT_RATE

    #Attribute _btime: time since the last shot
    #Invariant: _btime is a float >= 0s

    #Attribute _time2: time since last press of m
    #Invariant: _time2 is a float >=0s

    #Attribute _paused: if the ship is None, this is True
    #Invariant: _paused is a bool

    #Attribute _sound: If true, the sound plays.
    #Invariant: _sound is a bool

    #Attribute _pew1: A sound for ship shooting
    #Invariant: _pew1 is a Sound object

    #Attribute _pew2: A sound for alien shooting
    #Invariant: _pew2 is a Sound object

    #Attribute _pew3: Another sound fo   alien shooting
    #Invariant: _pew3 is a Sound object

    #Attribute _pop1: A sound for alien dying
    #Invariant: _pop1 is a Sound object

    #Attribute _blast2: a sound for ship dying
    #Invariant: _blast2 is a Sound object

    #Attribute _wavenum: number of the wave the player is on starting from 0
    #Invariant: _wavenum is an int >=0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        returns the ship
        """
        return self._ship

    def setShip(self):
        """
        sets the ship
        """
        self._ship = Ship()

    def getLives(self):
        """
        returns the lives
        """
        return self._lives

    def getLose(self):
        """
        returns _lose
        """
        return self._lose

    def getWin(self):
        """
        returns _win
        """
        return self._win

    def setWin(self, bool):
        """
        Sets self._win to the bool

        Parameter: bool
        Precondition: bool is a bool
        """
        self._win = bool
    def getPaused(self):
        """
        Returns if the game should be paused or not
        """
        return self._paused

    def setPaused(self, bool):
        """
        Changes the _paused attribute

        Parameter bool: if the game should be paused or not
        Precondition: bool is a bool
        """
        self._paused = bool

    def getSound(self):
        """
        Returns the _sound attribute
        """
        return self._sound

    def setSound(self, bool):
        """
        Changes _sound attribute

        Parameter sound: if the sound should be on or not
        Precondition: bool is a bool
        """
        self._sound = bool

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, wavenum, sound):
        """
        Initializes the ship and aliens.

        Parameter wavenum:
        Precondition:

        Parameter sound:
        Precondition: 
        """
        self._ship = Ship()
        self._count = 0
        self._aliens = self._alien_wave()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=2,linecolor="cyan")
        self._lives = SHIP_LIVES
        self._time = 0
        self._direction = 'right'
        self._lose = False
        self._win = False
        self._pbolt = False
        self._random = 0
        self._btime = 0
        self._time2 = 0
        self._paused = False
        self._sound = sound
        self._pew1 = Sound('pew1.wav')
        self._pew2 = Sound('pew2.wav')
        self._pew3 = Sound('pew2.wav')
        self._blast2 = Sound('blast2.wav')
        self._pop1 = Sound('pop1.wav')
        if wavenum < BOLT_RATE:
            self._wavenum = wavenum

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, dt, input):
        """
        Animates the ship, the aliens, and the laser bolts.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: A valid GInput
        Precondition: input is a float (positive)
        """
        self._update_ship(input)
        self._update_aliens(dt)
        self._update_laserbolts(input)
        self._changeSound(dt, input)
        if self._ship is None:
            if self._lives>0:
                self._paused = True
            elif self._lives == 0:
                self._lose = True
        if self._count == 0:
            self._win = True

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # IMPLEMENT ME
        if self._ship is not None:
            self._ship.draw(view)

        if self._aliens is not None:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.draw(view)

        if self._dline is not None:
            self._dline.draw(view)

        if self._bolts is not None:
            for row in self._bolts:
                row.draw(view)

    #SHIP HELPER METHODS
    def _update_ship(self, input):
        """
        Animates the ship.

        Parameter input: The key that is pressed by the player.
        Precondition: The 'right' or 'left' key.
        """
        if input.is_key_down('left') and (self._ship.x-(SHIP_WIDTH/2)) > 0:
            self._ship.x -= SHIP_MOVEMENT
        if input.is_key_down('right') and (self._ship.x+(SHIP_WIDTH/2)) < GAME_WIDTH:
            self._ship.x += SHIP_MOVEMENT

    #LASER BOLT HELPER METHODS
    def _update_laserbolts(self, input):
        """
        Animates the laserbolts and checks if player shoots a bolt.

        Parameter input: user input
        Precondition: The 'spacebar'
        """
        for x in self._bolts:
            if x.isPlayerBolt() == True:
                self._pbolt = True
        if input.is_key_down('spacebar') and self._pbolt == False and self._ship is not None:
            self._bolts.append(Bolt(x=self._ship.x,y= self._ship.y + self._ship.height/1.65,
            velocity=BOLT_SPEED))
            self._pbolt = True
            if self._sound == True:
                self._pew1.play()
        for x in self._bolts:
            x.move()
        self._shipcollision()
        self._deletebolt()

    def _deletebolt(self):
        """
        Delete Alien Bolts and Player Bolts as they leave the screen.
        """
        for x in self._bolts:
            if x.isPlayerBolt():
                if x.y - BOLT_HEIGHT/2 > GAME_HEIGHT:
                    self._bolts.remove(x)
                    self._pbolt = False
            if x.isAlienBolts():
                if x.y + BOLT_HEIGHT/2 < 0:
                    self._bolts.remove(x)
                    self._abolt = False

    # ALIEN HELPER METHODS
    def _alien_wave(self):
        """
        Helper method for making the alien wave.
        """
        something = GAME_HEIGHT-ALIEN_CEILING-(ALIEN_HEIGHT*ALIEN_ROWS)
        startingy = something-(ALIEN_V_SEP*(ALIEN_ROWS-1))+(ALIEN_HEIGHT/2)
        startingx = ALIEN_H_SEP+(ALIEN_WIDTH/2)
        listr = []
        for x in range(ALIEN_ROWS):
            tempx = startingx
            listy = []
            for y in range(ALIENS_IN_ROW):
                if x % 6 == 0 or x == 1:
                    image = "alien1.png"
                elif x % 6 == 2 or x % 6 == 3:
                    image = "alien2.png"
                else:
                    image = "alien3.png"
                listy.append(Alien(tempx,startingy,image))
                self._count = self._count + 1
                tempx = tempx + ALIEN_H_SEP + ALIEN_WIDTH
            listr.append(listy)
            startingy = startingy + ALIEN_V_SEP + ALIEN_HEIGHT
        return listr

    def _update_aliens(self,dt):
        """
        Animates the aliens.

        Parameter dt: The time in seconds since the last update.
        Precondition: dt is a number (int or float)
        """
        self._moveAliens(dt)
        if self._alien_rightbottom() < DEFENSE_LINE:
            self._lose = True
        self._btime = self._btime + dt
        if self._btime > self._random:
            self._alienshoot()
            self._random = random.randint(1, BOLT_RATE-self._wavenum)
            self._btime = 0
        self._aliencollision()
        self._countAliens()

    def _moveAliens(self, dt):
        """
        Moves the aliens appropriately

        Parameter dt: time since last alien step
        Precondition: dt is a float >= 0
        """
        self._time = dt + self._time
        if self._time > ALIEN_SPEED-(self._wavenum/10):
            if self._direction == 'right':
                if self._alien_right() > (GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH/2):
                    self._alien_down()
                    self._direction = 'left'
                else:
                    self._alien_rightmove()
            elif self._direction == 'left':
                if self._alien_left() < (ALIEN_H_SEP+ALIEN_WIDTH/2):
                    self._alien_down()
                    self._direction = 'right'
                else:
                    self._alien_leftmove()
            self._time = 0

    def _countAliens(self):
        """
        Counts the number of aliens left and stores it in the _count attribute.
        """
        count = 0
        for x in self._aliens:
            for y in x:
                if y is not None:
                    count += 1
        self._count = count

    def _alienshoot(self):
        """
        Makes the last alien in the bottom of the column shoot. Plays sound.
        """
        rando = self._randomcolumn()
        rownum = self._findBottom(rando)
        alien = self._aliens[rownum][rando]
        isalien = False
        for x in self._bolts:
            if x.isAlienBolts() == True:
                isalien = True
        if alien is not None:
            self._bolts.append(Bolt(x= alien.x,y=alien.y-ALIEN_HEIGHT/2,velocity=-BOLT_SPEED))
        if self._sound == True and isalien == False:
            self._pew2.play()
        elif self._sound == True and isalien == True:
            self._pew3.play()

    def _findBottom(self, column):
        """
        returns the row of the last alien in a column

        Parameter column: a column to find the alien in
        Precondition: column is a number from 0 to len(row)-1
        """
        number = 0
        for x in range(len(self._aliens)):
            if self._aliens[x][column] is None:
                number = number +1
        return number

    def _randomcolumn(self):
        """
        Finds a random column and checks if its empty.
        """
        ran = random.randint(0, ALIENS_IN_ROW-1)
        if not self._emptycolumn(ran):
            return ran
        else:
            return self._randomcolumn()

    def _emptycolumn(self, column):
        """
        Returns True if the column that wants to be checked is empty

        Parameter column: The column to check
        Precondition: The column is an int from 1 to len(row)
        """
        empty = False
        emptyalien = 0
        for row in self._aliens:
            if row[column] == None:
                emptyalien += 1
        if emptyalien == len(self._aliens):
            empty = True
        return empty

    def _alien_rightmove(self):
        """
        Moves the aliens to the right ALIEN_H_WALK pixels.
        """
        for x in self._aliens:
            for y in x:
                if y is not None:
                    y.x = y.x + ALIEN_H_WALK

    def _alien_leftmove(self):
        """
        Moves the aliens to the left ALIEN_H_WALK pixels.
        """
        for x in self._aliens:
            for y in x:
                if y is not None:
                    y.x = y.x - ALIEN_H_WALK

    def _alien_right(self):
        """
        Returns the position of the alien furthest to the right.
        """
        max = 0
        for x in self._aliens:
            for y in x:
                if y is not None:
                    if y.x > max:
                        max = y.x
        return max+(ALIEN_WIDTH/2)

    def _alien_left(self):
        """
        Returns the position of the alien furthest to the left.
        """
        min = 800
        for x in self._aliens:
            for y in x:
                if y is not None:
                    if y.x < min:
                        min = y.x
        return min-(ALIEN_WIDTH/2)

    def _alien_down(self):
        """
        Moves the alien down.
        """
        for x in self._aliens:
            for y in x:
                if y is not None:
                    y.y = y.y - ALIEN_V_WALK

    def _alien_rightbottom(self):
        """
        Returns the position of the alien furthest down.
        """
        min = 800
        for x in self._aliens:
            for y in x:
                if y is not None:
                    if y.y < min:
                        min = y.y
        return min-(ALIEN_HEIGHT/2)

    #HELPER METHODS FOR SOUND
    def _changeSound(self,dt,input):
        """
        Changes the _sound when 'm' is pressed

        Parameter dt: Time elapsed.
        Precondition: Time is number >0

        Parameter input: User input
        Precondition: the 'm' key.
        """
        self._time2 = self._time2 + dt
        if self._time2 > 1:
            if input.is_key_down('m'):
                if self._sound == True:
                    self._sound = False
                elif self._sound == False:
                    self._sound = True
                self._time2 = 0

    # HELPER METHODS FOR COLLISION DETECTION
    def _aliencollision(self):
        """
        Checks if a playerbolt and an alien collided and deletes them if so.
        Plays sound.
        """
        for bolt in self._bolts:
            for row in self._aliens:
                for alien in range(len(row)):
                    if row[alien] is not None:
                        if row[alien].aliencollides(bolt):
                            self._bolts.remove(bolt)
                            self._pbolt = False
                            row[alien] = None
                            if self._sound == True:
                                self._pop1.play()
    def _shipcollision(self):
        """
        Checks if a shipbolt and an alien has collided and deletes them if so.
        Plays sound.
        """
        for bolt in self._bolts:
            if bolt.isAlienBolts():
                if self._ship is not None:
                    if self._ship.shipcollides(bolt):
                        if self._sound == True:
                            self._blast2.play()
                        self._ship = None
                        self._paused = True
                        self._lives = self._lives - 1
                        self._bolts.remove(bolt)
