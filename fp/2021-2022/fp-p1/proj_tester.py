import unittest
import importlib.util
import sys

if len(sys.argv) < 2:
    print(
        "Por favor escreve o caminho para o ficheiro: python proj_tester.py caminho/para/projeto.py"
    )
    exit(1)

file_name = sys.argv[1]

print("A ler ficheiro", file_name)

# Import project file and save all functions to the variable "target"
target_spec = importlib.util.spec_from_loader('target', loader=None)
target = importlib.util.module_from_spec(target_spec)
exec(open(file_name).read(), target.__dict__)


class TestDocumentacao1(unittest.TestCase):
    def test_corrigir_palavra_1(self):
        """
        Exemplo enunciado (database)
        """
        self.assertEqual('database',
                         target.corrigir_palavra('cCdatabasacCADde'))

    def test_corrigir_palavra_2(self):
        """
        Exemplo enunciado (x)
        """
        self.assertEqual('x', target.corrigir_palavra('abBAx'))

    def test_eh_anagrama_1(self):
        """
        Exemplo enunciado (caso, SaCo)
        """
        self.assertTrue(target.eh_anagrama('caso', 'SaCo'))

    def test_eh_anagrama_2(self):
        """
        Exemplo enunciado (caso, casos)
        """
        self.assertTrue(target.eh_anagrama('caso', 'casos'))

    def test_corrigir_doc_1(self):
        """
        Exemplo enunciado (???)
        Deve lançar um ValueError
        """
        with self.assertRaises(ValueError, msg='ValueError not raised') as ctx:
            target.corrigir_doc('???')
        self.assertEqual('corrigir_doc: argumento invalido',
                         str(ctx.exception))

    def test_corrigir_doc_2(self):
        """
        Exemplo enunciado (Buggy data base has wrong data)
        """
        doc = 'BuAaXOoxiIKoOkggyrFfhHXxR duJjUTtaCcmMtaAGga eEMmtxXOjUuJQqQHhqoada JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn LyYlMmwmMrRrongTtoOkyYcCK daRfFKkLlhHrtZKqQkkvVKza'
        self.assertEqual('Buggy data base has wrong data',
                         target.corrigir_doc(doc))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])