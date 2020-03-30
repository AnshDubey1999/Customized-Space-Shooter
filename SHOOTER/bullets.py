def bullets_remove(bullets):
	# checks if bullets have crossed the display. If a bullet has passed the
	# current game window, remove it

	#returns an empty list if the bullet list is empty
	if len(bullets) == 0:
		return []

	else:
		index = 0
		while True:
			if len(bullets) == 0:
				break
			# checks if bullet's x or y coordinates (in relation to pixels) have crossed
			#  the game window
			if bullets[index][0] < 0 or bullets[index][0]> 900 or bullets[index][1]<0 or bullets[index][1] > 900:
				bullets.remove(bullets[index])
			else:
				index += 1

			#breaks once all bullets within list has been checked
			if index == len(bullets):
				break
		# returns empty list if all bullets have been removed
		if len(bullets) == 0:
			return []

		# returns the new list of bullets
		else:
			return bullets