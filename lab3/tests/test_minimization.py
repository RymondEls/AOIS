import pytest
from unittest.mock import patch
import minimization as mm

@pytest.fixture
def mock_logic_operations():
    with patch('minimization.build_truth_table') as mock_build, \
         patch('minimization.get_normal_forms') as mock_forms:
        yield mock_build, mock_forms

def test_parse_term_sdnf():
    term = 'a∧¬b'
    variables = ['a', 'b']
    binary = mm.parse_term(term, variables)
    assert binary == [1, 0]

def test_parse_term_sknf():
    term = 'a∨¬b'
    variables = ['a', 'b']
    binary = mm.parse_term(term, variables)
    assert binary == [1, 0]

def test_parse_term_invalid_variable():
    term = 'x∧b'
    variables = ['a', 'b']
    binary = mm.parse_term(term, variables)
    assert binary == [None, 1]

def test_terms_to_binary():
    terms = ['a∧b', '¬a∧b']
    variables = ['a', 'b']
    binary_terms = mm.terms_to_binary(terms, variables)
    assert binary_terms == [[1, 1], [0, 1]]

def test_can_glue_valid():
    term1 = [1, 1]
    term2 = [1, 0]
    can, pos = mm.can_glue(term1, term2)
    assert can == True
    assert pos == 1

def test_can_glue_invalid():
    term1 = [1, 1]
    term2 = [0, 0]
    can, pos = mm.can_glue(term1, term2)
    assert can == False
    assert pos == -1

def test_glue_terms_sdnf():
    term1 = [1, 1]
    term2 = [1, 0]
    variables = ['a', 'b']
    new_term, new_str = mm.glue_terms(term1, term2, 1, variables, "SDNF")
    assert new_term == [1, 'X']
    assert new_str == 'a'

def test_glue_terms_sknf():
    term1 = [1, 1]
    term2 = [1, 0]
    variables = ['a', 'b']
    new_term, new_str = mm.glue_terms(term1, term2, 1, variables, "SKNF")
    assert new_term == [1, 'X']
    assert new_str == 'a'

def test_glue_terms_all_dashes():
    term1 = ['X', 1]
    term2 = ['X', 0]
    variables = ['a', 'b']
    new_term, new_str = mm.glue_terms(term1, term2, 1, variables, "SDNF")
    assert new_term == ['X', 'X']
    assert new_str == ''

def test_is_term_covered():
    term_binary = [1, 'X']
    minterm_binary = [1, 1]
    assert mm.is_term_covered(term_binary, minterm_binary) == True

def test_is_term_covered_false():
    term_binary = [1, 'X']
    minterm_binary = [0, 1]
    assert mm.is_term_covered(term_binary, minterm_binary) == False

def test_calculation_method_sdnf():
    terms = ['a∧b', '¬a∧b']
    variables = ['a', 'b']
    steps, result = mm.calculation_method(terms, variables, "SDNF")
    assert 'b' in result
    assert len(steps) > 0

def test_calculation_method_sknf():
    terms = ['(a∨b)', '(¬a∨b)']
    variables = ['a', 'b']
    steps, result = mm.calculation_method(terms, variables, "SKNF")
    assert 'b' in result
    assert len(steps) > 0

def test_calculation_method_empty():
    steps, result = mm.calculation_method([], ['a'], "SDNF")
    assert steps == []
    assert result == []
    
def test_minimize_calculation_empty(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    table = [['a', 'f'], [0, 0], [1, 0]]
    mock_build.return_value = table
    mock_forms.return_value = ('', '1', [], [])
    steps, result = mm.minimize_calculation('0', ['a'], "SDNF")
    assert result == '0'

def test_print_calculation_results(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    table = [['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    mock_build.return_value = table
    mock_forms.return_value = ('(¬a∧b)∨(a∧b)', '(a∨¬b)∧(¬a∨b)', [], [])
    with patch('builtins.print') as mocked_print:
        mm.print_calculation_results('a ∧ b', ['a', 'b'])
        assert mocked_print.called

def test_print_calculation_results_empty(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    table = [['a', 'f'], [0, 0], [1, 0]]
    mock_build.return_value = table
    mock_forms.return_value = ('', '1', [], [])
    with patch('builtins.print') as mocked_print:
        mm.print_calculation_results('0', ['a'])
        mocked_print.assert_any_call("СДНФ пуста или не подлежит минимизации")