from csv import writer
import os

lista = [1,2,3,4,5,6,7]

write_path = "Test.csv"

with open(write_path, "a", newline="") as f:
    w = writer(f)

    w.writerow(lista)
