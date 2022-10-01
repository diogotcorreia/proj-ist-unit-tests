# Unit tests para Projeto 1 FP 2021-2022

## O que são?

_Unit tests_ são testes a partes de um certo programa.
Neste caso, poderão aqui encontrar um ou mais testes para cada função pedida no enunciado.

Estes testes vêm do enunciado, são criados por alunos, ou podem ser mesmo dos professores.
Aceitam-se contribuições para mais testes.

## Como usar?

1. Fazer download do ficheiro [proj_tester.py](https://raw.githubusercontent.com/diogotcorreia/proj-ist-unit-tests/master/fp/2022-2023/fp-p1/proj_tester.py), basta fazer `CTRL+S`.
2. Guardar o ficheiro numa pasta (preferencialmente sozinho, pois irá ser criado um ficheiro `.update_lock` na mesma para verificar atualizações).
3. Ir para a pasta do ficheiro de testes no terminal executando o seguinte comando:

    ```bash
    cd caminho/para/a/pasta
    ```
    Por exemplo, `C:\Users\diogo\Documents\FP\Tester` ou `/home/diogo/Documents/FP/Tester`.

4. Executar o ficheiro com o python com o seguinte comando:

    ```bash
    python proj_tester.py caminho/para/projeto.py
    ```

    Ou

    ```bash
    python proj_tester.py caminho/para/projeto.py 2> resultados.txt
    ```

    Onde devem substituir com o caminho para o projeto. Pode ser um caminho relativo, e depende do sistema operativo.

    Por exemplo, `C:\Users\diogo\Documents\FP\projeto.py` (para Windows) ou `/home/diogo/Documents/FP/projeto.py` (para Linux/macOS).

    Se utilizarem o último comando podem visualizar os resultados no ficheiro `resultados.txt` na pasta onde foi guardado o ficheiro `proj_tester.py`.
    

    Caso apareça o erro `ImportError: No module named requests` têm de correr este comando:
    ```bash
    pip install requests
    ```
    Se o anterior tiver dado erro corram este:
    ```bash
    pip3 install requests
    ```

    Se aparecer `ModuleNotFoundError: No module named 'pytest'` tente:
    ```bash
    pip install pytest
    ```

5. O script recebe também os mesmos argumentos que o pytest, ou seja é possivel pedir erros mais detalhados:
    ```bash
    python proj_tester.py caminho/para/projeto.py -vv 
    ```
    
    Ou pedir só para fazer testes a certas partes:
    ```bash
    python proj_tester.py caminho/para/projeto.py -k JustificarTextos
    ```
    Também para MetodoHondt e SistemasLineares

## Como contribuir?

É normal que ainda não saibam usar Git! Caso tenham interesse em contribuir com testes, falem comigo (Diogo Correia) que vos posso ensinar o suficiente de Git para conseguirem adicionar novos testes.

Caso queiram aprender sozinhos, deixo aqui uma palestra do MIT onde acabam por perceber como Git funciona bastante bem:

- [MIT Missing Semester: Version Control](https://missing.csail.mit.edu/2020/version-control/)
