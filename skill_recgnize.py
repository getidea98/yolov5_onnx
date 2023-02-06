import cv2 as cv


def score(skill_img):
    counter = 0
    for i in range(skill_img.shape[0]):
        for j in range(skill_img.shape[1]):
            if skill_img[i, j] > 200:
                counter += 1
    return counter / (skill_img.shape[0] * skill_img.shape[1])


def img_show(skill_img):
    cv.imshow("win", skill_img)
    cv.waitKey(0)
    cv.destroyAllWindows()


skill_height_base = 714
skill_width_base = 505
skill_height = 38
skill_width = 42

# skill_dict 保存着技能左上角的坐标
skill_dict = {"Q": (skill_height_base, skill_width_base),
              "W": (skill_height_base, skill_width_base + 1 * skill_width),
              "E": (skill_height_base, skill_width_base + 2 * skill_width),
              "R": (skill_height_base, skill_width_base + 3 * skill_width),
              "T": (skill_height_base, skill_width_base + 4 * skill_width),
              "Y": (skill_height_base, skill_width_base + 5 * skill_width),
              'U': (skill_height_base, skill_width_base + 6 * skill_width),
              "A": (skill_height_base + skill_height, skill_width_base),
              "S": (skill_height_base + skill_height, skill_width_base + 1 * skill_width),
              "D": (skill_height_base + skill_height, skill_width_base + 2 * skill_width),
              "F": (skill_height_base + skill_height, skill_width_base + 3 * skill_width),
              "G": (skill_height_base + skill_height, skill_width_base + 4 * skill_width),
              "H": (skill_height_base + skill_height, skill_width_base + 5 * skill_width),
              }


def get_skill_img(skill_name):
    return img[skill_dict[skill_name][0]: skill_dict[skill_name][0] + skill_height,
           skill_dict[skill_name][1]: skill_dict[skill_name][1] + skill_width, 2]


def skill_rec(skill_name):
    if score(skill_name) > 0.1:
        return True
    else:
        return False


if __name__ == "__main__":
    img_path = '042505.png'
    img = cv.imread(img_path)
    skill_imgA = get_skill_img('A')
    skill_imgS = get_skill_img('S')
    skill_imgD = get_skill_img('D')
    skill_imgF = get_skill_img('F')
    skill_imgG = get_skill_img('G')
    skill_imgH = get_skill_img('H')
    skill_imgQ = get_skill_img('Q')
    skill_imgW = get_skill_img('W')
    skill_imgE = get_skill_img('E')
    skill_imgR = get_skill_img('R')
    skill_imgT = get_skill_img('T')
    skill_imgY = get_skill_img('Y')
    skill_imgU = get_skill_img('U')
    print("A", skill_rec(skill_imgA))
    print("T", skill_rec(skill_imgT))
    print("Q", skill_rec(skill_imgQ))
    print("S", skill_rec(skill_imgS))
    print("D", skill_rec(skill_imgD))
    print("F", skill_rec(skill_imgF))
    print("W", skill_rec(skill_imgW))
    print("R", skill_rec(skill_imgR))
    print("Y", skill_rec(skill_imgY))
    print("H", skill_rec(skill_imgH))
    print("G", skill_rec(skill_imgG))
    print("E", skill_rec(skill_imgE))
