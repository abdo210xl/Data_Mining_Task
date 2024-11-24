def remove_duplicates(s):

    seen = set()
    result = []

    for char in s:
        if char not in seen:
            result.append(char)
            seen.add(char)
    
    return ''.join(result)

def generate_candidate_itemsets(items_count_per_transaction,k_level,frequent_k_1_itemsets):
    candidate_items_per_level=[]
    if k_level == 1:
        for transaction in items_count_per_transaction:
            for item,count in items_count_per_transaction[transaction].items():
                if item in candidate_items_per_level:
                    candidate_items_per_level[item]+=count
                else:
                    candidate_items_per_level[item]=count
    elif k_level == 2:
        keys = list(frequent_k_1_itemsets.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                candidate_items_per_level.append()
                


    return candidate_items_per_level

