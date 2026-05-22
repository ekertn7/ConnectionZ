**[‹ назад](/README.md)**

# Поиск кратчайшего пути и расстояния между вершинами с помощью алгоритма Дейкстры

В библиотеке реализованы функции поиска кратчайшего пути и кратчайшего расстояния между вершинами с помощью алгоритма Дейкстры.

-   [find_shortest_path](#find_shortest_path)
-   [find_shortest_distance](#find_shortest_distance)

## find_shortest_path

Возвращает список с идентификаторами вершин, через которые проходит путь от стартовой до конечной вершиы.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_edge('A', 'B', distance=14)
>>> graph.add_edge('B', 'C', distance=18)
>>> graph.add_edge('B', 'C', distance=11)
>>> graph.add_edge('C', 'D', distance=19)
>>> cnnnz.find_shortest_path('A', 'D')
['A', 'B', 'C', 'D']
```

## find_shortest_distance

Возвращает кратчайшее расстояние в формате int или float от стартовой до конечной вершиы.

Пример:

```python
>>> import connectionz as cnnnz
>>> graph = cnnnz.DirectedGraph()
>>> graph.add_edge('A', 'B', distance=14)
>>> graph.add_edge('B', 'C', distance=18)
>>> graph.add_edge('B', 'C', distance=11)
>>> graph.add_edge('C', 'D', distance=19)
>>> cnnnz.find_shortest_distance('A', 'D')
44
```
