# -*- coding:utf-8 -*-

import numpy as np

def build_checkerboard(w, h) :
    re = np.r_[ w*[0,1] ]        # 짝수
    ro = np.r_[ w*[1,0] ]        # 홀수
    return np.row_stack(h*(re, ro))


checkerboard = build_checkerboard(3, 3)
print(checkerboard)
