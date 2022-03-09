import hashlib
import socket
import threading
import os

listOfSongs = list()

from time import gmtime, strftime
import time

HOST = '127.0.0.1'
PORT = 50015
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""


# custom say hello command
def sayHello():
    print("----> The hello function was called")

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    print("parsing...")
    print(str(data))

    # Checking for commands 
    if "<hello>" in str(data):
        print("Hello command run")

    elif "<get" in str(data):
        parts = str(data).split('-')
        print(parts[0])  # name of the command
        print(parts[1])  # filename

        # start = str(data).index('<')
        # end = str(data).index('>')

        filename = str(parts[1])[0:-3]  # cut at < and >
        print("cleaned: " + filename)

        f = open(filename, 'rb')
        content = f.read()
        con.sendall(content)
        f.close()

    elif "<hash" in str(data):  # <hash-chunk0.mp3>
        print("hashing....")

        m = hashlib.sha256()
        parts = str(data).split('-')
        filename = parts[1]  # this contains the filename
        cleanedName = filename[0:-3]  # chop of the last 3
        print("cleaned file name: " + cleanedName)

        # read in the file
        file = open(cleanedName, 'rb')
        content = file.read()

        # get the hash
        m.update(content)  # passes in the content
        res = m.digest()  # just the actual hash itself
        # send back the result
        con.send(res)

    elif "<addsong" in str(data):
        print("adding a song....")

        start = str(data).index('<')
        end = str(data).index('>')

        parts = str(data).split('-')  # <addsong-britney.mp3-localhost>

        print(parts[0])  # name of the command
        print(parts[1])  # filename
        print(parts[2])  # location
        print(str(data[start + 1:end]))

        listOfSongs.append(parts[1])  # store the song name

        # receive the file and make it

        f = open('c0.mp3', 'wb')  # open a file

        partOfFile = con.recv(1000)

        while partOfFile:
            f.write(partOfFile)
            partOfFile = con.recv(1000)

        f.close()

    elif "<listall>" in str(data):
        files = os.listdir(path=".")

        justMp3s = list()

        for oneFile in files:  # loop over the files
            if ".mp3" in oneFile:
                print(oneFile)
                justMp3s.append(oneFile)

        con.send(str(justMp3s).encode())


# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)

    parseInput(str(data), conn)  # Calling the parser, passing the connection

    print("rec:" + str(data))
    buffer += str(data)

    # conn.send(str(buffer))

    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
