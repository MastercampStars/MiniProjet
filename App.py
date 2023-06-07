from Boat import Boat
from Map import Map


#################### TEST ####################
map = Map(20,"*")
boat = Boat([{"x":6,"y":3},{"x":6,"y":5}],"P")
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

    

        