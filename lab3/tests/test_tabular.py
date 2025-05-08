import pytest
from unittest.mock import patch
import tabular_computed_minimization as tcm

@pytest.fixture
def mock_logic_operations():
    with patch('tabular_computed_minimization.build_truth_table') as mock_build, \
         patch('tabular_computed_minimization.get_normal_forms') as mock_forms:
        yield mock_build, mock_forms

def test_build_coverage_table_empty():
    assert tcm.build_coverage_table([], [], ['a'], "SDNF") == []

def test_find_essential_implicants_full_coverage():
    coverage = [[True, False], [False, True]]
    minterms = ['a∧b', '¬a∧b']
    implicants = [('a∧b', ['1', '1']), ('¬a∧b', ['0', '1'])]
    essentials = tcm.find_essential_implicants(coverage, minterms, implicants)
    assert essentials == ['a∧b', '¬a∧b']

def test_find_essential_implicants_no_essentials():
    coverage = [[True, True], [True, True]]
    minterms = ['a∧b', '¬a∧b']
    implicants = [('a', ['1', 'X']), ('b', ['X', '1'])]
    essentials = tcm.find_essential_implicants(coverage, minterms, implicants)
    assert len(essentials) == 1  # Greedy selection picks one

def test_tabular_calculation_method_empty():
    steps, coverage, pis, essentials = tcm.tabular_calculation_method([], ['a'], "SDNF")
    assert steps == []
    assert coverage == []
    assert pis == []
    assert essentials == []

def test_tabular_calculation_method_sdnf_simple():
    terms = ['a∧b', '¬a∧b']
    variables = ['a', 'b']
    steps, coverage, pis, essentials = tcm.tabular_calculation_method(terms, variables, "SDNF")
    assert len(steps) > 0
    assert len(coverage) == 2
    assert any('b' in pi[0] for pi in pis)
    assert 'b' in essentials

def test_tabular_calculation_method_sknf_complex():
    terms = ['(a∨b∨c)', '(¬a∨b∨c)', '(a∨¬b∨c)']
    variables = ['a', 'b', 'c']
    steps, coverage, pis, essentials = tcm.tabular_calculation_method(terms, variables, "SKNF")
    assert len(steps) > 0
    assert len(coverage) == 3
    assert any('b∨c' in pi[0] for pi in pis)
    assert 'b∨c' in essentials

def test_minimize_tabular_sdnf(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    mock_build.return_value = [
        ['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]
    ]
    mock_forms.return_value = ('(¬a∧b)∨(a∧b)', '', [], [])
    steps, coverage, pis, essentials, terms, op, result = tcm.minimize_tabular('a ∧ b', ['a', 'b'], "SDNF")
    assert op == '∨'
    assert result == 'b'

def test_minimize_tabular_constant_one_sknf(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    mock_build.return_value = [['a', 'f'], [0, 1], [1, 1]]
    mock_forms.return_value = ('', '1', [], [])
    steps, coverage, pis, essentials, terms, op, result = tcm.minimize_tabular('1', ['a'], "SKNF")
    assert result == '1'

def test_print_coverage_table():
    original_terms = ['a∧b', '¬a∧b']
    pis = [('b', ['X', '1'])]
    coverage = [[True], [True]]
    variables = ['a', 'b']
    with patch('builtins.print') as mocked_print:
        tcm.print_coverage_table(original_terms, pis, coverage, variables)
        assert mocked_print.called

def test_print_coverage_table_empty():
    with patch('builtins.print') as mocked_print:
        tcm.print_coverage_table([], [], [], ['a'])
        mocked_print.assert_called_with("Таблица покрытия пуста или нет данных для отображения.")

def test_print_tabular_results(mock_logic_operations):
    mock_build, mock_forms = mock_logic_operations
    mock_build.return_value = [
        ['a', 'b', 'f'], [0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]
    ]
    mock_forms.return_value = ('(¬a∧b)∨(a∧b)', '(a∨¬b)∧(¬a∨b)', [], [])
    with patch('builtins.print') as mocked_print:
        tcm.print_tabular_results('a ∧ b', ['a', 'b'])
        assert mocked_print.called