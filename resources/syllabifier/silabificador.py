#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
# version 1.1

# Copyright (c) 2015, Francisco Costa, João Rodrigues, João Silva and
# António Branco from the NLX-Natural Language and Speech Group of the
# Departament of Computer Science of the
# Universidade de Lisboa, Faculdade de Ciências
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must  retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of [project] nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sys
import dicionario_silabificado

VOGAIS = 'aáàâãeéêiíoóôõuúy'
ACENTUADAS = 'áâãéêíóôõú'


def vogal(letra):
    return letra in VOGAIS


def consoante(letra):
    return not vogal(letra)


def so_consoantes(string):
    return len(string) >= 1 and consoante(string[0]) and \
     (len(string) == 1 or so_consoantes(string[1:]))


def digrafo(letras):
    return letras == 'nh' or \
           letras == 'lh' or \
           letras == 'ch' or \
           letras == 'sh' or \
           letras == 'ts' or \
           letras == 'ph' or \
           letras == 'th'


def ditongo(duasletras):
    return len(duasletras) == 2 and \
           vogal(duasletras[0] or duasletras[0] in 'yw') and \
           vogal(duasletras[1]) and \
           (duasletras[1] in 'iuyw' and
            duasletras[0] != duasletras[1] or
            duasletras[0] in 'yw' and
            duasletras[0] != duasletras[1] or
            duasletras == 'ão' or
            duasletras == 'ãe' or
            duasletras == 'õe')


def muta(letra):
    return letra in 'pbtdcgfv'


def liquida(letra):
    return letra in 'rl'


def silabifica(palavra):
    """ Exemplos:
      sei|xo
      qua|se
      a|de|quar
      a|de|qú|e
      a|tra|sa|do
      tes|te
      tem|po
      es|com|bro
      sols|tí|ci|o
      pers|pec|ti|va
      fac|to
      cep|tro
      se|nha
      ra|i|nha
      ca|ir
      pa|ul

      LIMITAÇÃO, não distingue:
      re|u|nir de reu|má|ti|co,
      sa|u|dar (cf. sa|ú|da) de cau|sar (cf. cau|sa),
      fa|is|car (cf. fa|ís|ca) de bai|xar (cf. bai|xa)
      pro|i|bir (cf. pro|í|be) de poi|sar (cf. poi|sa)

      LIMITAÇÃO 2, não distingue:
      Cae|ta|no de pa|e|lha,
      nem |Mao| (Mao Tse Tung) de Ma|o|ri

      LIMITAÇÃO 3: não lida com hífens
    """

    # 0. Substituir "qu" por "ŕ"
    #    Substituir "gu" antes de vogal por "ṕ"; e "wh" por "ẃ"
    palavra = palavra.replace('q', 'ŕ').replace('wh', 'ẃ')
    for vog in VOGAIS:
        palavra = palavra.replace('g' + vog, 'ṕ' + vog)

    # 1. Fronteira de sílaba a seguir a cada vogal
    pal = '|'
    for i in range(len(palavra)):

        pal += palavra[i]
        if vogal(palavra[i]):
            pal += '|'
    palavra = pal

    # 2. Colocar consoantes em final de palavra numa sílaba
    pal = ''
    for i in range(len(palavra)):
        if palavra[i] == '|' and \
           i + 1 < len(palavra) and \
           so_consoantes(palavra[i + 1:]):

            palavra = palavra[:i] + \
                       palavra[i + 1] + \
                       palavra[i] + \
                       palavra[i + 2:]

    # 3. Remover fronteiras de sílaba quando há ditongos
    for i in range(len(palavra)):
        if i + 2 < len(palavra) and ditongo(palavra[i] + palavra[i + 2]):

            # Em "baiuca", "iu" não é ditongo porque "ai" é;
            # manter fronteira entre "ai" e "u"
            if i == 0 or not ditongo(palavra[i - 1] + palavra[i]):
                # Em certas palavras relacionadas com verbos em "-uir"
                # (ex: "destruir")
                # o "ui" nunca é ditongo. É o caso de palavras formadas pelos
                # sufixos:"ção"; "dor"; "tivo", ...
                #
                # Com nomes em -idade derivados de adjetivos parece acontecer o
                # mesmo: contínuo <-> continuidade
                if palavra[i] + palavra[i+2] != 'ui' or \
                   palavra[i + 3:].replace('|', '') not in \
                   ['ção', 'ções', 'dor', 'dores', 'dora', 'doras',
                    'doramente', 'tivo', 'tiva', 'tivos', 'tivas',
                    'tivamente', 'damente', 'dade', 'dades', 'tário',
                   'tária', 'tários', 'tárias']:

                    # O mesmo para -mento a seguir a "oi" (cf. depoimento)
                    if palavra[i] + palavra[i+2] != 'oi' or \
                       palavra[i + 3:].replace('|', '') not in \
                       ['mento', 'mentos']:

                        # O mesmo para -damente a seguir a "ai"
                        # (cf. retraidamente)
                        if palavra[i] + palavra[i+2] != 'ai' or \
                           palavra[i + 3:].replace('|', '') not in \
                           ['damente']:

                            # O mesmo para -ficar, -ficação, -cultor, -cultura
                            # a seguir a "ei" (cf. gaseificação)
                            if palavra[i] + palavra[i+2] != 'ei' or \
                               palavra[i + 3:].replace('|', '') not in \
                               ['cultor', 'cultores', 'cultora',
                                'cultoras', 'cultura', 'culturas',
                                'ficação', 'ficações', 'ficar', 'fico',
                                'ficas', 'fica', 'ficamos', 'ficais',
                                'ficam', 'ficava', 'fiavas', 'ficávamos',
                                'ficáveis', 'ficavam', 'fiquei', 'ficaste',
                                'fico', 'ficámos', 'ficastes', 'ficaram',
                                'ficara', 'ficaras', 'ficáramos',
                                'ficáreis', 'ficarei', 'ficarás', 'ficará',
                                'ficaremos', 'ficareis', 'ficarão',
                                'ficaria', 'ficarias', 'ficaríamos',
                                'ficaríeis', 'ficariam', 'fique', 'fiques',
                                'fiquemos', 'fiqueis', 'fiquem', 'ficasse',
                                'ficasses', 'ficássemos', 'ficásseis',
                                'ficassem', 'ficares', 'ficarmos',
                                'ficardes', 'ficarem', 'ficando', 'ficado',
                               'ficada', 'ficados', 'ficadas']:

                                palavra = palavra[:i + 1] + palavra[i + 2:]
                                i = i - 1

    # 4. Separar sequências de consoantes, exceto "muta cum liquida"
    # e dígrafos (nh, lh, ch)
    for i in range(len(palavra)):
        if sum([vogal(letra) for letra in palavra[:i]]) and \
           i + 2 < len(palavra) and \
           palavra[i] == '|' and \
           consoante(palavra[i + 1]) and \
           consoante(palavra[i + 2]) and \
           not (muta(palavra[i + 1]) and liquida(palavra[i + 2])) and \
           not digrafo(palavra[i + 1] + palavra[i + 2]):

            palavra = palavra[:i] + palavra[i + 1] + "|" + palavra[i + 2:]

    # 5. "u" e "i" não fazem ditongo com vogal anterior se antes de "nh" ou se
    # antes de um "r" ou "l" ou "z" ou nasal em final de sílaba
    # ex: |ra|i|nha|, |pa|ul|, |ca|ir|, |re|im|pri|mir
    # mas: |bair|ris|ta|  |brail|le|
    # Nestes casos repor fronteira de sílaba
    pal = ''
    for i in range(len(palavra)):

        pal += palavra[i]
        if (pal[-1] == "u" or pal[-1] == 'i') and \
           len(pal) >= 2 and \
           ditongo(pal[-2] + pal[-1]):

            if i + 3 < len(palavra) and \
               palavra[i + 1] == '|' and \
               palavra[i+2] == 'n' and \
               palavra[i + 3] == 'h':

                pal = pal[:-1] + '|' + pal[-1]

            if i + 1 < len(palavra) and \
               (palavra[i + 1] == 'r' or
                palavra[i + 1] == 'l' or
                palavra[i + 1] == 'z' or
                palavra[i + 1] == 'm' or
                palavra[i + 1] == 'n') and \
               so_consoantes(palavra[i+1:][:palavra[i+1:].find('|')]):

                if palavra[i + 1] == 'r' and \
                    i + 3 < len(palavra) and \
                    palavra[i + 2] == '|' and \
                   palavra[i + 3] == 'r':

                    pass

                else:

                    if palavra[i + 1] == 'l' and \
                        i + 3 < len(palavra) and \
                        palavra[i + 2] == '|' and \
                       palavra[i + 3] == 'l':

                        pass

                    else:
                        pal = pal[:-1] + '|' + pal[-1]

    palavra = pal

    # 6. dividir água em á|gu|a
    # O acento ajuda-nos a fazer esta divisão;
    # sem acento antes não dá para saber qual a divisão correta
    pal = ""
    for i in range(len(palavra)):
        pal += palavra[i]

        if palavra[i] in 'ŕṕ' and \
           i > 0 and '|' in palavra[:i]:

            contem_acento = False
            silaba_anterior = palavra[:i]

            if '|' in silaba_anterior:
                silaba_anterior = silaba_anterior[:silaba_anterior.rfind('|')]
            if '|' in silaba_anterior:
                silaba_anterior = silaba_anterior[silaba_anterior.rfind('|')
                                                  + 1:]
            if '-' in silaba_anterior:
                silaba_anterior = silaba_anterior[silaba_anterior.find('-')
                                                  + 1:]
            for vogal_acentuada in ACENTUADAS:
                if vogal_acentuada in silaba_anterior:
                    contem_acento = True

            resto = palavra[i + 1:-1]
            if resto.endswith('s'):
                resto = resto[:-1]
            if contem_acento and len(resto) == 1 and vogal(resto):
                pal += '|'

    palavra = pal

    # 6. Finalmente: substituir "ŕ" por "qu" e "ṕ" por "gu"
    palavra = palavra.replace('ŕ', 'q')
    palavra = palavra.replace('ṕ', 'g')
    palavra = palavra.replace('ẃ', 'wh')

    return palavra


def minusculas(string):

    result = string.lower()
    for letra, subst in zip('ÁÀÂÃÉÊÍÓÕÚÇ', 'áàâãéêíóõúç'):
        result = result.replace(letra, subst)
    return result

#if __name__ == "__main__":
def main():
    #file = open("silabificador.log", "a")
    #txt = sys.argv[1]
    #file.write(txt + "\n")
    txt = 'Este é um teste.'
    if len(txt):
        #if len(sys.argv) > 1:
        #txt = sys.argv[1:]
        #txt = 'Este é um teste.'
        for palavra in txt.split(" "):
            # verifica se é uma palavra que não é correctamente silabificada
            exception = dicionario_silabificado.check(palavra.lower())
            if exception is not False:
                print(exception)
                continue

            if len(palavra) == 1:
                print(palavra)
            else:
                p = palavra

                resultado = silabifica(minusculas(p))
                resultado = resultado[1:len(resultado)-1]

                resultado = resultado.replace('!', ' !')
                resultado = resultado.replace('?', ' ?')
                resultado = resultado.replace(';', ' ;')
                resultado = resultado.replace(',', ' ,')
                resultado = resultado.replace(':', ' :')
                resultado = resultado.replace('.', ' .')

                if palavra[0] == palavra[0].upper():
                    print(resultado.capitalize())
                else:
                    print(resultado)
#main()
