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
    引数で与えられたRectが画面内か画面外かを判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向判定結果
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def create_bomb_lists() -> tuple:
    """
    10段階の大きさを変えた爆弾Surfaceのリストと加速度のリストを生成
    戻り値：（爆弾画像リスト、加速度リスト）
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 爆弾の大きさを段階的に変えるため、Surfaceのサイズを20*rに設定
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) # 爆弾を赤い円で描画、中心を(10*r, 10*r)にして半径を10*rに設定
        bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透過させる
        bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト [1, 2, 3, ..., 10]
    
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    bg_img.set_alpha(200); 
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    bg_img.blit(txt, [WIDTH // 2 - 150, HEIGHT // 2])
    kk_img = pg.image.load("fig/8.png")
    bg_img.blit(kk_img, [WIDTH // 2 - 250, HEIGHT // 2 - 20])
    bg_img.blit(kk_img, [WIDTH // 2 + 200, HEIGHT // 2 - 20])
    screen.blit(bg_img, [0, 0])
    pg.display.update()
    time.sleep(5)
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾のリストを生成
    bb_imgs, bb_accs = create_bomb_lists()
    bb_img = bb_imgs[0]  # 初期の爆弾画像
    bb_rct = bb_img.get_rect()  # 爆弾rctを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾の初期横座標を乱数で設定
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾の初期縦座標を乱数で設定
    vx, vy = +5, +5  # 爆弾の速度を設定

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return #ゲーム終了
        screen.blit(bg_img, [0, 0]) #背景を描画する


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        # tmrの値に応じて爆弾の大きさと速度を更新
        idx = min(tmr // 500, 9)  # 0～9の値に制限
        bb_img = bb_imgs[idx]  # 現在の爆弾画像を取得
        acceleration = bb_accs[idx]  # 現在の加速度を取得
        avx = vx * acceleration  # 加速された横速度
        avy = vy * acceleration  # 加速された縦速度
        
        # Rectのサイズを更新
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        
        bb_rct.move_ip(avx, avy)  # 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)  # 爆弾が画面内か画面外かを判定する
        if not yoko:  # 横方向の判定
            vx *= -1  # 横方向の速度を反転させる
        if not tate:  # 縦方向の判定
            vy *= -1  # 縦方向の速度を反転させる

        screen.blit(bb_img, bb_rct)  # 爆弾を画面に描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
