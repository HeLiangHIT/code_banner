import time, sys, os
from PIL import Image, ImageSequence, ImageEnhance
from clize import Parameter, run



# 将灰度映射到字符: 灰度值越小->越暗->对应的字符越越大
DEFAULT_HEIGHT_MULTIPLIER = 0.62
ASCII_CHAR = list("@B%8&WM#$ZO0QLCJUYXI*oahkbdpqwmzcvunxrjft-_+~il;:,\"^`'. ") # █▓▒░
_gray2char = lambda gray: ASCII_CHAR[int(gray / 256.0 * len(ASCII_CHAR))]


def prepare_img(img, width, height, enhance):
    '''归一化图像到固定长宽，以便转换为文字'''
    img = img.convert('L')
    img_w, img_h = img.size
    height = img_h * width / img_w if not height else height
    height *= DEFAULT_HEIGHT_MULTIPLIER # normalize the char height to width
    img = img.resize((int(width), int(height)), Image.NEAREST)
    # 对比度增强
    return ImageEnhance.Contrast(img).enhance(enhance)


def img2text(img): 
    '''将图像各个像素转换为字符'''
    txt = ''
    for h in range(img.size[1]):
        for w in range(img.size[0]):
            pixel = img.getpixel((w, h))
            txt += _gray2char(pixel)
        txt +='\n'
    return txt


def parser_out(txts, tty=True, file=None):
    '''输出内容'''
    index = 0
    for txt in txts:
        os.system('clear')
        print(txt)
        if file:
            file_name = '%s.%d' % (file, index)
            with open(file_name, 'w') as f:
                f.write(txt)
            index += 1
        time.sleep(0.1)


def main(*file, out_file:'o'=None, out_width: 'w'=100, out_height: 'l'=0, enhance: 'e'=1.0):
    '''生成banner
    
    :param file: banner image file
    :param out_file: output txt file name, append by 0-n for sequence
    :param out_width: output text width (unit: char)
    :param out_height: output text height (unit: line)
    :param enhance: image enhance factor, now try yourself diff value to get a better out
    '''
    if len(file) > 1:
        raise Exception('do not support multi files')
    img = Image.open(file[0])
    if file[0].endswith('.gif') and img.is_animated:
        frames = [f.copy() for f in ImageSequence.Iterator(img)]
        print("parser animated pic with %d-frames..." % img.n_frames)
    else:
        frames = [img, ]
        print("parser static pic...")

    out_seq = []
    for f in frames:
        img = prepare_img(f, out_width, out_height, enhance)
        out_seq.append(img2text(img))
    parser_out(out_seq, file=out_file)


if __name__ == '__main__':
    run(main)

