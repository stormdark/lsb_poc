from PIL import Image
from collections import deque

im = Image.open('img/imagen1.jpg')


def validation_message(queue_message, default_binary):
    res = queue_message.popleft() if len(queue_message) > 0 else default_binary
    return 'break' if (res == ' ') else res


def save_pixel(x_, y_, r_binary, g_binary, b_binary):
    r_dec = int(''.join(r_binary), 2)
    g_dec = int(''.join(g_binary), 2)
    b_dec = int(''.join(b_binary), 2)

    im.putpixel((x_, y_), (r_dec, g_dec, b_dec))


def hidde_message(message):

    x, y = im.size  # info | mode | format

    bits_to_modify = len(message) * 8
    available_bits_to_modify = x*y*3
    if bits_to_modify > available_bits_to_modify:
        print("Insufficient space in image! \n Available: " + str(available_bits_to_modify) + " Required: " + str(bits_to_modify))
        quit()

    msg_list = list(map(bin, bytearray(message.encode('utf8'))))
    for i_, s_ in enumerate(msg_list):
        msg_list[i_] = s_.replace('0b', '').rjust(8, '0')

    arr_message = list(' '.join(msg_list))
    queue_message = deque(arr_message)

    img_arr = im.load()

    for y_ in range(y):
        for x_ in range(x):
            r, g, b = img_arr[x_, y_]

            r_binary = list(bin(r)[2:])  # int(bin(...))
            g_binary = list(bin(g)[2:])
            b_binary = list(bin(b)[2:])

            r_new_val = validation_message(queue_message, r_binary[len(r_binary) - 1])
            if r_new_val == 'break':
                save_pixel(x_, y_, r_binary, g_binary, b_binary)
                break
            else:
                r_binary[len(r_binary) - 1] = r_new_val

            g_new_val = validation_message(queue_message, g_binary[len(g_binary) - 1])
            if g_new_val == 'break':
                save_pixel(x_, y_, r_binary, g_binary, b_binary)
                break
            else:
                g_binary[len(g_binary) - 1] = g_new_val

            b_new_val = validation_message(queue_message, b_binary[len(b_binary) - 1])
            if b_new_val == 'break':
                save_pixel(x_, y_, r_binary, g_binary, b_binary)
                break
            else:
                b_binary[len(b_binary) - 1] = b_new_val

            save_pixel(x_, y_, r_binary, g_binary, b_binary)

            if len(queue_message) == 0:
                break
                break

    im.save("img/stego.png")
    print("Message hidden")

def decode_message(img):
    im_s = Image.open(img)
    x, y = im_s.size
    stego_arr = im_s.load()
    octet_count = 0
    message = deque()

    for y_ in range(y):
        for x_ in range(x):
            r, g, b = stego_arr[x_, y_]

            r_binary = list(bin(r)[2:])
            g_binary = list(bin(g)[2:])
            b_binary = list(bin(b)[2:])

            if octet_count < 8:
                message.append(r_binary[len(r_binary) - 1])
                octet_count += 1
            else:
                message.append('_')
                octet_count = 0
                break

            if octet_count < 8:
                message.append(g_binary[len(g_binary) - 1])
                octet_count += 1
            else:
                message.append('_')
                octet_count = 0
                break

            if octet_count < 8:
                message.append(b_binary[len(b_binary) - 1])
                octet_count += 1
            else:
                message.append('_')
                octet_count = 0
                break

    message_str = ''.join(message).split('_')
    result = []

    for character in message_str:
        # print(character)
        try:
            n = int(character, 2)
            ascii_char = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
            result.append(ascii_char)
        except:
            break
    print("Message: " + ''.join(result))


def verify(img_stego):
    im = Image.open('img/imagen1.jpg')
    img_arr = im.load()

    ims = Image.open(img_stego)
    imgs_arr = ims.load()

    x, y = im.size
    for x_ in range(10):
        for y_ in range(10):
            print(str(img_arr[x_, y_]) + " - " + str(imgs_arr[x_, y_]))


if __name__ == '__main__':
    #hidde_message("HOLA AMIGOS DEL STUDY GROUP")
    decode_message('img/stego.png')
    #verify('img/stego.png')
