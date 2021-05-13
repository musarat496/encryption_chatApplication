import socket
import sys
import time

key = 0
s = socket.socket()
host = socket.gethostname()
print("user A will start at host machine: ", host)
print("")
port = 1234
s.bind((host, port))
s.listen(1)
print("User A is waiting for incoming connections...")
print("")
connection, address = s.accept()
print(address, " has connected to user A")

ask_comp_name = str("what is your computer name?")
ask_comp_name = ask_comp_name.encode()
connection.send(ask_comp_name)
print("")
comp_name_rec = connection.recv(1024)
comp_name_rec = comp_name_rec.decode()
print("User B: My computer name is ", comp_name_rec)

ask_mac_address = str("what is your mac address?")
ask_mac_address = ask_mac_address.encode()
connection.send(ask_mac_address)
print("")
mac_address_rec = connection.recv(1024)
mac_address_rec = mac_address_rec.decode()
print("User B: My mac address is: ", mac_address_rec)


def key_calculate():
    comp_name_ascii = []
    for character in comp_name_rec:
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


def key_update(ky, cnt):
    mac_char_no = cnt // 5
    mac_char = int(mac_address_rec[mac_char_no], 16)
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


while 1:
    count = 0
    count = count + 1
    if count % 5 == 0:
        key = key.key_update(key, count)

    message = input(">>")
    message = my_encode(message, key)
    # message = message.encode(message)
    message = bytes(message, 'utf-8')
    connection.send(message)
    print("Message sent.")
    print("")

    incoming_msg = connection.recv(1024)
    incoming_msg = incoming_msg.decode()
    incoming_msg = my_decrypt(incoming_msg, key)
    print("User B: ", incoming_msg)


