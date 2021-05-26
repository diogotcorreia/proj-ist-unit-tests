# FAQs

Esta página é dedicada a agregar respostas dadas pelos professores no Slack e outros meios.

Para adicionar uma pergunta/resposta, editem este ficheiro (dá para fazê-lo diretamente no GitHub!).

### Em que casos temos de usar o `#define`?

É recomendado usar o `#define` para:

- Definir constantes globais (e.g. tamanho de arrays, strings, etc)
- Definir mensagens usadas no `printf` (e.g. `task %d`)
- _(opcional)_ Definir exit codes do programa (e.g. `0`, `-1`, etc)

(Prof. Reis Santos)

### Quão bem/mal formatado é o input?

> "O input é sempre bem formatado, com um comando por linha. Não precisa verificar a sanidade dos dados, mas onde se pede um inteiro decimal, este pode ser passado um valor positivo ou negativo, mesmo que tal não esteja no domínio da função. Não vai haver espaços brancos no início ou no fim, mas no meio do comando pode haver vários espaços brancos." -Prof. Reis Santos

#### Follow-up: Se vão haver valores que não estão no domínio, o que fazemos com, por exemplo, `t -10 description`?

> "O programa deve reportar o erro e continuar. Neste caso devia ser 'invalid duration', como no caso do tempo, ~~mas a mensagem não está no enunciado~~. Para já assuma que mensagem existe."
>
> "Se não está no enunciado, não vai ser testado. Qualquer atilização [sic] será indicada no log." -Prof. Reis Santos

Update: Mensagem adicionada ao enunciado do projeto

### O que é suposto acontecer se não recebermos nenhum dos comandos (caracteres) possíveis?

> "Os comandos têm os argumentos em número e tipo corretos. Os erros possíveis estão assinalados por comando." -Prof. Reis Santos

### Se tivermos o projeto estruturado em vários ficheiros .c, é suposto termos um ficheiro .h para cada .c?

> "Um só .h (em C++, com classes, é que se justifica um .h por cada .c)." -Prof. Reis Santos

### Podemos utilizar as funções `malloc` e `free`?

> "Não deve reservar memória (`malloc`, ..) neste projeto." -Prof. Reis Santos

### Se o comando `l` for invocado _com_ argumentos, "as tarefas devem ser listadas pela ordem dos respetivos <id>s" significa que devem ser listados pela ordem númerica dos IDs ou pela ordem com que aparecem na lista de argumentos do comando?

> "Pela ordem que aparecem no comando `l`" -Prof. Reis Santos

### Com que informação é que preenchemos o campo de utilizador de uma nova tarefa?

> "O comando move '`m`' atribui um utilizador à tarefa, até lá não tem utilizador atribuído." -Prof. Reis Santos

### Na função `l` não se deveria saber quantos IDs são introduzidos?

> "O número de IDs não vem especificado. Devem ler todos os IDs nessa linha." -Prof. Vasco Manquinho

### Podemos fazer passagens por referência/usar pointers no projeto?

(Extrapolado de inteiros para todos os tipos) Sim. (Prof. Reis Santos)
