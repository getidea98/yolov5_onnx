import cv2 as cv
import numpy as np

firstIndex = [91, 41]


def img_show(img):
    cv.imshow("win", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


# 计算当前的关卡数
# img：当前屏幕的截图
def current_door(img, stride=24):
    crop = img[57:160, 1145:1270, 0]  # crop右上角小地图范围
    # img_show(crop)
    index = np.unravel_index(crop.argmax(), crop.shape)  # crop.argmax()：返回最大值的在一维数字的下标；index：最大值在二维数组下的坐标
    value = crop[index[0], index[1]]
    if value < 200:
        #  BOSS房间
        return 6
    # 经实验，index是当前关卡的坐标。其中黑暗都市、皇家娱乐每关卡相差24像素
    i = hbl(index)
    return i  # 返回的是在第几个房间


def hbl(index, stride=24.0):
    a = int(round(abs(index[0] - firstIndex[0]) / stride, 1))
    b = int(round(abs(index[1] - firstIndex[1]) / stride, 1))
    return a + b


def next_door(img):
    img_temp = np.load("问号模板.npy")
    th, tw = img_temp.shape[:2]
    # img_show(img_temp)
    target = img[:, :]
    result = cv.matchTemplate(target, img_temp, cv.TM_SQDIFF_NORMED)
    cv.normalize(result, result, 0, 1, cv.NORM_MINMAX, -1)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    tl = min_loc  # tl是左上角点
    br = (tl[0] + tw, tl[1] + th)  # 右下点
    cv.rectangle(target, tl, br, (0, 0, 255))
    cv.imshow("match-cv.TM_SQDIFF_NORMED", target)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # next_door_id = 0
    # if min_val < 1e-10:
    #     print(min_val, max_val, min_loc, max_loc)
    #     strmin_val = str(min_val)
    #     theight, twidth = img_temp.shape[:2]
    #     cv.rectangle(target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (225, 0, 0), 2)
    #     cv.imshow("MatchResult----MatchingValue=" + strmin_val, target)
    #     cv.waitKey()
    #     cv.destroyAllWindows()
    #     next_door_id = int(((min_loc[0] + 0.5 * twidth) // 18.11) + 1)
    # return next_door_id


if __name__ == "__main__":
    img = cv.imread('042504.png')
    print(next_door(img))
