from django.core.exceptions import ValidationError

from datamodel import tests
from datamodel.models import Game, GameStatus, Move

class BotMoveTests(tests.BaseModelTest):

    def setUp(self):
        super().setUp()
        self.
        self.game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

    def test1(self):
        """ Solo los jugadores pueden mover """
        no_player = self.get_or_create_user("no_player")
        moves = [
            {"origin": 0, "target": 9},
            {"origin": 59, "target": 50},
        ]

        for move in moves:
            with self.assertRaisesRegex(ValidationError, tests.MSG_ERROR_MOVE):
                Move.objects.create(
                    game=self.game, player=no_player, origin=move["origin"], target=move["target"])
            self.assertEqual(self.game.moves.count(), 0)