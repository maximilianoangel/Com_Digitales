import binascii

def detectar(d):
    aux=''
    data=list(d)
    data.reverse()
    c,ch,j,r,error,h,parity_list,h_copy=0,0,0,0,0,[],[],[]

    for k in range(0,len(data)):
        p=(2**c)
        h.append(int(data[k]))
        h_copy.append(data[k])
        if(p==(k+1)):
            c=c+1
            
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
            parity_list.append(h[parity])
            ch+=1
    parity_list.reverse()
    error=sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))
    
    if((error)==0):
        print('There is no error in the hamming code received')
        aux=d

    elif((error)>=len(h_copy)):
        print('Error cannot be detected')
        aux=d

    else:
        print('Error is in',error,'bit')

        if(h_copy[error-1]=='0'):
            h_copy[error-1]='1'

        elif(h_copy[error-1]=='1'):
            h_copy[error-1]='0'
            print('After correction hamming code is:- ')
        h_copy.reverse()
        print(h_copy)
        aux=str(''.join(map(str, h_copy)))
        print(str(''.join(map(str, h_copy))))
    return aux

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
def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

for ab in range(1,31):
    name=str(ab) + ".txt"
    aux=[]
    path="./error_generado/" + name
    archivo=open(path)
    contenido=archivo.read(128)
    archivo.close()
    a=arreglador(contenido)
    for i in a:
        aux.append(detectar(i))
    print(aux)