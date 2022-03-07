import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *


class Particle:
	allParticles = []
	gravity = Vec2(0, 0.1)
	lifeTime = 255
	wind = Vec2(0, 0)

	def __init__(self, x, y, color=white):
		self.pos = Vec2(x, y)
		self.vel = Vec2.Random()
		self.acc = Vec2(0, 0, lists=[])
		self.radius = 5
		
		self.color = color
		self.bounceLoss = Vec2(-0.95, -(randint(3, 5) / 10))

		self.lifeTime = randint(Particle.lifeTime // 2, Particle.lifeTime)

		Particle.allParticles.append(self)

	def Draw(self):
		DrawCircleAlpha(screen, (self.color[0], self.color[1], self.color[2], max(0, min(255, self.lifeTime))), (self.pos.x, self.pos.y), self.radius)

	def ApplyForce(self, force):
		self.acc = self.acc.Add(force)

	def Update(self):
		self.vel = self.vel.Add(self.acc)
		self.pos = self.pos.Add(self.vel)
		self.acc = Vec2(0, 0, lists=[])

		if Particle.lifeTime != -1:
			self.lifeTime -= 1

			if self.lifeTime <= 0:
				if self in Particle.allParticles:
					Particle.allParticles.remove(self)

			if (self.pos.x <= self.radius or self.pos.x >= width - self.radius) and (self.pos.y <= self.radius or self.pos.y >= height - self.radius):
				if self in Particle.allParticles:
					Particle.allParticles.remove(self)

	def Edges(self, y=True, x=True):
		if y:
			if self.pos.y >= height - self.radius:
				self.pos.y = height - self.radius
				self.vel.y *= self.bounceLoss.y

			if self.pos.y <= self.radius:
				self.pos.y = self.radius
				self.vel.y *= self.bounceLoss.y
		if x:
			if self.pos.x >= width - self.radius:
				self.pos.x = width - self.radius
				self.vel.x *= self.bounceLoss.x

			if self.pos.x <= self.radius:
				self.pos.x = self.radius
				self.vel.x *= self.bounceLoss.x


class Emitter:
	allEmitters = []
	maxNumOfParticles = 100

	def __init__(self, x, y, color=white):
		self.pos = Vec2(x, y)
		self.vel = Vec2.Random()
		self.acc = Vec2(0, 0, lists=[])
		self.radius = 5
		self.maxNumOfParticles = Emitter.maxNumOfParticles

		self.particles = []
		
		self.color = color

		Emitter.allEmitters.append(self)

	def Draw(self):
		pg.gfxdraw.aacircle(screen, self.pos.x, self.pos.y, self.radius, self.color)

	def CreateParticle(self):
		if len(self.particles) <= self.maxNumOfParticles:
			Particle(self.pos.x, self.pos.y, self.color)

	def Update(self):
		self.CreateParticle()




def DrawLoop():
	screen.fill(black)

	for emitter in Emitter.allEmitters:
		emitter.Draw()

	for particle in Particle.allParticles:
		particle.Draw()

	DrawAllGUIObjects()

	pg.display.update()



def HandleEvents(event):
	HandleGui(event)



def Update():
	# Particle.wind = Vec2(((pg.mouse.get_pos()[0] - width // 2) / width), ((pg.mouse.get_pos()[1] - height // 2) / height))
	
	for emitter in Emitter.allEmitters:
		emitter.Update()
	
	for particle in Particle.allParticles:
		particle.ApplyForce(Particle.gravity)

	for particle in Particle.allParticles:
		particle.Update()
		particle.Edges(x=False)



fpsLbl = Label((0, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False})

Emitter(width // 4, height // 2)
Emitter(width // 2, height // 2)
Emitter(width // 4 + width // 2, height // 2)

while running:
	clock.tick_busy_loop(fps)

	fpsLbl.UpdateText(f"{round(clock.get_fps())}")

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()

pg.quit()