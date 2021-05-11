
import sys
import json
import pickle
import heapq
from collections import Counter
from strgen import StringGenerator
import time
def generador():
    contenido=StringGenerator("[\A\B\C\D\E\F\G\H\I\J\K\L\M]{20}").render_list(1,unique=True)
    arch=open("./111.txt","w")
    cont=str(contenido)
    arch.write(cont)
    arch.close()
def compres(uncompressed):
    """Compress a string to a list of output symbols."""
 
    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}
 
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
 
    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result
 
 
def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO
 
    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}
 
    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
 
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 
        w = entry
    return result.getvalue()

def decode(dic, bitstr):
    res = []
    length = bitstr.bit_length() - 1
    if bitstr >> length != 1:
        raise Error("Corrupt file!")
    done = False
    while length > 0 and not done:
        shift = length - 1
        while True:
            num = bitstr >> shift
            bitnum = bin(num)[3:] # Quitamos '0b1' - el 1 inicial y el 0b de formato
            if bitnum not in dic:
                shift -= 1
                continue
            char = dic[bitnum]
            if char == 'end':
                done = True
                break
            res.append(char)
            bitstr = bitstr - ((num - 1) << shift)
            length = shift
    return ''.join(res)

def get_probabilities(content):
    total = len(content) + 1 # Agregamos uno por el caracter FINAL
    c = Counter(content)
    res = {}
    for char,count in c.items():
        res[char] = float(count)/total
    res['end'] = 1.0/total
    return res

def make_tree(probs):
    q = []
    for ch,pr in probs.items():
        # La fila de prioridad está ordenada por prioridad y PROFUNDIDAD
        heapq.heappush(q,(pr,0,ch))

    while len(q) > 1:
        e1 = heapq.heappop(q)
        e2 = heapq.heappop(q)
        nw_e = (e1[0]+e2[0],max(e1[1],e2[1])+1,[e1,e2])
        heapq.heappush(q,nw_e)
    return q[0]

def make_dictionary(tree):
    res = {}
    search_stack = []
    search_stack.append(tree+("",)) # El último elemento de la lista es el prefijo!
    while len(search_stack) > 0:
        elm = search_stack.pop()
        if type(elm[2]) == list:
            prefix = elm[-1]
            search_stack.append(elm[2][1]+(prefix+"0",))
            search_stack.append(elm[2][0]+(prefix+"1",))
            continue
        else:
            res[elm[2]] = elm[-1]
        pass
    return res

def compress(dic,content):
    res = ""
    for ch in content:
        code = dic[ch]
        res = res + code
    res = '1' + res + dic['end'] # Agregamos el caracter final y el 1 inicial
    res = res + (len(res) % 8 * "0") # Agregamos ceros para convertir en multiplo de 8
    return int(res,2)

def store(data,dic,outfile):
    # Lo guardamos en un archivo
    outf = open(outfile,'wb')
    pickle.dump(compressed,outf)
    outf.close()

    # Guardamos el diccionario en otro archivo
    outf = open("./comprimido.txt.dic","w")
    json.dump(dic,outf)
    outf.close()
    pass

import rle
# How to use:
path="111.txt"
opcion=int(input("¿Que algoritmo desea utilizar?\n  1. LZW\n  2. RLE\n  3. Huffman\n  4. Cambiar txt\n"))
if opcion==1:
    archivo=open(path)
    contenido=archivo.read(128)
    aux1=time.perf_counter()
    compressed = compres(contenido)
    aux2=time.perf_counter()
    archivo.close()
    tiempo=aux2-aux1
    print(tiempo)
    print (compressed)
    arch=open("./comprimido.txt","w")
    for i in compressed:
        parseo=str(i)
        arch.write(parseo)
    arch.close()
    aux1=time.perf_counter()
    decompressed = decompress(compressed)
    aux2=time.perf_counter()
    tiempo=aux2-aux1
    print(tiempo)
    print (decompressed)
elif opcion==2:
    w=[]
    archivo=open(path)
    contenido=archivo.read(128)
    aux1=time.perf_counter()
    cod=rle.encode(contenido)
    aux2=time.perf_counter()
    tiempo=aux2-aux1
    print(tiempo)
    print(cod)
    archivo.close()
    arch=open("./comprimido.txt","w")
    for i in cod:
        parseo=str(i)
        arch.write(parseo)
    arch.close()
    aux1=time.perf_counter()
    decod=rle.decode(cod[0],cod[1])
    aux2=time.perf_counter()
    tiempo=aux2-aux1
    print(tiempo)
    print(decod)
elif opcion==3:
    archivo=open(path)
    contenido=archivo.read(128)
    archivo.close()
    probs = get_probabilities(contenido)
    tree = make_tree(probs)
    dic = make_dictionary(tree)
    compressed = compress(dic,contenido)
    aux1=time.perf_counter()
    store(compressed,dic,"comprimido.txt")
    aux2=time.perf_counter()
    tiempo=aux2-aux1
    print(tiempo)
    f = open("./comprimido.txt.dic")
    dic = json.load(f)
    nwdic = {}
    for i,e in dic.items(): nwdic[e] = i
    f.close()
    f = open("./comprimido.txt",'rb')
    bstr = pickle.load(f)
    f.close()
    aux1=time.perf_counter()
    content = decode(nwdic,bstr)
    aux2=time.perf_counter()
    tiempo=aux2-aux1
    print(tiempo)
    print(content)
elif opcion==4:
    generador()