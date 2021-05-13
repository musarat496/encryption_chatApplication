import socket
import sys
import time
import uuid

key = 0
s = socket.socket()
my_comp_name = socket.gethostname()
print("MAC address is : ", end="")
mac_address = ''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
print(mac_address)
print("")

host = input(str("Please enter machine name with which you want to connect: "))
port = 1234
s.connect((host, port))
print("User B Connected to: ", host)
print("")

first = s.recv(1024)
first = first.decode()
print("User A: ", first)

my_com_name = my_comp_name.encode()
s.send(my_com_name)
print("")

second = s.recv(1024)
second = second.decode()
print("User A: ", second)

mac_address = mac_address.encode()
s.send(mac_address)
print("")


def key_calculate():
    comp_name_ascii = []
    for character in my_comp_name:
        comp_name_ascii.append(ord(character))
    # print("Computer name of User B in ASCII: ", comp_name_ascii)

    ascii_sum = sum(comp_name_ascii)
    # print("sum of ASCII is: ", ascii_sum)
    ascii_avg = ascii_sum / len(comp_name_ascii)
    # print("average of ASCII is: ", ascii_avg)
    ascii_round = round(ascii_avg)
    # print("Rounded off number is: ", ascii_round)
    global key
    key = ascii_round % 26
    # print("key is: ", key)
    return key


key_calculate()


def key_update(ky, cnt):
    mac_char_no = cnt // 5
    mac_char = int(mac_address[mac_char_no], 16)
    global key
    key = (ky + mac_char) % 26
    return key


def my_decrypt(input_string, ky):
    decrypted_msg = ""
    for i in range(len(input_string)):
        char_ascii = ord(input_string[i])
        if 65 <= char_ascii <= 90:
            char_ascii = char_ascii - ky
            if char_ascii < 65:
                char_ascii = char_ascii + 26

        elif 97 <= char_ascii <= 122:
            char_ascii = char_ascii - ky
            if char_ascii < 97:
                char_ascii = char_ascii + 26

        decrypted_msg += chr(char_ascii)
    return decrypted_msg


def my_encode(input_str, keey):
    encrypted_msg = ""
    for i in range(len(input_str)):
        char_ascii = ord(input_str[i])
        if 65 <= char_ascii <= 90:
            char_ascii = char_ascii + keey
            if char_ascii > 90:
                char_ascii = 64 + (char_ascii - 90) % 90

        elif 97 <= char_ascii <= 122:
            char_ascii = char_ascii + keey
            if char_ascii > 122:
                char_ascii = 96 + (char_ascii - 122) % 122

        encrypted_msg += chr(char_ascii)
        # shifted_msg = shifted_msg.join(chr(char_ascii))
    return encrypted_msg


while 1:
    count = 0
    count = count + 1
    if count % 5 == 0:
        key = key_update(key, count)

    incoming_msg = s.recv(1024)
    incoming_msg = incoming_msg.decode()
    incoming_msg = my_decrypt(incoming_msg, key)
    print("User A: ", incoming_msg)

    message = input(str(">>"))
    message = my_encode(message, key)
    message = message.encode()
    s.send(message)
    print("Message sent.")
    print("")



