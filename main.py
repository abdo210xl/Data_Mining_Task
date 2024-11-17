import openpyxl

from openpyxl import Workbook, load_workbook

work_book = load_workbook('Horizontal_Format.xlsx')

work_sheet = work_book.active

print(work_sheet)
print("free palestine")
