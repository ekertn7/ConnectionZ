**[‹ назад](/README.md)**

# Основы работы

В библиотеке реализовано два базовых класса: **DirectedGraph** (направленный граф) и **UndirectedGraph** (ненаправленный граф).

Оба типа графа содержат вершины (nodes) и взаимосвязи/ребра (edges).

## Представление вершин

Вершины представлены в виде словаря, где ключами являются уникальные индентификаторы вершин (node identifier), а значениями - атрибуты вершин (node attributes). Идентификаторы вершин - это значения строкового типа. Атрибуты вершин, в свою очередь, являются словарем со строковыми ключами и значениями любого типа.

Пример:

```python
{
    'Elizabeth': {'age': 19, 'sex': False},
    'Sebastian': {'age': 21, 'sex': True},
}
```

## Представление ребер

Ребра представлены в виде словаря, где ключами являются пары (couple), а значениями - множества ребер (multiples). Пара - это кортеж, содержащий два идентификатора вершин (node identifier). Множество ребер - это словарь, где ключами являются идентификаторы ребер (edge identifier), а значениями - атрибуты ребер (edge attributes). Идентификаторы ребер - строковые. Атрибуты ребер, как и в случае с вершинами, являются словарем со строковыми ключами и значениями любого типа.

Пример для направленного графа:

```python
{
    ('Voronezh', 'Lipetsk'): {
        '46f893e': {'distance': 132, 'minutes': 149},
        '206ij5s': {'distance': 109, 'minutes': 112},
    },
    ('Lipetsk', 'Voronezh'): {
        '239af58': {'distance': 116, 'minutes': 121},
    },
}
```

Пример для ненаправленного графа (couple в ненаправленном графе представляется в виде отсортированного кортежа, поэтому представления для некоторых графов будут отличаться, но структура одинакова):

```python
{
    ('Lipetsk', 'Voronezh'): {
        '46f893e': {'distance': 132, 'minutes': 149},
        '206ij5s': {'distance': 109, 'minutes': 112},
        '239af58': {'distance': 116, 'minutes': 121},
    },
}
```

## Создание графа

Существует несколько способов создать граф напрямую.

_В модуле [импорт и экспорт графа](/documentation/import_export.md) описаны способы создания графа из файла._

Можно создать пустой граф и добавить вершины и ребра с помощью встроенных методов `add_node` и `add_edge`:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_node('Nathan', age=22, sex=True)
>>> graph.add_node('Kamila', age=19, sex=False)
>>> graph.add_edge('Nathan', 'Kamila', '2024-09-23', amount=1700)
>>> graph
'Directed Graph with 2 nodes, 1 couple and 1 edge'
```

Можно добавить вершины и ребра сразу при создании графа с помощью словарей:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph(
...     nodes={
...         'Nathan': {'age': 22, 'sex': True},
...         'Kamila': {'age': 19, 'sex': False} },
...     edges={
...         ('Nathan', 'Kamila'): {'2024-09-23': {'amount': 1700}} } )
>>> graph
'Complete Undirected Graph with 2 nodes, 1 couple and 1 edge'
```

Или с помощью списков, кортежей или наборов (атрибуты при этом добавить нельзя, идентификаторы ребер генерируются автоматически):

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph(
...     nodes=['Nathan', 'Kamila'],
...     edges=[('Nathan', 'Kamila')])
>>> graph
'Directed Graph with 2 nodes, 1 couple and 1 edge'
```

Можно также передать в граф только ребра, без указания вершин (отсутствующие вершины будут добавлены автоматически):

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph(edges=[('Nathan', 'Kamila')])
>>> graph
'Complete Undirected Graph with 2 nodes, 1 couple and 1 edge'
```

В каждом классе реализована валидация, поэтому в случае передачи данных, не соответствующих используемому формату, будет вызвано исключение с подробным описанием ошибки. Например:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph(nodes=[4823_234564, 4253_452643, 4351_348909])
'WrongTypeOfNodeIdentifierException: Nodes validation exception! Wrong type of node identifier: node identifier type must be str!'
```

# Методы

-   [add_node](#add_node)
-   [del_node](#del_node)
-   [has_node](#has_node)
-   [clear_nodes](#clear_nodes)
-   [add_edge](#add_edge)
-   [del_edge](#del_edge)
-   [has_edge](#has_edge)
-   [clear_edges](#clear_edges)
-   [clear_degree](#clear_degree)
-   [calc_degree](#calc_degree)
-   [clear_neighbors](#clear_neighbors)
-   [find_neighbors](#find_neighbors)
-   [get_subgraph](#get_subgraph)
-   [find_loops](#find_loops)
-   [check_type](#check_type)
-   [check_is_complete](#check_is_complete)
-   [check_is_pseudo](#check_is_pseudo)
-   [check_is_multi](#check_is_multi)
-   [describe](#describe)

## add_node

Добавляет новую вершину в граф. Если вершина успешно добавлена, возвращает ее идентификатор.

В случае, если тип переданного идентификатора неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`. Если не передавать идентификатор, он будет автоматически сгенерирован.

В случае, если такая вершина существует, вызывает ошибку `NodeAlreadyExistsException`. Если задать параметр `replace = True`, то существующая вершина будет заменена новой.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_node('Grace', age=19, city='Voronezh')
>>> graph.add_node('Grace', age=19, city='Lipetsk', replace=True)
>>> graph.nodes
{'Grace': {'age': 19, 'city': 'Lipetsk'}}
```

## del_node

Удаляет вершину и инцидентные ей ребра из графа. Ничего не возвращает.

В случае, если тип переданного идентификатора неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`.

В случае, если вершины не существует, вызывает ошибку `NodeIsNotExistsException`.

По умолчанию пересчитывает вычисляемые атрибуты (degree, neighbors). Это снижает производительность. Если задать параметр `recalculate_calculated_attributes = False`, то пересчет вычисляемых атрибутов не будет производиться. Такую опцию следует использовать только в случае множественного удаления вершин. Производительность повысится в разы. После чего не забудьте запустить методы для пересчета значений: `calc_degree()` + `find_neighbors()` или `describe()`.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph(edges=[('Riley', 'Layla'), ('Riley', 'Eliana'), ('Stella', 'Eliana')])
>>> graph.del_node('Riley')
>>> graph.nodes
{'Layla': {'degree': 0, 'neighbors': set()},
 'Eliana': {'degree': 1, 'neighbors': {'Stella'}},
 'Stella': {'degree': 1, 'neighbors': {'Eliana'}}}
>>> graph.edges
{('Eliana', 'Stella'): {'992513c2a2a24d67b12ab4171b1c7409': {}}}
```

## has_node

Проверяет, существует ли вершина в графе. Возвращает булевое значение.

В случае, если тип переданного идентификатора неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_node('Freya')
>>> graph.has_node('Freya')
True
>>> graph.has_node('Kimberly')
False
```

## clear_nodes

Удаляет все вершины в графе.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph(nodes=['Michael', 'Rebecca', 'Ethan'])
>>> graph.clear_nodes()
>>> len(graph.nodes)
0
```

## add_edge

Добавляет новое ребро и отсутствующие инцидентные ему вершины в граф. Если ребро успешно добавлено, возвращает ее идентификатор.

В случае, если тип переданного идентификатора одной из вершин неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`.

В случае, если тип переданного идентификаторы ребра неправильный, вызывает ошибку `WrongTypeOfEdgeIdentifierException`. Если не передавать идентификатор, он будет автоматически сгенерирован.

В случае, если такое ребро существует, вызывает ошибку `EdgeAlreadyExistsException`. Если задать параметр `replace = True`, то существующее ребро будет заменено новым.

По умолчанию пересчитывает вычисляемые атрибуты вершин (degree, neighbors). Это снижает производительность. Если задать параметр `recalculate_calculated_attributes = False`, то пересчет вычисляемых атрибутов не будет производиться. Такую опцию следует использовать только в случае множественного добавления ребер. Производительность повысится в разы. После чего не забудьте запустить методы для пересчета значений: `calc_degree()` + `find_neighbors()` или `describe()`.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> # добавляю вершину с атрибутами чтобы показать, что при добавлении ребра существующие вершины не изменяются
>>> graph.add_node('Samuel', age=23, sex=True)
>>> graph.add_edge('Samuel', 'Kimberly', '26-09-2024', amount=1600)
>>> graph.nodes
{'Samuel': {'age': 23, 'sex': True, 'degree': 1, 'neighbors': {'Kimberly'}},
 'Kimberly': {'degree': 1, 'neighbors': {'Samuel'}}}
>>> graph.edges
{('Kimberly', 'Samuel'): {'26-09-2024': {'amount': 1600}}}
```

## del_edge

Удаляет ребро из графа. Ничего не возвращает.

В случае, если тип переданного идентификатора одной из вершин неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`.

В случае, если пары из двух вершин не существует, вызывает ошибку `CoupleIsNotExistsException`.

В случае, если тип переданного идентификаторы ребра неправильный, вызывает ошибку `WrongTypeOfEdgeIdentifierException`.

В случае, если ребра не существует, вызывает ошибку `EdgeIsNotExistsException`.

По умолчанию пересчитывает вычисляемые атрибуты вершин (degree, neighbors). Это снижает производительность. Если задать параметр `recalculate_calculated_attributes = False`, то пересчет вычисляемых атрибутов не будет производиться. Такую опцию следует использовать только в случае множественного удаления ребер. Производительность повысится в разы. После чего не забудьте запустить методы для пересчета значений: `calc_degree()` + `find_neighbors()` или `describe()`.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph(edges=[('Alexandra', 'Alexander'), ('Alexandra', 'James')])
>>> graph.del_edge('Alexandra', 'James')
>>> graph.nodes
{'Alexandra': {'degree': 1, 'neighbors': {'Alexander'}},
 'Alexander': {'degree': 1, 'neighbors': set()},
 'James': {'degree': 0, 'neighbors': set()}}
>>> graph.edges
{('Alexandra', 'Alexander'): {'3d8904bf9b40440797c60fc9c9031197': {}}}
```

## has_edge

Проверяет, существует ли пара и/или ребро в графе. Возвращает булевое значение.

В случае, если тип переданного идентификатора одной из вершин неправильный, вызывает ошибку `WrongTypeOfNodeIdentifierException`.

В случае, если тип переданного идентификаторы ребра неправильный, вызывает ошибку `WrongTypeOfEdgeIdentifierException`.

Пример для проверки существования пары:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
>>> graph.has_edge('Robert', 'Sienna')
False
>>> graph.has_edge('Jonathan', 'Alina')
True
```

Пример для проверки существования ребра:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> graph.add_edge('Jonathan', 'Alina', '0bac3283bf')
>>> graph.has_edge('Jonathan', 'Alina', '0bac3283bf')
True
```

## clear_edges

Удаляет все ребра в графе. Устанавливает нулевые значения для вычисляемых атрибутов.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph(edges=[('Lucas', 'Norah'), ('Theodore', 'Adalyn')])
>>> graph.clear_edges()
>>> len(graph.edges)
0
>>> graph.nodes
{'Lucas': {'degree': 0, 'neighbors': set()},
 'Norah': {'degree': 0, 'neighbors': set()},
 'Theodore': {'degree': 0, 'neighbors': set()},
 'Adalyn': {'degree': 0, 'neighbors': set()}}
```

## clear_degree

Устанавливает нулевые значения для степени вершин в графе.

## calc_degree

Вычисляет степени вершин в графе. Добавляет ко всем вершинам атрибут "degree" со значением степени.

_Степень вершины_ - это количество ребер, инцидентных указанной вершине. Петля увеливает степень вершины на 2. _Изолированная вершина_ - вершина с нулевой степенью. _Висячая вершина_ - вершина со степенью 1.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> graph.add_edge('Voronezh', 'Lipetsk', distance=109, minutes=112, recalculate_calculated_attributes=False)
>>> graph.add_edge('Lipetsk', 'Ryazan', distance=258, minutes=264, recalculate_calculated_attributes=False)
>>> graph.calc_degree()
>>> graph.nodes
{'Voronezh': {'degree': 1}, 'Lipetsk': {'degree': 2}, 'Ryazan': {'degree': 1}}
```

## clear_neighbors

Устанавливает пустые значения для соседей вершин в графе.

## find_neighbors

Находит соседей вершин в графе. Добавляет ко всем вершинам атрибут "neighbors", содержащий сет с соседними вершинами.

_Сосед в ненапрвленном графе_ - это вершина, смежная с выбранной.

_Сосед в направленном графе_ - это вершина, смежная с выбранной, если в нее направлено ребро.

Пример с ненаправленным графом:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> graph.add_node('Samuel')
>>> graph.add_edge('Oliver', 'Katherine', friends=True, recalculate_calculated_attributes=False)
>>> graph.add_edge('Amaya', 'Oliver', friends=True, recalculate_calculated_attributes=False)
>>> graph.find_neighbors()
>>> graph.nodes
{'Samuel': {'neighbors': set()},
 'Oliver': {'neighbors': {'Amaya', 'Katherine'}},
 'Katherine': {'neighbors': {'Oliver'}},
 'Amaya': {'neighbors': {'Oliver'}}}
```

Пример с направленным графом:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> graph.add_node('Molly')
>>> graph.add_edge('Cooper', 'Khloe', datetime='2024-06-29 14:15:34', amount=1700, recalculate_calculated_attributes=False)
>>> graph.add_edge('Cooper', 'Ariella', datetime='2024-09-14 09:45:19', amount=2100, recalculate_calculated_attributes=False)
>>> graph.find_neighbors()
>>> graph.nodes
{'Molly': {'neighbors': set()},
 'Cooper': {'neighbors': {'Ariella', 'Khloe'}},
 'Khloe': {'neighbors': set()},
 'Ariella': {'neighbors': set()}}
```

## get_subgraph

Возвращает подграф, состоящий из выбранных вершин и инцидентных им ребер из исходного графа.

По умолчанию пересчитывает вычисляемые атрибуты вершин (degree, neighbors).

По умолчанию создает подграф только с выбранными вершинами и ребрами между ними. Если задать параметр `include_adjacent_nodes=True`, то будет построен подграф, в котором присутствуют соседи выбранных вершин и, соответственно, добавятся инцидентные этим вершинам ребра.

Пример с построением подграфа, в котором присутствуют только выбранные вершины:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
>>> graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
>>> graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
>>> graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
>>> subgraph = graph.get_subgraph(['Milani', 'Adrian'])
>>> subgraph.nodes
{'Adrian': {'degree': 1, 'neighbors': {'Milani'}},
 'Milani': {'degree': 1, 'neighbors': set()}}
>>> subgraph.edges
{('Adrian', 'Milani'): {'2024-12-18': {'amount': 1200}}}
```

Пример с построением подграфа, в котором присутствуют соседи выбранных вершин:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.UndirectedGraph()
>>> graph.add_edge('Juliana', 'Roman', '2024-09-23', amount=1700)
>>> graph.add_edge('Adrian', 'Diana', '2024-05-16', amount=2400)
>>> graph.add_edge('Adrian', 'Milani', '2024-12-18', amount=1200)
>>> graph.add_edge('Presley', 'Adrian', '2024-11-03', amount=2100)
>>> subgraph = graph.get_subgraph(['Milani', 'Adrian'], include_adjacent_nodes=True)
>>> subgraph.nodes
{'Adrian': {'degree': 3, 'neighbors': {'Diana', 'Milani', 'Presley'}},
 'Diana': {'degree': 1, 'neighbors': {'Adrian'}},
 'Milani': {'degree': 1, 'neighbors': {'Adrian'}},
 'Presley': {'degree': 1, 'neighbors': {'Adrian'}}}
>>> subgraph.edges
{('Adrian', 'Diana'): {'2024-05-16': {'amount': 2400}},
 ('Adrian', 'Milani'): {'2024-12-18': {'amount': 1200}},
 ('Adrian', 'Presley'): {'2024-11-03': {'amount': 2100}}}
```

## find_loops

Находит петли в графе. Возвращает объект генератора, состоящий из пар идентификаторов вершин.

_Петля_ - это ребро, инцидентное одной вершине.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph(
...     edges=[
...         ('Diana', 'Lilly'), ('Lilly', 'Lilly'), ('Angela', 'Taylor'),
...         ('Alana', 'Alana'), ('Kimberly', 'Alana'), ('Taylor', 'Kimberly')])
>>> for loop in graph.find_loops():
...     print(loop)
('Lilly', 'Lilly')
('Alana', 'Alana')
```

## check_type

Возвращает название класса для текущего экземпляра класса.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.check_type()
'DirectedGraph'
```

## check_is_complete

Проверяет, является ли граф полным. Возвращает булевое значение.

_Полный ненаправленный граф - это граф, в котором каждая пара различных вершин смежна._

_Полный направленный граф - это граф, в котором каждая пара различных вершин соединена двумя и более ребрами с противоположными направлениями._

Пример для полного ненаправленного графа:

```python
>>> import connectionz as cnnnz
>>> graph = UndirectedGraph(
...     nodes=['A', 'B', 'C', 'D'],
...     edges=[
...         ('A', 'B'), ('A', 'C'), ('A', 'D'),
...         ('B', 'C'), ('B', 'D'),
...         ('C', 'D')])
>>> graph.check_is_complete()
True
```

Пример для полного направленного графа:

```python
>>> import connectionz as cnnnz
>>> graph = DirectedGraph(
...     nodes=['A', 'B', 'C', 'D'],
...     edges=[
...         ('A', 'B'), ('A', 'C'), ('A', 'D'),
...         ('B', 'A'), ('B', 'C'), ('B', 'D'),
...         ('C', 'A'), ('C', 'B'), ('C', 'D'),
...         ('D', 'A'), ('D', 'B'), ('D', 'C')])
>>> graph.check_is_complete()
True
```

## check_is_pseudo

Проверяет, содержит ли граф петли (то есть, является ли граф псевдографом). Возвращает булевое значение.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = DirectedGraph(
...     nodes=['A', 'B', 'C', 'D'],
...     edges=[('A', 'A'), ('B', 'C'), ('C', 'D')])
>>> graph.check_is_pseudo()
True
```

## check_is_multi

Проверяет, содержит ли граф больше одного ребра между смежными вершинами (то есть, является ли граф мультиграфом). Возвращает булевое значение.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = DirectedGraph(nodes=['A', 'B', 'C'])
>>> graph.add_edge('A', 'B', weight=146)
>>> graph.add_edge('B', 'C', weight=237)
>>> graph.add_edge('B', 'C', weight=524)
>>> graph.check_is_multi()
True
```

## describe

Возвращает словарь с описанием графа.

Описание включает:

-   _type_: тип графа
-   _number_of_nodes_: количество вершин
-   _number_of_couples_: количество пар из двух вершин
-   _number_of_edges_: количество ребер
-   _multi_graph_: является ли граф мультиграфом
-   _pseudo_graph_: является ли граф псевдографом
-   _complete_graph_: является ли граф полным / полностью связанным
