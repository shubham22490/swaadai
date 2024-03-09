import pickle

with open("filtered_data_list.txt", "r") as f:
    result = f.read()

ans = list(i.split(": ")[-1] for i in result.split(", "))