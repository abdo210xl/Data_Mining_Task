import matplotlib.pyplot as plt, ast
from itertools import combinations


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
    frequent_itemsets =  {key: value for key, value in itemsets.items() if value >= support_count}
    return frequent_itemsets


def generate_all_rules(frequent_itemsets, baskets_amount):
    all_rules = []    
    rules_generation_itemsets =  {k: v for k, v in frequent_itemsets.items() if len(ast.literal_eval(k)) > 1}

    for itemset, support_count in rules_generation_itemsets.items():
        itemset = ast.literal_eval(itemset) 
        itemset_support = support_count 
        for i in range(1, len(itemset)):
            subsets = combinations(itemset, i)
            for subset in subsets:
                X = list(subset)
                Y = [item for item in itemset if item not in X]

                X_support = frequent_itemsets[str(X)]

                confidence = itemset_support / X_support
                Y_support = frequent_itemsets[str(Y)]
                    
                lift = (itemset_support/baskets_amount) / ((X_support/baskets_amount)*(Y_support/baskets_amount))

                all_rules.append((list(X), list(Y), itemset_support, confidence, lift))
    
    return all_rules


def visualize_frequent_itemsets(frequent_itemsets):
    x_labels = list(frequent_itemsets.keys())
    y_values = list(frequent_itemsets.values())

    plt.figure(figsize=(12, 5))

    plt.bar(x_labels, y_values, color='skyblue')

    plt.xlabel("Frequent Itemsets")
    plt.ylabel("Support")
    plt.title("Frequent Itesets Bar Chart")

    plt.show()
