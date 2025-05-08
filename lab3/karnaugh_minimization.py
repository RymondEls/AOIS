from collections import defaultdict
from logic_operations import build_truth_table

def get_karnaugh_map_indices(num_vars):
    if num_vars == 1: return ['0', '1'] 
    if num_vars == 2: return ['0', '1'], ['0', '1'] 
    if num_vars == 3: return ['0', '1'], ['00', '01', '11', '10'] 
    if num_vars == 4: return ['00', '01', '11', '10'], ['00', '01', '11', '10']
    if num_vars == 5: return ['00', '01', '11', '10'], ['000', '001', '011', '010', '110', '111', '101', '100']
    raise ValueError("Поддерживаются только 1-5 переменных")

def _get_binary_index(r_idx, c_idx, num_vars, row_indices, col_indices):
    if num_vars == 1: return str(col_indices[c_idx]) 
    if num_vars == 2: 
        return f"{row_indices[r_idx]}{col_indices[c_idx]}"
    if num_vars == 3:
        row_label_bit = row_indices[r_idx]
        col_map = {'00': (0,0), '01': (0,1), '11': (1,1), '10': (1,0)}
        bc_bits_str = col_indices[c_idx] 
        return f"{row_label_bit}{bc_bits_str}" 
        
    if num_vars == 4:
        ab_bits_str = row_indices[r_idx]
        cd_bits_str = col_indices[c_idx]
        return f"{ab_bits_str}{cd_bits_str}" 

    if num_vars == 5:
        row_gray_to_bin_map = {0: (0,0), 1: (0,1), 2: (1,1), 3: (1,0)} 
        col_gray_to_bin_map = { 
            0:(0,0,0), 1:(0,0,1), 2:(0,1,1), 3:(0,1,0), 
            4:(1,1,0), 5:(1,1,1), 6:(1,0,1), 7:(1,0,0)  
        }
        
        bits_for_ab = row_gray_to_bin_map[r_idx]
        bits_for_cde = col_gray_to_bin_map[c_idx] 
        return f"{bits_for_ab[0]}{bits_for_ab[1]}{bits_for_cde[0]}{bits_for_cde[1]}{bits_for_cde[2]}"
    return ""

def build_karnaugh_map(table, variables, form_type="SDNF"):
    num_vars = len(variables)
    if not 1 <= num_vars <= 5:
        raise ValueError("Поддерживаются только 1-5 переменных для Карты Карно")

    map_values = {} 
    for row_idx in range(1, len(table)): 
        row_data = table[row_idx]
        values_for_vars = row_data[:num_vars] 
        result = row_data[-1]
        binary_index_key = "".join(map(str, values_for_vars))
        map_values[binary_index_key] = result

    if num_vars == 1:
        col_indices = get_karnaugh_map_indices(num_vars)
        row_indices = [''] 
        k_map = [['0'] * len(col_indices)]
    else:
        row_indices, col_indices = get_karnaugh_map_indices(num_vars)
        k_map = [['0'] * len(col_indices) for _ in range(len(row_indices))]

    for r_idx in range(len(row_indices)):
        for c_idx in range(len(col_indices)):
            lookup_binary_str = _get_binary_index(r_idx, c_idx, num_vars, row_indices, col_indices)
            val = map_values.get(lookup_binary_str, '0') 
            k_map[r_idx][c_idx] = str(val)
    return k_map

def print_karnaugh_map(k_map, variables):
    num_vars = len(variables)
    if not k_map:
        print("Карта Карно пуста")
        return

    if num_vars == 1:
        col_indices = get_karnaugh_map_indices(num_vars)
        row_indices = [""] 
    else:
        row_indices, col_indices = get_karnaugh_map_indices(num_vars)
    if num_vars == 1:
        row_vars_display, col_vars_display = "", variables[0]
    elif num_vars == 2:
        row_vars_display, col_vars_display = variables[0], variables[1]
    elif num_vars == 3: 
        row_vars_display, col_vars_display = variables[0], "".join(variables[1:])
    elif num_vars == 4: 
        row_vars_display, col_vars_display = "".join(variables[:2]), "".join(variables[2:])
    elif num_vars == 5: 
        row_vars_display, col_vars_display = "".join(variables[:2]), "".join(variables[2:])
    else: 
        row_vars_display, col_vars_display = "",""


    print(f"\nКарта Карно ({row_vars_display}\\{col_vars_display}):")
    header_col_labels = "    |" + "|".join(f"{l:^4}" for l in col_indices) + "|"
    print(header_col_labels)
    print("-" * len(header_col_labels))

    for r_idx, row_label in enumerate(row_indices):
        row_str = f"{row_label:^4}|" + "|".join(f"{k_map[r_idx][c_idx]:^4}" for c_idx in range(len(col_indices))) + "|"
        print(row_str)

    print("-" * len(header_col_labels))
    
    if num_vars == 5:
        label_var_for_split = variables[2] 
        span_width_per_half = (len(col_indices) // 2) * 4 + (len(col_indices) // 2 - 1)
        print(f"{'':^4}|{label_var_for_split + '=0':^{span_width_per_half}}|{label_var_for_split + '=1':^{span_width_per_half}}|")


def get_target_indices(table, form_type="SDNF"):
    target_value = 1 if form_type == "SDNF" else 0
    indices = [i for i, row in enumerate(table[1:]) if row[-1] == target_value]
    return indices

def int_to_binary(n, num_vars):
    return format(n, f'0{num_vars}b')

def count_set_bits(binary_string):
    return binary_string.count('1')

def combine_terms(term1_data, term2_data): 
    term1_binary = term1_data['binary']
    term2_binary = term2_data['binary']
    
    if len(term1_binary) != len(term2_binary): 
        return None

    diff = 0
    diff_idx = -1
    new_term_binary_list = list(term1_binary) 

    for i in range(len(term1_binary)):
        if term1_binary[i] != term2_binary[i]:
            if term1_binary[i] == '-' or term2_binary[i] == '-':
                if term1_binary[i] != term2_binary[i]: 
                    return None 
            diff += 1
            diff_idx = i
            if diff > 1:
                return None 
    if diff == 1:
        new_term_binary_list[diff_idx] = '-'
        new_term_binary_str = "".join(new_term_binary_list)
        combined_indices = term1_data['indices'] | term2_data['indices'] 
        return new_term_binary_str, combined_indices
    
    return None 

def binary_to_term_string(binary_repr, variables, form_type="SDNF"):
    term_parts = []
    if form_type == "SDNF":
        for i, bit in enumerate(binary_repr):
            if bit == '1':
                term_parts.append(variables[i])
            elif bit == '0':
                term_parts.append(f"¬{variables[i]}")
        return "∧".join(term_parts) if term_parts else "1"
    else:
        for i, bit in enumerate(binary_repr):
            if bit == '0':
                term_parts.append(variables[i])
            elif bit == '1':
                term_parts.append(f"¬{variables[i]}")
        return "∨".join(term_parts) if term_parts else "0"

def find_prime_implicants_qm(target_indices, num_vars, variables, form_type="SDNF"):
    if not target_indices:
        return [], []

    groups = defaultdict(list)
    terms = {} 
    steps = []
    for index in target_indices:
        binary_str = int_to_binary(index, num_vars)
        num_ones = count_set_bits(binary_str) 
        term_data = {'binary': binary_str, 'indices': {index}, 'used': False}
        groups[num_ones].append(term_data)
        if binary_str not in terms: 
            terms[binary_str] = term_data

    current_groups_dict = groups
    prime_implicants_data_list = [] 

    while True:
        next_groups_dict = defaultdict(list)
        made_combination_in_pass = False
        
        sorted_group_keys = sorted(current_groups_dict.keys())
        for i in range(len(sorted_group_keys)):
            key1 = sorted_group_keys[i]
            for j in range(i, len(sorted_group_keys)):
                key2 = sorted_group_keys[j]

                for term1_data in current_groups_dict[key1]:
                    term2_candidates = current_groups_dict[key2]
                    if key1 == key2: 
                        term2_candidates = [t for t in current_groups_dict[key2] if t['binary'] > term1_data['binary']] 

                    for term2_data in term2_candidates:
                        if term1_data['binary'] == term2_data['binary']: continue 
                        combination_result = combine_terms(term1_data, term2_data)
                        
                        if combination_result: 
                            combined_binary_str, combined_indices = combination_result 
                            
                            term1_data['used'] = True
                            term2_data['used'] = True
                            made_combination_in_pass = True

                            term1_str_alg = binary_to_term_string(term1_data['binary'], variables, form_type)
                            term2_str_alg = binary_to_term_string(term2_data['binary'], variables, form_type)
                            combined_str_alg = binary_to_term_string(combined_binary_str, variables, form_type)
                            
                            indices_list_str = str(sorted(list(combined_indices))) 
                            
                            step_description = f"{term1_str_alg} ({term1_data['binary']}) + {term2_str_alg} ({term2_data['binary']}) → {combined_str_alg} ({combined_binary_str}) (индексы: {indices_list_str})"
                            if step_description not in steps:
                                steps.append(step_description)
                            if combined_binary_str not in terms:
                                new_term_data = {'binary': combined_binary_str, 'indices': combined_indices, 'used': False}
                                terms[combined_binary_str] = new_term_data
                                current_num_ones = count_set_bits(combined_binary_str.replace('-', ''))
                                next_groups_dict[current_num_ones].append(new_term_data)
                            else:
                                terms[combined_binary_str]['indices'].update(combined_indices)
                                existing_term_data = terms[combined_binary_str]
                                if not any(d['binary'] == combined_binary_str for group_list in next_groups_dict.values() for d in group_list):
                                    current_num_ones = count_set_bits(combined_binary_str.replace('-', ''))
                                    next_groups_dict[current_num_ones].append(existing_term_data)
        for key in sorted_group_keys:
            for term_data in current_groups_dict[key]:
                if not term_data['used']:
                    is_already_added = False
                    for pi_data in prime_implicants_data_list:
                        if pi_data['binary'] == term_data['binary']:
                            pi_data['indices'].update(term_data['indices']) 
                            is_already_added = True
                            break
                    if not is_already_added:
                        prime_implicants_data_list.append(term_data.copy()) 

        if not made_combination_in_pass:
            break
        current_groups_dict = defaultdict(list)
        for key, group_list in next_groups_dict.items():
            for term_data_ref in group_list:
                term_instance = terms[term_data_ref['binary']]
                term_instance['used'] = False 
                current_groups_dict[key].append(term_instance)
    final_prime_implicants_map = {}
    for pi_data in prime_implicants_data_list:
        if pi_data['binary'] not in final_prime_implicants_map:
            final_prime_implicants_map[pi_data['binary']] = pi_data
        else:
            final_prime_implicants_map[pi_data['binary']]['indices'].update(pi_data['indices'])
            
    return list(final_prime_implicants_map.values()), steps

def select_essential_implicants(prime_implicants, target_indices):
    if not target_indices or not prime_implicants:
        return []

    coverage_chart = defaultdict(list)
    for i, pi in enumerate(prime_implicants):
        for index in pi['indices']:
            if index in target_indices:
                coverage_chart[index].append(i)

    essential_pi_indices = set()
    covered_indices = set()

    for index in target_indices:
        if index in coverage_chart and len(coverage_chart[index]) == 1:
            pi_index = coverage_chart[index][0]
            essential_pi_indices.add(pi_index)
            covered_indices.update(prime_implicants[pi_index]['indices'])

    uncovered_indices = set(target_indices) - covered_indices
    current_selection = essential_pi_indices.copy()
    remaining_pi = [(i, pi) for i, pi in enumerate(prime_implicants) if i not in essential_pi_indices]

    while uncovered_indices:
        best_pi_index = -1
        candidate_pis = []
        for i, pi in remaining_pi:
            covers_count = len(pi['indices'].intersection(uncovered_indices))
            if covers_count > 0:
                candidate_pis.append({'index': i, 'count': covers_count, 'term_len': len(pi['binary'].replace('-',''))})

        if not candidate_pis:
            break

        candidate_pis.sort(key=lambda x: (-x['count'], x['term_len']))
        best_pi_index = candidate_pis[0]['index']

        if best_pi_index != -1:
            current_selection.add(best_pi_index)
            newly_covered = prime_implicants[best_pi_index]['indices'].intersection(uncovered_indices)
            covered_indices.update(newly_covered)
            uncovered_indices -= newly_covered
            remaining_pi = [(i, pi) for i, pi in remaining_pi if i != best_pi_index]
        else:
            break

    return [prime_implicants[i] for i in current_selection]

def minimize_karnaugh(expression, variables):
    table = build_truth_table(expression, variables)
    num_vars = len(variables)

    minimized_dnf = "0"
    minterms_indices = get_target_indices(table, "SDNF")
    prime_implicants_dnf, steps_dnf = find_prime_implicants_qm(minterms_indices, num_vars, variables, "SDNF")
    if minterms_indices:
        selected_pis_dnf = select_essential_implicants(prime_implicants_dnf, minterms_indices)
        dnf_terms = [binary_to_term_string(pi['binary'], variables, "SDNF") for pi in selected_pis_dnf]
        minimized_dnf = "∨".join(sorted(dnf_terms)) if dnf_terms else "0"
        if minimized_dnf == "1": minimized_dnf = "1"

    minimized_cnf = "1"
    maxterms_indices = get_target_indices(table, "SKNF")
    prime_implicants_cnf, steps_cnf = find_prime_implicants_qm(maxterms_indices, num_vars, variables, "SKNF")
    if maxterms_indices:
        selected_pis_cnf = select_essential_implicants(prime_implicants_cnf, maxterms_indices)
        cnf_terms = [binary_to_term_string(pi['binary'], variables, "SKNF") for pi in selected_pis_cnf]
        minimized_cnf = "∧".join(sorted(cnf_terms)) if cnf_terms else "1"
        if minimized_cnf == "0": minimized_cnf = "0"

    k_map = build_karnaugh_map(table, variables)
    return k_map, minimized_dnf, minimized_cnf, steps_dnf, steps_cnf

def print_karnaugh_results(expression, variables):
    print("\n=== Минимизация методом Карт Карно ===")
    try:
        k_map, minimized_dnf, minimized_cnf, steps_dnf_raw, steps_cnf_raw = minimize_karnaugh(expression, variables)

        print_karnaugh_map(k_map, variables)

        print("\nГруппировки для ДНФ:")
        if steps_dnf_raw:
            unique_steps_dnf = []
            for step in steps_dnf_raw:
                if step not in unique_steps_dnf:
                    unique_steps_dnf.append(step)
            
            for i, step in enumerate(unique_steps_dnf, 1):
                print(f"{i}. {step}")
            print(f"... (всего {len(unique_steps_dnf)} уникальных группировок)")
        else:
            print("Нет группировок (ДНФ пуста или не требует группировки)")
        dnf_to_print = "("
        for char in minimized_dnf:
            if char == "∨":
                dnf_to_print = ''.join([dnf_to_print, ')', '∧', '('])
            else:
                dnf_to_print = ''.join([dnf_to_print, char])
        dnf_to_print = dnf_to_print + ")"
        print(f"Результат: {dnf_to_print}")

        print("\nГруппировки для КНФ:")
        if steps_cnf_raw:
            unique_steps_cnf = []
            for step in steps_cnf_raw:
                if step not in unique_steps_cnf:
                    unique_steps_cnf.append(step)

            for i, step in enumerate(unique_steps_cnf, 1):
                print(f"{i}. {step}")
            print(f"... (всего {len(unique_steps_cnf)} уникальных группировок)")
        else:
            print("Нет группировок (КНФ пуста или не требует группировки)")
        knf_to_print = "("
        for char in minimized_cnf:
            if char == "∧":
                knf_to_print = ''.join([knf_to_print, ')', '∧', '('])
            else:
                knf_to_print = ''.join([knf_to_print, char])
        knf_to_print = knf_to_print + ")"
        print(f"Результат: {knf_to_print}")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка при минимизации Карно: {e}")