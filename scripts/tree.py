from typing import Optional

# Definition of a TreeNode class to represent a node in the tree
class TreeNode:
    def __init__(self, state=None, action=None, parent=None):
        # The state (prompt) associated with this node
        self.state = state
        # The action taken (code accepted) to arrive at this node
        self.action = action
        
        # A list of child nodes (initially empty)
        self.children: list[TreeNode] = []
        # Reference to the parent node (if any)
        self.parent: TreeNode = parent

        # The accumulated value of this node
        self.value = 0
        # The number of times this node has been visited
        self.visit = 0
        # The score provided by execution (reward)
        self.score = 0
        # The depth of this node in the tree (0 for the root, parent depth + 1 otherwise)
        self.depth = parent.depth + 1 if parent else 0

        # A set of possible actions (code) from this node
        self.actions: Optional[set[str]] = None


# Definition of a Tree class to manage the entire tree structure
class Tree:
    def __init__(self, getAction, getReward, max_w=3, step=5, budget=50):
        # Initialize the root of the tree with the given initial state (prompt)
        self.root = TreeNode()

        # The maximum width of the tree (e.g., limit on the number of children per node)
        self.max_w = max_w
        # Step parameter for code chunks (e.g., number of lines each time accepted)
        self.step = step
        # Budget constraint for the tree (restricted number of nodes to explore)
        self.budget = budget

        # Function to generate actions (code) for a given state (prompt)
        self.getAction = getAction
        # Function to run the code and get the reward
        self.getReward = getReward
        
    def print_tree(self, node=None, indent="#####\n", level=0):
        """Print the tree structure starting from a given node."""
        if node is None:
            node = self.root

        print(f"{indent}Level {level}: Visits={node.visit} Value={node.value:.2f} Score={node.score:.2f}")
        for child in node.children:
            self.print_tree(child, indent + "    ", level + 1)