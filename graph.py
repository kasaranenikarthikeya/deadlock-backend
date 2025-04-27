import networkx as nx

class ResourceAllocationGraph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.history = []
        self.redo_stack = []

    def add_process(self, process):
        if not process or not isinstance(process, str):
            return False
        if process in self.G.nodes:
            return False
        self.G.add_node(process, type='process')
        self.history.append({'action': 'add_process', 'process': process})
        self.redo_stack = []
        return True

    def add_resource(self, resource):
        if not resource or not isinstance(resource, str):
            return False
        if resource in self.G.nodes:
            return False
        self.G.add_node(resource, type='resource')
        self.history.append({'action': 'add_resource', 'resource': resource})
        self.redo_stack = []
        return True

    def request_resource(self, process, resource):
        if (process not in self.G.nodes or resource not in self.G.nodes or 
            self.G.has_edge(process, resource)):
            return False
        self.G.add_edge(process, resource)
        self.history.append({'action': 'request_resource', 'process': process, 'resource': resource})
        self.redo_stack = []
        return True

    def allocate_resource(self, process, resource):
        if (process not in self.G.nodes or resource not in self.G.nodes or 
            self.G.has_edge(resource, process)):
            return False
        self.G.add_edge(resource, process)
        self.history.append({'action': 'allocate_resource', 'process': process, 'resource': resource})
        self.redo_stack = []
        return True

    def remove_node(self, node):
        if node not in self.G.nodes:
            return False
        node_data = self.G.nodes[node]
        edges = list(self.G.in_edges(node)) + list(self.G.out_edges(node))
        self.G.remove_node(node)
        self.history.append({'action': 'remove_node', 'node': node, 'node_data': node_data, 'edges': edges})
        self.redo_stack = []
        return True

    def remove_edge(self, process, resource):
        if not self.G.has_edge(process, resource):
            return False
        self.G.remove_edge(process, resource)
        self.history.append({'action': 'remove_edge', 'process': process, 'resource': resource})
        self.redo_stack = []
        return True

    def reset_graph(self):
        nodes = list(self.G.nodes(data=True))
        edges = list(self.G.edges())
        self.G.clear()
        self.history = []
        self.redo_stack = []
        self.history.append({'action': 'reset_graph', 'nodes': nodes, 'edges': edges})

    def check_deadlock(self, root=None):
        try:
            cycle_edges = nx.find_cycle(self.G, orientation="original")
            cycle = [(u, v) for u, v, _ in cycle_edges]
            return cycle
        except nx.NetworkXNoCycle:
            return None

    def undo(self):
        if not self.history:
            return
        action = self.history.pop()
        self.redo_stack.append(action)
        if action['action'] == 'add_process':
            self.G.remove_node(action['process'])
        elif action['action'] == 'add_resource':
            self.G.remove_node(action['resource'])
        elif action['action'] == 'request_resource':
            self.G.remove_edge(action['process'], action['resource'])
        elif action['action'] == 'allocate_resource':
            self.G.remove_edge(action['resource'], action['process'])
        elif action['action'] == 'remove_node':
            self.G.add_node(action['node'], **action['node_data'])
            for u, v in action['edges']:
                self.G.add_edge(u, v)
        elif action['action'] == 'remove_edge':
            self.G.add_edge(action['process'], action['resource'])
        elif action['action'] == 'reset_graph':
            for node, data in action['nodes']:
                self.G.add_node(node, **data)
            self.G.add_edges_from(action['edges'])

    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        self.history.append(action)
        if action['action'] == 'add_process':
            self.G.add_node(action['process'], type='process')
        elif action['action'] == 'add_resource':
            self.G.add_node(action['resource'], type='resource')
        elif action['action'] == 'request_resource':
            self.G.add_edge(action['process'], action['resource'])
        elif action['action'] == 'allocate_resource':
            self.G.add_edge(action['resource'], action['process'])
        elif action['action'] == 'remove_node':
            self.G.remove_node(action['node'])
        elif action['action'] == 'remove_edge':
            self.G.remove_edge(action['process'], action['resource'])
        elif action['action'] == 'reset_graph':
            self.G.clear()

    def get_graph_state(self):
        return {
            'nodes': [{'id': n, 'type': d['type']} for n, d in self.G.nodes(data=True)],
            'edges': [{'from': u, 'to': v} for u, v in self.G.edges()],
            'history': self.history[-5:]
        }