from collections import deque


class DependencyGraph:
    def __init__(self):
        self.graph = {}

    def add_component(self, name):
        if name not in self.graph:
            self.graph[name] = []

    def add_dependency(self, source, target):
        self.add_component(source)
        self.add_component(target)
        if target not in self.graph[source]:
            self.graph[source].append(target)

    def get_topological_order(self):
        dependency_count = {name: len(dependencies) for name, dependencies in self.graph.items()}
        dependents = {name: [] for name in self.graph}

        for component, dependencies in self.graph.items():
            for dependency in dependencies:
                dependents[dependency].append(component)

        queue = deque(name for name, count in dependency_count.items() if count == 0)
        order = []

        while queue:
            component = queue.popleft()
            order.append(component)

            for dependent in dependents[component]:
                dependency_count[dependent] -= 1
                if dependency_count[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(self.graph):
            return None
        return order

    def is_acyclic(self):
        return self.get_topological_order() is not None


class DependencyAnalyzer:
    def __init__(self, dependency_graph):
        self.graph = dependency_graph.graph

    def find_dependencies_bfs(self, start):
        if start not in self.graph:
            return []

        visited = {start}
        queue = deque([start])
        levels = []

        while queue:
            level = []
            for _ in range(len(queue)):
                component = queue.popleft()
                for dependency in self.graph[component]:
                    if dependency not in visited:
                        visited.add(dependency)
                        queue.append(dependency)
                        level.append(dependency)
            if level:
                levels.append(level)

        return levels

    def find_dependencies_dfs(self, start):
        if start not in self.graph:
            return set()

        visited = set()

        def dfs(component):
            for dependency in self.graph[component]:
                if dependency not in visited:
                    visited.add(dependency)
                    dfs(dependency)

        dfs(start)
        return visited


def main():
    dependency_graph = DependencyGraph()
    dependency_graph.add_dependency("A", "B")
    dependency_graph.add_dependency("A", "C")
    dependency_graph.add_dependency("B", "D")
    dependency_graph.add_dependency("C", "D")
    dependency_graph.add_dependency("C", "E")
    dependency_graph.add_dependency("E", "B")

    analyzer = DependencyAnalyzer(dependency_graph)
    order = dependency_graph.get_topological_order()

    if order is None:
        print("Обнаружен цикл")
    else:
        print("Порядок сборки:", order)

    print("BFS для A:", analyzer.find_dependencies_bfs("A"))
    print("DFS для A:", analyzer.find_dependencies_dfs("A"))


if __name__ == "__main__":
    main()
