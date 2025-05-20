import os
import random
import sys
import time
import pygame as pg


WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    画面下では跳ね返らない
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0:
        tate = False
    return yoko, tate


class Bord(pg.sprite.Sprite):
    """
    ゲームキャラクター（操作バー）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def __init__(self):
        """
        操作バーSurfaceを生成する
        引数 xy：操作バーの初期位置座標タプル
        """
        super().__init__()
        self.image = pg.Surface((80, 20))
        pg.draw.rect(self.image, (0, 0, 0), (0, 0, 80, 20))
        self.rect = self.image.get_rect()
        self.dire = (+1, 0)
        self.rect.center = (WIDTH/2, HEIGHT-30)
        self.speed = 20


    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じて操作バーを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(sum_mv)
        if check_bound(self.rect) != (True, True):
            self.rect.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(self.image, self.rect)


class Bird(pg.sprite.Sprite):
    """
    こうかとんに関するクラス
    """
    def __init__(self):
        """
        こうかとんSurfaceを生成する
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/ball.png"), 0, 0.9)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-60)
        self.vx, self.vy = +5, +5

    def update(self):
        """
        こうかとんを速度ベクトルself.vx, self.vyに基づき移動させる
        """
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rect.move_ip(self.vx, self.vy)


# class Score:
#     """
#     スコアについてのクラス
#     """
#     def __init__(self):
#         self.fonto = pg.font.SysFont("hgp創英角ポップ体", 30)
#         self.color = (0, 0, 255)
#         self.score = 0
#         self.image = self.fonto.render(str(self.score), 0, self.color)
#         self.rect = self.image.get_rect()
#         self.rect.center = (100, HEIGHT-50)       
#     def update(self):
#         """
#         現在のスコアを描画するメソッド
#         """
#         self.image = self.fonto.render(str(self.score), 0, self.color)

# class Explosin(pg.sprite.Sprite):
#     """
#     爆発エフェクトの為のクラス
#     """
#     def __init__(self, obj:"Bird", life: int):
#         super().__init__()
#         img = pg.image.load(f"fig/explosion.gif")
#         self.imgs = [img, pg.transform.flip(img, 1, 1)]
#         self.image = self.imgs[0]
#         self.rect = self.image.get_rect(center=obj.rect.center)
#         self.life = life

#     def update(self):
#         """
#         爆発経過時間のメソッド
#         """
#         self.life -= 1
#         self.image = self.imgs[self.life // 10 % 2]
#         if self.life < 0:
#             self.kill()

#他の人用の未完成機能



def main():
    pg.display.set_caption("壁にレッツゴーこうかとん！")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bord = Bord()
    birds = pg.sprite.Group()
    birds.add(Bird())
    clock = pg.time.Clock()
    tmr = 0
    # score = Score()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        for bird in pg.sprite.spritecollide(bord, birds, False):#バーとbirdが衝突したとき
            bird.vy *= -1 #上に跳ね返す
        key_lst = pg.key.get_pressed()
        bord.update(key_lst, screen)
        birds.update()
        birds.draw(screen)
        # score.update()
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
