import graph
import characters
import path_finding
import bullets
import collisions
import pygame, sys
from pygame.locals import *

if __name__ == "__main__":
	# initialize necessary pygame elements to run the game
	pygame.init()
	pygame.font.init()
	clock = pygame.time.Clock()
	pygame.mouse.set_visible(0)
	screen = pygame.display.set_mode((900,900))

	# load the jpg of the triangle used to represent the player
	triangle = pygame.image.load("images/triangle.jpg")

	# retrieve the coordinates of the left of the player triangle
	triangle_left = (screen.get_width()/2) - (triangle.get_width()/2)

	# retrieve the coordinates of the top of the player triangle
	triangle_top = (screen.get_height()/2) - (triangle.get_height()/2)

	# initialize bullet lists of all 4 directions
	bullets1 = []
	bullets2 = []
	bullets3 = []
	bullets4 = []

	# variable that keeps track of current player direction
	position = "UP"
	c_centre_x = 450
	c_centre_y = 450

	# initialize colours used within the game
	white = (255,255,255)
	black = (0,0,0)
	red = (255, 0, 0)

	text = pygame.font.SysFont("Comic Sans MS", 60)
	textsurface = text.render("GAME OVER", False, white)
	gameover = False

	# initialize graph that that the characters and bullets use
	# to keep track of their coordinates
	vset, elist = graph.create_grid()
	graph = graph.Graph(vset, elist)

	# initialize the player class that will keep track of the player's
	# coordinates
	player = characters.Player((7,7))
	playerXCoord = 7
	playerYCoord = 7

	#initialize zombie list
	zombielist = []

	while not gameover:
		# game runs at 30 ticks per second
		clock.tick(30)
		screen.fill(black)

		#draw triangle onto screen
		screen.blit(triangle,(triangle_left,triangle_top))

		# if there are no more zombies that exist in the game, respawn the 4 zombies
		# with random coordinates. (zombies will only spawn on the outer 2 rings of
		# of the 15 x 15 grid)
		if not zombielist:
			print("zombie list empty")

			# initialize the zombies into the corners of the grid
			# then randomize their coordinates
			zombie1 = characters.Zombie((0,7))
			zombie2 = characters.Zombie((14,0))
			zombie3 = characters.Zombie((0,14))
			zombie4 = characters.Zombie((14,14))
			zombielist = [zombie1, zombie2, zombie3, zombie4]
			zombielist = characters.spawnzombies(zombielist, player.coordinates, graph)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			# check if a key has been pressed
			elif event.type == pygame.KEYDOWN:
				# conditional to check it the up arrow key has been pressed
				if event.key == pygame.K_UP:

					# if the player is not facing up, rotate player
					# to face up
					if position != "UP":
						if position == "DOWN":
							triangle = pygame.transform.rotate(triangle,180)
						elif position == "RIGHT":
							triangle_left -= 45
							triangle_top += 45
							triangle = pygame.transform.rotate(triangle,90)
						elif position == "LEFT":
							triangle_left -= 45
							triangle_top += 45
							triangle = pygame.transform.rotate(triangle,270)

					# move player up 1 unit if player if already facing up
					else:
						triangle_top -= 60
						playerYCoord -= 1

						#constrain player within window
						if playerYCoord < 3:
							playerYCoord = 3
							triangle_top += 60

						# recalculate the new path zombie must take to
						# reach player
						player.coordinates = (playerXCoord, playerYCoord)
						characters.recalculate_zombie_path(zombielist, player, graph)
					position = "UP"

				# check if the down arrow key has been pressed
				elif event.key == pygame.K_DOWN:

					# if player is not already facing down, rotate player
					# to face down
					if position != "DOWN":
						if position == "UP": 
							triangle = pygame.transform.rotate(triangle,180)
						elif position == "LEFT":
							triangle_left -= 45
							triangle_top += 45
							triangle = pygame.transform.rotate(triangle,90)
						elif position == "RIGHT":
							triangle_left -= 45
							triangle_top += 45
							triangle = pygame.transform.rotate(triangle,270)

					# if player is already facing down, move player down 1 unit
					else:
						triangle_top += 60
						playerYCoord += 1

						# constrain player to stay within screen 
						if playerYCoord > 11:
							playerYCoord = 11
							triangle_top -= 60

						# recalculate zombie's path to player
						player.coordinates = (playerXCoord, playerYCoord)
						characters.recalculate_zombie_path(zombielist, player, graph)
					position = "DOWN"

				# check if the left arrow key has been pressed
				elif event.key == pygame.K_LEFT:

					# if player is not already facing left, rotate player
					# to face left
					if position != "LEFT":
						if position == "UP":
							triangle_left +=45
							triangle_top -= 45
							triangle = pygame.transform.rotate(triangle,90)
						elif position == "DOWN":
							triangle_left += 45
							triangle_top -= 45
							triangle = pygame.transform.rotate(triangle,270)
						elif position == "RIGHT":
							triangle = pygame.transform.rotate(triangle,180)

					# if player is already facing left, move player left 1 unit
					else:
						triangle_left -= 60
						playerXCoord -= 1

						# constrain player within window
						if playerXCoord < 3:
							playerXCoord = 3
							triangle_left += 60

						# recalculate zombie's path to player
						player.coordinates = (playerXCoord, playerYCoord)
						characters.recalculate_zombie_path(zombielist, player, graph)					
					position = "LEFT"

				# check if the left arrow key has been pressed
				elif event.key == pygame.K_RIGHT:
					if position != "RIGHT":
						if position == "UP":
							triangle_left += 45
							triangle_top -= 45
							triangle = pygame.transform.rotate(triangle,270)
						elif position == "DOWN":
							triangle_left += 45
							triangle_top -= 45
							triangle = pygame.transform.rotate(triangle,90)
						elif position == "LEFT":
							triangle = pygame.transform.rotate(triangle,180)

					# if player is already facing right, move player right 1 unit
					else:
						triangle_left += 60
						playerXCoord += 1

						# constrain player to stay within screen 
						if playerXCoord > 11:
							playerXCoord = 11
							triangle_left -= 60

						# recalculate zombie's path to player
						player.coordinates = (playerXCoord, playerYCoord)
						characters.recalculate_zombie_path(zombielist, player, graph)					
					position = "RIGHT"

				# if the space bar has been pressed, append a bullet to bulletlist that
				# corresponds to the direction faced.
				# bullet must also be appended with coordinates of front tip of the triangle
				if event.key == K_SPACE:
					if position == "UP":
						c_centre_x = int(triangle_left) + 105
						c_centre_y = int(triangle_top) + 20
						bullets1.append([c_centre_x,c_centre_y])
					elif position == "DOWN":
						c_centre_x = int(triangle_left) + 105
						c_centre_y = int(triangle_top) + 100
						bullets2.append([c_centre_x,c_centre_y])
					elif position == "LEFT":
						c_centre_x = int(triangle_left) + 20
						c_centre_y = int(triangle_top) + 105
						bullets3.append([c_centre_x,c_centre_y])
					elif position == "RIGHT":
						c_centre_x = int(triangle_left) + 100
						c_centre_y = int(triangle_top) + 105
						bullets4.append([c_centre_x,c_centre_y])

		# check to see if bullets have passed the game window.
		# if so remove them from the bullet list
		bullets1 = bullets.bullets_remove(bullets1)
		bullets2 = bullets.bullets_remove(bullets2)
		bullets3 = bullets.bullets_remove(bullets3)
		bullets4 = bullets.bullets_remove(bullets4)

		# calculate the bullet coordinates in relation to the 15 x 15 grid
		# then check if the bullet has collided with zombie.
		# if bullet has collided with zombie, remove both zombie and bullet
		# (done to bullets of all 4 directions)
		if bullets1 != []:
			for coords in bullets1:
				coords[1] -= 12
				xgridcoord = coords[0] // 60
				ygridcoord = coords[1] // 60
				bulletgridcoords = (xgridcoord, ygridcoord)
				collisions.check_bullet_collisions(bullets1,bulletgridcoords,coords, zombielist)


		if bullets2 != []:
			for coords in bullets2:
				coords[1] += 12
				xgridcoord = coords[0] // 60
				ygridcoord = coords[1] // 60
				bulletgridcoords = (xgridcoord, ygridcoord)
				collisions.check_bullet_collisions(bullets2,bulletgridcoords,coords, zombielist)
		if bullets3 != []:
			for coords in bullets3:
				coords[0] -= 12
				xgridcoord = coords[0] // 60
				ygridcoord = coords[1] // 60
				bulletgridcoords = (xgridcoord, ygridcoord)
				collisions.check_bullet_collisions(bullets3, bulletgridcoords,coords, zombielist)

		if bullets4 != []:
			for coords in bullets4:
				coords[0] += 12
				xgridcoord = coords[0] // 60
				ygridcoord = coords[1] // 60
				bulletgridcoords = (xgridcoord, ygridcoord)
				collisions.check_bullet_collisions(bullets4, bulletgridcoords,coords, zombielist)


		# draw bullets into game window
		if bullets1 != []:
			for x in bullets1:
				pygame.draw.circle(screen,white,tuple(x),8)
		if bullets2 != []:
			for x in bullets2:
				pygame.draw.circle(screen,white,tuple(x),8)
		if bullets3 != []:
			for x in bullets3:
				pygame.draw.circle(screen,white,tuple(x),8)
		if bullets4 != []:
			for x in bullets4:
				pygame.draw.circle(screen,white,tuple(x),8)

		# get the current timer of the zombies
		timer = characters.Zombie.gettimer()

		# if zombie timer has reached 30, reset the zombie timer and
		# move the zombie by 1 vertex (according to the zombie's path)
		if timer > 30:
			characters.Zombie.resettimer()
			for zombie in zombielist:
				zombie.increasepathindex()

		# if there are zombies that still exist,
		# draw them to the game screen
		if zombielist:
			for zombie in zombielist:            
				currentvertex = zombie.path[zombie.currentpathindex]
				zombie.coordinates = currentvertex
				pygame.draw.circle(screen,red, [currentvertex[0] * 60 + 30, \
		  		currentvertex[1] * 60 + 30], 30) 


		# check if zombie has collided with player. If so, return gameover as True
		gameover = collisions.zombie_player_collision(zombielist, player)
		pygame.display.update()

		# increase the zombie timer by 3 every tick
		characters.Zombie.increasetimer(3)

	# if a zombie has reached the player, display the game over text
	while gameover == True:
		clock.tick(10)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		screen.fill((0,0,0))
		screen.blit(textsurface, (350,400))
		pygame.display.update()





