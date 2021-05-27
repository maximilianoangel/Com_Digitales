import numpy as np
import random

def binario_a_decimal(numero_binario):
    aux=int(numero_binario)
    if aux%10==0:
        numero_binario=aux+1
    elif aux%10==1:
        numero_binario=aux-1
    else:
        print("no es un formato adecuado")
    print(str(numero_binario))
    return str(numero_binario)

def Error(data):
    error="error"
    normal="normal"
    prob=0.9
    probN=1-prob
    opcion=np.random.choice([error, normal], size = 100, p=[prob,probN])
    l=random.randrange(100)-1
    print(opcion[l])
    if opcion[l]=="error":
        m=len(data)
        aux=random.randrange(m)-1
        aux2=binario_a_decimal(data[aux])
        print(aux2)
        data[aux]='0' + aux2
        return data
    elif opcion[l]=="normal":
        return data

def arreglador(arr):
    i=0
    count=0
    aux2=[]
    while count<5:
        index=i+12
        aux=""
        while i<index and index<=len(arr):
            aux +=str(arr[i])
            i=i+1
        aux2.append(aux)
        i=i+1
        count=count+1
    return aux2

        


for i in range(1,31):
    name = str(i) + ".txt"
    path="./gerror/" + name
    archivo=open(path)
    contenido=archivo.read(128)
    archivo.close()
    b=arreglador(contenido)
    print(b)
    a=[]
    a=Error(b)
    print(a)
    for aux in a:
        archivo = open("./error_generado/" + name,"a")
        archivo.write(aux)
        archivo.write(" ")
        archivo.close()