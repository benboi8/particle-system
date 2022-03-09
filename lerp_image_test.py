import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *

color = blue
radius = 100

img1 = pg.image.load("soft_texture.png").convert_alpha()
img_texture1 = pg.transform.smoothscale(img1, (radius * 2, radius * 2))

for x in range(img_texture1.get_width()):
	for y in range(img_texture1.get_height()):
		img_color = img_texture1.get_at((x, y))
		img_texture1.set_at((x, y), (color[0], color[1], color[2], img_color[3]))


color = red
radius = 100

img2 = pg.image.load("soft_texture.png").convert_alpha()
img_texture2 = pg.transform.smoothscale(img2, (radius * 2, radius * 2))

for x in range(img_texture2.get_width()):
	for y in range(img_texture2.get_height()):
		img_color = img_texture2.get_at((x, y))
		img_texture2.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

color = LerpColor(red, blue, 0.5)
radius = 100

img3 = pg.image.load("soft_texture.png").convert_alpha()
img_texture3 = pg.transform.smoothscale(img2, (radius * 2, radius * 2))

for x in range(img_texture3.get_width()):
	for y in range(img_texture3.get_height()):
		img_color = img_texture3.get_at((x, y))
		img_texture3.set_at((x, y), (color[0], color[1], color[2], img_color[3]))


def DrawLoop():
	screen.fill(black)

	screen.blit(img_texture1, (100, 100))
	screen.blit(img_texture2, (200, 100))
	screen.blit(img_texture3, (150, 100))


	DrawAllGUIObjects()


	pg.display.update()



def HandleEvents(event):
	HandleGui(event)




while running:
	clock.tick_busy_loop(fps)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	DrawLoop()
