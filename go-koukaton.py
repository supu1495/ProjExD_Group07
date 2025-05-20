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
    引数：こうかとんや爆弾，ビームなどのRect
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


class Bomb(pg.sprite.Sprite):
    """
    爆弾に関するクラス
    """
    def __init__(self):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("fig/ball.png"), 0, 0.9)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-60)
        self.vx, self.vy = +5, +5

    def update(self):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rect.move_ip(self.vx, self.vy)

class Score:
    """
    スコアについてのクラス
    """
    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ポップ体", 30)
        self.color = (0, 0, 255)
        self.score = 0
        self.image = self.fonto.render(str(self.score), 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT-50)       
    def update(self):
        """
        現在のスコアを描画するメソッド
        """
        self.image = self.fonto.render(str(self.score), 0, self.color)

class Explosin(pg.sprite.Sprite):
    """
    爆発エフェクトの為のクラス
    """
    def __init__(self, obj:"Bomb", life: int):
        super().__init__()
        img = pg.image.load(f"fig/explosion.gif")
        self.imgs = [img, pg.transform.flip(img, 1, 1)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def update(self):
        """
        爆発経過時間のメソッド
        """
        self.life -= 1
        self.image = self.imgs[self.life // 10 % 2]
        if self.life < 0:
            self.kill()

class clear:
    """
    ブロックを全て壊した時のエフェクト
    """
    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ポップ体", 30)
        self.color = (0, 0, 255)
        self.cle = ("ブロック崩しクリアめでとう!")
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
    bombs = pg.sprite.Group()
    bombs.add(Bomb())
    clock = pg.time.Clock()
    tmr = 0
    score = Score()
    cle = clear()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
<<<<<<< HEAD
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # スペースキー押下でBeamクラスのインスタンス生成
                beam = Beam(bird)          
                beams.append(beam) #ビームをリストに追加  
        screen.blit(bg_img, [0, 0])
        
        #if bomb is not None:
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                bird.change_img(8, screen)
            if ブロックが無くなったら:
                cle.update(screen)
                pg.display.update()
                time.sleep(1)
                return
      
            for j, bomb in enumerate(bombs):
                for k, beam in enumerate(beams):
                    if beam is not None:
                    #if bomb is not None:
                        if check_bound(beam.rct) != (True, True):
                            beams[k] = None
                        if beam.rct.colliderect(bomb.rct): #ビームと爆弾の衝突判定
                            beams[k] = None #ビームを消す
                            bombs[j] = None #爆弾を消す
                            bird.change_img(6, screen)
                            score.score += 1
                beams = [beam for beam in beams if beam is not None]
                bombs = [bomb for bomb in bombs if bomb is not None]
=======
>>>>>>> f06f8a2ef0abb98625c8b0a459c44423f969c119

        screen.blit(bg_img, [0, 0])
        for bomb in pg.sprite.spritecollide(bord, bombs, False):#バーとbombが衝突したとき
            bomb.vy *= -1 #上に跳ね返す
        key_lst = pg.key.get_pressed()
        bord.update(key_lst, screen)
        bombs.update()
        bombs.draw(screen)
        score.update()
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
