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


#######################################################
# Logic to handle updates automatically. DO NOT TOUCH #
#######################################################


def get_lastest_commit_hash():
    try:
        result = requests.get(
            "https://api.github.com/repos/diogotcorreia/proj-ist-unit-tests/commits?path=fp%2F2021-2022%2Ffp-p1%2Fproj_tester.py&page=1&per_page=1"
        )
        return result.json()[0]['sha']
    except:
        print(
            "Não foi possível verificar novas atualizações (o GitHub apenas permite 60 verificações por hora)"
        )


def get_saved_commit_hash():
    try:
        return open('.update_lock').read()
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
    if response.lower() == 'y':
        update_files(latest_hash)
    else:
        print("Os testes não foram atualizados a pedido do utilizador")


def update_files(new_hash):
    print("A atualizar os testes...")
    open('.update_lock', 'w+').write(new_hash)

    new_file = requests.get(
        "https://raw.githubusercontent.com/diogotcorreia/proj-ist-unit-tests/master/fp/2021-2022/fp-p1/proj_tester.py"
    )
    open('proj_tester.py', 'w+').write(new_file.text)

    print("Volta a executar o programa para carregar os novos testes")
    exit()


if __name__ == '__main__':
    check_for_updates()
    unittest.main(argv=['first-arg-is-ignored'])
