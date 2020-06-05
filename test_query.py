import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ratonGato.settings')
django.setup()
from datamodel.models import *
from django.contrib.auth.models import User

def test_query():
	
	#Creating or getting the users with id 10 and id 11
	user10 = User.objects.get_or_create(id = 10, username = "test_user_1")[0]
	user10.save
	user11 = User.objects.get_or_create(id = 11, username = "test_user_2")[0]
	user11.save
	
	print("Users with id "+ str(user10.id) + "and id " + str(user11.id) + "have been created successfuly")

	#Creating the game to perform the query on
	Game.objects.filter(id = 1).delete()
	game = Game.objects.get_or_create(id = 1, cat_user = user10)[0]

	#Game variable to store the lowest id game for the next step of this query program
	game_t = None

	print("Result of searching for games with only one user assigned: ")
	for g in Game.objects.all():
		if (g.mouse_user is None and g.cat_user is not None):
			if(game_t is None or game_t.id > g.id):
				game_t = g;
			print (g)
		if (g.mouse_user is not None and g.cat_user is None):
			if(game_t is None or game_t.id > g.id):
				game_t = g;
			print (g)
	
	print("Game with the lowest id from last query (games with only one user): ")
	
	print(game_t)

	if (game_t.mouse_user is None and game_t.cat_user is not None):
		game_t.mouse_user = user11
	if (game_t.mouse_user is not None and game_t.cat_user is None):
		game_t.cat_user = user11

	print("Updated game with user with id 11 assigned to it: ")
	
	print(game_t)
	
	game_t.cat2 = 11

	print("Updated game by moving cat 2 to position 11: ")
	
	print(game_t)

	game_t.mouse = 52

	print("Updated game by moving the mouse to position 52: ")
	
	print(game_t)
	
test_query()
