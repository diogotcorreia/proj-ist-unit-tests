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
exec(open(file_name).read(), target.__dict__)


class TestDocumentacao1(unittest.TestCase):
    def test_corrigir_palavra_1(self):
        """
        Exemplo enunciado (database)
        """
        self.assertEqual("database", target.corrigir_palavra("cCdatabasacCADde"))

    def test_corrigir_palavra_2(self):
        """
        Exemplo enunciado (x)
        """
        self.assertEqual("x", target.corrigir_palavra("abBAx"))

    def test_corrigir_palavra_3(self):
        self.assertEqual("", target.corrigir_palavra("aaDBbdAcCeEA"))

    def test_corrigir_palavra_4(self):
        self.assertEqual("abAB", target.corrigir_palavra("abAB"))

    def test_corrigir_palavra_5(self):
        self.assertEqual("aabAAB", target.corrigir_palavra("aabAAB"))

    def test_corrigir_palavra_6(self):
        self.assertEqual("Ol", target.corrigir_palavra("OlaA"))

    def test_eh_anagrama_1(self):
        """
        Exemplo enunciado (caso, SaCo)
        """
        self.assertTrue(target.eh_anagrama("caso", "SaCo"))

    def test_eh_anagrama_2(self):
        """
        Exemplo enunciado (caso, casos)
        """
        self.assertFalse(target.eh_anagrama("caso", "casos"))

    def test_eh_anagrama_3(self):
        self.assertTrue(target.eh_anagrama("caso", "caso"))

    def test_eh_anagrama_4(self):
        self.assertTrue(target.eh_anagrama("casO", "Caso"))

    def test_corrigir_doc_1(self):
        """
        Exemplo enunciado (???)
        Deve lançar um ValueError
        """
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("???")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_2(self):
        """
        Exemplo enunciado (Buggy data base has wrong data)
        """
        doc = "BuAaXOoxiIKoOkggyrFfhHXxR duJjUTtaCcmMtaAGga eEMmtxXOjUuJQqQHhqoada JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn LyYlMmwmMrRrongTtoOkyYcCK daRfFKkLlhHrtZKqQkkvVKza"
        self.assertEqual("Buggy data base has wrong data", target.corrigir_doc(doc))

    def test_corrigir_doc_3(self):
        """
        Exemplo enunciado (Programacao e programacao)
        """
        doc = "Programacao porgramacao e programacao"
        self.assertEqual("Programacao e programacao", target.corrigir_doc(doc))

    def test_corrigir_doc_4(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("Dois  espaços")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_5(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc(1)
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_6(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_7(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("letr4s e numer0s")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_8(self):
        doc = "Programacao Programacao porgramacao"
        self.assertEqual("Programacao Programacao", target.corrigir_doc(doc))

    def test_corrigir_doc_9(self):
        doc = "Programacao com objetos e bojetos"
        self.assertEqual("Programacao com objetos e", target.corrigir_doc(doc))

    def test_corrigir_doc_10(self):
        doc = "Era la suma souvenir del universo la inmaculada briosa y sobria marioneta danesa de adanes"
        self.assertEqual(
            "Era la suma souvenir del la inmaculada briosa y marioneta danesa de",
            target.corrigir_doc(doc),
        )


class TestPIN2(unittest.TestCase):
    def test_obter_posicao_1(self):
        self.assertEqual(1, target.obter_posicao("C", 1))

    def test_obter_posicao_2(self):
        self.assertEqual(2, target.obter_posicao("C", 2))

    def test_obter_posicao_3(self):
        self.assertEqual(3, target.obter_posicao("C", 3))

    def test_obter_posicao_4(self):
        self.assertEqual(1, target.obter_posicao("C", 4))

    def test_obter_posicao_5(self):
        self.assertEqual(2, target.obter_posicao("C", 5))

    def test_obter_posicao_6(self):
        self.assertEqual(3, target.obter_posicao("C", 6))

    def test_obter_posicao_7(self):
        self.assertEqual(4, target.obter_posicao("C", 7))

    def test_obter_posicao_8(self):
        self.assertEqual(5, target.obter_posicao("C", 8))

    def test_obter_posicao_9(self):
        self.assertEqual(6, target.obter_posicao("C", 9))

    def test_obter_posicao_10(self):
        self.assertEqual(4, target.obter_posicao("B", 1))

    def test_obter_posicao_11(self):
        self.assertEqual(5, target.obter_posicao("B", 2))

    def test_obter_posicao_12(self):
        self.assertEqual(6, target.obter_posicao("B", 3))

    def test_obter_posicao_13(self):
        self.assertEqual(7, target.obter_posicao("B", 4))

    def test_obter_posicao_14(self):
        self.assertEqual(8, target.obter_posicao("B", 5))

    def test_obter_posicao_15(self):
        self.assertEqual(9, target.obter_posicao("B", 6))

    def test_obter_posicao_16(self):
        self.assertEqual(7, target.obter_posicao("B", 7))

    def test_obter_posicao_17(self):
        self.assertEqual(8, target.obter_posicao("B", 8))

    def test_obter_posicao_18(self):
        self.assertEqual(9, target.obter_posicao("B", 9))

    def test_obter_posicao_19(self):
        self.assertEqual(1, target.obter_posicao("E", 1))

    def test_obter_posicao_20(self):
        self.assertEqual(1, target.obter_posicao("E", 2))

    def test_obter_posicao_21(self):
        self.assertEqual(2, target.obter_posicao("E", 3))

    def test_obter_posicao_22(self):
        self.assertEqual(4, target.obter_posicao("E", 4))

    def test_obter_posicao_23(self):
        self.assertEqual(4, target.obter_posicao("E", 5))

    def test_obter_posicao_24(self):
        self.assertEqual(5, target.obter_posicao("E", 6))

    def test_obter_posicao_25(self):
        self.assertEqual(7, target.obter_posicao("E", 7))

    def test_obter_posicao_26(self):
        self.assertEqual(7, target.obter_posicao("E", 8))

    def test_obter_posicao_27(self):
        self.assertEqual(8, target.obter_posicao("E", 9))

    def test_obter_posicao_28(self):
        self.assertEqual(2, target.obter_posicao("D", 1))

    def test_obter_posicao_29(self):
        self.assertEqual(3, target.obter_posicao("D", 2))

    def test_obter_posicao_30(self):
        self.assertEqual(3, target.obter_posicao("D", 3))

    def test_obter_posicao_31(self):
        self.assertEqual(5, target.obter_posicao("D", 4))

    def test_obter_posicao_32(self):
        self.assertEqual(6, target.obter_posicao("D", 5))

    def test_obter_posicao_33(self):
        self.assertEqual(6, target.obter_posicao("D", 6))

    def test_obter_posicao_34(self):
        self.assertEqual(8, target.obter_posicao("D", 7))

    def test_obter_posicao_35(self):
        self.assertEqual(9, target.obter_posicao("D", 8))

    def test_obter_posicao_36(self):
        self.assertEqual(9, target.obter_posicao("D", 9))

    def test_obter_digito_1(self):
        self.assertEqual(1, target.obter_digito("CEE", 5))

    def test_obter_digito_2(self):
        self.assertEqual(8, target.obter_digito("BECDECBBDB", 2))

    def test_obter_pin_1(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(1)
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_2(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("E", "C", "D"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_3(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("E", "C", "D", "E", "C", "D", "E", "C", "D", "E", "C"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_4(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("z", "E", "C", "D"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_5(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("", "E", "C", "D"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_6(self):
        t = ("CEE", "DDBBB", "ECDBE", "CCCCB")
        self.assertEqual((1, 9, 8, 5), target.obter_pin(t))
        
    def test_obter_pin_7(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(["CEE", "DDBBB", "ECDBE", "CCCCB"])
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))


class TestVerificacaoDados3(unittest.TestCase):
    def test_eh_entrada_1(self):
        self.assertFalse(target.eh_entrada(1))

    def test_eh_entrada_2(self):
        self.assertFalse(target.eh_entrada(("a")))

    def test_eh_entrada_3(self):
        self.assertFalse(target.eh_entrada(("a", "b")))

    def test_eh_entrada_4(self):
        self.assertFalse(target.eh_entrada(("a", "b", "c")))

    def test_eh_entrada_5(self):
        self.assertFalse(target.eh_entrada(("", "[aaaaa]", (1, 2))))

    def test_eh_entrada_6(self):
        self.assertFalse(target.eh_entrada(("A", "[aaaaa]", (1, 2))))

    def test_eh_entrada_7(self):
        self.assertFalse(target.eh_entrada(("aa", "", (1, 2))))

    def test_eh_entrada_8(self):
        self.assertFalse(target.eh_entrada(("aa", "abcde", (1, 2))))

    def test_eh_entrada_9(self):
        self.assertFalse(target.eh_entrada(("aa", "abcdefg", (1, 2))))

    def test_eh_entrada_10(self):
        self.assertFalse(target.eh_entrada(("aa", "[abcdef", (1, 2))))

    def test_eh_entrada_11(self):
        self.assertFalse(target.eh_entrada(("aa", "aabcde]", (1, 2))))

    def test_eh_entrada_12(self):
        self.assertFalse(target.eh_entrada(("aa", "[a[aaa]", (1, 2))))

    def test_eh_entrada_13(self):
        self.assertFalse(target.eh_entrada(("aa", "[aaa]a]", (1, 2))))

    def test_eh_entrada_14(self):
        self.assertFalse(target.eh_entrada(("aa-", "[aaaaa]", (1, 2))))

    def test_eh_entrada_15(self):
        self.assertFalse(target.eh_entrada(("-aa", "[aaaaa]", (1, 2))))

    def test_eh_entrada_16(self):
        self.assertFalse(target.eh_entrada(("a--a", "[aaaaa]", (1, 2))))

    def test_eh_entrada_17(self):
        self.assertFalse(target.eh_entrada(("aa", "[aaaaa]", ())))

    def test_eh_entrada_18(self):
        self.assertFalse(target.eh_entrada(("aa", "[aaaaa]", ("a", 2))))

    def test_eh_entrada_19(self):
        self.assertFalse(target.eh_entrada(("aa", "[aaaaa]", (-1, 2))))

    def test_eh_entrada_20(self):
        self.assertTrue(target.eh_entrada(("a-b-c-d-e-f-g-h", "[xxxxx]", (950, 300))))

    def test_eh_entrada_21(self):
        self.assertTrue(target.eh_entrada(("a-b-c-d-e-f-g", "[xxxxx]", (124, 325, 7))))

    def test_validar_cifra_1(self):
        self.assertTrue(target.validar_cifra("zzz-yyy-ccc-aaa-bbb", "[abcyz]"))

    def test_validar_cifra_2(self):
        self.assertTrue(target.validar_cifra("zzz-bb-aa-d-c", "[zabcd]"))

    def test_validar_cifra_3(self):
        self.assertFalse(target.validar_cifra("a-b-c-d-e-f-g-h", "[xxxxx]"))
        
    def test_validar_cifra_4(self):
        self.assertFalse(target.validar_cifra("aaa-b-c-d-e-f", "[bcdef]"))
        
    def test_validar_cifra_5(self):
        self.assertTrue(target.validar_cifra("a-b-c-d-e-f", "[bcdef]"))

    def test_filtrar_bdb_1(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb(1)
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_2(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb([("aaaaa-bbb-zx-yz-xy", "[]", (950, 300))])
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_3(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb([("aaaaa-bbb-zx-yz-xy", "[abxyz]")])
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_4(self):
        self.assertEqual(
            [], target.filtrar_bdb([("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950, 300))])
        )

    def test_filtrar_bdb_5(self):
        self.assertEqual(
            [
                ("a-b-c-d-e-f-g-h", "[xxxxx]", (124, 325, 7)),
                ("entrada-muito-errada", "[abcde]", (50, 404)),
            ],
            target.filtrar_bdb(
                [
                    ("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950, 300)),
                    ("a-b-c-d-e-f-g-h", "[xxxxx]", (124, 325, 7)),
                    ("entrada-muito-errada", "[abcde]", (50, 404)),
                ]
            ),
        )
        
    def test_filtrar_bdb_6(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb((("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950, 300))))
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))


class TesteDesencriptacaoDeDados4(unittest.TestCase):
    def test_obter_num_seguranca_1(self):
        self.assertEqual(9, target.obter_num_seguranca((1, 10, 100)))

    def test_obter_num_seguranca_2(self):
        self.assertEqual(9, target.obter_num_seguranca((100, 1, 10)))

    def test_obter_num_seguranca_3(self):
        self.assertEqual(9, target.obter_num_seguranca((100, 10, 1)))

    def test_obter_num_seguranca_4(self):
        self.assertEqual(351, target.obter_num_seguranca((420, 69, 31415)))

    def test_obter_num_seguranca_5(self):
        self.assertEqual(9, target.obter_num_seguranca((1, 100, 10)))

    def test_obter_num_seguranca_6(self):
        self.assertEqual(9, target.obter_num_seguranca((10, 100, 1)))

    def test_obter_num_seguranca_7(self):
        self.assertEqual(9, target.obter_num_seguranca((10, 1, 100)))

    def test_obter_num_seguranca_8(self):
        self.assertEqual(325, target.obter_num_seguranca((2223, 424, 1316, 99)))

    def test_decifrar_texto_1(self):
        self.assertEqual(
            "esta cifra e quase inquebravel",
            target.decifrar_texto("qgfo-qutdo-s-egoes-wzegsnfmjqz", 325),
        )

    def test_decifrar_texto_2(self):
        self.assertEqual(
            "bpqx zfcox b nrxpb fknrbyoxsbi",
            target.decifrar_texto("qgfo-qutdo-s-egoes-wzegsnfmjqz", 10),
        )

    def test_decifrar_bdb_1(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.decifrar_bdb(1)
        self.assertEqual("decifrar_bdb: argumento invalido", str(ctx.exception))

    def test_decifrar_bdb_2(self):
        bdb = [
            ("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223, 424, 1316, 99)),
            ("lctlgukvzwy-ji-xxwmzgugkgw", "[abxyz]", (2388, 367, 5999)),
            ("nyccjoj-vfrex-ncalml", "[xxxxx]", (50, 404)),
        ]
        self.assertEqual(
            [
                "esta cifra e quase inquebravel",
                "fundamentos da programacao",
                "entrada muito errada",
            ],
            target.decifrar_bdb(bdb),
        )
        
    def test_decifrar_bdb_4(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.decifrar_bdb((("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223, 424, 1316, 99))))
        self.assertEqual("decifrar_bdb: argumento invalido", str(ctx.exception))


class TestDepuracao5(unittest.TestCase):
    def test_eh_utilizador_1(self):
        """
        Exemplo enunciado {'name':'john.doe','pass':'aabcde','rule':{'vals':(1,3),'char':'a'}}
        """
        self.assertTrue(
            target.eh_utilizador(
                {
                    "name": "john.doe",
                    "pass": "aabcde",
                    "rule": {"vals": (1, 3), "char": "a"},
                }
            )
        )

    def test_eh_utilizador_2(self):
        """
        Exemplo enunciado {'name':'john.doe','pass':'aabcde','rule':{'vals':1,'char':'a'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"name": "john.doe", "pass": "aabcde", "rule": {"vals": 1, "char": "a"}}
            )
        )

    def test_eh_utilizador_3(self):
        """
        Exemplo enunciado {'name':'bruce','surname':'wayne','pass':'mynameisbatman','rule':{'vals':(2,8),'char':'m'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce",
                    "surname": "wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 8), "char": "m"},
                }
            )
        )

    def test_eh_utilizador_4(self):
        """
        Exemplo enunciado {'pass':'mynameisbatman','rule':{'vals':(2,8),'char':'m'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"pass": "mynameisbatman", "rule": {"vals": (2, 8), "char": "m"}}
            )
        )

    def test_eh_utilizador_5(self):
        """
        Exemplo enunciado {'name':'','pass':'mynameisbatman','rule':{'vals':(2,8),'char':'m'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 8), "char": "m"},
                }
            )
        )

    def test_eh_utilizador_6(self):
        """
        Exemplo enunciado {'name':'bruce.wayne','pass':'mynameisbatman','rule':{}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"name": "bruce.wayne", "pass": "mynameisbatman", "rule": {}}
            )
        )

    def test_eh_utilizador_7(self):
        """
        Exemplo enunciado {'name':'bruce.wayne','pass':'mynameisbatman','rule':{'vals':(2,8),'char':'ma'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 8), "char": "ma"},
                }
            )
        )

    def test_eh_utilizador_8(self):
        """
        Exemplo enunciado {'name':'bruce.wayne','pass':'mynameisbatman','rule':{'vals':(2,8),'char':'m'}}
        """
        self.assertTrue(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 8), "char": "m"},
                }
            )
        )
        
    def test_eh_utilizador_9(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (5, 2), "char": "m"},
                }
            )
        )
        
    def test_eh_utilizador_10(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (-3, 2), "char": "m"},
                }
            )
        )

    def test_eh_senha_valida_1(self):
        """
        Exemplo enunciado ('aabcd', {'vals': (1,3), 'char':'a'})
        """
        self.assertTrue(target.eh_senha_valida("aabcde", {"vals": (1, 3), "char": "a"}))

    def test_eh_senha_valida_2(self):
        """
        Exemplo enunciado ('cdefgh', {'vals': (1,3), 'char':'b'})
        """
        self.assertFalse(
            target.eh_senha_valida("cdefgh", {"vals": (1, 3), "char": "b"})
        )

    def test_filtrar_senhas_1(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(1)
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_2(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(1)
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_3(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas([])
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_4(self):
        bdb = [
            {
                "outracoisasemsernome": "john.doe",
                "pass": "aabcde",
                "rule": {"vals": (1, 3), "char": "a"},
            },
            {
                "name": "jane.doe",
                "pass": "cdefgh",
                "rule": {"vals": (1, 3), "char": "b"},
            },
            {
                "name": "jack.doe",
                "pass": "cccccc",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(bdb)
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_5(self):
        bdb = [
            {
                "nome": "john.doe",
                "pass": "aabcde",
                "rule": {"vals": (1, 3), "char": "a"},
            },
            {
                "name": "jane.doe",
                "pass": "cdefghpqppp",
                "rule": {"vals": (1, 3), "char": "b"},
            },
            {
                "name": "jack.doe",
                "pass": "cccccc",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(bdb)
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_6(self):
        bdb = [
            {
                "nome": "john.doe",
                "pass": "aabcde",
                "rule": {"vals": (1, 3), "char": "a"},
            },
            {
                "name": "jane.doe",
                "pass": "cdefgh",
                "rule": {"vals": (3), "char": "b"},
            },
            {
                "name": "jack.doe",
                "pass": "cccccc",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(bdb)
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_7(self):
        bdb = [
            {
                "name": "john.doe",
                "pass": "aabcde",
                "rule": {"vals": (1, 3), "char": "a"},
            },
            {
                "name": "jane.doe",
                "pass": "cdefgh",
                "rule": {"vals": (1, 3), "char": "b"},
            },
            {
                "name": "jack.doe",
                "pass": "cccccc",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        self.assertEqual(
            ["jack.doe", "jane.doe"],
            target.filtrar_senhas(bdb),
        )


#######################################################
# Logic to handle updates automatically. DO NOT TOUCH #
#######################################################


def get_lastest_commit_hash():
    try:
        result = requests.get(
            "https://api.github.com/repos/diogotcorreia/proj-ist-unit-tests/commits?path=fp%2F2021-2022%2Ffp-p1%2Fproj_tester.py&page=1&per_page=1"
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
        "https://raw.githubusercontent.com/diogotcorreia/proj-ist-unit-tests/master/fp/2021-2022/fp-p1/proj_tester.py"
    )
    open("proj_tester.py", "w+", encoding="utf-8").write(new_file.text)

    print("Volta a executar o programa para carregar os novos testes")
    exit()


if __name__ == "__main__":
    check_for_updates()
    unittest.main(argv=["first-arg-is-ignored"])
