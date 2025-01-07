**[‹ назад](/README.md)**

# Импорт и экспорт графа

В библиотеке реализованы функции для сохранения и создания графа в/из файл(а).

-   JSON:
    -   [export_graph_to_json](#export_graph_to_json)
    -   [import_graph_from_json](#import_graph_from_json)

## export_graph_to_json

Экспортирует граф в файл JSON. Ничего не возвращает.

Сохраняет тип графа. Для вершин и ребер преобразует атрибуты из tuple и set в list, из date и datetime в str.

Пример:

```python
>>> import connectionz as cnnnz
>>> from datetime import datetime, date
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_node('Alex', sex=True, birth=date(2003, 1, 17))
>>> graph.add_node('Robert', sex=True, birth=date(2004, 4, 12), likes=('Victoria', 'Alex'))
>>> graph.add_node('Victoria', sex=False, birth=date(2005, 11, 23))
>>> graph.add_edge('Alex', 'Victoria', '135152425', datetime=datetime(2024, 5, 16, 23, 54, 18), amount=1832.74)
>>> graph.add_edge('Robert', 'Victoria', '249851454', datetime=datetime(2024, 8, 19, 17, 25, 46), amount=2131.6)
>>> graph.add_edge('Robert', 'Victoria', '952591475', datetime=datetime(2024, 8, 23, 11, 16, 3), amount=1286)
>>> export_graph_to_json(graph=graph, file_path='~/Documents/graph.json')
```

## import_graph_from_json

Считывает граф из файла JSON. Возвращает объект направленного или ненаправленного графа.

Для вершин преобразует атрибут _neighbors_ из list в set.

Пример:

```python
>>> graph = import_graph_from_json(file_path='~/Documents/graph.json')
>>> graph.check_type()
'DirectedGraph'
>>> graph.nodes
{'Alex': {'sex': True,
  'birth': '2003-01-17',
  'degree': 1,
  'neighbors': {'Victoria'}},
 'Robert': {'sex': True,
  'birth': '2004-04-12',
  'degree': 2,
  'neighbors': {'Victoria'}},
 'Victoria': {'sex': False,
  'birth': '2005-11-23',
  'degree': 3,
  'neighbors': set()}}
>>> graph.edges
{('Alex', 'Victoria'): {
  '135152425': {'datetime': '2024-05-16 23:54:18', 'amount': 1832.74}},
 ('Robert', 'Victoria'): {
  '249851454': {'datetime': '2024-08-19 17:25:46', 'amount': 2131.6},
  '952591475': {'datetime': '2024-08-23 11:16:03', 'amount': 1286}}}
```
