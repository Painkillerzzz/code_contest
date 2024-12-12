import math
from tree import Tree, TreeNode
from typing import Optional

class MCTSNode(TreeNode):
    def __init__(self, state = None, action = None, parent = None):
        super().__init__(state, action, parent)

    def is_fully_expanded(self):
        """Check if all possible children have been expanded."""
        return self.actions is not None and len(self.actions) == 0

    def expand(self, getAction, max_a, step):
        """Expand the node by creating a new child node for an unexplored action."""
        if self.actions is None:
            self.actions = set(getAction(self.state, max_a))
        
        action = self.actions.pop()
        
        split_action = action.split("\n")
        action_steps = min(len(split_action), step * (self.depth + 1))
        
        child_state = "\n".join(split_action[:action_steps])
        child_node = MCTSNode(child_state, action, parent=self)
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_weight=1.0):
        """Select the best child node using the UCT formula."""
        return max(
            self.children,
            key=lambda child: child.value / (child.visit + 1e-6) +
            exploration_weight * math.sqrt(math.log(self.visit + 1) / (child.visit + 1e-6))
        )

    def backpropagate(self, result):
        """Propagate the result of a simulation up the tree."""
        self.visit += 1
        self.value += result
        if self.parent:
            self.parent.backpropagate(result)

class MCTSTree(Tree):
    def __init__(self, getAction, getReward, max_w = 3, step = 5 , budget = 50):
        super().__init__(getAction, getReward, max_w, step, budget)
        self.root = MCTSNode()

    def search(self):
        """Perform MCTS search for a given number of iterations."""
        while self.budget > 0:
            node: MCTSNode = self.select()
            max_a = min(self.budget, self.max_w)
            node = node.expand(self.getAction, max_a, self.step)
            self.budget -= 1
            result = self.getReward(node.action)
            node.score = result
            if result == 1.0:
                return node.action
            node.backpropagate(result)
            
            self.print_tree()

        return self.final_select()

    def select(self):
        """Select a node to expand based on the UCT formula."""
        node = self.root

        while node.is_fully_expanded():
            node = node.best_child()

        return node
    
    def final_select(self):
        """Traverse the entire tree and select the node with the highest score."""
        def traverse(node: MCTSNode):
            """Recursively traverse the tree to find the node with the highest score."""
            best_node = node
            for child in node.children:
                candidate = traverse(child)
                if candidate.score > best_node.score:
                    best_node = candidate
            return best_node

        # Start traversal from the root and return the action of the best node
        best_node = traverse(self.root)
        return best_node.action
