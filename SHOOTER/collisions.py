def check_bullet_collisions(bullets, bulletgridcoords,bulletpixelcoords, zombielist):
# iterates through every zombie to check if the current bullet has the 
# same coordinates the current zombie (in relation to the 15 x 15 grid)
# if the bullet and zombie have the same coordinates, remove both

	for zombie in zombielist:
					if bulletgridcoords == zombie.coordinates:
						bullets.remove(bulletpixelcoords)
						zombielist.remove(zombie)
						break

# checks if any zombie has the same coordinates (in relation to the 15 x 15 grid)
# as the player
# if a zombie and player share the same coordinate, return gameover as True

def zombie_player_collision(zombielist, player):
	for zombie in zombielist:
			if zombie.coordinates == player.coordinates:
				return True
