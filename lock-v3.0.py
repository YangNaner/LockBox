# -*- coding:utf-8 -*-

import math
import os
import random
import tkinter as tk
from tkinter import filedialog

filepaths = []
root = tk.Tk()
root.withdraw()  # 隐藏主窗口


# 生成小于max_num的素数
def gen_prime_num(max_num):
    prime_num = []
    for i in range(2, max_num):
        temp = 0
        sqrt_max_num = int(math.sqrt(i)) + 1
        for j in range(2, sqrt_max_num):
            if i % j == 0:
                temp = j
                break
        if temp == 0:
            prime_num.append(i)
    return prime_num


# 生成公私钥
def gen_rsa_key():
    prime = gen_prime_num(500)
    p = random.choice(prime[-50:-1])  # 从后50个素数中随机选择一个作为p
    q = random.choice(prime[-50:-1])  # 从后50个素数中随机选择一个作为q
    while p == q:  # 如果p和q相等则重新选择
        q = random.choice(prime[-50:-1])
    N = p * q
    r = (p - 1) * (q - 1)
    r_prime = gen_prime_num(r)
    r_len = len(r_prime)
    e = r_prime[int(random.uniform(0, r_len))]
    d = 0
    for n in range(2, r):
        if (e * n) % r == 1:
            d = n
            break
    return (N, e), (N, d)


# 使用公钥进行加密
def encrypt(pub_key, origal):
    N, e = pub_key
    return (origal ** e) % N


# 使用私钥进行解密
def decrypt(pri_key, encry):
    N, d = pri_key
    return (encry ** d) % N


# 将字符串写入文件
def write_file(str_input, str_filename):
    try:
        f = open(str_filename, 'w', encoding='utf-8')
        f.write(str_input)
        f.close()
        print(str_filename + '文件写入成功！')
    except IOError:
        print(str_filename + '文件写入错误！')


# 读取文件内容
def read_file(str_filename):
    try:
        f = open(str_filename, 'r', encoding='utf-8')
        s = f.read()
        f.close()
        print(str_filename + '文件读取成功！')
        # print('文件内容为：')
        # print(s)
        return s
    except IOError:
        print(str_filename + '文件读取错误！')


# 读取加密的文件内容
def readencry_file(str_filename):
    try:
        f = open(str_filename, 'r', encoding='utf-8')
        s = f.read().split(',')
        f.close()
        print(str_filename + '文件读取成功！')
        # print('文件内容为：')
        # print(s)
        return s
    except IOError:
        print(str_filename + '文件读取错误！')


# 读取公钥文件
def read_publicKeyFile():
    try:
        filename = filedialog.askopenfilename(title="选择加密公钥")  # 弹出文件对话框让用户选择
        with open(filename, 'r', encoding='utf-8') as f:
            s = f.read().split(',')
        f.close()
        print("key/public.pem文件读取成功！")
        N, e = s
        pub_key = (int(N), int(e))
        return pub_key
    except IOError:
        print("key/public.pem文件读取错误！")
        return None


# 读取私钥文件
def read_privateKeyFile():
    try:
        filename = filedialog.askopenfilename(title="选择解密私钥")  # 弹出文件对话框让用户选择
        with open(filename, 'r', encoding='utf-8') as f:
            s = f.read().split(',')
        f.close()
        print("key/public.pem文件读取成功！")
        N, e = s
        pri_key = (int(N), int(e))
        return pri_key
    except IOError:
        print("key/private.pem文件读取错误！")
        return None


# 进行文件夹递归读取
def all_files_path(rootDir):
    for root, dirs, files in os.walk(rootDir):  # walk方法返回一个三元组，分别代表根目录、文件夹、文件
        for file in files:  # 遍历文件
            file_path = os.path.join(root, file)  # 拼接文件路径，用于获取文件绝对路径
            filepaths.append(file_path)  # 将文件路径添加进列表
            # print(file_path)
        for dir in dirs[:-1]:  # 遍历目录下的子目录
            dir_path = os.path.join(root, dir)  # 获取子目录路径
            all_files_path(dir_path)  # 递归调用


# 选择模式
def get_mode():
    print("请输入序号，选择对应的功能：")
    print("1.生成公私钥    "
          "\n2.使用公钥加密字符串    3.使用私钥解密字符串    "
          "\n4.使用公钥加密文件    5.使用私钥解密文件    "
          "\n6.使用公钥加密文件夹    7.使用私钥解密文件夹")
    mode = input()

    if mode == '1':
        pub_key, pri_key = gen_rsa_key()
        print("公钥：", pub_key)
        print("私钥：", pri_key)
        public_key, private_key = gen_rsa_key()
        with open("public.pem", "w") as f:
            f.write(str(public_key).replace("(", "").replace(")", ""))
            print("公钥已保存到public.pem文件中")
        with open("private.pem", "w") as f:
            f.write(str(private_key).replace("(", "").replace(")", ""))
            print("私钥已保存到private.pem文件中")

    elif mode == '2':
        pub_key = read_publicKeyFile()  # 读取公钥文件

        origal_text = input("\n 请输入要加密的文本: ")
        encrypt_text = [encrypt(pub_key, ord(x)) for x in origal_text]  # 对文本进行加密
        encrypt_show = ",".join([str(x) for x in encrypt_text])  # 输出加密后的内容
        # print(type(encrypt_show))
        print(" 加密后的密文: ", encrypt_show)

    elif mode == '3':
        pri_key = read_privateKeyFile()  # 读取私钥文件

        encrypt_str = input('请输入要解密的文本：').split(',')
        encrypt_text = [int(x) for x in encrypt_str]  # 将输入的文本处理为整数
        decrypt_text = [chr(decrypt(pri_key, x)) for x in encrypt_text]  # 对密文进行解密
        decrypt_show = "".join(decrypt_text)  # 输出解密后的内容
        print(" 解密后的明文: ", decrypt_show)

    elif mode == '4':
        pub_key = read_publicKeyFile()  # 读取公钥文件

        filename = filedialog.askopenfilename(title="选择要加密的文件")  # 弹出文件对话框让用户选择要加密的文件
        origal_text = read_file(filename)  # 读取文件中的明文
        encrypt_text = [encrypt(pub_key, ord(x)) for x in origal_text]  # 对明文进行加密
        encrypt_show = ",".join([str(x) for x in encrypt_text])  # 将加密后的内容输出
        write_file(encrypt_show, filename)  # 将加密后的内容写回文件

    elif mode == '5':
        pri_key = read_privateKeyFile()  # 读取私钥文件
        filename = filedialog.askopenfilename(title="选择要解密的文件")  # 弹出文件对话框让用户选择要解密的文件
        encrypt_str = readencry_file(filename)  # 读取文件中的密文
        encrypt_text = [int(x) for x in encrypt_str]  # 处理文件中的密文，保存为整数
        decrypt_text = [chr(decrypt(pri_key, x)) for x in encrypt_text]  # 将密文进行解密
        decrypt_show = "".join(decrypt_text)  # 输出解密后的内容
        write_file(decrypt_show, filename)  # 写入文件

    elif mode == '6':
        filepaths.clear()  # 清除全局列表中的内容
        pub_key = read_publicKeyFile()  # 读取公钥文件
        filepath = filedialog.askdirectory(title="选择要加密的文件夹")  # 弹出文件对话框让用户选择要加密的文件夹
        all_files_path(filepath)
        for filename in filepaths:  # 对遍历出的文件挨个进行加密
            origal_text = read_file(filename)
            encrypt_text = [encrypt(pub_key, ord(x)) for x in origal_text]
            encrypt_show = ",".join([str(x) for x in encrypt_text])
            write_file(encrypt_show, filename)

    elif mode == '7':
        filepaths.clear()  # 清除全局列表中的内容
        pri_key = read_privateKeyFile()  # 读取私钥文件
        filepath = filedialog.askdirectory(title="选择要解密的文件夹")  # 弹出文件对话框让用户选择要解密的文件夹
        all_files_path(filepath)
        for filename in filepaths:  # 对遍历出的文件挨个进行解密
            encrypt_str = readencry_file(filename)
            encrypt_text = [int(x) for x in encrypt_str]
            decrypt_text = [chr(decrypt(pri_key, x)) for x in encrypt_text]
            decrypt_show = "".join(decrypt_text)
            write_file(decrypt_show, filename)

    else:
        print('输入错误！')


if __name__ == '__main__':
    while True:
        get_mode()
