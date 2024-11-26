def generate_candidates(past_level_candidates):
    generated_itemets = list()
    other_candidates = past_level_candidates.copy()
    for candidate in past_level_candidates:
        prefix_removed = candidate.copy()
        prefix_removed.pop(0)
        other_candidates.pop(0)
        for other_candidate in other_candidates:
            postfix_removed = other_candidate.copy()
            postfix_removed.pop()
            if prefix_removed == postfix_removed:
                new_candidate = postfix_removed
                new_candidate.insert(0, candidate[0])
                new_candidate.append(other_candidate[-1])
                generated_itemets.append(new_candidate)
    return generated_itemets

def filter_frequent_itemsets(candidates, baskets, support_count):
    itemsets = dict()
    for candidate in candidates:
        itemsets[str(candidate)] = 0
    is_in_basket = True
    for candidate in candidates:
        for basket in baskets:
            for item in candidate:
                if item not in basket:
                    is_in_basket = False
                    break
            if is_in_basket:
                itemsets[str(candidate)] += 1
            is_in_basket = True
    print(itemsets)
    frequent_itemsets =  {key: value for key, value in itemsets.items() if value >= support_count}
    return frequent_itemsets
