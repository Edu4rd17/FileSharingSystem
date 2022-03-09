# Echo client program
import socket
import segment
from pydub import AudioSegment
from pydub.utils import make_chunks
import os

while True:
    HOST = '127.0.0.1'  # The remote host
    PORT = 50015  # The same port as used by the server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print("Please enter username:")
    username = input()

    print("MENU")
    print("1 = <addsong-britney.mp3-localhost>")
    print("2 = <get-chunk0.mp3>")
    print("3 = <hash-c0.mp3>")
    print("4 = <listall>")
    print("5 = <segment>")
    print("Please choose one of the options above:")
    text = input()

    if "1" in text:
        text = "<addsong-britney.mp3-localhost>"
    elif "2" in text:
        text = "<get-chunk0.mp3>"
    elif "3" in text:
        text = "<hash-c0.mp3>"
    elif "4" in text:
        text = "<listall>"
    elif "5" in text:
        text = "<segment>"

    # when we send data to the server, we are using a colon
    # at the end of a sentence to mark the end of the current sentence
    # later when the input comes back, we will then be breaking the input
    # into individual parts using the colon : to separate the lines
    s.sendall((text + ":").encode())

    # data = s.recv(80000)

    if "<addsong" in text:
        print("getting ready to send file....")
        # read in the file and send it
        f = open('chunk0.mp3', 'rb')
        content = f.read()
        print(content)
        # send it
        s.sendall(content)
        f.close()

    elif "<get" in text:
        f = open('part.mp3', 'wb')
        output = s.recv(1000)
        while output:
            f.write(output)
            output = s.recv(1000)
        f.close()

    elif "<hash" in text:
        answer = s.recv(1000)
        print(answer)

    elif "<listall" in text:
        answer = s.recv(1000)
        print(answer)

    elif "<segment>" in text:
        # break it down in segments
        print("Please enter a file name:")
        file_name = input()

        segment.splitSegments(file_name)
        # print("Response:" + str(data))
s.close()
