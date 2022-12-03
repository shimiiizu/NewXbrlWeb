"""
辞書のリスト

[
      { x: 50, y: 40 },
      { x: 60, y: 70 },
      { x: 70, y: 90 },
    ]
"""
"""
List =[]
List.append({'x:' + 50, 'y:' + 40})
print(List)

"""

List = []
a_dict = {}


# 辞書のリスト作成
keys = ['x', 'y']
values = [50, 40]

for value in values:
    d = dict(zip(keys, values))

print(d)
print(d['x'])

    #a_dict.append(d)
    #List.append(d)



"""

{'x': [50, 40], 'y': [60, 70]}
"""



"""
# 辞書のリスト作成
keys = ['x', 'y']
values = [50, 40]

d = dict(zip(keys, values))
print(d)

List = []

List.append(d)
print(List)
"""
