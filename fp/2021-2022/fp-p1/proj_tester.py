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



class TestDocumentacao1(unittest.TestCase):
    def test_corrigir_palavra_001(self):
        """
        Exemplo enunciado (database)
        """
        self.assertEqual("database", target.corrigir_palavra("cCdatabasacCADde"))

    def test_corrigir_palavra_002(self):
        """
        Exemplo enunciado (x)
        """
        self.assertEqual("x", target.corrigir_palavra("abBAx"))

    def test_corrigir_palavra_029(self):
        self.assertEqual("teste", target.corrigir_palavra("sMEjJeqcCQmStvVeFTtfVvVBbJjvgdDNOBbAaLlNaAnoHJrRjzZeEFfsSyYYyoOxQquUXbBvVqQhBkKbnGsxXtwWMmeAapEePzZvVbBUu"))

    def test_corrigir_palavra_030(self):
        self.assertEqual("fundamentosdaprogramacao", target.corrigir_palavra("TtfdDBbjJuhHPSspnZyYtiITzJxAXxaXjdaCcJjyYgEeGmentosewWEdaoOprnNoOZyYQqeElLzohHgrbBcMmCMmamMmaciIQMmqnTtAajJNUuamMohlgGLPpuUH"))

    def test_corrigir_palavra_031(self):
        self.assertEqual("FundamentosDaProgramacao", target.corrigir_palavra("FNnYyuOonDNnddFfgGsSaEemDdVOmMoDdvyGgYCcyOoYsSentohXKkxHsPpVvDatTPrUuRrogrnNamaCcIiYGHoOhgeEHhWwycCXxzZdDJzZjceEAaaqQyYodpPD"))

    def test_corrigir_palavra_032(self):
        self.assertEqual("supercalifragilisticoespialidoso", target.corrigir_palavra("yYsupGgwWeEPPpNneENnFfRtTrYypfaAdDFerlLoOcaAascCSzeEZIjJFfiFVKkvflrKkRifTtragXxvVZxQHhsSdDqXgqQGnkZzKNlLzImMuUiyYnaANdDXfFxjJhHcCnNirDdRtTlKkUuilLsPptHnNhiGgbBcowVvWyYesSspkEeKqQcJjCtTiaITIitQqiPOoplGglLLlxUuXMmDdLVvdDXxlidSsoxXscCo"))

    def test_eh_anagrama_003(self):
        """
        Exemplo enunciado (caso, SaCo)
        """
        self.assertTrue(target.eh_anagrama("caso", "SaCo"))

    def test_eh_anagrama_004(self):
        """
        Exemplo enunciado (caso, casos)
        """
        self.assertFalse(target.eh_anagrama("caso", "casos"))

    def test_eh_anagrama_033(self):
        self.assertFalse(target.eh_anagrama("amoro", "amora"))

    def test_eh_anagrama_034(self):
        self.assertTrue(target.eh_anagrama("Amor", "Roma"))
        
    def test_eh_anagrama_035(self):
        self.assertTrue(target.eh_anagrama("poder", "Pedro"))
        
    def test_eh_anagrama_036(self):
        self.assertTrue(target.eh_anagrama("QuidEstVeritas", "EstVirQuiAdest"))

    def test_corrigir_doc_005(self):
        """
        Exemplo enunciado (???)
        Deve lançar um ValueError
        """
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("???")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_006(self):
        """
        Exemplo enunciado (Buggy data base has wrong data)
        """
        doc = "BuAaXOoxiIKoOkggyrFfhHXxR duJjUTtaCcmMtaAGga eEMmtxXOjUuJQqQHhqoada JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn LyYlMmwmMrRrongTtoOkyYcCK daRfFKkLlhHrtZKqQkkvVKza"
        self.assertEqual("Buggy data base has wrong data", target.corrigir_doc(doc))

    def test_corrigir_doc_037(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc(5)
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))
        
    def test_corrigir_doc_038(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc(())
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))
        
    def test_corrigir_doc_039(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc(["a", "b", "c"])
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))
        
    def test_corrigir_doc_040(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc(1234567)
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))
        
    def test_corrigir_doc_041(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.corrigir_doc("Fundamentos da Programacao.")
        self.assertEqual("corrigir_doc: argumento invalido", str(ctx.exception))

    def test_corrigir_doc_042(self):
        doc = "Fundamentos da Programacao"
        self.assertEqual("Fundamentos da Programacao", target.corrigir_doc(doc))
        
    def test_corrigir_doc_043(self):
        doc = "Fundamentos da Programacao e Programacao com objetos"
        self.assertEqual("Fundamentos da Programacao e Programacao com objetos", target.corrigir_doc(doc))
        
    def test_corrigir_doc_044(self):
        doc = "Fundamentos da Programacao e Programacao com objetos"
        self.assertEqual("Fundamentos da Programacao e Programacao com objetos", target.corrigir_doc(doc))
        
    def test_corrigir_doc_045(self):
        doc = "Programacao com objetos e bojetos"
        self.assertEqual("Programacao com objetos e", target.corrigir_doc(doc))
        
    def test_corrigir_doc_046(self):
        doc = "FuKknfbBFdamvVEIicCeetTntUJjuos DddBfFbrRQKkquUlLNnajJ NnzZPnNrBbbBdDogDvVdrwoOWamTtaSfFscwkKWaouUtbBTKQqk"
        self.assertEqual("Fundamentos da Programacao", target.corrigir_doc(doc))
        
    def test_corrigir_doc_047(self):
        doc = "ProgtBbTrajJmagGcaGgo FfZqQzcmYyQSsqMomPZzUuERraAJjep JjFfqQobjKkuUkKetQqSspPCcAaEeovVTtSvVtTvVss eMmlxqQXOoIiLLlOo XxbhHodDWwjejJtwWoOos"
        self.assertEqual("Programacao com objetos e", target.corrigir_doc(doc))
        
    def test_corrigir_doc_048(self):
        doc = "ErgGAaxXrRhVvHsSUuJjapPnN WwNnXxgGXxlLMmYyla sgGAauOyEeYoTtmsSoOwkKWaGg CtTcpiIPZJcCjzShHkKsBbmuzVvzZkKdBbDZGgYyszZa sNnjoOJbBTtouvenXxCTtcidDr HGguUYyhdBaAbPpKkeZzlCc univeZUubYRvVryBzKkiIrLlNnsMmLnNlo IiFfaAlOoVuUjJAavPpiIaMmdHhDBbgG ixXiIPpnmacutlLTzZlrRadIia cXtTxayYyYlyiIYumnuUiAaaSsdEejJa DdbiIryYiLjJloJjfFSsBbAWwayYyYsCcpGgGgPgGaaA uUdDIhHiwWyPTtpBbhvVHIiYUvwWVuCcy sLlCQqFfPphHHhLlcoDdgGxXPpFfIibBbriTJjaAtaQqsS drRDmadDrBseESbizZonTtFfUucCeta LoOlmhHonhHbaABeHoOhtaRiIrrMmiuDdUwWaLEeljJZz danesa de"
        self.assertEqual("Era la suma souvenir del la inmaculada briosa y marioneta danesa de", target.corrigir_doc(doc))

        
                
class TestPIN2(unittest.TestCase):
    """
    obter_posicao, apenas um caractere + inteiro, dados oficiais não obtidos.
    Estes testes estão mai completos que os oficiais, ambiguidades não presentes.
    Exercícios: 007, 049, 050, 051, 052, 053, 054, 055, 056
    """
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

        
    def test_obter_digito_008(self):
        self.assertEqual(1, target.obter_digito("CEE", 5))

    def test_obter_digito_057(self):
        self.assertEqual(5, target.obter_digito("DDCEDEB", 3))
       
    def test_obter_digito_058(self):
        self.assertEqual(8, target.obter_digito("DDCEDEB", 8))
       
    def test_obter_digito_059(self):
        self.assertEqual(8, target.obter_digito("DDCEDEB", 9))
        
    def test_obter_digito_060(self):
        self.assertEqual(8, target.obter_digito("DBDEBCBEBD", 5))
       
    
    def test_obter_pin_009(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(())
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_010(self):
        t = ("CEE", "DDBBB", "ECDBE", "CCCCB")
        self.assertEqual((1, 9, 8, 5), target.obter_pin(t))
        
    def test_obter_pin_061(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(25)
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_062(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("CEE"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))
    
    def test_obter_pin_063(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(["CEE", "DDBBB", "ECDBE", "CCCCB"])
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_064(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("CEE", "DDBBBA", "ECDBE", "CCCCB"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_065(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("CEE", "DDBBB", "", "CCCCB"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))
        
    def test_obter_pin_066(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.obter_pin(("DDBBB", "ECDBE", "CCCCB"))
        self.assertEqual("obter_pin: argumento invalido", str(ctx.exception))

    def test_obter_pin_067(self):
        t = ("BCCDBDCE", "BDEEC", "EDCCEBB", "EECCDBEBC")
        self.assertEqual((2, 1, 7, 4), target.obter_pin(t))
        
    def test_obter_pin_068(self):
        t = ("DBCDEE", "DDDDE", "DCE", "BB", "EDDD", "BD")
        self.assertEqual((4, 5, 2, 8, 9, 9), target.obter_pin(t))
        
    def test_obter_pin_069(self):
        t = ("BDD", "BBBEE", "BCCBEE", "EDCCDB", "EDECD", "DDCED", "CB", "BCE", "DCB", "CEBCEB")
        self.assertEqual((9, 7, 4, 6, 3, 3, 6, 5, 6, 4), target.obter_pin(t))
        

        
class TestVerificacaoDados3(unittest.TestCase):
    def test_eh_entrada_011(self):
        self.assertFalse(target.eh_entrada(("a-b-c-d-e-f-g-h", "[abcd]", (950, 300))))

    def test_eh_entrada_012(self):
        self.assertFalse(target.eh_entrada(("a-b-c-d-e-f-g-h-2", "[abcde]", (950, 300))))

    def test_eh_entrada_013(self):
        self.assertTrue(target.eh_entrada(("a-b-c-d-e-f-g-h", "[xxxxx]", (950, 300))))
        
    def test_eh_entrada_018(self):
        self.assertTrue(target.eh_entrada(("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223, 424, 1316, 99))))

    def test_eh_entrada_070(self):
        self.assertFalse(target.eh_entrada(()))

    def test_eh_entrada_071(self):
        self.assertFalse(target.eh_entrada(["a-b-c-d-e-f-g-h", "[abcde]", (950, 300)]))

    def test_eh_entrada_072(self):
        self.assertFalse(target.eh_entrada(("a-b-c-d-e-f-g-h", "[abcde]")))

    def test_eh_entrada_073(self):
        self.assertFalse(target.eh_entrada(("a-b-c-d-e-f-g-h", "[abcde]", (950,300), "ola")))

    def test_eh_entrada_074(self):
        self.assertFalse(target.eh_entrada(("ERRADO", "[abcde]", (950, 300))))

    def test_eh_entrada_075(self):
        self.assertFalse(target.eh_entrada(("errado2", "[abcde]", (950, 300))))

    def test_eh_entrada_076(self):
        self.assertFalse(target.eh_entrada(("ainda errado", "[abcde]", (950, 300))))

    def test_eh_entrada_077(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", 25, (950, 300))))

    def test_eh_entrada_078(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "[12345]", (950, 300))))

    def test_eh_entrada_079(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "abcde", (950, 300))))

    def test_eh_entrada_080(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "[abcde]", (950, ))))

    def test_eh_entrada_081(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "[abcde]", 950)))

    def test_eh_entrada_082(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "[abcde]", (950, "a"))))

    def test_eh_entrada_083(self):
        self.assertFalse(target.eh_entrada(("ainda-errado", "[abcde]", (950, -30))))

    def test_eh_entrada_084(self):
        self.assertTrue(target.eh_entrada(("agora-sim", "[abcde]", (2, 3, 7, 200))))

    def test_eh_entrada_085(self):
        self.assertTrue(target.eh_entrada(("esta-entrada-e-correta", "[abzxy]", (20, 2, 1979))))


    def test_validar_cifra_014(self):
        self.assertFalse(target.validar_cifra("a-b-c-d-e-f-g-h", "[xxxxx]"))

    def test_validar_cifra_015(self):
        self.assertTrue(target.validar_cifra("a-b-c-d-e-f-g-h", "[abcde]"))

    def test_validar_cifra_086(self):
        self.assertFalse(target.validar_cifra("xxyyaabbcdcdeex", "[abcde]"))

    def test_validar_cifra_087(self):
        self.assertTrue(target.validar_cifra("fundamentos-da-programacao", "[aodmn]"))

    def test_validar_cifra_088(self):
        self.assertTrue(target.validar_cifra("xxyyaabbcdcdee", "[abcde]"))

    def test_validar_cifra_089(self):
        self.assertTrue(target.validar_cifra("lorem-ipsum-dolor-sit-amet-consectetur-adipiscing-elit-sed-do-eiusmod-tempor-incididunt-ut-labore-et-dolore-magna-aliqua-ut-enim-ad-minim-veniam-quis-nostrud-exercitation-ullamco-laboris-nisi-ut-aliquip-ex-ea-commodo-consequat-duis-aute-irure-dolor-in-reprehenderit-in-voluptate-velit-esse-cillum-dolore-eu-fugiat-nulla-pariatur-excepteur-sint-occaecat-cupidatat-non-proident-sunt-in-culpa-qui-officia-deserunt-mollit-anim-id-est-laborum", "[ietao]"))

    
    def test_filtrar_bdb_016(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb(" ")
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_017(self):
        self.assertEqual(
            [
                ("entrada-muito-errada", "[abcde]", (50, 404)),
            ],
            target.filtrar_bdb(
                [
                    ("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950, 300)),
                    ("a-b-c-d-e-f-g-h", "[abcde]", (124, 325, 7)),
                    ("entrada-muito-errada", "[abcde]", (50, 404)),
                ]
            ),
        )

    def test_filtrar_bdb_090(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb(())
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_091(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb([100])
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_092(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_bdb([(), ()])
        self.assertEqual("filtrar_bdb: argumento invalido", str(ctx.exception))

    def test_filtrar_bdb_093(self):
        self.assertEqual(
            [
                ("programar-e-fixe", "[raefh]", (3, 4, 5)),
            ],
            target.filtrar_bdb(
                [
                    ("programar-e-fixe", "[raefh]", (3, 4, 5)),
                    ("entrada-sem-erros", "[erasd]", (52, 404)),
                    ("fundamentos-da-programacao", "[aodmn]", (1, 2)),
                ]
            ),
        )

    def test_filtrar_bdb_094(self):
        self.assertEqual([],
            target.filtrar_bdb(
                [
                    ("beautiful-is-better-than-ugly", "[teuab]", (1, 2)),
                    ("explicit-is-better-than-implicit", "[itecl]", (3, 4)),
                    ("simple-is-better-than-complex", "[etilm]", (5, 6)),
                    ("complex-is-better-than-complicated", "[etcai]", (7, 8)),
                ]
            ),
        )

    def test_filtrar_bdb_095(self):
        self.assertEqual(
            [
                ("beautiful-is-better-than-ugly", "[etuab]", (1, 2)),
                ("explicit-is-better-than-implicit", "[tiecl]", (3, 4)),
                ("simple-is-better-than-complex", "[etiml]", (5, 6)),
                ("complex-is-better-than-complicated", "[etcia]", (7, 8)),
            ],
            target.filtrar_bdb(
                [
                    ("beautiful-is-better-than-ugly", "[etuab]", (1, 2)),
                    ("explicit-is-better-than-implicit", "[tiecl]", (3, 4)),
                    ("simple-is-better-than-complex", "[etiml]", (5, 6)),
                    ("complex-is-better-than-complicated", "[etcia]", (7, 8)),
                ]
            ),
        )


        
class TesteDesencriptacaoDeDados4(unittest.TestCase):
    def test_obter_num_seguranca_019(self):
        self.assertEqual(325, target.obter_num_seguranca((2223, 424, 1316, 99)))

    def test_obter_num_seguranca_096(self):
        self.assertEqual(70, target.obter_num_seguranca((777, 707, 901)))

    def test_obter_num_seguranca_097(self):
        self.assertEqual(161, target.obter_num_seguranca((4929, 19786, 6046, 18239, 17005, 17656, 11057, 14014, 11739, 17495)))

    def test_obter_num_seguranca_098(self):
        self.assertEqual(19, target.obter_num_seguranca((1390, 1558, 483, 1748, 1879, 1930, 1501, 41, 1175, 502)))

    def test_obter_num_seguranca_099(self):
        self.assertEqual(1, target.obter_num_seguranca((79, 1289, 589, 144, 1230, 275, 1016, 1200, 1933, 1383, 446, 795, 277, 1941, 1190, 441, 1788, 583, 1653, 1551, 56, 1286, 251, 1365, 723, 1501, 644, 1964, 404, 1631, 732, 252, 677, 1625, 902, 422, 131, 288, 136, 1387, 31, 1368, 20, 619, 1027, 475, 1256, 435, 1237, 387, 156, 385, 1013, 967, 1208, 1868, 386, 900, 675, 1191, 1627, 1437, 704, 1900, 591, 1145, 1275, 1296, 707, 1494, 1002, 1421, 99, 1774, 1334, 1283, 290, 548, 1127, 1199, 1515, 595, 297, 1339, 1700, 1748, 1390, 201, 216, 274, 266, 379)))
        

    def test_decifrar_texto_020(self):
        self.assertEqual(
            "esta cifra e quase inquebravel",
            target.decifrar_texto("qgfo-qutdo-s-egoes-wzegsnfmjqz", 325),
        )

    def test_decifrar_texto_100(self):
        self.assertEqual(
            "programar e muito fixe",
            target.decifrar_texto("bfaudoyod-q-yiuha-rwjs", 793),
        )

    def test_decifrar_texto_101(self):
        self.assertEqual(
            "beautiful is better than ugly",
            target.decifrar_texto("uztpmdype-bn-wxomzk-mcti-pzgr", 526),
        )

    def test_decifrar_texto_102(self):
        self.assertEqual(
            "explicit is better than implicit",
            target.decifrar_texto("vqgezvzm-bj-sxkmvk-myte-zfgezvzm", 1152),
        )

    def test_decifrar_texto_103(self):
        self.assertEqual(
            "simple is better than complex",
            target.decifrar_texto("fxzeyt-xf-otgirg-iupa-pdzeytk", 9060),
        )


    def test_decifrar_bdb_021(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.decifrar_bdb(["nothing"])
        self.assertEqual("decifrar_bdb: argumento invalido", str(ctx.exception))

    def test_decifrar_bdb_022(self):
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

    def test_decifrar_bdb_104(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.decifrar_bdb((('bfaudoyod-q-yiuha-rwjs', '[adouy]', (2, 795, 3223, 4316)), ('lctlgukvzwy-ji-xxwmzgugkgw', '[abxyz]', (2388, 367, 5999)), ('nyccjoj-vfrex-ncalml', '[xxxxx]', (50, 404))))
        self.assertEqual("decifrar_bdb: argumento invalido", str(ctx.exception))
        
    def test_decifrar_bdb_105(self):
        bdb = [
            ('bfaudoyod-q-yiuha-rwjs', '[adouy]', (2, 795, 3223, 4316)),
        ]
        self.assertEqual(
            [
                "programar e muito fixe",
            ],
            target.decifrar_bdb(bdb),
        )

    def test_decifrar_bdb_106(self):
        bdb = [
            ('qvplizula-xj-stkivg-iype-lvcn', '[ilvpa]', (762, 2586, 310)),
            ('avljeaer-go-xcprap-rdyj-ekljeaer', '[earjl]', (929, 2915, 380)),
            ('zrtysn-rz-inacla-coju-jxtysne', '[nacjr]', (3354, 33, 805, 1859)),
            ('dtp-kav-whivv-sx-pzmy-phl', '[pvhad]', (1706, 1048, 380, 4385))
        ]
        self.assertEqual(
            [
                "beautiful is better than ugly",
                "explicit is better than implicit",
                "simple is better than complex",
                "may the force be with you",
            ],
            target.decifrar_bdb(bdb),
        )
       
    
    
class TestDepuracao5(unittest.TestCase):
    def test_eh_utilizador_023(self):
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

    def test_eh_utilizador_024(self):
        """
        Exemplo enunciado {'name':'john.doe','pass':'aabcde','rule':{'vals':1,'char':'a'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"name": "john.doe", "pass": "aabcde", "rule": {"vals": 1, "char": "a"}}
            )
        )

    def test_eh_utilizador_107(self):
        self.assertFalse(target.eh_utilizador(56.7))

    def test_eh_utilizador_108(self):
        self.assertFalse(target.eh_utilizador(("name", "pass", "rule")))

    def test_eh_utilizador_109(self):
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

    def test_eh_utilizador_110(self):
        """
        Exemplo enunciado {'pass':'mynameisbatman','rule':{'vals':(2,8),'char':'m'}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"pass": "mynameisbatman", "rule": {"vals": (2, 8), "char": "m"}}
            )
        )

    def test_eh_utilizador_111(self):
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

    def test_eh_utilizador_112(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": 56,
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 8), "char": "m"},
                }
            )
        )

    def test_eh_utilizador_113(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {},
                }
            )
        )

    def test_eh_utilizador_114(self):
        """
        Exemplo enunciado {'name':'bruce.wayne','pass':'mynameisbatman','rule':{}}
        """
        self.assertFalse(
            target.eh_utilizador(
                {"name": "bruce.wayne", "pass": "mynameisbatman", "rule": {}}
            )
        )

    def test_eh_utilizador_115(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (2, 1), "char": "m"},
                }
            )
        )

    def test_eh_utilizador_116(self):
        self.assertFalse(
            target.eh_utilizador(
                {
                    "name": "bruce.wayne",
                    "pass": "mynameisbatman",
                    "rule": {"vals": (-2, 8), "char": "m"},
                }
            )
        )

    def test_eh_utilizador_117(self):
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

    def test_eh_utilizador_118(self):
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
        
    
    def test_eh_senha_valida_025(self):
        """
        Exemplo enunciado ('aabcd', {'vals': (1,3), 'char':'a'})
        """
        self.assertTrue(target.eh_senha_valida("aabcde", {"vals": (1, 3), "char": "a"}))

    def test_eh_senha_valida_026(self):
        """
        Exemplo enunciado ('cdefgh', {'vals': (1,3), 'char':'b'})
        """
        self.assertFalse(
            target.eh_senha_valida("cdefgh", {"vals": (1, 3), "char": "b"})
        )

    def test_eh_senha_valida_119(self):
        self.assertTrue(
            target.eh_senha_valida("aaaaa", {"vals": (1, 5), "char": "a"})
        )

    def test_eh_senha_valida_120(self):
        self.assertFalse(
            target.eh_senha_valida("aaaaaa", {"vals": (1, 5), "char": "a"})
        )

    def test_eh_senha_valida_121(self):
        self.assertFalse(
            target.eh_senha_valida("aaaaa", {"vals": (2, 5), "char": "d"})
        )

    def test_eh_senha_valida_122(self):
        self.assertFalse(
            target.eh_senha_valida("ddddei", {"vals": (2, 5), "char": "d"})
        )

    def test_eh_senha_valida_123(self):
        self.assertTrue(
            target.eh_senha_valida("addddei", {"vals": (2, 5), "char": "d"})
        )

    def test_eh_senha_valida_124(self):
        self.assertFalse(
            target.eh_senha_valida("adedidodei", {"vals": (2, 5), "char": "d"})
        )

    def test_eh_senha_valida_125(self):
        self.assertTrue(
            target.eh_senha_valida("ajejidojeii", {"vals": (3, 3), "char": "j"})
        )

    def test_eh_senha_valida_126(self):
        self.assertTrue(
            target.eh_senha_valida("aXaxaaa", {"vals": (1, 3), "char": "X"})
        )

    def test_eh_senha_valida_127(self):
        self.assertTrue(
            target.eh_senha_valida("..adedidodei", {"vals": (2, 5), "char": "d"})
        )

    def test_eh_senha_valida_128(self):
        self.assertTrue(
            target.eh_senha_valida("fundamentosdaprogramacao21-22", {"vals": (2, 5), "char": "n"})
        )


    def test_filtrar_senhas_027(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas([])
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_028(self):
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

    def test_filtrar_senhas_129(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas(())
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_130(self):
        with self.assertRaises(ValueError, msg="ValueError not raised") as ctx:
            target.filtrar_senhas("nothing")
        self.assertEqual("filtrar_senhas: argumento invalido", str(ctx.exception))

    def test_filtrar_senhas_131(self):
        bdb = [
            {
                'name': 'bruce.wayne',
                'pass': 'mynameisbatman',
                'rule': {'vals': (1, 3), 'char': 'm'},
            },
            {
                "name": "peter.parker",
                "pass": "sppidie",
                "rule": {"vals": (1, 4), "char": "p"},
            },
            {
                "name": "clark.kent",
                "pass": "notsure",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        self.assertEqual(
            ["bruce.wayne", "clark.kent"],
            target.filtrar_senhas(bdb),
        )

    def test_filtrar_senhas_132(self):
        bdb = [
            {
                "name": "bruce.wayne",
                "pass": "XXmynameisbatman",
                "rule": {"vals": (1, 3), "char": "m"},
            },
            {
                "name": "peter.parker",
                "pass": "spidie",
                "rule": {"vals": (1, 4), "char": "p"},
            },
            {
                "name": "clark.kent",
                "pass": "notsure",
                "rule": {"vals": (2, 9), "char": "c"},
            },
        ]

        self.assertEqual(
            ["clark.kent", "peter.parker"],
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
