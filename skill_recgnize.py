import time

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

skill_time = {}


def score(skill_img):
    counter = 0
    for i in range(skill_img.shape[0]):
        for j in range(skill_img.shape[1]):
            if skill_img[i, j] > 200:
                counter += 1
    return counter / (skill_img.shape[0] * skill_img.shape[1])


# def img_show(skill_img):
#     cv.imshow("win", skill_img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()


def get_skill_img(skill_img, skill_name):
    return skill_img[skill_dict[skill_name][0]: skill_dict[skill_name][0] + skill_height,
           skill_dict[skill_name][1]: skill_dict[skill_name][1] + skill_width, 2]


def skill_rec(skill_img, skill_char_name):
    skill_img = get_skill_img(skill_img, skill_char_name)
    if score(skill_img) > 0.1:
        if time.time() - skill_time.get(skill_char_name, 1) > 5:
            skill_time[skill_char_name] = time.time() # 跟新技能的使用时间
            return True
        else:
            # 技能上次使用时间距现在不足5S
            return False
    else:
        # 技能处在冷却期
        return False


def attack(skill_img):
    # 优先使用'H', 'T', 'Y', 'U'
    for char in ['H', 'T', 'Y', 'U']:
        if skill_rec(skill_img, char.upper()):
            return char

    # 97, 123 是字母a-z
    for i in range(97, 123):
        # num to char
        char = chr(i)
        if skill_rec(skill_img, char.upper()):
            return char


if __name__ == "__main__":
    print(skill_time.get('A', 1))
    skill_time['A'] = 2
    print(skill_time['A'])

    # img_path = '042505.png'
    # img = cv.imread(img_path)
    # skill_imgA = get_skill_img('A')
    # print("A", skill_rec(skill_imgA))
