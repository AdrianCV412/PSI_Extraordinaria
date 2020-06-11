from django.core.exceptions import ValidationError

from datamodel import tests
from datamodel.models import Game, GameStatus, Move
from django.contrib.auth.models import User
from django.test import Client

class BotMoveTests(tests.BaseModelTest):

    def setUp(self):
        user_c = User.objects.create_user(username='cat_user_test', password='cat_user_test')
        user_m = User.objects.create_user(username='Bot', password='0i80t81d16s810')
        self.client = Client()
        self.game_bot = Game.objects.create(
            cat_user=user_c, mouse_user=user_m, status=GameStatus.ACTIVE)
        self.client.post('/login/', {'username': 'cat_user_test', 'password': 'cat_user_test'})

    # Testing upward movement (after movement of cat the "Bot" user will move upwards to either position 50 or 52)
    def test1(self):

        correct_pos = [50, 52]
        session = self.client.session
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing downward movement (after movement of cat the "Bot" user will move downwards to either position 34 or 36)
    def test2(self):

        correct_pos = [34, 36]
        session = self.client.session
        self.game_bot.cat2 = 18
        self.game_bot.cat3 = 20
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing down left movement (after movement of cat the "Bot" user will move downwards to position 34)
    def test3(self):

        correct_pos = [34]
        session = self.client.session
        self.game_bot.cat2 = 18
        self.game_bot.cat3 = 20
        self.game_bot.cat4 = 36
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing down right movement (after movement of cat the "Bot" user will move downwards to position 36)
    def test4(self):

        correct_pos = [36]
        session = self.client.session
        self.game_bot.cat2 = 18
        self.game_bot.cat3 = 20
        self.game_bot.cat4 = 34
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing up right movement (after movement of cat the "Bot" user will move upwards to position 20)
    def test5(self):

        correct_pos = [20]
        session = self.client.session
        self.game_bot.cat2 = 18
        self.game_bot.cat3 = 34
        self.game_bot.cat4 = 36
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing up left movement (after movement of cat the "Bot" user will move upwards to position 18)
    def test6(self):

        correct_pos = [18]
        session = self.client.session
        self.game_bot.cat2 = 20
        self.game_bot.cat3 = 34
        self.game_bot.cat4 = 36
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing movement when mouse has all surrounding spaces empty (in that case it should move forward to position 18
    # or 20)
    def test7(self):

        correct_pos = [18, 20]
        session = self.client.session
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 0, 'target': 9})
        self.assertTrue(Game.objects.get(id=session['game_selected']).mouse in correct_pos)

    # Testing scenario in which a real user movement ends the game, therefore making the mouse not move and setting the
    # game status to finished.
    def test8(self):

        correct_pos = [27]
        session = self.client.session
        self.game_bot.cat1 = 9
        self.game_bot.cat2 = 20
        self.game_bot.cat3 = 34
        self.game_bot.cat4 = 36
        self.game_bot.mouse = 27
        self.game_bot.save()
        session['game_selected'] = self.game_bot.id
        session.save()
        response = self.client.post('/move/', {'origin': 9, 'target': 18})
        self.assertTrue(Game.objects.get(id=session['game_selected']).status == GameStatus.FINISHED and
                        (Game.objects.get(id=session['game_selected']).mouse in correct_pos))

