import pytest
from logic_operations import function_spellcheck, shunting_yard, evaluate_rpn, build_truth_table, get_normal_forms, print_truth_table, OPERATORS

def test_function_spellcheck_valid():
    variables, is_valid = function_spellcheck("a & b | !c")
    assert variables == ['a', 'b', 'c']
    assert is_valid is True

def test_function_spellcheck_invalid_char():
    variables, is_valid = function_spellcheck("a & b | 2")
    assert is_valid is False

def test_function_spellcheck_unbalanced_brackets():
    variables, is_valid = function_spellcheck("(a & b")
    assert is_valid is False

def test_function_spellcheck_empty():
    variables, is_valid = function_spellcheck("")
    assert variables == []
    assert is_valid is True

def test_shunting_yard_simple():
    assert shunting_yard("a & b") == ['a', 'b', '&']

def test_shunting_yard_with_not():
    assert shunting_yard("!a & b") == ['a', '!', 'b', '&']

def test_shunting_yard_with_brackets():
    assert shunting_yard("(a | b) & c") == ['a', 'b', '|', 'c', '&']

def test_shunting_yard_complex():
    assert shunting_yard("!a & (b | c)") == ['a', '!', 'b', 'c', '|', '&']

def test_evaluate_rpn_and():
    rpn = ['a', 'b', '&']
    variables = ['a', 'b']
    values = {'a': True, 'b': False} 
    result, _ = evaluate_rpn(rpn, variables, values)
    assert result == 0

def test_evaluate_rpn_or():
    rpn = ['a', 'b', '|']
    variables = ['a', 'b']
    values = {'a': False, 'b': True} 
    result, _ = evaluate_rpn(rpn, variables, values)
    assert result == 1

def test_evaluate_rpn_not():
    rpn = ['a', '!']
    variables = ['a']
    values = {'a': True}
    result, steps = evaluate_rpn(rpn, variables, values)
    assert result == 0
    assert steps == [('!a', 0)]

def test_evaluate_rpn_implication():
    rpn = ['a', 'b', '>']
    variables = ['a', 'b']
    values = {'a': True, 'b': False}
    result, steps = evaluate_rpn(rpn, variables, values)
    assert result == 0
    assert steps == [('(a>b)', 0)]

def test_build_truth_table():
    expression = "a & b"
    variables = ['a', 'b']
    table = build_truth_table(expression, variables)
  
    assert len(table) == 5 
    assert table[0] == ['a', 'b', '(a&b)', 'a & b']  
    
    assert [0, 0, 0, 0] in table[1:]  
    assert [1, 1, 1, 1] in table[1:]   

def test_get_normal_forms_and():
    table = [
        ['a', 'b', '(a&b)'],
        [0, 0, 0],  
        [0, 1, 0],  
        [1, 0, 0],  
        [1, 1, 1]   
    ]
    
    sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, ['a', 'b'])
    
    assert sdnf == "(a∧b)"
    
    assert "(¬a∨¬b)" in sknf  
    assert "(¬a∨b)" in sknf   
    assert "(a∨¬b)" in sknf 
    
    # Проверяем индексы
    assert idx_sdnf == [3]    
    assert set(idx_sknf) == {0, 1, 2} 

def test_get_normal_forms_or():
    table = [
        ['a', 'b', '(a|b)'],
        [0, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, ['a', 'b'])
    
    assert "(¬a∧b)" in sdnf
    assert "(a∧¬b)" in sdnf
    assert "(a∧b)" in sdnf
    assert sknf == "(¬a∨¬b)"

def test_print_truth_table(capsys):
    test_table = [
        ['a', 'b', 'a&b'],
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]
    
    print_truth_table(test_table)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "a" in output
    assert "b" in output
    assert "a&b" in output
    assert "0" in output
    assert "1" in output
    
    assert "+---" in output 
    assert "|" in output 
    assert output.count('\n') == 8 

def test_print_empty_table(capsys):
    print_truth_table([])
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Пустая таблица" in output
    assert output.strip() == "Пустая таблица" 

def test_print_table_with_long_values(capsys):
    long_table = [
        ['variable1', 'variable2', 'result'],
        [12345, 0, 'very_long_result_value'],
        [0, 98765, 'another_long_value']
    ]
    
    print_truth_table(long_table)
    captured = capsys.readouterr()
    output = captured.out

    assert "variable1" in output
    assert "very_long_result_value" in output
    assert "12345" in output

    lines = output.split('\n')
    for line in lines:
        if "|" in line: 
            parts = line.split('|')
            for part in parts[1:-1]: 
                stripped = part.strip()
                if stripped: 
                    assert part.startswith(' ') and part.endswith(' ')