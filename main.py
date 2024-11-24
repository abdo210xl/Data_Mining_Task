import openpyxl
import pandas as pd
from utils import *

from openpyxl import Workbook, load_workbook


print("Free Palestine")

excel_file='Horizontal_Format.xlsx'

data_frame = pd.read_excel(excel_file,sheet_name="Sheet1")
work_book = load_workbook('Horizontal_Format.xlsx')

work_sheet = work_book.active

# data_frame_dict=data_frame.to_dict()

#min_support = int(input("Enter minimum support in %: "))
#min_confidence = int(input("Enter minimum confidence in %: "))

#support_count=min_support/100

support_count=3

frequent_items={}
items_count_per_transaction={}
frequent_items_per_level={}
k_level = 1 

x=1
while x:

    
    index=0
    if k_level == 1:
        for items in data_frame['items']:
            print(index)
            print(items)
            # item_list=remove_duplicates(items)
            # data_frame.at[items,'items']=item_list
            is_visited={}
            items_count_per_transaction[index]={}
            for item in items:
                if item in items_count_per_transaction.keys() and not is_visited[item]:
                    items_count_per_transaction[index][item]+=1
                    is_visited[item]=1
                elif item != ",":
                    items_count_per_transaction[index][item]=1
                    is_visited[item]=1
            index+=1


    print(items_count_per_transaction)

    candidate_items_per_level=generate_candidate_itemsets(items_count_per_transaction,k_level,frequent_items_per_level)

    for item,count in candidate_items_per_level.items():
        if count >= support_count:
            frequent_items_per_level[item]=count

    if not bool(frequent_items_per_level):
        break

    frequent_items.update(frequent_items_per_level)

    k_level+=1
    x-=1


print(frequent_items)


