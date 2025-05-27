import os
import sys

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
    if obj_rct.top < 0: #画面下は飛び出る
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
        # 画像を用意
        self.image = pg.Surface((80, 20)) # 操作バーを作成
        pg.draw.rect(self.image, (0, 0, 0), (0, 0, 80, 20))
        self.rect = self.image.get_rect()
        self.dire = (+1, 0)
        self.rect.center = (WIDTH / 2, HEIGHT - 30) # 中央下に配置
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



# 個々のブロッククラス
class Block(pg.sprite.Sprite):
    """
    ブロックを表すクラス
    """

    def __init__(self, x, y, color=(255, 0, 0)):
        super().__init__()
        self.image = pg.Surface((80, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)


# ブロックのグループを管理するクラス
class BlockGroup(pg.sprite.Group):
    """
    複数のブロックを管理するクラス
    """

    def __init__(self):
        super().__init__()
        # インスタンス化したらブロックを生成
        self.create_blocks()

    def create_blocks(self):
        """
        ブロックを生成する
        """
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        for y in range(6):  # 5行
            for x in range(13):
                color = colors[y % len(colors)]
                block = Block(x * 85, y * 35 + 50, color)
                self.add(block)

    def update(self, screen: pg.Surface):
        """
        全てのブロックを更新する
        """
        for block in self.sprites():
            block.update(screen)

    def check_collision(self, _ball):
        """
        ボールとブロックの衝突を検出する
        """
        collision_list = pg.sprite.spritecollide(_ball, self, True)
        if collision_list:
            # 衝突したブロックを削除 と ボールのはね返し処理
            return True
        return False

class Ball(pg.sprite.Sprite):
    """
    こうかとんボールに関するクラス
    """
    def __init__(self):
        """
        こうかとんSurfaceを生成する
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/ball.png"), 0, 0.9) #画像呼び出し
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-60) #バー上を初期位置に
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

class Clear:
    """
    ブロックを全て壊した時のエフェクト
    """

    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ポップ体", 30)
        self.color = (0, 0, 255)
        self.cle = "ブロック崩しクリアめでとう!"
        self.image = pg.Surface((WIDTH, HEIGHT))
        pg.draw.rect(self.image, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.image.set_alpha(128)

    def update(self, screen: pg.Surface):
        self.img = self.fonto.render(str(self.cle), 0, self.color)
        screen.blit(self.img, self.rct)


def main():
    pg.display.set_caption("壁にレッツゴーこうかとん！")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    bord = Bord()
    blocks = BlockGroup()
    balls = pg.sprite.Group()
    balls.add(Ball())
    clear = Clear()
    clock = pg.time.Clock()
    tmr = 0
    is_gameover = False
    is_clear = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 背景の描画
        screen.blit(bg_img, (0, 0))

        for bird in pg.sprite.spritecollide(bord, balls, False): # バーとbirdが衝突したとき
            bird.vy *= -1 #上に跳ね返す

        # ボールとブロックが衝突したとき
        for ball in balls:
            if blocks.check_collision(ball):
                ball.vy *= -1

        if not is_gameover and not is_clear:
            # ブロックの更新と当たり判定
            blocks.update(screen)
            # if blocks.check_collision():
            #     score.update(screen, 10)
            # else:
            #     score.update(screen)

            # ブロックが全て消えたらクリア
            if len(blocks) == 0:
                is_clear = True

        # ゲームオーバー時の処理
        if is_gameover:
            game_over_font = pg.font.SysFont("hgp創英角ポップ体", 50)
            game_over_text = game_over_font.render("ゲームオーバー", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

        key_lst = pg.key.get_pressed()
        bord.update(key_lst, screen)
        balls.update()
        balls.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
