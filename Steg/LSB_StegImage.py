from PIL import Image
import sys

'''
message: (string) tin nhắn
image: (path) đường dẫn ảnh
img: (object) đối tượng ảnh
img_convert: (object) ảnh được convert sang RGB
pixel: (list) danh sách dữ liệu điểm ảnh
'''

class func():
    def __init__(self):
        pass
    
    def decToBin(self, integer):
            return format(integer, '08b')
    
    def binToDec(self, binary):
        return int(str(binary), 2)
    
    def setLSB(self, bin_pixel, char_bin):
        bin_pixel = list(bin_pixel)
        bin_pixel[-1:] = char_bin
        bin_pixel = ''.join(bin_pixel)
        return bin_pixel
    
    def rgb_bin(self, r, g, b):
        return  self.decToBin(r), \
                self.decToBin(g), \
                self.decToBin(b)
    
    def getLSB(self, binary):
        b = list(binary)
        return b[-1:]
    
    def binToAcii(self, binary):
        data = list(map(''.join,list(zip(*[iter(binary)]*8))))
        acii = [int(a, 2) for a in data]
        return ''.join([chr(int(a)) for a in acii])

class HidePrivate(func):
    def __init__(self, message, image):
        self.message = message
        self.image = image
        self.img = Image.open(image)
        self.img_convert = self.img.convert('RGB')
        self.pixel = list(self.img_convert.getdata())
    
    # Ẩn tin (thường)
    def hideNormal(self, file_name):
        message = self.message
        message_bin = ''.join(['{0:08b}'.format(ord(char), 'b') for char in message])
        message_bin = message_bin + '0' * (8 - (len(message_bin) % 8))
        print('Dữ liệu bin Message: ', message_bin)
        len_messBin = len(message_bin)
        print('Độ dài Message nhị phân: ', len_messBin)
        space_needed = len_messBin // 3 + 1
        print('Số pixel ảnh sẽ đọc: ', space_needed)
        data_pixel_storage = []
        for i in range(space_needed):
            data_pixel_storage += self.pixel[i]
        print(data_pixel_storage)
        
        data_pixel_be_hide_storage = []
        for i, char in zip(data_pixel_storage, message_bin):
            data_pixel_be_hide_storage.append(super().setLSB(super().decToBin(i), char))
        print(data_pixel_be_hide_storage)

        back_to_rgb_after_hide = list(tuple(zip(*[iter(data_pixel_be_hide_storage)]*3)))
        print(back_to_rgb_after_hide)
        
        data_new = []
        for rgb in back_to_rgb_after_hide:
            pixel = super().binToDec(rgb[0]), \
                    super().binToDec(rgb[1]), \
                    super().binToDec(rgb[2])
            data_new.append(pixel)
            print(pixel)
        print(data_new)
        self.img_convert.putdata(data_new)
        self.img_convert.save('static/hide/{}'.format(file_name))


class GetMessageHide(func):
    def __init__(self, image, so_pixel):
        self.so_pixel = so_pixel
        self.image = image
        self.img = Image.open(image)
        self.img_convert = self.img.convert('RGB')
        self.pixel = list(self.img_convert.getdata())
    
    # lấy ngược dữ liệu (thường)
    def getMessageHideNormal(self):
        if self.so_pixel < 1:
            bit_data = []
            for i in range(len(self.pixel)):
                rgb = super().rgb_bin(self.pixel[i][0],self.pixel[i][1],self.pixel[i][2])
                for i in rgb:
                    bit_data += super().getLSB(i)
                data_bin = ''.join(bit_data)
            print(super().binToAcii(data_bin))
            return super().binToAcii(data_bin)
        elif self.so_pixel > 1:
            bit_data = []
            print('\n\nXem pixel: ',self.pixel[1])
            for i in range(self.so_pixel):
                rgb = super().rgb_bin(self.pixel[i][0],self.pixel[i][1],self.pixel[i][2])
                for i in rgb:
                    bit_data += super().getLSB(i)
                data_bin = ''.join(bit_data)
            print('Thông tin được giấu:', super().binToAcii(data_bin))
            return super().binToAcii(data_bin)

# hide = HidePrivate('tran ba quang', '../static/hide/xdufwEtcMOin.png')
# hide.hideNormal('a.png')
# show = GetMessageHide('../static/hide/a.png', 100)
# show.getMessageHideNormal()