import numpy as np
import cv2
from PIL import Image


img = cv2.imread("test2.jpg")
coreimg = cv2.imread("mask.jpg")

b,g,r = cv2.split(img)
n = len(b)
n1 = len(b[0])
print(n, n1)
gr, q,q = cv2.split(coreimg)
keyn = len(gr)


b_final = [[0] * (n1) for i in range(n)]
g_final = [[0] * (n1) for i in range(n)]
r_final = [[0] * (n1) for i in range(n)]


gr = [[round(abs(j-255)/255) for j in i] for i in gr]
gr = np.array(gr)
b = [[(j/255) for j in i] for i in b]
b = np.array(b)
g = [[(j/255) for j in i] for i in g]
g = np.array(g)
r = [[(j/255) for j in i] for i in r]
r = np.array(r)
control_summ = np.sum(gr)
col_list = [b,g,r]
fin_list = [b_final, g_final, r_final]


for m_count in range(3):
    m = np.zeros((n + keyn // 2 * 2, n1 + keyn//2*2))
    print(len(m), len(m[0]))
    for i in range(len(col_list[m_count])):
        for j in range(len(col_list[m_count][0])):
            m[i + keyn //2 ][j + keyn // 2 ] = col_list[m_count][i][j]

    for i in range(keyn // 2 , len(m) - keyn //2):
        for j in range(keyn // 2, len(m[0]) - keyn // 2):
            #m[i][j]
            i_gr = 0
            j_gr = 0
            tms_s = 0

            for tmpi in range(i - keyn // 2, i + keyn //2):
                for tmpj in range(j - keyn // 2, j + keyn // 2):
                    tms_s += gr[i_gr][j_gr] * m[tmpi][tmpj]
                    j_gr += 1
                j_gr = 0
                i_gr += 1

            fin_list[m_count][i - (keyn // 2)][j - (keyn // 2)] = int(tms_s / control_summ * 255)
    print("finished layer number", str(m_count + 1))


new_image_blue = fin_list[2]
new_image_green = fin_list[1]
new_image_red = fin_list[0]

#np.save('new_image_blue', new_image_blue)
#np.save('new_image_green', new_image_green)
#np.save('new_image_red', new_image_red)

new_rgb = np.dstack([new_image_red, new_image_green, new_image_blue])
image = cv2.imwrite("newimage.jpg", new_rgb)
print("saved")