from itertools import combinations
from minimization import parse_term, terms_to_binary, can_glue, glue_terms, is_term_covered
from logic_operations import get_normal_forms, build_truth_table

def build_coverage_table(minterms, implicants, variables, form_type="SDNF"):
    coverage = []
    for minterm in minterms:
        minterm_binary = parse_term(minterm, variables)
        row = []
        for implicant, implicant_binary in implicants:
            if is_term_covered(implicant_binary, minterm_binary):
                row.append(True)
            else:
                row.append(False)
        coverage.append(row)
    return coverage

def find_essential_implicants(coverage, minterms, implicants):
    essential_implicants = []
    covered_minterms = set()
    remaining_minterms = set(range(len(minterms)))

    for j, (implicant, _) in enumerate(implicants):
        covers = set(i for i in range(len(minterms)) if coverage[i][j])
        if covers - covered_minterms:
            unique_covers = [i for i in covers if sum(coverage[i]) == 1]
            if unique_covers:
                essential_implicants.append(implicant)
                covered_minterms.update(covers)
                remaining_minterms.difference_update(covers)

    while remaining_minterms:
        max_coverage = 0
        best_implicant = None
        best_idx = -1
        for j, (implicant, _) in enumerate(implicants):
            if implicant in essential_implicants:
                continue
            covers = set(i for i in remaining_minterms if coverage[i][j])
            if len(covers) > max_coverage:
                max_coverage = len(covers)
                best_implicant = implicant
                best_idx = j
        if best_implicant:
            essential_implicants.append(best_implicant)
            covers = set(i for i in remaining_minterms if coverage[i][best_idx])
            covered_minterms.update(covers)
            remaining_minterms.difference_update(covers)
        else:
            break

    return essential_implicants

def tabular_calculation_method(terms, variables, form_type="SDNF"):
    if not terms:
        return [], [], [], [] 

    binary_terms = terms_to_binary(terms, variables)

    current_implicants = []
    for i, term_str in enumerate(terms):
        bin_repr = parse_term(term_str, variables)
        current_implicants.append({'binary': bin_repr, 'str': term_str, 'used': False})

    steps = []
    seen_implicant_strings_globally = set(term_str for term_str in terms)
    
    all_passes_implicants_data = {term['str']: term for term in current_implicants}

    while True:
        next_pass_implicants_data = {} 
        glued_in_this_pass = False
        
        current_implicants_list = [data for data in all_passes_implicants_data.values() if not data['used']]
        
        for i in range(len(current_implicants_list)):
            for j in range(i + 1, len(current_implicants_list)):
                term1_data = current_implicants_list[i]
                term2_data = current_implicants_list[j]

                can_glue_result, diff_pos = can_glue(term1_data['binary'], term2_data['binary'])
                
                if can_glue_result:
                    new_binary, new_str = glue_terms(term1_data['binary'], term2_data['binary'], diff_pos, variables, form_type)
                    
                    if new_str:
                        steps.append(f"{term1_data['str']} + {term2_data['str']} → {new_str}")
                        term1_data['used'] = True
                        term2_data['used'] = True
                        glued_in_this_pass = True
                        
                        if new_str not in seen_implicant_strings_globally:
                            next_pass_implicants_data[new_str] = {'binary': new_binary, 'str': new_str, 'used': False}
                            seen_implicant_strings_globally.add(new_str)
                        elif new_str in next_pass_implicants_data: 
                            pass 
                        else:
                            pass

        newly_found_prime_implicants_this_round = []
        for data in all_passes_implicants_data.values():
            if not data['used']:
                 newly_found_prime_implicants_this_round.append(data)


        if not glued_in_this_pass:
            break
        
        all_passes_implicants_data.clear()
        for data in newly_found_prime_implicants_this_round: 
             all_passes_implicants_data[data['str']] = data 
             all_passes_implicants_data[data['str']]['used'] = False 
        for str_key, data in next_pass_implicants_data.items(): 
             all_passes_implicants_data[str_key] = data
        
        if not next_pass_implicants_data and not glued_in_this_pass: 
            break

    all_prime_implicants_tuples = []
    for data in all_passes_implicants_data.values():
        all_prime_implicants_tuples.append((data['str'], data['binary']))
    unique_prime_implicants_map = {item[0]: item for item in all_prime_implicants_tuples}
    all_prime_implicants_tuples = list(unique_prime_implicants_map.values())


    if not all_prime_implicants_tuples:
        return steps, [], [], []

    coverage_table = build_coverage_table(terms, all_prime_implicants_tuples, variables, form_type)
    essential_implicant_strings = find_essential_implicants(coverage_table, terms, all_prime_implicants_tuples)

    return steps, coverage_table, all_prime_implicants_tuples, essential_implicant_strings


def minimize_tabular(expression, variables, form_type="SDNF"):
    table = build_truth_table(expression, variables)
    sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, variables)
    
    if form_type == "SDNF":
        minterms_or_maxterms = sdnf.split("∨") if sdnf else []
        final_join_op = "∨"
    else:
        minterms_or_maxterms = sknf.split("∧") if sknf else []
        final_join_op = "∧"
    processed_terms = []
    if minterms_or_maxterms:
        for term_group in minterms_or_maxterms:
            term = term_group.strip()
            if term.startswith("(") and term.endswith(")"):
                term = term[1:-1]
            if term: 
                processed_terms.append(term)
    
    if not processed_terms:
        return [], [], [], [], final_join_op, ("0" if form_type == "SDNF" else "1")

    steps, coverage, all_pis_tuples, essential_pi_strings = tabular_calculation_method(
        processed_terms, variables, form_type
    )
    
    result_str = final_join_op.join(essential_pi_strings) if essential_pi_strings else ("0" if form_type == "SDNF" else "1")
    
    return steps, coverage, all_pis_tuples, essential_pi_strings, processed_terms, final_join_op, result_str


def print_coverage_table(original_terms, all_prime_implicants_tuples, coverage_matrix, variables):
    if not original_terms or not all_prime_implicants_tuples or not coverage_matrix:
        print("Таблица покрытия пуста или нет данных для отображения.")
        return

    num_vars = len(variables)
    minterm_headers = []
    for i, term_str in enumerate(original_terms):
        simple_term_str = term_str.replace("∧", "").replace("∨", "").replace("(", "").replace(")", "")
        minterm_headers.append(simple_term_str if simple_term_str else f"m{i}")
    implicant_row_labels = [pi_str.replace("∧", "").replace("∨", "").replace("(", "").replace(")", "") 
                            for pi_str, _ in all_prime_implicants_tuples]

    if not minterm_headers:
        print("Не удалось создать заголовки для таблицы покрытия (минтермы).")
        return
    if not implicant_row_labels:
        print("Нет импликантов для отображения в таблице покрытия.")
        return
        
    min_col_width = 4 
    col_width = max(min_col_width, max((len(m_h) for m_h in minterm_headers), default=min_col_width)) +1

    min_row_label_width = 8
    row_label_width = max(min_row_label_width, max((len(i_h) for i_h in implicant_row_labels), default=min_row_label_width)) +1

    print("\nТаблица покрытия (Импликанты \\ Минтермы):")
    header_line = f"{'':<{row_label_width}}|"
    for m_h in minterm_headers:
        header_line += f" {m_h:^{col_width}} |"
    print(header_line)
    separator_line = "-" * row_label_width + "+"
    for _ in minterm_headers:
        separator_line += "-" * (col_width + 2) + "+" 
    print(separator_line)
    for i, implicant_label in enumerate(implicant_row_labels):
        data_row_line = f"{implicant_label:<{row_label_width}}|"
        for j in range(len(original_terms)):
            cell_char = 'X' if coverage_matrix[j][i] else ' '
            data_row_line += f" {cell_char:^{col_width}} |"
        print(data_row_line)
    print(separator_line)


def print_tabular_results(expression, variables):
    print("\n=== Минимизация СДНФ (Расчетно-табличный метод) ===")
    steps_sdnf_raw, coverage_sdnf, all_pis_sdnf, essential_pis_sdnf_str, minterms_sdnf, join_op_sdnf, result_sdnf_str = minimize_tabular(expression, variables, "SDNF")
    
    if not minterms_sdnf: 
        print("СДНФ пуста.")
    elif not all_pis_sdnf and not essential_pis_sdnf_str : 
        print("СДНФ не подлежит дальнейшей минимизации или результат пуст.")
        print(f"Результат: {result_sdnf_str}")

    else:
        unique_steps_sdnf = []
        if steps_sdnf_raw:
            for step in steps_sdnf_raw:
                if step not in unique_steps_sdnf:
                    unique_steps_sdnf.append(step)
        
        if unique_steps_sdnf:
            print("Шаги склеивания:")
            for i, step in enumerate(unique_steps_sdnf, 1):
                print(f"{i}. {step}")
            print(f"... (всего {len(unique_steps_sdnf)} уникальных шагов склеивания)")
        else:
            print("Нет шагов склеивания (возможно, исходная форма уже минимальна или содержит 1 терм).")
        
        print_coverage_table(minterms_sdnf, all_pis_sdnf, coverage_sdnf, variables)
        print(f"Все простые импликанты СДНФ: {', '.join(pi_str for pi_str, _ in all_pis_sdnf) if all_pis_sdnf else 'Нет'}")
        print(f"Существенные простые импликанты СДНФ: {', '.join(essential_pis_sdnf_str) if essential_pis_sdnf_str else 'Нет'}")
        dnf_to_print = "("
        for char in result_sdnf_str:
            if char == "∨":
                dnf_to_print = ''.join([dnf_to_print, ')', '∧', '('])
            else:
                dnf_to_print = ''.join([dnf_to_print, char])
        dnf_to_print = dnf_to_print + ")"
        print(f"Результат (минимизированная СДНФ): {dnf_to_print}")

    print("\n=== Минимизация СКНФ (Расчетно-табличный метод) ===")
    steps_sknf_raw, coverage_sknf, all_pis_sknf, essential_pis_sknf_str, maxterms_sknf, join_op_sknf, result_sknf_str = minimize_tabular(expression, variables, "SKNF")

    if not maxterms_sknf:
        print("СКНФ пуста.")
    elif not all_pis_sknf and not essential_pis_sknf_str:
        print("СКНФ не подлежит дальнейшей минимизации или результат пуст.")
        print(f"Результат: {result_sknf_str}")
    else:
        unique_steps_sknf = []
        if steps_sknf_raw:
            for step in steps_sknf_raw:
                if step not in unique_steps_sknf:
                    unique_steps_sknf.append(step)

        if unique_steps_sknf:
            print("Шаги склеивания:")
            for i, step in enumerate(unique_steps_sknf, 1):
                print(f"{i}. {step}")
            print(f"... (всего {len(unique_steps_sknf)} уникальных шагов склеивания)")
        else:
            print("Нет шагов склеивания.")
        
        print_coverage_table(maxterms_sknf, all_pis_sknf, coverage_sknf, variables)
        print(f"Все простые импликаты СКНФ: {', '.join(pi_str for pi_str, _ in all_pis_sknf) if all_pis_sknf else 'Нет'}")
        print(f"Существенные простые импликаты СКНФ: {', '.join(essential_pis_sknf_str) if essential_pis_sknf_str else 'Нет'}")
        knf_to_print = "("
        for char in result_sknf_str:
            if char == "∧":
                knf_to_print = ''.join([knf_to_print, ')', '∧', '('])
            else:
                knf_to_print = ''.join([knf_to_print, char])
        knf_to_print = knf_to_print + ")"
        print(f"Результат: {knf_to_print}")
