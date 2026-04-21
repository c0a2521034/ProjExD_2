import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5), #上
    pg.K_DOWN:(0,+5), #下
    pg.K_LEFT:(-5,0), #左
    pg.K_RIGHT:(+5,0) #右
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外かの判定
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向のはみ出し判定(True:はみ出していない,False:はみ出している)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko, tate


def show_game_over(screen: pg.Surface, width: int, height: int, clock: pg.time.Clock) -> None:
    """
    ゲームオーバー画面を5秒間表示
    引数：スクリーン、画面幅、画面高さ、clock
    """
    # 黒い矩形を描画するための空のSurfaceを作成
    black_surface = pg.Surface((width, height))
    black_surface.fill((0, 0, 0))  # 黒い矩形を描画
    black_surface.set_alpha(100)  # 透明度を設定
    
    # 泣いているこうかとん画像を読み込む
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.2) 
    crying_kk_rct = crying_kk_img.get_rect() #泣いているこうかとんのRectを取得
    crying_kk_rct.center = width // 2 - 200, height // 2  #泣いているこうかとんの位置を画面中央に設定
    
    # 「Game Over」テキストを作成
    font = pg.font.Font(None, 80) #フォントとサイズを指定
    game_over_text = font.render("Game Over", True, (255, 255, 255)) #白色のテキストを描画
    game_over_rct = game_over_text.get_rect() #テキストのRectを取得
    game_over_rct.center = width // 2, height // 2 #テキストの位置を画面中央に設定
    
    # 5秒間表示
    start_time = time.time()
    while time.time() - start_time < 5:
        
        screen.blit(black_surface, (0, 0)) #黒い矩形を画面に描画
        screen.blit(crying_kk_img, crying_kk_rct) #泣いているこうかとんを画面に描画
        screen.blit(game_over_text, game_over_rct) #「Game Over」テキストを画面に描画
        pg.display.update() #画面を更新
        


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20)) #赤い爆弾の画像を作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #赤い爆弾を描画
    bb_img.set_colorkey((0, 0, 0)) #黒い部分を透過させる
    bb_rct = bb_img.get_rect() #爆弾のRectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  #爆弾の初期横座標を乱数で設定
    bb_rct.centery = random.randint(0, HEIGHT) #爆弾の初期縦座標を乱数で設定
    vx, vy = +5, +5 #爆弾の速度
    
    


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が重なったら
            show_game_over(screen, WIDTH, HEIGHT, clock)
            return #ゲームオーバー:main関数から出る
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
     
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) #画面外だったら
        if check_bound(kk_rct) != (True, True): #こうかとんが画面外に出たら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #こうかとんを元に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾を移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向に画面外だったら
            vx *= -1 #横方向の速度を反転
        if not tate: #縦方向に画面外だったら
            vy *= -1 #縦方向の速度を反転
        screen.blit(bb_img, bb_rct) #爆弾を画面に描画
        pg.display.update()
        tmr += 1
        clock.tick(50)
    


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
