import networkx as nx

class GraphPipe():
    def __init__(self):
        self.__G = nx.DiGraph()
        self.__pointer_prompt = None
        self.__pointer_ID = None
        
    def step_0(self, 
               ID:str,
               prompt:str):
        """Setting del primo prompt della pipeline.

        Args:
            ID: identificativo prompt
            prompt: prompt iniziale.

        Returns:
            None.
        """
        self.__G.add_node(ID, prompt = prompt)
        
    def add_step(self, 
                 ID:str,
                 parent_ID:str,
                 prompt:str, 
                 expected_previous:str = "<GENERIC>"):
        """Setting dei successivi step della pipeline.

        Args:
            ID: identificativo prompt
            parent_ID: identificativo del prompt allo step precedente.
            prompt: prompt.
            expected_previous: risposta attesa per innescare il prompt dallo step precedente.

        Returns:
            None.
        """
        self.__G.add_node(ID, prompt = prompt)
        self.__G.add_edge(parent_ID, ID, expected_previous = expected_previous)
    
    def start_pipeline(self):
        """Inizializzazione della pipeline.

        Args:
            None.

        Returns:
            None.
        """
        if self.__G.number_of_nodes() == 0:
            raise ValueError("Il grafo risulta vuoto. Prima di avviare la pipeline assicurarsi che vi siano elementi dentro.")
        
        for node in self.__G.nodes:
            if self.__G.in_degree(node) == 0:
                self.__pointer_prompt = self.__G.nodes[node]['prompt']
                self.__pointer_ID = node
        
    def move_forward(self, 
                     response:str):
        """Muove la pipeline in base alla risposta del llm.

        Args:
            Response: risposta fornita dal llm.

        Returns:
            None.
        """
        is_next = 0
        for neighbour in self.__G.successors(self.__pointer_ID):
            if self.__G[self.__pointer_ID][neighbour]['expected_previous'] != "<GENERIC>":
                if self.__G[self.__pointer_ID][neighbour]['expected_previous'] == response:
                    self.__pointer_prompt = self.__G.nodes[neighbour]['prompt']
                    self.__pointer_ID = neighbour
                    is_next = 1
                    break
            else:
                self.__pointer_prompt = self.__G.nodes[neighbour]['prompt']
                self.__pointer_ID = neighbour
                is_next = 1
                break
            
        if is_next == 0:
            self.__pointer_prompt = "<STOP>"
            self.__pointer_ID = "<STOP>"
            
    def get_current_prompt(self):
        """Restituisce il prompt sullo step corrente della pipeline.

        Args:
            None.

        Returns:
            None.
        """
        return self.__pointer_prompt
    
    def stampa_albero_dfs(self, nodo_attuale, livello=0):
        """Stampa l'albero in modo ricorsivo, indentando i livelli.

        Args:
            nodo_attuale: Il nodo corrente da visitare.
            livello: Il livello di profondità del nodo.
        """
        print("  " * livello + self.__G.nodes[nodo_attuale]['prompt'])
        for vicino in self.__G.neighbors(nodo_attuale):
            self.stampa_albero_dfs(vicino, livello+1)