import pygame, sys
from App_1 import *
from Map import *
from Boat import *

WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

class Game:

	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Bataille Navale')
		self.clock = pygame.time.Clock()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()