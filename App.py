from Boat import Boat
from Map import Map
import keyboard
import time
def wait_for_keypress():
    key = keyboard.read_key()
    return key


#################### TEST ####################
map = Map({"x":100,"y":50},"*")
boat = Boat("P",map,[{"x":6,"y":3},{"x":6,"y":9}])
rock = Boat("P",map,[{"x":12,"y":14},{"x":17,"y":19}])

map.addElement(boat)
map.addElement(rock)

run = True
# Boucle principale
# lance le jeu

vitesse = 1
print(map)
# Boucle principale
while run:
    
    
    key = wait_for_keypress()
    if key == "q":
        direction = "left"
    elif key == "d":
        direction = "right"
    elif key == "z":
        direction = "up"
    elif key == "s":
        direction = "down"
    elif key == "+":
        vitesse += 1
    elif key == "-":
        vitesse -= 1
    elif key == "e":
        run = False
    if key in ["q","d","z","s"]:
        boat.move(direction,vitesse)   
        map.reloadMatrice()
        print(map)
    time.sleep(0.1)
    

    


    

        