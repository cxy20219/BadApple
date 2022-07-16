from socket import *  
import cv2
from ffpyplayer.player import MediaPlayer

def img_bitmap(img):
    # 灰度处理
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # 缩小图片
    small_img=cv2.resize(img,(128,64))

    # 二值化
    ret,img=cv2.threshold(small_img, 150, 1, cv2.THRESH_BINARY);

    # 将8位一组放在一起
    s1="0b"
    img = img.reshape(1024,8)
    ob_list=[s1+"".join(map(str,i.tolist())) for i in img]

    # #转换为16进制字符串 格式定位两位
    # ox_list=['0x'+'%02x' % int(i, 2) for i in ob_list]

    data = [int(i,2) for i in ob_list]
    return bytes(data)
    
def socket_init():
    # #  === TCP 服务端程序 server.py 
    # # 主机地址为空字符串，表示绑定本机所有网络接口ip地址
    # # 等待客户端来连接
    IP = ''
    # 端口号
    PORT = 50000

    # # 实例化一个socket对象
    # # 参数 AF_INET 表示该socket网络层使用IP协议
    # # 参数 SOCK_STREAM 表示该socket传输层使用TCP协议
    listenSocket = socket(AF_INET, SOCK_STREAM)

    # # socket绑定地址和端口
    listenSocket.bind((IP, PORT))


    # # 使socket处于监听状态，等待客户端的连接请求
    # # 参数 8 表示 最多接受多少个等待连接的客户端
    listenSocket.listen(5)
    print(f'服务端启动成功，在{PORT}端口等待客户端连接...')

    dataSocket, addr = listenSocket.accept()
    print('接受一个客户端连接:', addr)

    return dataSocket,listenSocket
def send_data(dataSocket,data):
    # 发送的数据类型必须是bytes，所以要编码
    dataSocket.send(data)

def socket_end(dataSocket,listenSocket):
    dataSocket.close()
    listenSocket.close()

if __name__ == "__main__":
    dataSocket,listenSocket = socket_init()

    video = cv2.VideoCapture("BadApple.mp4")
    ret,img = video.read()
    player = MediaPlayer("BadApple.mp4") #打开音频

    page = 1
    fps = 8

    while ret:
        # 读取图片数据
        ret,img = video.read()
        
        if (page % fps == 0):
            data = img_bitmap(img)
            send_data(dataSocket,data)
        
        out_img = cv2.resize(img,(500,400))
        cv2.imshow("Video", out_img)
        cv2.waitKey(16)

        page += 1

    
    cv2.destroyAllWindows()

    socket_end(dataSocket,listenSocket)
    video.release()