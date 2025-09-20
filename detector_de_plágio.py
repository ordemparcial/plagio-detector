import re

def le_assinatura():
    '''A funcao le os valores dos tracos linguisticos do modelo e devolve uma assinatura a ser comparada com os textos fornecidos'''
    print("Bem-vindo ao detector automático de COH-PIAH.")
    print("Informe a assinatura típica de um aluno infectado:")

    wal = float(input("Entre o tamanho médio de palavra:"))
    ttr = float(input("Entre a relação Type-Token:"))
    hlr = float(input("Entre a Razão Hapax Legomana:"))
    sal = float(input("Entre o tamanho médio de sentença:"))
    sac = float(input("Entre a complexidade média da sentença:"))
    pal = float(input("Entre o tamanho medio de frase:"))

    return [wal, ttr, hlr, sal, sac, pal]

def le_textos():
    '''A funcao le todos os textos a serem comparados e devolve uma lista contendo cada texto como um elemento'''
    i = 1
    textos = []
    texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")
    while texto:
               textos.append(texto)
               i += 1
               texto = input("Digite o texto " + str(i) +" (aperte enter para sair):")

    return textos

def separa_sentencas(texto):
    '''A funcao recebe um texto e devolve uma lista das sentencas dentro do texto'''
    sentencas = re.split(r'[.!?]+', texto)
    if sentencas[-1] == '':
        del sentencas[-1]
    return sentencas

def separa_frases(sentenca):
    '''A funcao recebe uma sentenca e devolve uma lista das frases dentro da sentenca'''
    return re.split(r'[,:;]+', sentenca)

def separa_palavras(frase):
    '''A funcao recebe uma frase e devolve uma lista das palavras dentro da frase'''
    return frase.split()
def n_palavras_unicas(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras que aparecem uma unica vez'''
    freq = dict()
    unicas = 0
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            if freq[p] == 1:
                unicas -= 1
            freq[p] += 1
        else:
            freq[p] = 1
            unicas += 1

    return unicas

def n_palavras_diferentes(lista_palavras):
    '''Essa funcao recebe uma lista de palavras e devolve o numero de palavras diferentes utilizadas'''
    freq = dict()
    for palavra in lista_palavras:
        p = palavra.lower()
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    return len(freq)

def compara_assinatura(as_a, as_b):
    '''Essa funcao recebe duas assinaturas de texto e deve devolver o grau de similaridade nas assinaturas.'''
    i=0
    similaridade=[0,0,0,0,0,0]
    while i<6:
        similaridade[i]=abs(as_a[i]-as_b[i])
        i = i + 1
    similaridade_fator=0
    j=0
    while j<6:
        similaridade_fator = similaridade_fator + similaridade[j]
        j = j + 1
    similaridade = similaridade_fator / 6
    return similaridade

def palavras_na_sentenca(sentenca):
    lista=[]
    lista_frases = separa_frases(sentenca)
    for frase in lista_frases:
        lista = lista + separa_palavras(frase)
    return lista

def palavras_no_texto(texto):
    lista = []
    lista_sentencas = separa_sentencas(texto)
    for sentenca in lista_sentencas:
        lista = lista + palavras_na_sentenca(sentenca)
    return lista

def frases_no_texto(texto):
    lista=[]
    lista_sentencas = separa_sentencas(texto)
    for sentenca in lista_sentencas:
        lista = lista + separa_frases(sentenca)
    return lista

def wal(texto):
#tamanho médio das palavras
    quant_palavras = len(palavras_no_texto(texto))
    tam_palavra = 0
    for palavra in palavras_no_texto(texto):
        tam_palavra = tam_palavra + len(palavra)
    wal=tam_palavra / quant_palavras
    return wal

def ttr(texto):
#relação type-token
    quant_palavras = len(palavras_no_texto(texto))
    diferente = n_palavras_diferentes(palavras_no_texto(texto))
    ttr = diferente / quant_palavras
    return ttr

def hlr(texto):
    quant_palavras = len(palavras_no_texto(texto))    
    uma_vez = n_palavras_unicas(palavras_no_texto(texto))
    hlr = uma_vez / quant_palavras
    return hlr

def sal(texto):
    lista = separa_sentencas(texto)
    quant_sentencas = len(lista)
    tamanho = 0
    for sentenca in lista:
        tamanho = tamanho + len(sentenca)
    sal = tamanho / quant_sentencas
    return sal

def sac(texto):
    lista = separa_sentencas(texto)
    quant_sentencas = len(lista)
    quant_frases = 0
    for sentenca in lista:
        frases = separa_frases(sentenca)
        quant_frases = quant_frases + len(frases)
    sac = quant_frases / quant_sentencas
    return sac

def pal(texto):
    lista = frases_no_texto(texto)
    quant_frases = len(lista)
    tamanho = 0
    for frase in lista:
        tamanho = tamanho + len(frase)
    pal= tamanho / quant_frases
    return pal

def calcula_assinatura(texto):
    '''Essa funcao recebe um texto e deve devolver a assinatura do texto.'''
    assinatura = [wal(texto),ttr(texto),hlr(texto),sal(texto),sac(texto),pal(texto)]
    return assinatura

def avalia_textos(textos, ass_cp):
    '''Essa funcao recebe uma lista de textos e uma assinatura ass_cp e deve devolver o numero (1 a n) do texto com maior probabilidade de ter sido infectado por COH-PIAH.'''
    colou = 1
    ass = calcula_assinatura(textos[0])
    diferenca = compara_assinatura(ass,ass_cp)
    i = 2
    while i<=len(textos):
        ass = calcula_assinatura(textos[i-1])
        diferenca_nova = compara_assinatura(ass,ass_cp)
        if diferenca_nova < diferenca:
            diferenca = diferenca_nova
            colou = i
        i = i + 1
    return colou
