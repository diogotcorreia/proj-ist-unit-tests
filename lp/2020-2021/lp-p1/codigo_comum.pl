
:- use_module(library(clpfd)).
%-------------------------------------------------------------------------------
% mat_transposta(Matriz, Transp) significa que Transp e' a transposta de Matriz
%-------------------------------------------------------------------------------
mat_transposta(Matriz, Transp) :-
    transpose(Matriz, Transp).

%-------------------------------------------------------------------------------
%                escreve_Puzzle(Puzzle)
%-------------------------------------------------------------------------------
escreve_Puzzle(Puzzle) :-
    enche_puzzle(Puzzle, Puzzle_imprimir, Largura_total),
    n_caracteres(Largura_total, "-", Linha_tracos),
    writeln(Linha_tracos),
    maplist(escreve_Linha(Linha_tracos), Puzzle_imprimir).

escreve_Linha(Linha_tracos, Linha) :-
    maplist(escreve_celula, Linha),
    write('|'), nl,
    writeln(Linha_tracos).

escreve_celula(Cel) :-
    write('|'), write(Cel).

% tansformar o conteudo de uma celula em string
celula_para_string(Cel, Str) :-
    var(Cel), !, Str = "?"
                ;
    is_list(Cel), !, lista_para_str(Cel, Str)
                ;
    term_string(Cel, Str).

lista_para_str(Lst, Str) :-
    nth1(1, Lst, Num1),  nth1(2, Lst, Num2),
    numero_string(Num1, Num1_Str), numero_string(Num2, Num2_Str),
    string_concat(Num1_Str, "\\", Temp),
    string_concat(Temp, Num2_Str, Str).

numero_string(Num, Num_Str) :-
    Num == 0, !, Num_Str = " "
            ;
    term_string(Num, Num_Str).

linha_para_strings(L, Lst_Strs) :-
    maplist(celula_para_string, L, Lst_Strs).

puzzle_para_strings(Puzzle, Puzzle_Strs) :-
       maplist(linha_para_strings, Puzzle, Puzzle_Strs).


% determinar o comprimento maximo de uma celula do puzzle
comp_max_linha(Linha, Max) :-
    maplist(string_length, Linha, Comps),
    max_list(Comps, Max).

comp_max(Puzzle_Strs, Max) :-
    maplist(comp_max_linha, Puzzle_Strs, Comps),
    max_list(Comps, Max).

enche_celula(Num_pos, Cel_Str, Res) :-
    string_length(Cel_Str, Comp_Cel),
    Faltam is Num_pos - Comp_Cel,
    divide_2(Faltam, Inicio, Fim),
    n_caracteres(Inicio, " ", Espacos_inicio), n_caracteres(Fim, " ", Espacos_fim),
    string_concat(Espacos_inicio, Cel_Str, Temp),
    string_concat(Temp, Espacos_fim, Res).

enche_linha(Num_pos, Linha_Str, Res) :-
    maplist(enche_celula(Num_pos), Linha_Str, Res).

enche_puzzle(Puzzle, Puzzle_imprimir, Largura_total) :-
    puzzle_para_strings(Puzzle, Puzzle_Strs),
    comp_max(Puzzle_Strs, Max),
    nth1(1, Puzzle, L1), length(L1, Num_els_linha),
    Largura_total is Num_els_linha * Max + Num_els_linha + 1,
    maplist(enche_linha(Max), Puzzle_Strs, Puzzle_imprimir).

divide_2(N, Metade1, Metade2) :-
    Metade1 is N div 2,
    Resto is N mod 2,
    Metade2 is Metade1 + Resto.
        
n_caracteres(N, Caractere, N_caracteres) :-
    n_caracteres(N, Caractere, N_caracteres, "").
    
n_caracteres(N, Caractere, N_caracteres, Temp) :-
    string_length(Temp, N), N_caracteres = Temp, !
                    ;
    string_concat(Temp, Caractere, N_Temp),
    n_caracteres(N, Caractere, N_caracteres, N_Temp).

%-------------------------------------------------------------------------------
%                combinacao(N, Els, Comb)
% combinacao(N, Els, Comb) significa que Comb eh uma
% combinacao dos elementos de Els, N a N
%-------------------------------------------------------------------------------
combinacao(0,_,[]).
combinacao(N,[X|T], [X|Comb]):-
    N > 0,
    N1 is N-1,
    combinacao(N1, T, Comb).
combinacao(N, [_|T], Comb):-
    N > 0,
    combinacao(N, T, Comb).

