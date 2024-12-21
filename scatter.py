import csv

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

file_path = './Stars.tiff'
img = Image.open(file_path)

# magic number 9：画像の解像度を1/9に落とす。解像度が高すぎると計算が重くなり、1つの散布図の点が隣接する複数の行列の要素に対応してしまう。
new_size = (img.size[0]//9, img.size[1]//9)
img = img.resize(new_size)

image_gray = img.convert('L')
# image_gray.show()

image_array = np.array(image_gray)

# magic number 128：255が白、0が黒。閾値が大きすぎると点周辺の要素まで0(黒)になってしまい、小さすぎると読み取れる点の数が減ってしまう。
threshold = 128
binary_matrix = (image_array > threshold).astype(int)  # bool演算で二値化

height = binary_matrix.shape[0]
width = binary_matrix.shape[1]
visited_map = np.zeros((height, width))


def dfs(x, y):
    # 深さ優先探索で0が隣接する場合は1つにまとめる。

    if binary_matrix[x][y] == 1:
        return
    else:
        stack = [(x, y)]

    def check_if_searchable(x, y):
        # x,yが到達済みかどうか判定
        if x < 0 or y < 0 or x >= height or y >= width:
            return False

        if visited_map[x][y] == 0 and binary_matrix[x][y] == 0:
            return True
        else:
            return False

    def search(x, y):
        if check_if_searchable(x, y):
            visited_map[x][y] = 1
            binary_matrix[x][y] = 1
            stack.append((x, y))
        return

    while stack:
        x, y = stack.pop()
        visited_map[x][y] = 1
        search(x-1, y)
        search(x+1, y)
        search(x, y-1)
        search(x, y+1)
    return


with open('scatter_data.csv', 'w') as f:
    f.write('y,x\n')

for i in range(height):
    for j in range(width):
        if binary_matrix[i][j] == 0:
            dfs(i, j)
            with open('scatter_data.csv', 'a') as f:
                f.write(f'{j}, {height - i - 1}\n')


# plt.imshow(binary_matrix, cmap='gray')
# plt.show()

# print(np.sum(binary_matrix == 0))  # 57個の点があるはず
