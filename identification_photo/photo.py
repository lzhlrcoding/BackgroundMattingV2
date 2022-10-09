import cv2
import numpy as np
from PIL import Image
import os
from pip import main


# 存放从小程序获取到的用户原始照片
xcx_original_img = 'identification_photo/456.JPG'
# 存放原始图片修改为600x800的照片
img = "content/img/img"
# 存放img的背景照片（content/bgr）
bgr = "content/bgr/img"


class Photo(object):
  # 初始化属性,size是一个元组
  def __init__(self, name=img, size=(600, 800), bgcolor='red', suffix='jpg'):
    self.__name = name
    self.__size = size 
    self.__bgcolor = bgcolor
    self.__suffix = suffix
  
  def get_name(self):
    return self.__name
  def get__size(self):
    return self.__size
  def get_bgcolor(self):
    return self.__bgcolor
  def get_duffix(self):
    return self.__suffix
  
  def set_name(self, name):    
    self.__name = name
  def set_size(self, size):
    self.__size = size
  def set_bgcolor(self, bgcolor):
    self.__bgcolor = bgcolor
  def set_suffix(self, suffix):
    self.__suffix = suffix

  #获取原始照片的后缀
  def get_orignal_suffix(self, name:str):
      # 先将原始字符串转换成小写,并返回其照片的后缀名
      suffix = os.path.splitext(name.lower())[-1]
      if(suffix == '.jpg' or suffix == '.png'):
        return suffix
      # 将信息返回给小程序
      # print("请上传.jpg或.png格式的照片")
      return "请上传.jpg或.png格式的照片"

  
  # 将照片的size改为600x800
  def change_size(self, name, suffix):
    # 获取原始resize后的照片的size
    width, height = self.get__size()[0], self.get__size()[1]
    original_img_lower = name.lower()
    write_img_quality = []
    if('.jpg' in original_img_lower):
      write_img_quality = [1, 100]
    elif('.png' in original_img_lower):
      write_img_quality = [16, 0]
    # 原始图像读取
    original_img = cv2.imread(name)
    # 更改照片尺寸
    resize_img = cv2.resize(original_img, (width, height), interpolation = cv2.INTER_AREA)
    # 将照片保存在content/img下,他只质量为write_img_quality
    # cv2.imwrite('img.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100]),100表示质量最高
    # cv2.imwrite('img.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])，0表示无损
    path = img + suffix
    # print(path)
    cv2.imwrite(path, resize_img, write_img_quality)
    self.fill_bgr(path, suffix)
    cv2.imshow('img', resize_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # 根据获取到的图片像素点的颜色填充图片
  def fill_bgr(self, name:str, suffix:str):
    pix_bgr = self.get_pix_bgr(name, 5, 5)
    # 颜色的顺序为蓝 绿 红
    color = (pix_bgr[0], pix_bgr[1], pix_bgr[2]) # color you want
    # 元组顺序为高 宽
    arr = np.zeros((800, 600, 3), dtype=np.uint8) # all-zero array
    bgr_img = color - arr
    original_img_lower = name.lower()
    write_img_quality = []
    if('.jpg' in original_img_lower):
      write_img_quality = [1, 100]
    elif('.png' in original_img_lower):
      write_img_quality = [16, 0]
    # 将图片存放在content/bgr/img.jpg下
    # cv2.imwrite('img.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100]),100表示质量最高
    # cv2.imwrite('img.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])，0表示无损
    path = bgr + suffix
    cv2.imwrite(path, bgr_img, write_img_quality)
  
  # 获取图片坐标bgr值
  def get_pix_bgr(self, name: str, x: int, y: int):
    img = cv2.imread(name)
    px = img[y, x]
    blue = img[y, x, 0]
    green = img[y, x, 1]
    red = img[y, x, 2]
    return blue, green, red


if __name__ == '__main__':
  # 创建Photo实例
  photo = Photo(xcx_original_img)
  # 获取原始照片的后缀
  suffix = photo.get_orignal_suffix(photo.get_name())
  photo.change_size(photo.get_name(), suffix)



  





