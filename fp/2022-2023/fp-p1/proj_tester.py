import pytest
import importlib.util
import sys
import requests
import copy
import os
import subprocess

if len(sys.argv) < 2:
    print(
        "Por favor escreve o caminho para o ficheiro: python proj_tester.py caminho/para/projeto.py"
    )
    exit(1)

file_name = sys.argv[1]

print("A ler ficheiro", file_name)

# Import project file and save all functions to the object variable "target"
target_spec = importlib.util.spec_from_loader("target", loader=None)
target = importlib.util.module_from_spec(target_spec)
exec(open(file_name, encoding="utf-8").read(), target.__dict__)


class TestJustificarTextos:

    # Limpa_texto
    # Forma geral
    def test_limpa_texto1(self):
        assert ('Fundamentos da Programacao' == target.limpa_texto(
            '  Fundamentos\n\tda      Programacao\n'))

    # Com espaços no final e \v, \f e \r
    def test_limpa_texto2(self):
        assert ('Fundamentos da Programacao' == target.limpa_texto(
            '  Fundamentos\v\fda      Programacao\r         '))

    def test_limpa_texto3(self):
        assert ('A B C D E F G' == target.limpa_texto(
            '\t\n\v\f\r A\t B\nC\vD \fE\rF G\r \f\n \v'))

    # Testar com caracteres brancos no meio da frase
    def test_limpa_texto4(self):
        assert ('Fundamentos da Program acao' == target.limpa_texto(
            '  Fundamentos\v\fda      Program\nacao\r         '))

    # Verificar que sobrevive uma string vazia
    def test_limpa_texto5(self):
        assert ('' == target.limpa_texto(''))

    # Corta Texto
    # Forma geral
    def test_corta_texto1(self):
        assert ('Fundamentos da', 'Programacao') == target.corta_texto(
            'Fundamentos da Programacao', 15)

    # 'Fundamentos da' -> tem 14 letras
    # Verifica se o utilizador conta com o espaço quando está a inserir
    def test_corta_texto2(self):
        assert ('Fundamentos', 'da Programacao') == target.corta_texto(
            'Fundamentos da Programacao', 13)
        
    # Verifica o texto no caso de ter uma palavra da segunda cadeia que ainda cabe na primeira
    def test_corta_texto3(self):
        assert ('Computers are incredibly fast, accurate and stupid. Human beings are incredibly slow', 'inaccurate, and brilliant. Together they are powerful beyond imagination.') == target.corta_texto("Computers are incredibly fast, accurate and stupid. Human beings are incredibly slow inaccurate, and brilliant. Together they are powerful beyond imagination.", 95)

    # Verifica se o utilizador consegue inserir espaços de forma uniforme
    def test_insere_espacos1(self):
        assert 'Fundamentos  da Programacao!!!' == target.insere_espacos(
            'Fundamentos da Programacao!!!', 30)

    # Verifica se o utilizador insere mais do que 2 espaços seguidos se for preciso
    def test_insere_espacos2(self):
        assert 'Fundamentos       da      Programacao!!!' == target.insere_espacos(
            'Fundamentos da Programacao!!!', 40)

    # Verifica se o utilizador consegue fazer com textos maiores que 3 palavras
    def test_insere_espacos3(self):
        assert 'Lorem  Ipsum  is  simply  dummy  text  of  the  printing and typesetting industry.' == target.insere_espacos(
            'Lorem Ipsum is simply dummy text of the printing and typesetting industry.', 82)

    # Verifica se o utilizador insere espaços quando só existem duas palavras
    def test_insere_espacos4(self):
        assert 'Lorem       Ipsum' == target.insere_espacos('Lorem Ipsum', 17)

    # Verifica se o utilizador insere espaços uniformes, caso seja preciso
    def test_insere_espacos5(self):
        assert 'Lorem  Ipsum  is  simply  dummy' == target.insere_espacos(
            'Lorem Ipsum is simply dummy', 31)

    # Verifica se o utilizador insere espaços só para a frente da palavra, mesmo que só seja uma letra
    def test_insere_espacos6(self):
        assert '?    ' == target.insere_espacos('?', 5)

    # Verifica se o utilizador insere espaços só para a frente da palavra
    def test_insere_espacos7(self):
        assert 'Fundamentos    ' == target.insere_espacos('Fundamentos', 15)

    # Verifica se o utilizador formata o texto pedido no pdf
    def test_justifica_texto1(self):
        cad = ('Computers are incredibly  \n\tfast,     \n\t\taccurate'
               ' \n\t\t\tand  stupid.   \n    Human beings are incredibly  slow  '
               'inaccurate, and brilliant. \n     Together  they  are powerful   '
               'beyond imagination.')

        ref = ('Computers  are  incredibly  fast, accurate and stupid. Human',
               'beings   are  incredibly  slow  inaccurate,  and  brilliant.',
               'Together they are powerful beyond imagination.              ')
        assert ref == target.justifica_texto(cad, 60)

    def test_justifica_texto2(self):
        cad = ('Computers are incredibly  \n\tfast,     \n\t\taccurate')
        ref = ('Computers are incredibly fast, accurate           ',)
        assert ref == target.justifica_texto(cad, 50)

    # Verifica se o utilizador formata cadeias com segmentos internos de comprimento igual à largura de coluna
    def test_justifica_texto3(self):
        cad = ('123456 123')
        ref = ('123456', '123   ')
        assert ref == target.justifica_texto(cad, 6)

    # levantar erro se primeiro argumento não é uma lista não vazia, ou o segundo não é um número inteiro positivo
    # ou existe uma palavra maior que o tamanho pretendido
    def test_justifica_texto_error1(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto('', 60)

    def test_justifica_texto_error2(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto('Fundamentos', "Banana")

    def test_justifica_texto_error3(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto(89, 60)

    def test_justifica_texto_error4(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto('Texto', -10)

    def test_justifica_texto_error5(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto('Otorrinolaringologista', 10)

    def test_justifica_texto_error6(self):
        with pytest.raises(ValueError, match='justifica_texto: argumentos invalidos'):
            target.justifica_texto('123456 123', 4)


class TestMetodoHondt:

    def test_calcula_quocientes1(self):

        ref = {'A': [12000.0, 6000.0, 4000.0, 3000.0, 2400.0, 2000.0, 12000/7],
               'B': [7500.0, 3750.0, 2500.0, 1875.0, 1500.0, 1250.0, 7500/7],
               'C': [5250.0, 2625.0, 1750.0, 1312.5, 1050.0, 875.0, 750.0],
               'D': [3000.0, 1500.0, 1000.0, 750.0, 600.0, 500.0, 3000/7]}

        hyp = target.calcula_quocientes(
            {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}, 7)

        assert ref == hyp

    def test_atribui_mandatos1(self):
        ref = ['A', 'B', 'A', 'C', 'A', 'B', 'D']
        assert ref == target.atribui_mandatos(
            {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}, 7)

    def test_atribui_mandatos2(self):
        ref = ['A', 'B', 'A', 'C', 'A', 'B', 'D']
        assert ref == target.atribui_mandatos(
            {'D': 3000, 'B': 7500, 'C': 5250, 'A': 12000}, 7)

    def test_obtem_partidos1(self):
        info = {
            'Endor':   {'deputados': 7,
                        'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
            'Hoth':    {'deputados': 6,
                        'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
            'Tatooine': {'deputados': 3,
                         'votos': {'A': 3000, 'B': 1900}}}

        ref = ['A', 'B', 'C', 'D', 'E']

        assert ref == target.obtem_partidos(info)

    def test_obtem_resultado_eleicoes1(self):
        info = {
            'Endor':   {'deputados': 7,
                        'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
            'Hoth':    {'deputados': 6,
                        'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
            'Tatooine': {'deputados': 3,
                         'votos': {'A': 3000, 'B': 1900}}}
        ref = [('A', 7, 24000), ('B', 6, 20900),
               ('C', 1, 5250), ('E', 1, 5000), ('D', 1, 4500)]

        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes2(self):
        info = {
            'Endor':   {'deputados': 12,
                        'votos': {'A': 117542, 'B': 79123, 'C': 47887, 'D': 28991}},
            'Hoth':    {'deputados': 4,
                        'votos': {'B': 47800, 'A': 56000, 'E': 12877, 'D': 28000}}}
        ref = [('A', 7, 173542), ('B', 5, 126923),
               ('D', 2, 56991), ('C', 2, 47887), ('E', 0, 12877)]

        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes3(self):
        ref = [('bb', 2, 175000), ('BB', 2, 120000), ('D', 1, 93000), ('C', 0, 45000)] 
        info = {'Tatooine': {'deputados': 5, 'votos': {'BB': 120000, 'bb': 175000, 'C': 45000, 'D': 93000}}}
        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultados_eleicoes4(self):
        ref = [('PS', 21, 482606), ('PSD', 13, 285522), ('IL', 4, 93341), ('CH', 4, 91889), ('PCP', 2, 59995), ('BE', 2, 55786), ('L', 1, 28834), ('PAN', 1, 23577), ('CDS', 0, 19524)] 
        info = {'Lisboa': {'deputados': 48, 'votos': {'PS': 482606, 'PSD': 285522, 'IL': 93341, 'CH': 91889, 'PCP': 59995, 'BE': 55786, 'L': 28834, 'PAN': 23577, 'CDS': 19524}}} 
        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultados_eleicoes5(self):
        ref = [('PS', 19, 418869), ('PSD', 14, 318343), ('IL', 2, 50359), ('BE', 2, 47118), ('CH', 2, 42998), ('PCP', 1, 32277), ('PAN', 0, 16707), ('CDS', 0, 14347), ('L', 0, 11433)] 
        info = {'Porto': {'deputados': 40, 'votos': {'PS': 418869, 'PSD': 318343, 'IL': 50359, 'BE': 47118, 'CH': 42998, 'PCP': 32277, 'PAN': 16707, 'CDS': 14347, 'L': 11433}}} 
        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultados_eleicoes6(self):
        ref = [('PS', 5, 89870), ('PSD', 3, 58630), ('CH', 1, 23813), ('PCP', 0, 11854), ('BE', 0, 10012)] 
        info = {'Santarem': {'deputados': 9, 'votos': {'PS': 89870, 'PSD': 58630, 'CH': 23813, 'PCP': 11854, 'BE': 10012}}} 
        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultados_eleicoes7(self):
        ref = [('PS', 45, 991345), ('PSD', 30, 662495), ('CH', 7, 158700), ('IL', 6, 143700), ('BE', 4, 112916), ('PCP', 3, 104126), ('PAN', 1, 40284), ('L', 1, 40267), ('CDS', 0, 33871)] 
        info = {'Lisboa': {'deputados': 48, 'votos': {'PS': 482606, 'PSD': 285522, 'IL': 93341, 'CH': 91889, 'PCP': 59995, 'BE': 55786, 'L': 28834, 'PAN': 23577, 'CDS': 19524}}, 'Santarem': {'deputados': 9, 'votos': {'PS': 89870, 'PSD': 58630, 'CH': 23813, 'PCP': 11854, 'BE': 10012}}, 'Porto': {'deputados': 40, 'votos': {'PS': 418869, 'PSD': 318343, 'IL': 50359, 'BE': 47118, 'CH': 42998, 'PCP': 32277, 'PAN': 16707, 'CDS': 14347, 'L': 11433}}} 
        assert ref == target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error1(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error2(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 0,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error3(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = 13
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error4(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 0, 'B': 0, 'C': 0, 'D': 0}},
                'Hoth':    {'deputados': 3,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error5(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {}},
                'Hoth':    {'deputados': 3,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error6(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {'Endor': 15}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error7(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': "não é número inteiro",
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 3,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error8(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7},
                'Hoth':    {'deputados': 3,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error9(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 3,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}}, }
            target.obtem_resultado_eleicoes(info)

    # Verificar que o programa gera Value Error no caso de argumentos não válidos com a mensagem correta
    # LISTA DE TESTES:
    #       -> Verificar se o argumento é do tipo DICT                                     (10)
    #       -> Verificar se o argumento está vazio                                         (11)
    #       -> Verificar se o dicionario dos votos está vazio                              (12)
    #       -> Verificar os nomes das keys (VOTOS, DEPUTADOS)                              (13, 14)
    #       -> Verificar se o valor de (DEPUTADOS, VOTOS) são do tipo correto (INT, DICT)  (15, 16)
    #       -> Verificar se o valor de votos de cada partido é do tipo correto INT         (17)
    #       -> Verificar se o valor de votos for negativo e valor de deputados for 0
    #          ou inferior                                                                 (18, 19)
    #       -> Verificar se existir um circulo eleitoral com 0 votos totais                (20)
    #       -> Verificar se falta a key VOTOS ou a key DEPUTADOS                           (21, 22)
    #       -> Verificar se a key correspondente aos numeros de votos é do tipo
    #           correto STR                                                                (23)

    def test_obtem_resultado_eleicoes_error10(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            target.obtem_resultado_eleicoes('deez nuts')

    def test_obtem_resultado_eleicoes_error11(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            target.obtem_resultado_eleicoes({})

    def test_obtem_resultado_eleicoes_error12(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error13(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'xxx': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error14(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'xxx': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error15(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 'zero',
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error16(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': 'zero'},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error17(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 'zero', 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error18(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': -69, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error19(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 0,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error20(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 0, 'B': 0, 'C': 0, 'D': 0}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error21(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error22(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    def test_obtem_resultado_eleicoes_error23(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {69: 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    # Ver se existe algum numero de deputados que não seja inteiro
    def test_obtem_resultado_eleicoes_error24(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 4.5,
                            'votos': {"A": 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    # Ver se existe algum numero de votos que não seja inteiro
    def test_obtem_resultado_eleicoes_error25(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
                'Endor':   {'deputados': 7,
                            'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
                'Hoth':    {'deputados': 6,
                            'votos': {"A": 9000.4, 'B': 11500, 'D': 1500, 'E': 5000}},
                'Tatooine': {'deputados': 3,
                             'votos': {'A': 3000, 'B': 1900}}}
            target.obtem_resultado_eleicoes(info)

    #################################################################
    # os dicionarios de entrada das funções não devem ser alterados #
    #################################################################

    def test_calcula_quocientes_alteracao_dicionarios(self):
        dicionario = {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}
        copia_dicionario = copy.deepcopy(dicionario)

        target.calcula_quocientes(
            {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}, 7)
        assert dicionario == copia_dicionario

    def test_atribui_mandatos_alteracao_dicionarios(self):
        dicionario = {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}
        copia_dicionario = copy.deepcopy(dicionario)

        target.atribui_mandatos(dicionario, 7)
        assert dicionario == copia_dicionario

    def test_obtem_partidos_alteracao_dicionarios(self):
        dicionario = {
            'Endor':   {'deputados': 7,
                        'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
            'Hoth':    {'deputados': 6,
                        'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
            'Tatooine': {'deputados': 3,
                         'votos': {'A': 3000, 'B': 1900}}}
        copia_dicionario = copy.deepcopy(dicionario)

        target.obtem_partidos(dicionario)
        assert dicionario == copia_dicionario

    def test_obtem_resultado_eleicoes_alteracao_dicionarios(self):
        dicionario = {
            'Endor':   {'deputados': 7,
                        'votos': {'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}},
            'Hoth':    {'deputados': 6,
                        'votos': {'A': 9000, 'B': 11500, 'D': 1500, 'E': 5000}},
            'Tatooine': {'deputados': 3,
                         'votos': {'A': 3000, 'B': 1900}}}
        copia_dicionario = copy.deepcopy(dicionario)

        target.obtem_resultado_eleicoes(dicionario)
        assert dicionario == copia_dicionario



class TestSistemasLineares:

    def test_produto_interno1(self):
        assert target.produto_interno(
            (1, 2, 3, 4, 5), (-4, 5, -6, 7, -8)) == -24.0

    def test_produto_interno_type(self):
        assert isinstance(target.produto_interno(
            (1, 2, 3, 4, 5), (-4, 5, -6, 7, -8)), float)
            
    def test_verifica_convergencia1(self):
        assert target.verifica_convergencia(
            ((1, -0.5), (-1, 2)), (-0.4, 1.9), (0.1001, 1), 0.00001) == False

    def test_verifica_convergencia2(self):
        assert target.verifica_convergencia(
            ((1, -0.5), (-1, 2)), (-0.4, 1.9), (0.1001, 1), 0.001) == True

    def test_retira_zeros_diagonal1(self):
        assert target.retira_zeros_diagonal(((0, 1, 1), (1, 0, 0), (0, 1, 0)), (1, 2, 3)) == (
            ((1, 0, 0), (0, 1, 0), (0, 1, 1)), (2, 3, 1))

    def test_eh_diagonal_dominante1(self):
        assert target.eh_diagonal_dominante(
            ((1, 2, 3, 4, 5), (4, -5, 6, -7, 8), (1, 3, 5, 3, 1), (-1, 0, -1, 0, -1), (0, 2, 4, 6, 8))) == False

    def test_eh_diagonal_dominante2(self):
        assert target.eh_diagonal_dominante(
            ((1, 0, 0), (0, 1, 0), (0, 1, 1))) == True

    def test_resolve_sistema1(self):
        def equal(x, y):
            delta = 1e-10
            return all(abs(x[i]-y[i]) < delta for i in range(len(x)))

        A4, c4 = ((2, -1, -1), (2, -9, 7), (-2, 5, -9)), (-8, 8, -6)
        ref = (-4.0, -1.0, 1.0)

        assert equal(target.resolve_sistema(A4, c4, 1e-20), ref)

    def test_resolve_sistema2(self):
        def equal(x, y):
            delta = 1e-10
            return all(abs(x[i]-y[i]) < delta for i in range(len(x)))

        A4, c4 = ((2.0, -1.0, -1.0), (2.0, -9.0, 7.0), (-2.0, 5.0, -9.0)), (-8.0, 8.0, -6.0)
        ref = (-4.0, -1.0, 1.0)

        assert equal(target.resolve_sistema(A4, c4, 1e-20), ref)


    # Verificar que o programa gera Value Error no caso de argumentos não válidos com a mensagem correta
    # LISTA DE TESTES:
    #       -> Verificar se os argumentos são respetivamente:
    #               1 -> Matriz
    #                   a) -> é do tipo tuplo                                           (1, 2)
    #                   b) -> todos os elementos são tuplos                             (3, 4)
    #                   c) -> todos os elementos dos elementos são ints ou floats       (5)
    #                   d) -> todos os elementos têm o mesmo tamanho                    (6)
    #                   e) -> é quadrada                                                (7, 8)
    #                   f) -> é não vazia                                               (9)
    #               2 -> Constante
    #                   a) -> é do tipo tuplo                                           (10, 11)
    #                   b) -> todos os elementos são ints ou floats                     (12)
    #                   c) -> tem o mesmo número de linhas que a matriz                 (13, 14)
    #                   d) -> é não vazia                                               (15)
    #               3 -> Precisão
    #                   a) -> é do tipo int ou float                                    (16, 17)
    #                   b) -> é maior que 0                                             (18, 19)
    #
    #       -> A diagonal é dominante                                                   (20)

    def test_resolve_sistema_error1(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(18, (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error2(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema("O panda é fixe!", (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error3(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), 456), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error4(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), "456"), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error5(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), ("15", 5, -9)), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error6(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9), (2, 5, -9)), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error7(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1, 0), (2, -9, 7, 0), (2, 5, -9, 0)), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error8(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1, 0), (2, -9, 7, 0), (2, 5, -9, 0)), (-8, 8, -6, 2), 1e-20)

    def test_resolve_sistema_error9(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema((), (-8, 8, -6), 1e-20)

    def test_resolve_sistema_error10(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), 15, 1e-20)

    def test_resolve_sistema_error11(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), "Str", 1e-20)

    def test_resolve_sistema_error12(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, "8", -6), 1e-20)

    def test_resolve_sistema_error13(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8), 1e-20)

    def test_resolve_sistema_error14(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8, -6, 9), 1e-20)

    def test_resolve_sistema_error15(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (), 1e-20)

    def test_resolve_sistema_error16(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8, -6), "2")

    def test_resolve_sistema_error17(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8, -6), None)

    def test_resolve_sistema_error18(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8, -6), 0)

    def test_resolve_sistema_error19(self):
        with pytest.raises(ValueError, match='resolve_sistema: argumentos invalidos'):
            target.resolve_sistema(((2, -1, -1), (2, -9, 7), (2, 5, -9)), (-8, 8, -6), -1e-20)

    def test_resolve_sistema_error20(self):
        with pytest.raises(ValueError, match='resolve_sistema: matriz nao diagonal dominante'):
            target.resolve_sistema(((0, 0, 0), (0, 0, 0), (0, -1, 0)), (-8, 8, -6), 1e-20)

#######################################################
# Logic to handle updates automatically. DO NOT TOUCH #
#######################################################


def get_lastest_commit_hash():
    try:
        result = requests.get(
            "https://api.github.com/repos/diogotcorreia/proj-ist-unit-tests/commits?path=fp%2F2022-2023%2Ffp-p1%2Fproj_tester.py&page=1&per_page=1"
        )
        return result.json()[0]["sha"]
    except:
        print(
            "Não foi possível verificar novas atualizações (o GitHub apenas permite 60 verificações por hora)"
        )


def get_saved_commit_hash():
    try:
        return open(".update_lock").read()
    except:
        return False


def is_under_git_control():
    try:
        repo_dir = os.path.dirname(__file__)

        command = ['git', 'rev-parse', '--is-inside-work-tree']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=repo_dir, universal_newlines=True)
        process_output = process.communicate()[0]

        is_git_repo = str(process_output.strip())

        if is_git_repo == "true":
            print("This file is under Git version control, skipping auto update.")
            print("Use `git pull` to manually update!")
            return True
    except:
        return False
    return False


def check_for_updates():
    if is_under_git_control():
        return

    saved_hash = get_saved_commit_hash()
    latest_hash = get_lastest_commit_hash()

    if not latest_hash:
        return

    if saved_hash:
        if saved_hash == latest_hash:
            return
        print("Foi encontrada uma nova atualização aos testes.")
    else:
        print("Esta é a primeira vez que estás a correr o programa.")

    print(
        "Esta operação irá substituir o teu ficheiro local com a nova versão, apagando quaisqueres alterações que tenham sido feitas aos testes locais."
    )
    print("Desejas atualizar dos testes? [y/N]")
    response = input()
    if response.lower() == "y":
        update_files(latest_hash)
    else:
        print("Os testes não foram atualizados a pedido do utilizador")


def update_files(new_hash):
    print("A atualizar os testes...")
    open(".update_lock", "w+").write(new_hash)

    new_file = requests.get(
        "https://raw.githubusercontent.com/diogotcorreia/proj-ist-unit-tests/master/fp/2022-2023/fp-p1/proj_tester.py"
    )
    open("proj_tester.py", "w+", encoding="utf-8").write(new_file.text)

    print("Volta a executar o programa para carregar os novos testes")
    exit()


if __name__ == "__main__":
    check_for_updates()
    pytest.main(sys.argv[:1] + sys.argv[2:])
