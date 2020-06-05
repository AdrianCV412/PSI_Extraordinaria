from django.db import models
from django.contrib.auth.models import User
from enum import IntEnum
from django.core.exceptions import ValidationError
from datetime import datetime

# datamodel models are created here.
# https://docs.djangoproject.com/es/2.1/ref/models/fields/#model-field-types

class GameStatus(IntEnum):
    CREATED = 1
    ACTIVE = 2
    FINISHED = 3

def validate_in_board(value):
    non_valid_pos = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
    if (value < 0):
        raise ValidationError(('Out of bounds.'))
    if (value > 63):
        raise ValidationError(('Out of bounds.'))
    if (value in non_valid_pos):
        raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

class Game(models.Model):

    cat_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'games_as_cat')
    mouse_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'games_as_mouse', null = True, blank = True)
    cat1 = models.IntegerField(default = 0, validators = [validate_in_board])
    cat2 = models.IntegerField(default = 2, validators = [validate_in_board])
    cat3 = models.IntegerField(default = 4, validators = [validate_in_board])
    cat4 = models.IntegerField(default = 6, validators = [validate_in_board])
    mouse = models.IntegerField(default = 59, validators = [validate_in_board])
    cat_turn = models.BooleanField(default=True)
    status = models.IntegerField(default = GameStatus.CREATED)
    winner = models.IntegerField(default = None, null = True, blank = True)
    MIN_CELL = 0
    MAX_CELL = 63

    def save(self, *args, **kwargs):
        non_valid_pos = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
        mouse_win_pos = [0,2,4,6]
        cat_pos_and_inv = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62,self.cat1,self.cat2,self.cat3,self.cat4]

        if self.mouse_user and self.status == GameStatus.CREATED:
            self.status = GameStatus.ACTIVE

        if self.cat1 < 0 or self.cat1 > 63:
            raise ValidationError("Invalid cell for a cat or the mouse")

        elif self.cat2 < 0 or self.cat2 > 63:
            raise ValidationError("Invalid cell for a cat or the mouse")

        elif self.cat3 < 0 or self.cat3 > 63:
            raise ValidationError("Invalid cell for a cat or the mouse")

        elif self.cat4 < 0 or self.cat4 > 63:
            raise ValidationError("Invalid cell for a cat or the mouse")

        elif self.mouse < 0 or self.mouse > 63:
            raise ValidationError("Invalid cell for a cat or the mouse")

        elif self.cat1 in non_valid_pos or self.cat2 in non_valid_pos or self.cat3 in non_valid_pos or self.cat4 in non_valid_pos or self.mouse in non_valid_pos:
            raise ValidationError("Invalid cell for a cat or the mouse")

        else:

            if self.mouse in mouse_win_pos:
                self.status = GameStatus.FINISHED
                self.winner = 0

            elif (self.mouse - 7) in cat_pos_and_inv or (self.mouse - 7) < 0 or (self.mouse - 7) > 63:
                if (self.mouse - 9) in cat_pos_and_inv or (self.mouse - 9) < 0 or (self.mouse - 9) > 63:
                    if (self.mouse + 7) in cat_pos_and_inv or (self.mouse + 7) < 0 or (self.mouse + 7) > 63:
                        if (self.mouse + 9) in cat_pos_and_inv or (self.mouse + 9) < 0 or (self.mouse + 9) > 63:
                            self.status = GameStatus.FINISHED
                            self.winner = 1


        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        if self.status == GameStatus.ACTIVE:
            s = 'Active'
        elif self.status == GameStatus.CREATED:
            s = 'Created'
        elif self.status == GameStatus.FINISHED:
            s = 'Finished'
        else:
            s = 'Error'

        if self.cat_turn == True:
            c = 'X'
            m = ' '
        else:
            c = ' '
            m = 'X'
        if(self.mouse_user is None):
            return '('+ str(self.id) +", "+s+")\tCat ["+c+"] cat_user_test("+str(self.cat1)+", "+str(self.cat2)+", "+str(self.cat3)+", "+str(self.cat4)+")"
        else:
            return '('+ str(self.id) +", "+s+")\tCat ["+c+"] cat_user_test("+str(self.cat1)+", "+str(self.cat2)+", "+str(self.cat3)+", "+str(self.cat4)+") --- Mouse ["+m+"] mouse_user_test("+str(self.mouse)+")"


class Move(models.Model):

    origin = models.IntegerField()
    target = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name = 'moves')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default = datetime.today().strftime('%Y-%m-%d'))

    def setGame(self, g):
        self.game = g

    def setOrigin(self, o):
        self.origin = o

    def setTarget(self, t):
        self.target = t

    def setPlayer(self, p):
        self.player = p

    def save(self, *args, **kwargs):
        non_valid_pos = [1,3,5,7,8,10,12,14,17,19,21,23,24,26,28,30,33,35,37,39,40,42,44,46,49,51,53,55,56,58,60,62]
        if self.game.status == GameStatus.CREATED or self.game.status == GameStatus.FINISHED:
            raise ValidationError(("Move not allowed"))
        elif self.player != self.game.cat_user and self.player != self.game.mouse_user:
            raise ValidationError(("Move not allowed"))

        if self.target == self.game.cat1 or self.target == self.game.cat2 or self.target == self.game.cat3 or self.target == self.game.cat4 or self.target == self.game.mouse:
            raise ValidationError(("Move not allowed"))

        if self.game.cat_turn == True:
            if self.game.cat1 == self.origin:
                if self.target in non_valid_pos or self.target < 0 or self.target > 63:
                    raise ValidationError(("Move not allowed"))
                elif self.target == self.game.cat1 + 7 or self.target == self.game.cat1 + 9:
                    self.game.cat1 = self.target
                    self.game.cat_turn = False
                else:
                    raise ValidationError(("Move not allowed"))
            elif self.game.cat2 == self.origin:
                if self.target in non_valid_pos or self.target < 0 or self.target > 63:
                    raise ValidationError(("Move not allowed"))
                elif self.target == self.game.cat2 + 7 or self.target == self.game.cat2 + 9:
                    self.game.cat2 = self.target
                    self.game.cat_turn = False
                else:
                    raise ValidationError(("Move not allowed"))
            elif self.game.cat3 == self.origin:
                if self.target in non_valid_pos or self.target < 0 or self.target > 63:
                    raise ValidationError(("Move not allowed"))
                elif self.target == self.game.cat3 + 7 or self.target == self.game.cat3 + 9:
                    self.game.cat3 = self.target
                    self.game.cat_turn = False
                else:
                    raise ValidationError(("Move not allowed"))
            elif self.game.cat4 == self.origin:
                if self.target in non_valid_pos or self.target < 0 or self.target > 63:
                    raise ValidationError(("Move not allowed"))
                elif self.target == self.game.cat4 + 7 or self.target == self.game.cat4 + 9:
                    self.game.cat4 = self.target
                    self.game.cat_turn = False
                else:
                    raise ValidationError(("Move not allowed"))
            else:
                raise ValidationError(("Move not allowed"))

        else:
            if self.game.mouse == self.origin:
                if self.target in non_valid_pos or self.target < 0 or self.target > 63:
                    raise ValidationError(("Move not allowed"))
                elif self.target == self.game.mouse + 7 or self.target == self.game.mouse + 9 or self.target == self.game.mouse - 7 or self.target == self.game.mouse - 9:
                    self.game.mouse = self.target
                    self.game.cat_turn = True
                else:
                    raise ValidationError(("Move not allowed"))
            else:
                raise ValidationError(("Move not allowed"))

        self.game.save()
        super().save(*args, **kwargs)

class counter_manager(models.Manager):

		def inc(self):

			c = Counter.objects.filter(id = 0).count()

			if c == 0:
				c_obj = Counter(id=0)
				c_obj.value += 1

			else:
				c_obj = Counter.objects.get(id = 0)
				c_obj.value += 1

			super(Counter, c_obj).save()
			return c_obj.value

		def get_current_value(self):
			c = Counter.objects.filter(id = 0).count()
			if c == 0:
				c_obj = Counter(id=0)
			else:
				c_obj = Counter.objects.get(id = 0)
			super(Counter, c_obj).save()
			return c_obj.value

class Counter(models.Model):

	value = models.IntegerField(default = 0)
	objects = counter_manager()

	def save(self, *args, **kwargs):
		raise  ValidationError("Insert not allowed|Inseción no permitida")
