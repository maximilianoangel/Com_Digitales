import random
import string
import numpy as np



def generador():
    for i in range(1,31):
        text = "".join(random.choices(string.ascii_lowercase,k=5))
        name = str(i) + ".txt"
        archivo = open("./caracteres/" + name,"w")
        archivo.write(text)
        archivo.close()

def hamming(path,name):
    resultado=[]
    byte_list=[]
    d=[]
    with open(path, "rb") as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            byte_list.append(byte)
    print(byte_list)
    for byte in byte_list:
        int_value = ord(byte)
        binary_string = '{0:08b}'.format(int_value)
        d.append(binary_string)
        print(binary_string)
    for dat in d:
        data=list(dat)
        data.reverse()
        c,ch,j,r,h=0,0,0,0,[]
        while ((len(d)+r+1)>(pow(2,r))):
            r=r+1
        for i in range(0,(r+len(data))):
            p=(2**c)
            if(p==(i+1)):
                h.append(0)
                c=c+1
            else:
                h.append(int(data[j]))
                j=j+1
        for parity in range(0,(len(h))):
            ph=(2**ch)
            if(ph==(parity+1)):
                startIndex=ph-1
                i=startIndex
                toXor=[]
                while(i<len(h)):
                    block=h[i:i+ph]
                    toXor.extend(block)
                    i+=2*ph
                for z in range(1,len(toXor)):
                    h[startIndex]=h[startIndex]^toXor[z]
                ch+=1
        h.reverse()
        resultado.append(h)
    print('Hamming code generated would be:- ', end="")
    print(resultado)
    archivo = open("./gerror/" + name,"a")
    for aux in resultado:
        aux3=''
        for aux2 in aux:
            aux3 +=str(aux2)
        archivo.write(str(aux3))
        archivo.write(" ")
    archivo.close()
    return resultado

opcion=int(input("¿Que desea realizar?\n  1. codec\n  2. generar archivo\n"))
if opcion==1:
    for i in range(1,31):
        name=str(i) + ".txt"
        aux=hamming("./caracteres/" + name,name)
    
elif opcion==2:
    generador()