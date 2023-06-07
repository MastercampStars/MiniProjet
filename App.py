from Boat import Boat
from Map import Map


#################### TEST ####################
map = Map(40,"*")
boat = Boat([{"x":16,"y":13},{"x":18,"y":18}],"P")
map.addElement(boat)
print(map)
print(boat)
boat.move("left",3)
map.reloadMatrice()
print(map)
print(boat)
boat.move("down",3)
map.reloadMatrice()
print(map)
print(boat)
boat.move("right",3)
map.reloadMatrice()
print(map)
print(boat)
boat.move("up",3)
map.reloadMatrice()
print(map)
print(boat)
boat.move("down",3)
boat.move("right",3)
boat.move("up",3)
boat.move("left",3)
map.reloadMatrice()
print(map)


    

        