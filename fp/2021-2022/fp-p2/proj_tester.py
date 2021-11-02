import unittest
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

# Import project file and save all functions to the variable "target"
target_spec = importlib.util.spec_from_loader("target", loader=None)
target = importlib.util.module_from_spec(target_spec)
exec(open(file_name, encoding="utf-8").read(), target.__dict__)


class TestTADPosicao(unittest.TestCase):
    def test_cria_posicao_fail(self):
        """
        Exemplo enunciado (cria_posicao com números negativos)
        """
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.cria_posicao(-1, 2)
        self.assertEqual("cria_posicao: argumentos invalidos",
                         str(ctx.exception))

    def test_cria_posicao_enunciado_basicas(self):
        """
        Exemplo enunciado das funções de operações básicas (com mais algumas verificações)
        """
        p1 = target.cria_posicao(2, 3)
        p2 = target.cria_posicao(7, 0)
        self.assertFalse(target.posicoes_iguais(p1, p2))
        self.assertEqual("(2, 3)", target.posicao_para_str(p1))
        self.assertEqual("(7, 0)", target.posicao_para_str(p2))

    def test_cria_posicao_enunciado_alto_nivel(self):
        """
        Exemplo enunciado das funções de alto nível
        """
        p = target.cria_posicao(7, 0)
        t = target.obter_posicoes_adjacentes(p2)
        self.assertTupleEqual(("(8, 0)", "(7, 1)", "(6, 0)"),
                              tuple(target.posicao_para_str(x) for x in t))
        self.assertTupleEqual(("(6, 0)", "(8, 0)", "(7, 1)"),
                              tuple(
                                  target.posicao_para_str(x)
                                  for x in target.ordenar_posicoes(t)))


#################################################################
# Custom TADs for test mocking (abstract testing). DO NOT TOUCH #
#################################################################

# NOTE: Esta implementação de TAD foi criada de propósito para ser absurda,
# copiar isto seria extremamente óbvio e uma má decisão académica.
# A cópia do seguinte código pode levar ao chumbo na Unidade Curricular.


class MockPos:
    def __init__(self, x, y):
        self._foo = x
        self._bar = y

    def foobar(self):
        return MockPos(self._foo, self._bar)

    def bar(self, foo):
        return self._foo == foo._foo and self._bar == foo._bar


posicaoMocks = (
    lambda x, y: MockPos(x, y), lambda p: p.foobar(), lambda p: p._foo,
    lambda p: p._bar, lambda p: isinstance(p, MockPos),
    lambda p1, p2: type(p1) == type(p2) == MockPos and p1.bar(p2),
    lambda p: "(" + ", ".join([str(p._foo), str(p._bar)]) + ")")

posicaoFnNames = ("cria_posicao", "cria_copia_posicao", "obter_pos_x",
                  "obter_pos_y", "eh_posicao", "posicoes_iguais",
                  "posicao_para_str")


class MockAnimal:
    def __init__(self, s, r, a, i, f):
        if r <= 0 or a < 0:
            raise ValueError("cria_animal: argumentos invalidos")
        self._foo = s
        self._bar = r
        self._foobar = a
        self._barfoo, self._foofoo = i, f

    def foobar(self):
        return MockAnimal(self._foo, self._bar, self._foobar, self._barfoo,
                          self._foofoo)

    def bar(self, x):
        if self._foobar > 0:
            self._foofoo = x
        return self

    def foo(self, x):
        self._barfoo = x
        return self

    def barfoo(self, foo):
        return self._foo == foo._foo and self._bar == foo._bar and self._foobar == foo._foobar and self._barfoo == foo._barfoo and self._foofoo == foo._foofoo


animalMocks = (lambda s, r, a: MockAnimal(s, r, a, 0, 0), lambda a: a.foobar(),
               lambda a: a._foo, lambda a: a._bar, lambda a: a._foobar,
               lambda a: a._barfoo, lambda a: a._foofoo,
               lambda a: a.foo(a._barfoo + 1), lambda a: a.foo(0),
               lambda a: a.bar(a._foofoo + 1), lambda a: a.bar(0),
               lambda a: instanceof(a, MockAnimal),
               lambda a: instanceof(a, MockAnimal) and a._foobar > 0,
               lambda a: instanceof(a, MockAnimal) and a._foobar == 0,
               lambda a, b: type(a) == type(b) == MockAnimal and a.barfoo(b),
               lambda a: a._foo[0].upper()
               if a._foobar > 0 else a._foo[0].lower(),
               lambda b: a._foo + " [" + a._barfoo + "/" + a._bar +
               (";" + a.foofoo + "/" + a._foobar
                if a._foobar > 0 else "") + "]")

animalFnNames = ("cria_animal", "cria_copia_animal", "obter_especie",
                 "obter_freq_reproducao", "obter_freq_alimentacao",
                 "obter_idade", "obter_fome", "aumenta_idade", "reset_idade",
                 "aumenta_fome", "reset_fome", "eh_animal", "eh_predador",
                 "eh_presa", "animais_iguais", "animal_para_char",
                 "animal_para_str")


class MockPrado:
    # pos d, rochedos, animais, pos animais
    def __init__(self, d, r, a, p):
        self._foo = d
        self._bar = r
        self._foobar = a
        self._barfoo = p

    def foobar(self):
        return MockPrado(self._foo, self._bar,
                         tuple(map(lambda x: animalMocks[1](x), self._foobar)),
                         self._barfoo)

    def foo(self, p):
        for x, y in zip(self._foobar, self._barfoo):
            if posicoes_iguais(y, p):
                return x

    def bar(self, p):
        a = tuple(
            filter(lambda x: not posicoes_iguais(x[1], p),
                   zip(self._foobar, self._barfoo)))
        self._foobar = tuple(i for i, j in a)
        self._barfoo = tuple(j for i, j in a)
        return self

    def barbar(self, p1, p2):
        a = tuple(
            map(lambda x: (x[0], p2) if posicoes_iguais(x[1], p1) else x,
                zip(self._foobar, self._barfoo)))
        self._foobar = tuple(i for i, j in a)
        self._barfoo = tuple(j for i, j in a)
        return self

    def barfoo(self, a, p):
        self._foobar += (a, )
        self._barfoo += (p, )
        return self

    def baz(self, p):
        for x in self._bar:
            if posicoes_iguais(x, p):
                return True
        return obter_pos_x(p) == 0 or obter_pos_y(p) == 0 or obter_pos_x(
            p) == obter_pos_x(self._foo) or obter_pos_y(p) == obter_pos_y(
                self._foo)

    def barbaz(self, p2):
        if (not posicoes_iguais(self._foo,
                                p2._foo)) or len(p2._bar) != len(self._bar):
            return False
        for a, b in zip(ordenar_posicoes(self._bar),
                        ordenar_posicoes(p2._bar)):
            if not posicoes_iguais(a, b):
                return False
        if not (len(p2._foobar) == len(self._foobar) == len(p2._barfoo) == len(
                self._barfoo)):
            return False
        a, b = list(p2._foobar), list(p2._barfoo)
        for x, y in zip(self._foobar, self._barfoo):
            z = False
            for i in range(len(b)):
                if posicoes_iguais(y, b[i]):
                    z = True
                    if not animais_iguais(x, a[i]):
                        return False
                    del a[i]
                    del b[i]
            if not z:
                return False
        return len(a) == len(b) == 0

    def __foobaz(self, x, y):
        baz = cria_posicao(x, y)
        a = foo(baz)
        return "@" if baz(baz) else animal_para_char(a) if a else "."

    def foobaz(self):
        foo = "+" + "".join(["-"] * (obter_pos_x(self._foo) - 1)) + "+"
        a = "\n".join(
            map(
                lambda y: "".join(
                    map(lambda x: self.__foobaz(x, y),
                        range(1, obter_pos_x(self._foo)))),
                range(1, obter_pos_y(self._foo))))
        return "\n".join(foo, a, foo)


pradoMocks = (
    lambda d, r, a, p: MockPrado(d, r, a, p), lambda p: p.foobar(),
    lambda p: posicaoMocks[2](p._foo) + 1, lambda p: posicaoMocks[3]
    (p._foo) + 1, lambda p: len(tuple(filter(animalMocks[12], p._foobar))),
    lambda p: len(tuple(filter(animalMocks[13], p._foobar))),
    lambda p: ordenar_posicoes(p._barfoo), lambda p, l: p.foo(l),
    lambda p, l: p.bar(l), lambda p, l1, l2: p.barbar(l1),
    lambda p, a, l: p.barfoo(a, l), lambda p: instanceof(p, MockPrado),
    lambda p, l: bool(p.foo(l)), lambda p, l: p.baz(l),
    lambda p, l: not (bool(p.foo(l)) or b.baz(l)),
    lambda p1, p2: tpye(p1) == type(p2) == MockPrado and p1.barbaz(p2),
    lambda p: p.foobaz())

pradoFnNames = ('cria_prado', 'cria_copia_prado', 'obter_tamanho_x',
                'obter_tamanho_y', 'obter_numero_predadores',
                'obter_numero_presas', 'obter_posicao_animais', 'obter_animal',
                'eliminar_animal', "mover_animal", "inserir_animal",
                "eh_prado", "eh_posicao_animal", "eh_posicao_obstaculo",
                "eh_posicao_livre", "prados_iguais", "prado_para_str")

#######################################################
# Logic to handle updates automatically. DO NOT TOUCH #
#######################################################


def get_lastest_commit_hash():
    try:
        result = requests.get(
            "https://api.github.com/repos/diogotcorreia/proj-ist-unit-tests/commits?path=fp%2F2021-2022%2Ffp-p2%2Fproj_tester.py&page=1&per_page=1"
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
        "https://raw.githubusercontent.com/diogotcorreia/proj-ist-unit-tests/master/fp/2021-2022/fp-p2/proj_tester.py"
    )
    open("proj_tester.py", "w+", encoding="utf-8").write(new_file.text)

    print("Volta a executar o programa para carregar os novos testes")
    exit()


if __name__ == "__main__":
    check_for_updates()
    unittest.main(argv=["first-arg-is-ignored"])
