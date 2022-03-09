import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *


class Particle:
	allParticles = []
	maxNumOfParticles = 2000
	gravity = Vec2(0, 0.1)
	lifeTime = 255
	wind = Vec2(0, 0)
	radius = 5
	lifeReduction = 1
	
	def __init__(self, x, y, color=white, func=None):
		self.pos = Vec2(x, y)
		self.vel = Vec2.Random()
		self.acc = Vec2(0, 0, lists=[])
		self.radius = Particle.radius
		self.lifeReduction = Particle.lifeReduction

		self.color = color
		self.bounceLoss = Vec2(-0.95, -(randint(3, 5) / 10))

		self.lifeTime = randint(Particle.lifeTime // 2, Particle.lifeTime)

		self.killFunc = func

		Particle.allParticles.append(self)

	def Draw(self):
		DrawCircleAlpha(screen, (self.color[0], self.color[1], self.color[2], Constrain(self.lifeTime, 0, 255)), (self.pos.x, self.pos.y), self.radius)

	def ApplyForce(self, force):
		self.acc = self.acc.Add(force)

	def Update(self):
		self.vel = self.vel.Add(self.acc)
		self.pos = self.pos.Add(self.vel)
		self.acc = Vec2(0, 0, lists=[])

		if Particle.lifeTime != -1:
			self.lifeTime -= self.lifeReduction

			if self.lifeTime <= 0:
				self.Kill()

			# if (self.pos.x <= self.radius or self.pos.x >= width - self.radius) and (self.pos.y <= self.radius or self.pos.y >= height - self.radius):
				# self.Kill()

	def Kill(self):
		if self in Particle.allParticles:
			Particle.allParticles.remove(self)

		if callable(self.killFunc):
			self.killFunc(self)

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


class Fire(Particle):
	gravity = Vec2(0, 0)
	wind = Vec2(0.01, -0.04)

	color = red
	radius = 32

	img = pg.image.load("soft_texture.png").convert_alpha()
	img_texture = pg.transform.smoothscale(img, (radius * 2, radius * 2))

	for x in range(img_texture.get_width()):
		for y in range(img_texture.get_height()):
			img_color = img_texture.get_at((x, y))
			img_texture.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

	def __init__(self, x, y, func=None):
		super().__init__(x, y, Fire.color, func)
		self.vel = Vec2.Random(-0.5, 0.5, -3, -2)
		self.radius = Fire.radius
		self.img_texture = Fire.img_texture
		self.lifeReduction = 3
	
	def Draw(self):
		self.img_texture.set_alpha(Constrain(self.lifeTime, 0, 255))
		screen.blit(self.img_texture, (self.pos.x - self.radius, self.pos.y - self.radius))	


class Smoke(Particle):
	gravity = Vec2(0, 0)
	wind = Vec2(0.02, 0)

	color = LerpColor((45, 51, 46), white, 0.3)
	radius = 24

	img = pg.image.load("smoke1.png").convert_alpha()
	img_texture = pg.transform.smoothscale(img, (radius * 2, radius * 2))

	for x in range(img_texture.get_width()):
		for y in range(img_texture.get_height()):
			img_color = img_texture.get_at((x, y))
			img_texture.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

	def __init__(self, x, y, func=None):
		super().__init__(x, y, Smoke.color, func)
		self.vel = Vec2.Random(-0.5, 0.5, -3, -2)
		self.radius = Smoke.radius
		self.img_texture = Smoke.img_texture
	
	def Draw(self):
		self.img_texture.set_alpha(Constrain(self.lifeTime, 0, 255))
		screen.blit(self.img_texture, (self.pos.x - self.radius, self.pos.y - self.radius))

class Smoke2(Particle):
	gravity = Vec2(0, 0)
	wind = Vec2(0.02, 0)

	color = LerpColor((45, 51, 46), white, 0.3)
	radius = 24

	img = pg.image.load("smoke2.png").convert_alpha()
	img_texture = pg.transform.smoothscale(img, (radius * 2, radius * 2))

	for x in range(img_texture.get_width()):
		for y in range(img_texture.get_height()):
			img_color = img_texture.get_at((x, y))
			img_texture.set_at((x, y), (color[0], color[1], color[2], img_color[3]))

	def __init__(self, x, y, func=None):
		super().__init__(x, y, Smoke2.color, func)
		self.vel = Vec2.Random(-0.5, 0.5, -3, -2)
		self.radius = Smoke2.radius
		self.img_texture = Smoke2.img_texture
	
	def Draw(self):
		self.img_texture.set_alpha(Constrain(self.lifeTime, 0, 255))
		screen.blit(self.img_texture, (self.pos.x - self.radius, self.pos.y - self.radius))


class Emitter:
	allEmitters = []
	maxNumOfParticles = 300

	def __init__(self, x, y, particleType=Particle, w=5, h=5, color=white):
		self.pos = Vec2(x, y)
		self.particleType = particleType
		self.w, self.h = w, h
		self.vel = Vec2.Random()
		self.acc = Vec2(0, 0, lists=[])
		self.radius = 5
		self.maxNumOfParticles = Emitter.maxNumOfParticles

		self.particles = []
		
		self.color = color

		Emitter.allEmitters.append(self)

	def Draw(self):
		pg.gfxdraw.aacircle(screen, self.pos.x, self.pos.y, self.radius, self.color)

	def RemoveFromSelf(self, particle):
		if particle in self.particles:
			self.particles.remove(particle)

	def CreateParticle(self, attempts=1):
		for i in range(attempts):
			if len(self.particles) <= self.maxNumOfParticles and len(self.particleType.allParticles) <= self.particleType.maxNumOfParticles:
				self.particles.append(self.particleType(randint(self.pos.x, self.pos.x + self.w), randint(self.pos.y, self.pos.y + self.h), func=self.RemoveFromSelf))

	def Update(self):
		self.CreateParticle(1)



def DrawLoop():
	screen.fill(black)

	# for emitter in Emitter.allEmitters:
		# emitter.Draw()

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
		particle.ApplyForce(type(particle).gravity)
		particle.ApplyForce(type(particle).wind)

	for particle in Particle.allParticles:
		particle.Update()
		
		if type(particle) != Smoke:
			particle.Edges(x=False)


fpsLbl = Label((0, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False})
numOfParticlesLbl = Label((30, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False})

# Emitter(width // 4, height // 2)
# Emitter(width // 4, height - 10, Smoke)
Emitter(width // 2 - 25, height - 40, Smoke, 50, 10)
Emitter(width // 2 - 25, height - 40, Smoke2, 50, 10)
# Emitter(width // 2, height - 10, Fire)
# Emitter(width // 4 + width // 2, height - 10, Smoke)
# Emitter(width // 4 + width // 2, height // 2)
# Emitter(0, 0, color=lightBlue, w=width, h=10)

while running:
	clock.tick_busy_loop(fps)

	fpsLbl.UpdateText(f"{round(clock.get_fps())}")
	numOfParticlesLbl.UpdateText(f"{len(Particle.allParticles)}")

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()


# using images ~ 900 total @60fps
# without ~ 2000 total @60fps

pg.quit()