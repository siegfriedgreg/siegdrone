#    SiegDrone.py writtten by Greg Siegfried
#    Sources used were:
#         ps_drone.py
#         (w)+(c) J. Philipp de Graaff, www.playsheep.de, drone@playsheep.de, 2012-2015
#         Project homepage: www.playsheep.de/drone and 
#             https://sourceforge.net/projects/ps-drone/
#
#         ps4constroller.py
#         (w)+(c) Jacob Laney MIT 2016
#         Project homepage: https://github.com/JacobLaney/py-drone
#
#    This project tries to use the pygames as input and feedback for the user.
#    The current button configuration is:
#    Pad:
#    Down/Up = -/+ Animation Options             Triangle = FRONT-FLIP
#    Left/Right = -/+ Led Options       Square = LEFT-FLIP    Circle = RIGHT-FLIP
#                                                eXe = BACK-FLIP
#
#    Shoulder:    L1 = LED PATTERN        R1 = TAKEOFF/LANDING
#    
#    LEFT-CLICK JOYSTICK: NOT USED
#    RIGHT-CLICK JOYSTICK: Set's the new drone speed value.
#
#    SPECIAL:    
#    Share:    Set Megneto Trim (Must be in flight!)
#    Option:    Set Drone Soft Reset (Must be on ground!)
#    *** PLAYSTATION BUTTON = ENDS THE RUNNING STATE TO EXIT THE PROGRAM!
#                            ***    BE ON THE GROUND WHEN PRESSED!
#
#    The axis for the PS4 controller are:
#        W/Forward = Left-Stick Up    S/Backward = Left-Stick Down
#        A/SideLeft = Left-Stick Left  D/SideRight = Left-Stick Right
#       
#        Raise Drone = Right-Stick Up    Lower Done = Right-Stick Down
#        Turn Left = Right-Stick Left    Turn Right = Right-Stick Right
##
####
######

import time
import sys
import ps_drone
import pygame


# Start using drone
drone = ps_drone.Drone()  
# Connects to drone and starts subprocesses                                   
drone.startup()                                              
# Sets drone's status to good (LEDs turn green when red)
drone.reset()
# Give me everything...fast
drone.useMDemoMode(False) 
# Packets, which shall be decoded                                                     
drone.getNDpackage(["demo", "time","pressure_raw","altitude","magneto","wifi", "hdvideo_stream"]) 
# Packages to add to Decode
#drone.addNDpackage(["all"]) 
# Give it some time to awake fully after reset     
time.sleep(1.0)                                                              

# Go to multiconfiguration-mode   
drone.setConfigAllID() 
# Choose lower resolution (hdVideo() for...well, guess it)     
drone.hdVideo() 
# Choose front view                                             
drone.frontCam()                                             
CDC = drone.ConfigDataCount
# Wait until it is done (after resync is done)
while CDC == drone.ConfigDataCount:       time.sleep(0.0001) 
# Start video-function
drone.startVideo()
# Display the video                                           
drone.showVideo()
time.sleep(1.0) 

# Set Drone Speed.
drone.setSpeed(drone.speedval)

#### init the display ####
pygame.init()
WIDTH = 600
HEIGHT = 400
size = [WIDTH, HEIGHT] # size of window in pixels [width,height]
DISPLAY = pygame.display.set_mode(size)

#### some colors that can be used for the display ####
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#### init ps4 controller ####
pygame.joystick.init()
try:
    controller = pygame.joystick.Joystick(0)
    controller.init()
except:
    print "#### Please connect a ps4 controller! ####"
    exit()
print "#### CONNECTED TO PS4 CONTROLLER ####"

#### process pygame event queue ####
def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print "QUIT"
            return True
        if e.type == pygame.JOYBUTTONUP:
            if e.button == 0: # X button
                if drone.isFlying == True:
                    print "#### X = BACK-FLIP##"
                    drone.anim(17,15)
                else:
                    print "#### X = DRONE NOT FLYING! ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)                       
            elif e.button == 1: # Circle Button
                if drone.isFlying == True:
                    print "#### CIRCLE = RIGHT-FLIP ####"
                    drone.anim(19,15)
                else:
                    print "#### CIRCLE = DRONE NOT FLYING! ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)
            elif e.button == 2: # Triangle Button
                if drone.isFlying == True:
                    print "#### TRIANGLE = FRONT-FLIP ####"
                    drone.anim(16,15)
                else:
                    print "#### TRIANGLE = DRONE NOT FLYING! ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)
            elif e.button == 3: # Square Button
                if drone.isFlying == True:
                    print "#### SQUARE = LEFT-FLIP ####"
                    drone.anim(18,15)
                else:
                    print "#### SQUARE = DRONE NOT FLYING! ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)
            elif e.button == 4: # L1 Button
                print "#### L1 = EXECUTE LEDS & STOP! ####"
                drone.stop()
                drone.led(drone.ledval, 1.5, 3)                               
            elif e.button == 5: # R1 Button
                if drone.isFlying == False:
                    print "#### R1 = TAKING OFF ####"
                    drone.led(9,1.5,5) 
                    time.sleep(2)
                    drone.takeoff()
                    drone.isFlying = True
                else:
                    print "#### R1 = LANDING ####"
                    drone.led(3,1.5,3)
                    time.sleep(0.5)
                    drone.land()
                    drone.isFlying = False
            elif e.button == 8: # SHARE Button
                if drone.isFlying == False:
                    print "#### SHARE = Soft Reset ####"
                    drone.led(7, 1.5, 1)
                    drone.reset()
                    time.sleep(1)
                    drone.reconnectNavData()
                    drone.led(8, 1.5, 1)
                    time.sleep(1)
                else:
                    print "#### SHARE = Soft Reset Not Allowed ####"             
            elif e.button == 9: # OPTIONS Button  
                if drone.isFlying == True:
                    print "#### OPTIONS = Magnetometer Trim ####"
                    drone.led(9,1.5,5)
                    drone.mtrim()
                else:
                    print "#### OPTIONS = MagTrim Reset Not Allowed ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)
            elif e.button == 10: # PLAYSTATION Button 
                drone.Running = False
                time.sleep(1) 
                print "#### Exiting Program ####"
            elif e.button == 12: # CLICK-IN RIGHTJOYSTICK
                if drone.isFlying == True:
                    print "#### RJSC = CHANGE SPEED ####"
                    drone.setSpeed(drone.speedval)
                    time.sleep(1)
                else:
                    print "#### RJSC = DRONE NOT FLYING! ####"
                    drone.led(2,1.5,5)
                    time.sleep(1)
    (x,y) = controller.get_hat(0)
    if x == -1:
        if drone.ledval - 1 > -1:
            drone.ledval -= 1
    if x == 1:
        if drone.ledval + 1 < 21:
            drone.ledval += 1
    if y == 1:
        if drone.speedval + 0.1 < 0.9:
            drone.speedval += 0.1
    if y == -1:
        if drone.speedval - 0.1 > -0.1:
            drone.speedval -= 0.1
    return False

##### reduces ps4 controller joystick sensitivity ####
def smooth_axis_input(value):
    if abs(value) < 0.1:
        return 0.0
    return value

#### process moving the drone ####
def handle_movement():
    #### MOVE ####
    valueAD = smooth_axis_input(controller.get_axis(0))
    valueWS = smooth_axis_input(controller.get_axis(1) * -1)

    #### UP and DOWN ####
    valueUpDn = smooth_axis_input(controller.get_axis(4) * -1)
    #### ROTATE
    valueLfRt = smooth_axis_input(controller.get_axis(3))

    #### Tell the drone to move ####
    if drone.isFlying:
        drone.move( valueAD, valueWS, valueUpDn, valueLfRt)
    #### slow down ####
    
#### draw the pygame window ####
def draw():
    DISPLAY.fill(WHITE)

    if drone.isFlying:
        pygame.draw.rect(DISPLAY, GREEN, (0, 0, WIDTH, HEIGHT/10))
    else:
        pygame.draw.rect(DISPLAY, RED, (0, 0, WIDTH, HEIGHT/10))

    #### output speed, led, battery information
    font = pygame.font.SysFont("impact", 25)
    speedLabel = font.render("SPEED-X (def=0.3):  {}".format(drone.speedval), 1, BLUE)
    ledLabel = font.render("LED ID (def=9):  {}".format(drone.ledval), 1, BLUE)
    flyLabel = font.render("IN FLIGHT?----> {}".format(drone.isFlying), 1, BLUE)
    bat1Label = font.render("BATTERY----> {}%".format(drone.getBattery()[0]), 1, BLUE)
    bat2Label = font.render("BATTERY----> {}".format(drone.getBattery()[1]), 1, BLUE)
    DISPLAY.blit(speedLabel, (10, HEIGHT/10 + 30 * 1))
    DISPLAY.blit(ledLabel, (10, HEIGHT/10 + 30 * 2))
    DISPLAY.blit(flyLabel, (310, HEIGHT/10 + 30 * 1))
    DISPLAY.blit(bat1Label, (310, HEIGHT/10 + 30 * 2))
    DISPLAY.blit(bat2Label, (310, HEIGHT/10 + 30 * 3))

    # draw joysticks
    pygame.draw.rect(DISPLAY, BLACK, (0, HEIGHT / 2, WIDTH, HEIGHT / 2))
    pygame.draw.circle(DISPLAY, BLUE, (WIDTH/4, 3*HEIGHT/4), 60, 5)
    pygame.draw.circle(DISPLAY, BLUE, (int(WIDTH/4 + controller.get_axis(0) * 20), int(3*HEIGHT/4 + controller.get_axis(1) * 20)), 40)
    pygame.draw.circle(DISPLAY, BLUE, (3*WIDTH/4, 3*HEIGHT/4), 60, 5)
    pygame.draw.circle(DISPLAY, BLUE, (int(3*WIDTH/4 + controller.get_axis(3) * 20), int(3*HEIGHT/4 + controller.get_axis(4) * 20)), 40)

    pygame.display.update()

####################################################
####                MAIN LOOP
####################################################
while drone.Running:
    if handle_events() == True:
        break
    handle_movement()  # tell the drone to move
    draw()  # draw the GUI
    pygame.time.Clock().tick(40) # make sure loop does not exceed 40 fps

print "#### Shutting Down ####"
drone.stopVideo()
time.sleep(1)
drone.shutdown()
time.sleep(1)

################    END FILE    ####################
