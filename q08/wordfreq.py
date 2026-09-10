# wordfreq.py
words = open("words.txt", encoding="utf-8").read().split()
unique = set() # 使用集合
for word in words: # 集合查找接近 O(1)
    if word not in unique:
        unique.add(word) # 加入集合
print("count=", len(unique))
