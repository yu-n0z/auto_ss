import os
import pyautogui as gui
import sys
import time
import numpy as np
import cv2
import os
import img2pdf
from PIL import Image # img2pdfと一緒にインストールされたPillowを使います


#### 実行形式でのpath取得
path_current_dir = os.path.dirname(sys.argv[0])

# print(sys.argv[0]) 
# print(path_current_dir)


#### 保存ディレクトリを指定
Savedir = path_current_dir + "/capture/"
Bookname = ""

print('中断するにはCrt+Cを入力してください。')

InFlg = 0

#### ファイル名の入力
while True:
    try:
        Bookname = input("ファイル名を入力してください")
    except ValueError as ex:
        if Bookname == "":
            print(end= "")
        else:
            print("ファイル名として有効な文字列を入力してください")
    except TypeError:
        print()
    else:
        break

#### 座標の取得
try:
    while True:
        if InFlg == 0:
            x=input("キャプチャしたい画像の左上にカーソルを当てEnterキー押してください\n")
            XLeftTop,YLeftTop = gui.position()
            InFlg += 1

        if InFlg == 1:
            x=input("キャプチャしたい画像の右下にカーソルを当てEnterキー押してください\n")
            XRightLow,YRightLow = gui.position()
            InFlg += 1
        
        if InFlg == 2:
            cursol=input("ページ送り方向を指定してください(→:1 / ←:2)'\n")
            if cursol == "1":
                cursol = "right"
                InFlg+=1
            elif cursol == "2":
                cursol="left"
                InFlg+=1
        
        if InFlg == 3:
            x=input("Enterを押下し5秒後に開始します\nキャプチャしたい画面を全面に表示し待機してください。")
            InFlg += 1

        if InFlg == 4:
            break
except KeyboardInterrupt:
    print('\n終了')
    sys.exit()

#### キャプチャ範囲の幅と高さを格納
Width =  XRightLow - XLeftTop
Height =  YRightLow - YLeftTop

#### 実行開始までのwait
time.sleep(5)

Pagecount = 1

while True:
    time.sleep(0.3)
    Pagenum = str(Pagecount).zfill(4)
    # #region = (左からの配置位置, 上からの配置位置, 幅, 高さ)
    SS = gui.screenshot(region = (XLeftTop,YLeftTop,Width,Height))
    SS = SS.convert('RGB')

    #### 2ページ以降は前回のキャプチャ内容と比較する
    if Pagecount >= 2:
        # 前回のキャプチャ内容と今回のキャプチャを比較、一致したあと再度比較し終了判定へ
        if np.array_equal(SS,BeforeSS):
            time.sleep(2)
            SS = gui.screenshot(region = (XLeftTop,YLeftTop,Width,Height))
            SS = SS.convert('RGB')

            #### キャプチャ終了判定
            if np.array_equal(SS,BeforeSS):
                print("キャプチャ画像が一致したので終了します")
                break
    
    Fname = Savedir + Bookname + '_' + str(Pagenum) + '.jpg'
    SS.save(Fname)
    BeforeSS = SS
    Pagecount += 1
    gui.press(cursol)
    time.sleep(0.5)

#### pdf変換
print("PDF化を開始します")

pdf_FileName = Savedir + Bookname + '.pdf' # 出力するPDFの名前
png_Folder = Savedir # 画像フォルダ
extension  = ".jpg" # 拡張子がPNGのものを対象

with open(pdf_FileName,"wb") as f:
    # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
    f.write(img2pdf.convert([Image.open(png_Folder+j).filename for j in os.listdir(png_Folder)if j.endswith(extension)]))

print("PDF化完了しました")