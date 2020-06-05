"""
@author: rlatorre
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from datamodel import tests
from datamodel.models import Game, GameStatus, Move

#Two different cases, cats win (by trapping between cat and edge of board) and mouse wins by getting to the last row

class GameEndTests(tests.BaseModelTest):
    def setUp(self):
        super().setUp()

    #Cats win
    def test1(self):

        game_t = Game(
            cat_user=self.users[0],
            mouse_user=self.users[1],
            cat1=47,
            mouse=63)

        game_t.save()


        move = Move(
            game=game_t,
            player=self.users[0],
            origin=47,
            target=54
        )

        Move.save(move)
        self.assertEqual(GameStatus.FINISHED, game_t.status)

    #Mouse wins
    def test2(self):

        game_t = Game(
            cat_user=self.users[0],
            mouse_user=self.users[1],
            cat1=11,
            mouse=9,
            cat_turn=False)

        game_t.save()

        Move.objects.create(
            game=game_t,
            player=self.users[1],
            origin=9,
            target=0
        )

        self.assertEqual(GameStatus.FINISHED, game_t.status)
