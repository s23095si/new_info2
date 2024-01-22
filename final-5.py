import pyxel
from random import randint

class Player:
    def __init__(self):
        self.x = 20
        self.y = 60
        self.gravity = 2.5
        self.MAX_GRAVITY = self.gravity
        self.POWER = 0.25

    def update(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.gravity > -self.MAX_GRAVITY:
                self.gravity = self.gravity - self.POWER
        else:
            if self.gravity < self.MAX_GRAVITY:
                self.gravity = self.gravity + self.POWER

        self.y = self.y + self.gravity

        if 0 > self.y:
            self.y = 0

        if self.y > pyxel.height - 16:
            self.y = pyxel.height - 16

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x -= 2

        if self.x < -40:
            self.x += 240
            self.y = randint(0, 104)

class Point:
    def __init__(self, x, y, image_index):
        self.x = x
        self.y = y
        self.image_index = image_index

    def update(self):
        self.x -= 2
        if self.x < -40:
            self.x += 240
            self.y = randint(0, 104)

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("final.pyxres")
        pyxel.playm(0, loop=True)

        self.START = False
        self.GAMEOVER = False
        self.score = 0

        self.player = Player()
        self.bombs = [Bomb(i * 60, randint(0, 104)) for i in range(3, 15)]
        self.points = [Point(i * 60, randint(0, 104), 1) for i in range(3, 15)]
        self.alt_point_image = 2

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_SPACE):
            self.START = True

        if self.GAMEOVER and (pyxel.btn(pyxel.KEY_LEFT)):
            self.reset()

        if not self.START or self.GAMEOVER:
            return

        self.player.update()

        for bomb in self.bombs:
            bomb.update()

        for point in self.points:
            point.update()

        self.check_collisions()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 1, 0, 0, 160, 120, 0)

        if self.GAMEOVER:
            pyxel.text(67, 54, 'score:' + str(self.score), 2)

            MESSAGE = \
"""
    GAMEOVER


PUSH LEFT RESTART
"""
            pyxel.text(51, 40, MESSAGE, 2)
            pyxel.text(50, 40, MESSAGE, 7)
            return

        if not self.GAMEOVER:
            pyxel.blt(self.player.x, self.player.y, 0, 0, 0, 16, 32, 0)

        for bomb in self.bombs:
            pyxel.blt(bomb.x, bomb.y, 0, 48, 0, 16, 16, 3)

        for point in self.points:
            pyxel.blt(point.x, point.y, 0, point.image_index * 16, 0, 16, 16, 0)

        s = "SCORE {:>4}".format(self.score)
        pyxel.text(5, 4, s, 2)
        pyxel.text(4, 4, s, 7)

        if not self.START:
            MESSAGE = "PUSH SPACE KEY"
            pyxel.text(61, 50, MESSAGE, 2)
            pyxel.text(60, 50, MESSAGE, 7)
            return

    def check_collisions(self):
        for point in self.points:
            if (
                self.player.x + 16 > point.x
                and self.player.x < point.x + 16
                and self.player.y + 32 > point.y
                and self.player.y < point.y + 16
            ):
                point.x = 1000
                if point.image_index == self.alt_point_image:
                # 新しい画像になったポイントをゲットしたときは通常よりも多くのスコア
                    self.score += 8
                    pyxel.play(3,6, loop=False)
                else:
                    self.score += 1
                    pyxel.play(2, 5, loop=False)

        

                if self.score >= 1 and point.image_index != self.alt_point_image:
                    new_x = (len(self.points) - 1) * 60
                    new_y = randint(0, 104)
                    point.x, point.y, point.image_index = new_x, new_y, self.alt_point_image

                


        for bomb in self.bombs:
            if (
                self.player.x + 10 > bomb.x
                and self.player.x < bomb.x + 10
                and self.player.y + 10 > bomb.y
                and self.player.y < bomb.y + 10
            ):
                self.GAMEOVER = True
                pyxel.playm(1, loop=False)

    def reset(self):
        self.START = True
        self.GAMEOVER = False
        self.score = 0

        self.player = Player()
        self.bombs = [Bomb(i * 60, randint(0, 104)) for i in range(3, 15)]
        self.points = [Point(i * 60, randint(0, 104), 1) for i in range(3, 15)]

        pyxel.playm(0, loop=True)

App()
