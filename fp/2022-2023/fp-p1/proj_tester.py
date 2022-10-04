import pytest
import importlib.util
import sys
import requests

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

class TestPublicJustificarTextos:
    def test_limpa_texto1(self):
        assert ('Fundamentos da Programacao' == target.limpa_texto('  Fundamentos\n\tda      Programacao\n'))


    def test_corta_texto1(self):
        assert ('Fundamentos da', 'Programacao') == target.corta_texto('Fundamentos da Programacao', 15)


    def test_insere_espacos1(self):
        assert 'Fundamentos  da Programacao!!!' == target.insere_espacos('Fundamentos da Programacao!!!', 30)

    def test_insere_espacos2(self):
        assert 'Fundamentos       da      Programacao!!!' == target.insere_espacos('Fundamentos da Programacao!!!', 40)

    def test_insere_espacos3(self):
        assert 'Fundamentos    ' == target.insere_espacos('Fundamentos', 15)


    def test_justifica_texto1(self):

        cad = ('Computers are incredibly  \n\tfast,     \n\t\taccurate'
            ' \n\t\t\tand  stupid.   \n    Human beings are incredibly  slow  '
            'inaccurate, and brilliant. \n     Together  they  are powerful   ' 
            'beyond imagination.')

        ref = ('Computers  are  incredibly  fast, accurate and stupid. Human',
            'beings   are  incredibly  slow  inaccurate,  and  brilliant.',
            'Together they are powerful beyond imagination.              ')
        assert ref == target.justifica_texto(cad, 60)

    # levantar erro se primeiro argumento não é uma lista não vazia, ou o segundo não é um número inteiro positivo
    # ou existe uma palavra maior que o tamanho pretendido
    def test_justifica_texto2(self):
        with pytest.raises(ValueError, match='justifica texto: argumentos invalidos'):
            target.justifica_texto('', 60)

    def test_justifica_texto3(self):
        with pytest.raises(ValueError, match='justifica texto: argumentos invalidos'):
            target.justifica_texto('Fundamentos', "Banana")
    
    def test_justifica_texto4(self):
        with pytest.raises(ValueError, match='justifica texto: argumentos invalidos'):
            target.justifica_texto(89, 60)

    def test_justifica_texto5(self):
        with pytest.raises(ValueError, match='justifica texto: argumentos invalidos'):
            target.justifica_texto('Texto', -10)
    
    def test_justifica_texto6(self):
        with pytest.raises(ValueError, match='justifica texto: argumentos invalidos'):
            target.justifica_texto('Otorrinolaringologista', 10)
    


class TestPublicMetodoHondt:

    def test_calcula_quocientes1(self):

        ref =  {'A': [12000.0, 6000.0, 4000.0, 3000.0, 2400.0, 2000.0, 12000/7],
                    'B': [7500.0, 3750.0, 2500.0, 1875.0, 1500.0, 1250.0, 7500/7],
                    'C': [5250.0, 2625.0, 1750.0, 1312.5, 1050.0, 875.0, 750.0],
                    'D': [3000.0, 1500.0, 1000.0, 750.0, 600.0, 500.0, 3000/7]}

        hyp = target.calcula_quocientes({'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}, 7)
        
        assert ref == hyp


    def test_atribui_mandatos1(self):
        ref = ['A', 'B', 'A', 'C', 'A', 'B', 'D']
        assert ref == target.atribui_mandatos({'A': 12000, 'B': 7500, 'C': 5250, 'D': 3000}, 7)

    def test_atribui_mandatos2(self):
        ref = ['A', 'B', 'A', 'C', 'A', 'B', 'D']
        assert ref == target.atribui_mandatos({'D': 3000, 'B': 7500, 'C': 5250, 'A': 12000}, 7)


    def test_obtem_partidos1(self):
        info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}

        ref = ['A', 'B', 'C', 'D', 'E']
        
        assert ref == target.obtem_partidos(info)


    def test_obtem_resultado_eleicoes1(self):
        info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
        ref = [('A', 7, 24000), ('B', 6, 20900), ('C', 1, 5250), ('E', 1, 5000), ('D', 1, 4500)]
        
        assert ref == target.obtem_resultado_eleicoes(info)
        
    def test_obtem_resultado_eleicoes2(self):
        info = {
            'Endor':   {'deputados': 12,
                        'votos': {'A':117542, 'B':79123, 'C':47887, 'D':28991}},
            'Hoth':    {'deputados': 4,
                        'votos': {'B':47800, 'A':56000, 'E':12877, 'D':28000}}}
        ref = [('A', 7, 173542), ('B', 5, 126923), ('D', 2, 56991), ('C', 2, 47887), ('E', 0, 12877)]
        
        assert ref == target.obtem_resultado_eleicoes(info)
      
    # Verificar que o programa gera Value Error no caso de argumentos não válidos
    # LISTA DE TESTES:
    #       -> Verificar se o argumento é do tipo DICT                                     (3)
    #       -> Verificar se o argumento está vazio                                         (4)
    #       -> Verificar se o dicionario dos votos está vazio                              (5)
    #       -> Verificar os nomes das keys (VOTOS, DEPUTADOS)                              (6, 7)
    #       -> Verificar se o valor de (DEPUTADOS, VOTOS) são do tipo correto (INT, DICT)  (8, 9)
    #       -> Verificar se o valor de votos de cada partido é do tipo correto INT         (10)
    #       -> Verificar se o valor de votos for negativo e valor de deputados for 0       
    #          ou inferior                                                                 (11, 12)
    #       -> Verificar se existir um circulo eleitoral com 0 votos totais                (13)
    #       -> Verificar se falta a key VOTOS ou a key DEPUTADOS                           (14, 15)
    #       -> Verificar se a key correspondente aos numeros de votos é do tipo
    #           correto STR                                                                   (16)
        
    def test_obtem_resultado_eleicoes3(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            target.obtem_resultado_eleicoes('deez nuts')
    def test_obtem_resultado_eleicoes4(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            target.obtem_resultado_eleicoes({})
    def test_obtem_resultado_eleicoes5(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes6(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'xxx': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes7(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'xxx': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes8(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 'zero', 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes9(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': 'zero'},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes10(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':'zero', 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes11(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':-69, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes12(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 0, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes13(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':0, 'B':0, 'C':0, 'D':0}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes14(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7}, 
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes15(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {'A':9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    def test_obtem_resultado_eleicoes16(self):
        with pytest.raises(ValueError, match='obtem_resultado_eleicoes: argumento invalido'):
            info = {
            'Endor':   {'deputados': 7, 
                        'votos': {'A':12000, 'B':7500, 'C':5250, 'D':3000}},
            'Hoth':    {'deputados': 6, 
                        'votos': {69:9000, 'B':11500, 'D':1500, 'E':5000}},
            'Tatooine': {'deputados': 3, 
                        'votos': {'A':3000, 'B':1900}}}
            target.obtem_resultado_eleicoes(info)
    
            

class TestPublicSistemasLineares:

   def test_produto_interno1(self):
       assert target.produto_interno((1,2,3,4,5),(-4,5,-6,7,-8)) == -24.0

   def test_verifica_convergencia1(self):
       assert target.verifica_convergencia(((1, -0.5), (-1, 2)), (-0.4, 1.9), (0.1001, 1), 0.00001) == False

   def test_verifica_convergencia2(self):
       assert target.verifica_convergencia(((1, -0.5), (-1, 2)), (-0.4, 1.9), (0.1001, 1), 0.001) == True

   def test_retira_zeros_diagonal1(self):
       assert target.retira_zeros_diagonal(((0, 1, 1), (1, 0, 0), (0, 1, 0)), (1, 2, 3)) == (((1, 0, 0), (0, 1, 0), (0, 1, 1)), (2, 3, 1))

   def test_eh_diagonal_dominante1(self):
       assert target.eh_diagonal_dominante(((1, 2, 3, 4, 5),(4, -5, 6, -7, 8), (1, 3, 5, 3, 1), (-1, 0, -1, 0, -1), (0, 2, 4, 6, 8))) == False

   def test_eh_diagonal_dominante2(self):
       assert target.eh_diagonal_dominante(((1, 0, 0), (0, 1, 0), (0, 1, 1))) == True

   def test_resolve_sistema1(self):    
       def equal(x,y):
           delta = 1e-10
           return all(abs(x[i]-y[i])<delta for i in range(len(x)))

       A4, c4 = ((2, -1, -1), (2, -9, 7), (-2, 5, -9)), (-8, 8, -6)
       ref = (-4.0, -1.0, 1.0)
           
       assert equal(target.resolve_sistema(A4, c4, 1e-20), ref)

       


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


def check_for_updates():
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