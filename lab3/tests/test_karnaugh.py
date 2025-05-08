import pytest
from unittest.mock import patch
from collections import defaultdict
import karnaugh_minimization as km

@pytest.fixture
def mock_build_truth_table():
    with patch('karnaugh_minimization.build_truth_table') as mock_build:
        yield mock_build

def test_get_karnaugh_map_indices():
    assert km.get_karnaugh_map_indices(1) == ['0', '1']
    assert km.get_karnaugh_map_indices(2) == (['0', '1'], ['0', '1'])
    assert km.get_karnaugh_map_indices(3) == (['0', '1'], ['00', '01', '11', '10'])
    assert km.get_karnaugh_map_indices(4) == (['00', '01', '11', '10'], ['00', '01', '11', '10'])
    assert km.get_karnaugh_map_indices(5) == (['00', '01', '11', '10'], ['000', '001', '011', '010', '110', '111', '101', '100'])
    with pytest.raises(ValueError, match="Поддерживаются только 1-5 переменных"):
        km.get_karnaugh_map_indices(6)

def test_get_binary_index_single_variable():
    assert km._get_binary_index(0, 0, 1, [''], ['0', '1']) == '0'
    assert km._get_binary_index(0, 1, 1, [''], ['0', '1']) == '1'

def test_get_binary_index_two_variables():
    assert km._get_binary_index(0, 0, 2, ['0', '1'], ['0', '1']) == '00'
    assert km._get_binary_index(1, 1, 2, ['0', '1'], ['0', '1']) == '11'

def test_get_binary_index_three_variables():
    assert km._get_binary_index(0, 0, 3, ['0', '1'], ['00', '01', '11', '10']) == '000'
    assert km._get_binary_index(1, 2, 3, ['0', '1'], ['00', '01', '11', '10']) == '111'

def test_get_binary_index_four_variables():
    assert km._get_binary_index(0, 0, 4, ['00', '01', '11', '10'], ['00', '01', '11', '10']) == '0000'
    assert km._get_binary_index(2, 3, 4, ['00', '01', '11', '10'], ['00', '01', '11', '10']) == '1110'

def test_get_binary_index_five_variables():
    assert km._get_binary_index(0, 0, 5, ['00', '01', '11', '10'], ['000', '001', '011', '010', '110', '111', '101', '100']) == '00000'
    assert km._get_binary_index(2, 5, 5, ['00', '01', '11', '10'], ['000', '001', '011', '010', '110', '111', '101', '100']) == '11111'

def test_build_karnaugh_map_single_variable():
    table = [['a', 'f'], [0, 0], [1, 1]]
    k_map = km.build_karnaugh_map(table, ['a'], "SDNF")
    assert k_map == [['0', '1']]  

def test_build_karnaugh_map_two_variables_sdnf():
    table = [['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    k_map = km.build_karnaugh_map(table, ['a', 'b'], "SDNF")
    assert k_map == [['0', '1'], ['0', '1']] 

def test_build_karnaugh_map_two_variables_sknf():
    table = [['a', 'b', 'f'], [0, 0, 1], [0, 1, 0], [1, 0, 1], [1, 1, 0]]
    k_map = km.build_karnaugh_map(table, ['a', 'b'], "SKNF")
    assert k_map == [['1', '0'], ['1', '0']] 

def test_build_karnaugh_map_three_variables():
    table = [['a', 'b', 'c', 'f']] + [[int(b) for b in format(i, '03b')] + [1 if i in [1, 3, 5, 7] else 0] for i in range(8)]
    k_map = km.build_karnaugh_map(table, ['a', 'b', 'c'], "SDNF")
    assert k_map == [['0', '1', '1', '0'], ['0', '1', '1', '0']]

def test_build_karnaugh_map_five_variables():
    table = [['a', 'b', 'c', 'd', 'e', 'f']] + [[int(b) for b in format(i, '05b')] + [0] for i in range(32)]
    k_map = km.build_karnaugh_map(table, ['a', 'b', 'c', 'd', 'e'], "SDNF")
    assert k_map == [['0'] * 8 for _ in range(4)]

def test_build_karnaugh_map_invalid_variables():
    table = [['a', 'b', 'c', 'd', 'e', 'f', 'g']] + [[0] * 7]
    with pytest.raises(ValueError, match="Поддерживаются только 1-5 переменных"):
        km.build_karnaugh_map(table, ['a', 'b', 'c', 'd', 'e', 'f'], "SDNF")

def test_print_karnaugh_map_empty():
    with patch('builtins.print') as mocked_print:
        km.print_karnaugh_map([], ['a'])
        mocked_print.assert_called_with("Карта Карно пуста")

def test_print_karnaugh_map_five_variables():
    k_map = [['0'] * 8 for _ in range(4)]
    with patch('builtins.print') as mocked_print:
        km.print_karnaugh_map(k_map, ['a', 'b', 'c', 'd', 'e'])
        mocked_print.assert_any_call("\nКарта Карно (ab\\cde):")
        mocked_print.assert_any_call("    |000 |001 |011 |010 |110 |111 |101 |100 |")
        mocked_print.assert_any_call(" 00 | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |")
        mocked_print.assert_any_call(" 01 | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |")
        mocked_print.assert_any_call(" 11 | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |")
        mocked_print.assert_any_call(" 10 | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |")
        mocked_print.assert_any_call("    |        c=0        |        c=1        |")

def test_get_target_indices_sdnf():
    table = [['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    indices = km.get_target_indices(table, "SDNF")
    assert indices == [1, 3] 

def test_get_target_indices_empty():
    table = [['a', 'f'], [0, 0], [1, 0]]
    indices = km.get_target_indices(table, "SDNF")
    assert indices == []

def test_int_to_binary():
    assert km.int_to_binary(0, 2) == '00'
    assert km.int_to_binary(3, 2) == '11'
    assert km.int_to_binary(5, 3) == '101'

def test_count_set_bits():
    assert km.count_set_bits('110') == 2
    assert km.count_set_bits('000') == 0
    assert km.count_set_bits('1-1') == 2

def test_combine_terms_valid():
    term1 = {'binary': '00', 'indices': {0}}
    term2 = {'binary': '01', 'indices': {1}}
    result = km.combine_terms(term1, term2)
    assert result == ('0-', {0, 1})

def test_combine_terms_no_diff():
    term1 = {'binary': '00', 'indices': {0}}
    term2 = {'binary': '00', 'indices': {0}}
    result = km.combine_terms(term1, term2)
    assert result is None

def test_combine_terms_multiple_diffs():
    term1 = {'binary': '00', 'indices': {0}}
    term2 = {'binary': '11', 'indices': {3}}
    result = km.combine_terms(term1, term2)
    assert result is None

def test_combine_terms_different_lengths():
    term1 = {'binary': '00', 'indices': {0}}
    term2 = {'binary': '000', 'indices': {0}}
    result = km.combine_terms(term1, term2)
    assert result is None
def test_binary_to_term_string_sdnf():
    binary = '01-'
    variables = ['a', 'b', 'c']
    term = km.binary_to_term_string(binary, variables, "SDNF")
    assert term == '¬a∧b'

def test_binary_to_term_string_sknf():
    binary = '01-'
    variables = ['a', 'b', 'c']
    term = km.binary_to_term_string(binary, variables, "SKNF")
    assert term == 'a∨¬b'

def test_binary_to_term_string_all_dashes_sdnf():
    binary = '--'
    variables = ['a', 'b']
    term = km.binary_to_term_string(binary, variables, "SDNF")
    assert term == '1'

def test_binary_to_term_string_all_dashes_sknf():
    binary = '--'
    variables = ['a', 'b']
    term = km.binary_to_term_string(binary, variables, "SKNF")
    assert term == '0'

def test_find_prime_implicants_qm_sdnf():
    indices = [1, 3]  
    variables = ['a', 'b']
    pis, steps = km.find_prime_implicants_qm(indices, 2, variables, "SDNF")
    assert any(pi['binary'] == '-1' for pi in pis) 
    assert steps == ['¬a∧b (01) + a∧b (11) → b (-1) (индексы: [1, 3])']

def test_find_prime_implicants_qm_empty():
    pis, steps = km.find_prime_implicants_qm([], 1, ['a'], "SDNF")
    assert pis == []
    assert steps == []

def test_select_essential_implicants_no_essentials():
    pis = [
        {'binary': '0-', 'indices': {0, 1}},
        {'binary': '-0', 'indices': {0, 1}}
    ]
    indices = [0, 1]
    essentials = km.select_essential_implicants(pis, indices)
    assert len(essentials) == 1 

def test_select_essential_implicants_empty():
    assert km.select_essential_implicants([], [1]) == []
    assert km.select_essential_implicants([{'binary': '0', 'indices': {0}}], []) == []
def test_minimize_karnaugh_sdnf(mock_build_truth_table):
    table = [['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    mock_build_truth_table.return_value = table
    k_map, dnf, cnf, steps_dnf, steps_cnf = km.minimize_karnaugh('a ∧ b', ['a', 'b'])
    assert k_map == [['0', '1'], ['0', '1']]
    assert dnf == 'b'
    assert steps_dnf == ['¬a∧b (01) + a∧b (11) → b (-1) (индексы: [1, 3])']

def test_print_karnaugh_results_error(mock_build_truth_table):
    mock_build_truth_table.side_effect = ValueError("Invalid input")
    with patch('builtins.print') as mocked_print:
        km.print_karnaugh_results('a ∧ b', ['a', 'b'])
        mocked_print.assert_any_call("Ошибка: Invalid input")