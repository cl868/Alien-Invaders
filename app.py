"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Chelci Lee cl868 Ada Luo al2342
# 2019.12.12
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py


class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _text2: another currently active message
    #Invariant: _text2 is a GLabel object, or None if there is no message to
    # display. It is only None if _state is STATE_ACTIVE.

    #Attribute _text3: a third currently active message.
    #Invariant: _text3 is a GLabel object, or None if there is no message to
    # display. It is only None if _state is STATE_ACTIVE.

    # Attribute _lastkeys: the number of keys that were pressed
    # Invariant: _lastkeys is an int > 0

    #Attribute _wavenum: the wave number + 9
    #Invariant: _wavenum is a number >=10

    #Attribute _sound: if the sound is on or off
    #Invariant: _sound is a bool

    #GETTERS AND SETTERS

    def getState(self):
        """
        Returns self._state
        """
        return self._state

    def setState(self, state):
        """
        Sets self._state to a new state
        """
        assert 0 <= state and state <= 5
        self._state = state

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # IMPLEMENT ME
        self._wave = None
        self._state = STATE_INACTIVE
        self._lastkeys = 0
        self._wavenum = -1
        self._sound = True
        self._text=GLabel(text='Press \'S\' to play',font_sizez=75,x=GAME_WIDTH/2,
        y=GAME_HEIGHT/2,font_name = 'Arcade.ttf')
        self._text2 = GLabel(text='Press \'M\' to mute/unmute sound',font_size=24,
        x=200,y=20, font_name = 'ArialBold.ttf', linecolor = 'navy')
        self._text3 = GLabel(text='Use arrow keys to move and spacebar to shoot',font_size=24,
        x = GAME_WIDTH/2, y = 600, font_name = 'ArialBold.ttf', linecolor = 'navy')

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._determineState()
        elif self._state == STATE_NEWWAVE:
            self._text = None
            self._text2 = None
            self._text3 = None
            self._wavenum = self._wavenum + 1
            self._wave = Wave(self._wavenum, self._sound)
            self._state = STATE_ACTIVE
        elif self._state == STATE_ACTIVE:
            self._activestate(dt,input)
        elif self._state == STATE_PAUSED:
            self._pausedstate()
        elif self._state == STATE_CONTINUE: 
            self._state = STATE_ACTIVE
            self._determineState()
        elif self._state == STATE_COMPLETE:
            self._completestate()

    def draw(self):
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
        if self._wave is not None:
            self._wave.draw(self.view)

        if self._text is not None:
            self._text.draw(self.view)

        if self._text2 is not None:
            self._text2.draw(self.view)

        if self._text3 is not None:
            self._text3.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Determines the current state and assigns it to self.state

        This method checks for a key press, and if there is one, changes the state
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        """
        self._active()
        if self._state is not STATE_ACTIVE and self._state is not STATE_CONTINUE:
            self._newwave()
        self._pause()
        self._finish()

    def _activestate(self,dt,input):
        """
        What to do when the state is active.
        """
        self._wave.update(dt, self.input)
        if self._wave.getLives() == SHIP_LIVES:
            self._text = GLabel(text= 'Lives: 3', font_size=24, font_name = 'Arial.ttf',
            x = GAME_WIDTH-50, y = GAME_HEIGHT-25)
        elif self._wave.getLives() == SHIP_LIVES-1:
            self._text = GLabel(text= 'Lives: 2', font_size=24, font_name = 'Arial.ttf',
            x = GAME_WIDTH-50, y = GAME_HEIGHT-25)
        elif self._wave.getLives() == SHIP_LIVES-2:
            self._text = GLabel(text= 'Lives: 1', font_size=24, font_name = 'Arial.ttf',
            x = GAME_WIDTH-50, y = GAME_HEIGHT-25)
        if self._wave.getSound() == True:
            self._text2 = GLabel(text='Sound On',font_size=24,x=60,y=20,
            linecolor = 'forest green', font_name = 'Arial.ttf')
            self._sound = True
        elif self._wave.getSound() == False:
            self._text2 = GLabel(text='Sound Off',font_size=24,x=60,y=20,
            linecolor = 'dark red', font_name = 'Arial.ttf')
            self._sound = False
        self._determineState()

    def _continuestate(self):
        """
        What do to when the the player loses a life.
        """
        self._text = GLabel(text= 'PRESS \'S\' TO CONTINUE', font_size = 50,
        font_name = 'Arcade.ttf',x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
        curr_keys = self.input.key_count

        change = curr_keys > 0 and self._lastkeys == 0

        if change and self.input.is_key_down("s"):
            self._text = None
            self.lastkeys= curr_keys
            self._wave.setShip()
            self._wave.setPaused(False)
            self._state = STATE_CONTINUE
        self._determineState()

    def _pausedstate(self):
        """
        What to do when the state is paused.
        """
        if self._wave.getWin():
            if self._wavenum == 4:
                self._state = STATE_COMPLETE
            else:
                self._text=GLabel(text='WAVE COMPLETE',font_size=75,
                font_name = 'Arcade.ttf',x=GAME_WIDTH/2,y=GAME_HEIGHT/2)
                self._anotherwave()
        else:
            self._continuestate()

    def _completestate(self):
        """
        What to do when the state is complete.
        """
        if self._wave is not None:
            if self._wave.getLose():
                self._wave = None
                self._text2 = None
                self._text=GLabel(text='GAME OVER',font_size=75,x=GAME_WIDTH/2,
                y=GAME_HEIGHT/2,fillcolor='white')
            else:
                self._wave = None
                self._text2 = GLabel(text= 'CONGRATULATIONS',font_size=50,x=GAME_WIDTH/2,
                y=GAME_HEIGHT/2-100,fillcolor='white', font_name = 'RetroGame.ttf')
                self._text=GLabel(text='GAME COMPLETE',font_size=75,x=GAME_WIDTH/2,
                y=GAME_HEIGHT/2,fillcolor='white', font_name = 'Arcade.ttf')

    def _newwave(self):
        """
        Detects when the player presses the key to make a new wave
        and changes the state.
        """
        curr_keys = self.input.key_count

        change = curr_keys > 0 and self._lastkeys == 0

        if change and self.input.is_key_down("s"):
            self._state = STATE_NEWWAVE
            self._text = None
            self._text2 = None

        self._lastkeys= curr_keys

    def _active(self):
        """
        Changes state to active after a new wave.
        """
        if self._state == STATE_NEWWAVE:
            if self._wave is not None:
                self._state = STATE_ACTIVE

    def _pause(self):
        """
        Changes state to paused.
        """
        if self._wave is not None:
            if self._wave.getPaused() == True:
                self._state = STATE_PAUSED

    def _finish(self):
        """
        A way to get the finish attribute in the wave object and changes state to
        complete or paused.
        """
        if self._wave != None:
            if self._wave.getLose():
                self._state = STATE_COMPLETE
            if self._wave.getWin():
                self._state = STATE_PAUSED

    def _anotherwave(self):
        """
        What to display and do when the player kills all the aliens and waits
        for input to make a new wave.
        """
        self._text2 = GLabel(text= 'PRESS \'S\' TO CONTINUE', font_size = 50, x=GAME_WIDTH/2,
        y=200, font_name = 'Arcade.ttf')
        self._newwave()
