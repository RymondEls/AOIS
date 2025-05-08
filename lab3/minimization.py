from itertools import combinations
from logic_operations import get_normal_forms, build_truth_table

def parse_term(term, variables):
    term = term.replace("(", "").replace(")", "")
    binary = [None] * len(variables)
    literals = term.split("∧") if "∧" in term else term.split("∨")
    for lit in literals:
        lit = lit.strip()
        negated = lit.startswith("¬")
        var = lit[1:] if negated else lit
        if var in variables:
            idx = variables.index(var)
            binary[idx] = 0 if negated else 1
    return binary

def terms_to_binary(terms, variables):
    return [parse_term(term, variables) for term in terms]

def can_glue(term1, term2):
    differences = 0
    diff_pos = -1
    for i, (v1, v2) in enumerate(zip(term1, term2)):
        if v1 != v2 and v1 is not None and v2 is not None:
            differences += 1
            diff_pos = i
        if differences > 1:
            return False, -1
    return differences == 1, diff_pos

def glue_terms(term1, term2, diff_pos, variables, form_type="SDNF"):
    new_term = term1[:]
    new_term[diff_pos] = 'X'
    term_str = []
    for i, val in enumerate(new_term):
        if val == 'X':
            continue
        term_str.append(f"{'¬' if val == 0 else ''}{variables[i]}")
    join_op = "∧" if form_type == "SDNF" else "∨"
    return new_term, join_op.join(term_str) if term_str else ""

def is_term_covered(term_binary, minterm_binary):
    for tb, mb in zip(term_binary, minterm_binary):
        if tb != 'X' and tb != mb and mb is not None:
            return False
    return True

def calculation_method(terms, variables, form_type="SDNF"):
    if not terms:
        return [], []

    binary_terms = terms_to_binary(terms, variables)
    original_terms = [t.replace("(", "").replace(")", "") for t in terms]
    steps = []
    current_terms = list(zip(binary_terms, original_terms))
    used_terms = set()
    seen_terms = set()

    while True:
        new_terms = []
        glued = False
        term_pairs = list(combinations(range(len(current_terms)), 2))

        for i, j in term_pairs:
            term1, str1 = current_terms[i]
            term2, str2 = current_terms[j]
            can_glue_result, diff_pos = can_glue(term1, term2)
            if can_glue_result:
                new_term, new_str = glue_terms(term1, term2, diff_pos, variables, form_type)
                if new_str and new_str not in seen_terms:
                    new_terms.append((new_term, new_str))
                    seen_terms.add(new_str)
                    used_terms.add(i)
                    used_terms.add(j)
                    steps.append(f"{str1} + {str2} → {new_str}")
                    glued = True

        for i, (term, term_str) in enumerate(current_terms):
            if i not in used_terms:
                new_terms.append((term, term_str))

        if not glued:
            break

        current_terms = new_terms
        used_terms = set()

    final_terms = [(t, s) for t, s in current_terms if s]
    essential_terms = []
    covered_minterms = set()
    minterms = terms
    term_coverage = []

    for term_binary, term_str in final_terms:
        covered = set()
        for i, minterm in enumerate(minterms):
            minterm_binary = parse_term(minterm, variables)
            if is_term_covered(term_binary, minterm_binary):
                covered.add(i)
        term_coverage.append((term_binary, term_str, covered))

    minterm_to_terms = {i: [] for i in range(len(minterms))}
    for idx, (_, term_str, covered_set) in enumerate(term_coverage):
        for minterm_idx in covered_set:
            minterm_to_terms[minterm_idx].append(idx)

    essential_indices = set()
    for minterm_idx, covering_terms in minterm_to_terms.items():
        if len(covering_terms) == 1:
            idx = covering_terms[0]
            if idx not in essential_indices:
                essential_indices.add(idx)
                essential_term = term_coverage[idx][1]
                steps.append(f"Импликанта {essential_term} добавлена как существенная")

    final_selected = set(essential_indices)
    covered_now = set()
    for idx in final_selected:
        covered_now.update(term_coverage[idx][2])

    uncovered = set(range(len(minterms))) - covered_now
    while uncovered:
        best_term = None
        best_cover = set()
        for idx, (_, term_str, covered_set) in enumerate(term_coverage):
            if idx in final_selected:
                continue
            cover = covered_set & uncovered
            if len(cover) > len(best_cover):
                best_term = idx
                best_cover = cover
        if best_term is None:
            break
        final_selected.add(best_term)
        term_str = term_coverage[best_term][1]
        steps.append(f"Импликанта {term_str} добавлена для покрытия оставшихся минтермов")
        uncovered -= best_cover

    result_terms = [term_coverage[i][1] for i in sorted(final_selected)]
    return steps, result_terms


def minimize_calculation(expression, variables, form_type="SDNF"):
    table = build_truth_table(expression, variables)
    sdnf, sknf, idx_sdnf, idx_sknf = get_normal_forms(table, variables)
    
    if form_type == "SDNF":
        terms = sdnf.split(" ∨ ") if sdnf else []
        join_op = "∨"
    else:
        terms = sknf.split(" ∧ ") if sknf else []
        join_op = "∨" 

    steps, result_terms_list = calculation_method(terms, variables, form_type)
    
    final_join_op = "∨" if form_type == "SDNF" else "∧"
    
    return steps, final_join_op.join(t for t in result_terms_list) if result_terms_list else ("0" if form_type == "SDNF" else "1")

def print_calculation_results(expression, variables):
    print("\n=== Минимизация СДНФ (Расчетный метод) ===")
    steps_sdnf_raw, result_sdnf = minimize_calculation(expression, variables, "SDNF")
    if not steps_sdnf_raw:
        print("СДНФ пуста или не подлежит минимизации")
    else:
        unique_steps_sdnf = []
        for step in steps_sdnf_raw:
            if step not in unique_steps_sdnf:
                unique_steps_sdnf.append(step)
        
        print("Шаги минимизации:")
        for i, step in enumerate(unique_steps_sdnf, 1):
            print(f"{i}. {step}")
        print(f"... (всего {len(unique_steps_sdnf)} уникальных шагов)")
        dnf_to_print = "("
        for char in result_sdnf:
            if char == "∨":
                dnf_to_print = ''.join([dnf_to_print, ')', '∧', '('])
            else:
                dnf_to_print = ''.join([dnf_to_print, char])
        dnf_to_print = dnf_to_print + ")"
        print(f"Результат: {dnf_to_print}")

    print("\n=== Минимизация СКНФ (Расчетный метод) ===")
    steps_sknf_raw, result_sknf = minimize_calculation(expression, variables, "SKNF")
    if not steps_sknf_raw:
        print("СКНФ пуста или не подлежит минимизации")
    else:
        unique_steps_sknf = []
        for step in steps_sknf_raw:
            if step not in unique_steps_sknf:
                unique_steps_sknf.append(step)

        print("Шаги минимизации:")
        for i, step in enumerate(unique_steps_sknf, 1):
            print(f"{i}. {step}")
        print(f"... (всего {len(unique_steps_sknf)} уникальных шагов)")
        knf_to_print = "("
        for char in result_sknf:
            if char == "∧":
                knf_to_print = ''.join([knf_to_print, ')', '∧', '('])
            else:
                knf_to_print = ''.join([knf_to_print, char])
        knf_to_print = knf_to_print + ")"
        print(f"Результат: {knf_to_print}")