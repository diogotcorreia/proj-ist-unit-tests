import unittest
import importlib.util
import sys
import requests
from itertools import combinations

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

print("Desejas correr os testes de verificação de abstração? [y/N]")
response = input()
ENABLE_MOCK_TESTING = response.lower() == "y"


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
        t = target.obter_posicoes_adjacentes(p)
        self.assertTupleEqual(("(8, 0)", "(7, 1)", "(6, 0)"),
                              tuple(target.posicao_para_str(x) for x in t))
        self.assertTupleEqual(("(6, 0)", "(8, 0)", "(7, 1)"),
                              tuple(
                                  target.posicao_para_str(x)
                                  for x in target.ordenar_posicoes(t)))

    @unittest.skipUnless(ENABLE_MOCK_TESTING, "skipping mock tests")
    def test_posicao_mock(self, *_):
        """
        Testa as barreiras de abstração do TAD Posição
        """
        __mocks = enable_mocks(target, posicaoFnNames, posicaoMocks)
        try:
            self.test_cria_posicao_enunciado_alto_nivel()
        finally:
            restore_mocks(target, __mocks)


class TestTADAnimal(unittest.TestCase):
    def test_cria_animal_fail(self):
        for r, a in ((0, 5), (0, 0), (-3, 3), (-1, 0)):
            with self.subTest(msg="Testing with r <= 0 or a < 0:", r=r, a=a):
                with self.assertRaises(ValueError,
                                       msg="ValueError not raised") as ctx:
                    target.cria_animal('rabbit', -1, 2)
                self.assertEqual("cria_animal: argumentos invalidos",
                                 str(ctx.exception))

    def test_animal_para_str(self):
        tests = (
            ('rabbit', 5, 0, 'rabbit [0/5]'),
            ('fox', 20, 10, 'fox [0/20;0/10]'),
        )
        for name, r, a, result in tests:
            with self.subTest(name=name, r=r, a=a):
                animal = target.cria_animal(name, r, a)
                self.assertEqual(result, target.animal_para_str(animal))

    def test_animal_para_char(self):
        tests = (
            ('rabbit', 5, 0, 'r'),
            ('fox', 20, 10, 'F'),
        )
        for name, r, a, result in tests:
            with self.subTest(name=name, r=r, a=a):
                animal = target.cria_animal(name, r, a)
                self.assertEqual(result, target.animal_para_char(animal))

    def test_cria_animal(self):
        """
        Testa um animal e verifica que os seletores e reconhecedores retornam
        as propriedades corretas.
        """
        tests = (
            ('rabbit', 5, 0, False, True),
            ('fox', 20, 10, True, False),
        )
        for name, r, a, predador, presa in tests:
            with self.subTest(name=name, r=r, a=a):
                animal = target.cria_animal(name, r, a)
                self.assertEqual(name, target.obter_especie(animal))
                self.assertEqual(r, target.obter_freq_reproducao(animal))
                self.assertEqual(a, target.obter_freq_alimentacao(animal))
                self.assertTrue(target.eh_animal(animal))
                self.assertEqual(predador, target.eh_predador(animal))
                self.assertEqual(presa, target.eh_presa(animal))

    def test_cria_copia_animal(self):
        """
        Relembra-se que a cópia não pode ser o mesmo objeto que o original,
        isto é, "original is copia" tem de retornar False.
        """
        tests = (
            ('rabbit', 5, 0),
            ('fox', 20, 10),
        )
        for name, r, a in tests:
            with self.subTest(name=name, r=r, a=a):
                animal1 = target.cria_animal(name, r, a)
                animal2 = target.cria_copia_animal(animal1)
                self.assertIsNot(animal1, animal2)
                self.assertTrue(target.animais_iguais(animal1, animal2))

    def test_aumenta_idade(self):
        animal = target.cria_animal("fox", 20, 10)
        target.aumenta_idade(target.aumenta_idade(animal))
        self.assertEqual("fox [2/20;0/10]", target.animal_para_str(animal))
        self.assertEqual(2, target.obter_idade(animal))

    def test_aumenta_fome_predador(self):
        animal = target.cria_animal("fox", 20, 10)
        target.aumenta_fome(target.aumenta_fome(animal))
        self.assertEqual("fox [0/20;2/10]", target.animal_para_str(animal))
        self.assertEqual(2, target.obter_fome(animal))

    def test_aumenta_fome_presa(self):
        animal = target.cria_animal("rabbit", 7, 0)
        target.aumenta_fome(target.aumenta_fome(animal))
        self.assertEqual("rabbit [0/7]", target.animal_para_str(animal))
        self.assertEqual(0, target.obter_fome(animal))

    @unittest.skipUnless(ENABLE_MOCK_TESTING, "skipping mock tests")
    def test_animal_mock(self, *_):
        """
        Testa as barreiras de abstração do TAD Animal
        """
        __mocks = enable_mocks(target, animalFnNames, animalMocks)
        try:
            pass
            # TODO
            # self.test_eh_animal_fertil()
            # self.test_eh_animal_faminto()
            # self.test_reproduz_animal()
        finally:
            restore_mocks(target, __mocks)


class TestTADPrado(unittest.TestCase):
    def test_cria_prado(self):
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        with self.subTest(msg="Test obter_tamanho_x"):
            self.assertEqual(12, target.obter_tamanho_x(prado))
        with self.subTest(msg="Test obter_tamanho_y"):
            self.assertEqual(5, target.obter_tamanho_y(prado))
        with self.subTest(msg="Test prado_para_str"):
            self.assertEqual(
                """+----------+
|....rL...r|
|...@@.r...|
|..........|
+----------+""", target.prado_para_str(prado))
        with self.subTest(msg="Test obter_numero_predadores"):
            self.assertEqual(1, target.obter_numero_predadores(prado))
        with self.subTest(msg="Test obter_numero_presas"):
            self.assertEqual(3, target.obter_numero_presas(prado))
        with self.subTest(msg="Test obter_posicao_animais"):
            t = target.obter_posicao_animais(prado)
            self.assertTupleEqual(("(5, 1)", "(6, 1)", "(10, 1)", "(7, 2)"),
                                  tuple(target.posicao_para_str(x) for x in t))
        for (x, y), animal in zip(((5, 1), (7, 2), (10, 1), (6, 1)),
                                  an1 + an2):
            with self.subTest(msg="Test obter_animal and eh_posicao_animal",
                              x=x,
                              y=y):
                pos_animal = target.cria_posicao(x, y)
                a = target.obter_animal(prado, pos_animal)
                self.assertTrue(target.eh_posicao_animal(prado, pos_animal))
                self.assertTrue(target.animais_iguais(animal, a))
        # both rocks and the border
        for x, y in ((4, 2), (5, 2), (0, 0), (0, 5), (3, 0), (11, 4), (11, 2),
                     (7, 4)):
            with self.subTest(msg="Test eh_posicao_obstaculo (expecting true)",
                              x=x,
                              y=y):
                pos_obs = target.cria_posicao(x, y)
                self.assertTrue(target.eh_posicao_obstaculo(prado, pos_obs))
        with self.subTest("Test eh_posicao_obstaculo (expecting false)"):
            self.assertFalse(
                target.eh_posicao_obstaculo(prado, target.cria_posicao(3, 2)))
        with self.subTest("Test eh_posicao_livre (expecting true)"):
            self.assertTrue(
                target.eh_posicao_livre(prado, target.cria_posicao(3, 3)))
        with self.subTest("Test eh_posicao_livre (expecting false)"):
            self.assertFalse(
                target.eh_posicao_livre(prado, target.cria_posicao(5, 1)))

    def test_mover_animal(self):
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        p1 = target.cria_posicao(7, 2)
        p2 = target.cria_posicao(9, 3)
        prado = target.mover_animal(prado, p1, p2)
        with self.subTest(msg="Test prado_para_str"):
            self.assertEqual(
                """+----------+
|....rL...r|
|...@@.....|
|........r.|
+----------+""", target.prado_para_str(prado))

    def test_cria_copia_prado(self):
        """
        Relembra-se que a cópia não pode ser o mesmo objeto que o original,
        isto é, "original is copia" tem de retornar False.
        """
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        prado_copia = target.cria_copia_prado(prado)

        self.assertIsNot(prado, prado_copia)
        self.assertTrue(target.prados_iguais(prado, prado_copia))

        with self.subTest(msg="Mover animal na cópia"):
            p1 = target.cria_posicao(7, 2)
            p2 = target.cria_posicao(9, 3)
            prado = target.mover_animal(prado, p1, p2)

            self.assertFalse(target.prados_iguais(prado, prado_copia))

    def test_eliminar_animal(self):
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        p1 = target.cria_posicao(7, 2)
        prado = target.eliminar_animal(prado, p1)
        with self.subTest(msg="Test prado_para_str"):
            self.assertEqual(
                """+----------+
|....rL...r|
|...@@.....|
|..........|
+----------+""", target.prado_para_str(prado))

    def test_inserir_animal(self):
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        a = target.cria_animal('fox', 30, 7)
        p1 = target.cria_posicao(9, 3)
        prado = target.inserir_animal(prado, a, p1)
        with self.subTest(msg="Test prado_para_str"):
            self.assertEqual(
                """+----------+
|....rL...r|
|...@@.r...|
|........F.|
+----------+""", target.prado_para_str(prado))

    def test_obter_valor_numerico(self):
        dim = target.cria_posicao(5, 16)
        animal = target.cria_animal('rabbit', 5, 0)
        posicao = target.cria_posicao(3, 5)
        prado = target.cria_prado(dim, (), (animal, ), (posicao, ))

        for x, y, res in ((0, 0, 0), (5, 0, 5), (0, 1, 6), (4, 1, 10),
                          (4, 11, 70), (5, 16, 101)):
            with self.subTest(x=x, y=y, valor_numerico=res):
                pos = target.cria_posicao(x, y)
                self.assertEqual(res, target.obter_valor_numerico(prado, pos))

    def test_obter_movimento(self):
        dim = target.cria_posicao(11, 4)
        obs = (target.cria_posicao(4, 2), target.cria_posicao(5, 2))
        an1 = tuple(target.cria_animal('rabbit', 5, 0) for i in range(3))
        an2 = (target.cria_animal('lynx', 20, 15), )
        pos = tuple(
            target.cria_posicao(p[0], p[1])
            for p in ((5, 1), (7, 2), (10, 1), (6, 1)))
        prado = target.cria_prado(dim, obs, an1 + an2, pos)

        for x, y, res in ((5, 1, '(4, 1)'), (6, 1, '(5, 1)'), (10, 1,
                                                               '(10, 2)')):
            with self.subTest(x=x, y=y, resultado=res):
                mov = target.obter_movimento(prado, target.cria_posicao(x, y))
                self.assertEqual(res, target.posicao_para_str(mov))

    @unittest.skipUnless(ENABLE_MOCK_TESTING, "skipping mock tests")
    def test_prado_mock_low_level(self, *_):
        """
        Testa as barreiras de abstração do TAD Prado nas funções do TAD
        """
        mocks_to_use = (
            ("posicao", posicaoFnNames, posicaoMocks),
            ("animal", animalFnNames, animalMocks),
            ("prado", pradoFnNames, pradoMocks),
        )

        for active_mocks in sum((tuple(combinations(mocks_to_use, r))
                                 for r in range(1,
                                                len(mocks_to_use) + 1)), ()):
            names = ', '.join(map(lambda x: x[0], active_mocks))
            fnNames = sum(map(lambda x: x[1], active_mocks), ())
            mocks = sum(map(lambda x: x[2], active_mocks), ())

            with self.subTest(msg="Active mocks: {}".format(names)):
                __mocks = enable_mocks(target, fnNames, mocks)
                try:
                    self.test_cria_prado()
                    self.test_cria_copia_prado()
                    self.test_eliminar_animal()
                    self.test_inserir_animal()
                finally:
                    restore_mocks(target, __mocks)

    @unittest.skipUnless(ENABLE_MOCK_TESTING, "skipping mock tests")
    def test_prado_mock_high_level(self, *_):
        """
        Testa as barreiras de abstração do TAD Prado nas funções de alto nível
        """
        mocks_to_use = (
            ("posicao", posicaoFnNames, posicaoMocks),
            ("animal", animalFnNames, animalMocks),
        )

        for active_mocks in sum((tuple(combinations(mocks_to_use, r))
                                 for r in range(1,
                                                len(mocks_to_use) + 1)), ()):
            names = ', '.join(map(lambda x: x[0], active_mocks))
            fnNames = sum(map(lambda x: x[1], active_mocks), ())
            mocks = sum(map(lambda x: x[2], active_mocks), ())

            with self.subTest(msg="Active mocks: {}".format(names)):
                __mocks = enable_mocks(target, fnNames, mocks)
                try:
                    self.test_obter_valor_numerico()
                    self.test_obter_movimento()
                finally:
                    restore_mocks(target, __mocks)


class TestFuncoesAdicionais(unittest.TestCase):
    # TODO

    @unittest.skipUnless(ENABLE_MOCK_TESTING, "skipping mock tests")
    def test_funcoes_adicionais_mock(self, *_):
        """
        Testa as barreiras de abstração das funções adicionais
        """
        mocks_to_use = (
            ("posicao", posicaoFnNames, posicaoMocks),
            ("animal", animalFnNames, animalMocks),
            ("prado", pradoFnNames, pradoMocks),
        )

        for active_mocks in sum((tuple(combinations(mocks_to_use, r))
                                 for r in range(1,
                                                len(mocks_to_use) + 1)), ()):
            names = ', '.join(map(lambda x: x[0], active_mocks))
            fnNames = sum(map(lambda x: x[1], active_mocks), ())
            mocks = sum(map(lambda x: x[2], active_mocks), ())

            with self.subTest(msg="Active mocks: {}".format(names)):
                __mocks = enable_mocks(target, fnNames, mocks)
                try:
                    pass
                    # TODO
                    # self.test_geracao()
                    # self.test_simula_ecossistema()
                finally:
                    restore_mocks(target, __mocks)


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
               lambda a: isinstance(a, MockAnimal),
               lambda a: isinstance(a, MockAnimal) and a._foobar > 0,
               lambda a: isinstance(a, MockAnimal) and a._foobar == 0,
               lambda a, b: type(a) == type(b) == MockAnimal and a.barfoo(b),
               lambda a: a._foo[0].upper()
               if a._foobar > 0 else a._foo[0].lower(),
               lambda a: a._foo + " [" + str(a._barfoo) + "/" + str(a._bar) +
               (";" + str(a._foofoo) + "/" + str(a._foobar)
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
        return MockPrado(
            self._foo, self._bar,
            tuple(map(lambda x: target.cria_copia_animal(x), self._foobar)),
            self._barfoo)

    def foo(self, p):
        for x, y in zip(self._foobar, self._barfoo):
            if target.posicoes_iguais(y, p):
                return x

    def bar(self, p):
        a = tuple(
            filter(lambda x: not target.posicoes_iguais(x[1], p),
                   zip(self._foobar, self._barfoo)))
        self._foobar = tuple(i for i, j in a)
        self._barfoo = tuple(j for i, j in a)
        return self

    def barbar(self, p1, p2):
        a = tuple(
            map(
                lambda x: (x[0], p2)
                if target.posicoes_iguais(x[1], p1) else x,
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
            if target.posicoes_iguais(x, p):
                return True
        return target.obter_pos_x(p) == 0 or target.obter_pos_y(
            p) == 0 or target.obter_pos_x(p) == target.obter_pos_x(
                self._foo) or target.obter_pos_y(p) == target.obter_pos_y(
                    self._foo)

    def barbaz(self, p2):
        if (not target.posicoes_iguais(
                self._foo, p2._foo)) or len(p2._bar) != len(self._bar):
            return False
        for a, b in zip(target.ordenar_posicoes(self._bar),
                        target.ordenar_posicoes(p2._bar)):
            if not target.posicoes_iguais(a, b):
                return False
        if not (len(p2._foobar) == len(self._foobar) == len(p2._barfoo) == len(
                self._barfoo)):
            return False
        a, b = list(p2._foobar), list(p2._barfoo)
        for x, y in zip(self._foobar, self._barfoo):
            z = False
            for i in range(len(b)):
                if target.posicoes_iguais(y, b[i]):
                    z = True
                    if not target.animais_iguais(x, a[i]):
                        return False
                    del a[i]
                    del b[i]
                    break
            if not z:
                return False
        return len(a) == len(b) == 0

    def __foobaz(self, x, y):
        baz = target.cria_posicao(x, y)
        a = self.foo(baz)
        return "@" if self.baz(baz) else target.animal_para_char(
            a) if a else "."

    def foobaz(self):
        foo = "+" + "".join(["-"] * (target.obter_pos_x(self._foo) - 1)) + "+"
        a = "\n".join(
            map(
                lambda y: "".join(
                    ('|', *map(lambda x: self.__foobaz(x, y),
                               range(1, target.obter_pos_x(self._foo))), '|')),
                range(1, target.obter_pos_y(self._foo))))
        return "\n".join((foo, a, foo))


pradoMocks = (
    lambda d, r, a, p: MockPrado(d, r, a, p), lambda p: p.foobar(),
    lambda p: target.obter_pos_x(p._foo) + 1,
    lambda p: target.obter_pos_y(p._foo) + 1,
    lambda p: len(tuple(filter(target.eh_predador, p._foobar))),
    lambda p: len(tuple(filter(target.eh_presa, p._foobar))),
    lambda p: target.ordenar_posicoes(p._barfoo), lambda p, l: p.foo(l),
    lambda p, l: p.bar(l), lambda p, l1, l2: p.barbar(l1, l2),
    lambda p, a, l: p.barfoo(a, l), lambda p: instanceof(p, MockPrado),
    lambda p, l: bool(p.foo(l)), lambda p, l: p.baz(l),
    lambda p, l: not (bool(p.foo(l)) or p.baz(l)),
    lambda p1, p2: type(p1) == type(p2) == MockPrado and p1.barbaz(p2),
    lambda p: p.foobaz())

pradoFnNames = ("cria_prado", "cria_copia_prado", "obter_tamanho_x",
                "obter_tamanho_y", "obter_numero_predadores",
                "obter_numero_presas", "obter_posicao_animais", "obter_animal",
                "eliminar_animal", "mover_animal", "inserir_animal",
                "eh_prado", "eh_posicao_animal", "eh_posicao_obstaculo",
                "eh_posicao_livre", "prados_iguais", "prado_para_str")


def enable_mocks(target, fn_names, functions):
    restore = []
    setattr(target, '__mock', True)
    for (fn_name, fn) in zip(fn_names, functions):
        try:  # ignore undefined functions
            old_fn = getattr(target, fn_name)
            restore.append((fn_name, old_fn))
            setattr(target, fn_name, fn)
        except:
            pass
    return restore


def restore_mocks(target, restore):
    setattr(target, '__mock', False)
    for (fn_name, fn) in restore:
        setattr(target, fn_name, fn)


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
        "Esta operação irá substituir o teu ficheiro local com a nova versão, apagando quaisquer alterações que tenham sido feitas aos testes locais."
    )
    print("Desejas atualizar os testes? [y/N]")
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
