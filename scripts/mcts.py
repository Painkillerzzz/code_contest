import math
from tqdm import tqdm
from tree import Tree, TreeNode
from typing import Optional

class MCTSNode(TreeNode):
    def __init__(self, state = None, action = None, parent = None):
        super().__init__(state, action, parent)

    def is_fully_expanded(self):
        """Check if all possible children have been expanded."""
        return self.actions is not None and len(self.actions) == 0

    def expand(self, getAction, max_a, step, policy = "append"):
        """Expand the node by creating a new child node for an unexplored action."""
        if self.actions is None:
            self.actions = set(getAction(max_a, self.state,policy))
        
        action = self.actions.pop()
        if policy == "append":
            split_action = action.split("\n")
            action_steps = min(len(split_action), step * (self.depth + 1))
            child_state = "\n".join(split_action[:action_steps])
        elif policy == "modify":
            child_state = action
        child_node = MCTSNode(child_state, action, parent=self)
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_weight=1.0):
        """Select the best child node using the UCB formula."""
        return max(
            self.children,
            key=lambda child: child.value / (child.visit + 1e-6) +
            exploration_weight * math.sqrt(math.log(self.visit + 1) / (child.visit + 1e-6))
        )
        
    def bp_max(self, result):
        """Propagate the result of a simulation up the tree."""
        self.visit += 1
        self.value = max(result, self.value)
        if self.parent:
            self.parent.bp_max(result)

    def bp_acc(self, result):
        """Propagate the result of a simulation up the tree."""
        self.visit += 1
        self.value += result
        if self.parent:
            self.parent.bp_acc(result)

class MCTSTree(Tree):
    def __init__(self, getAction, getReward, max_w = 3, step = 5 , budget = 50, method = "max",derive_policy = "append"):
        super().__init__(getAction, getReward, max_w, step, budget)
        self.root = MCTSNode()
        self.method = method
        self.derive_policy = derive_policy
        if self.method not in ["max", "accumulate"]:
            raise ValueError("Invalid method, should be 'max' or 'accumulate'")
        if self.derive_policy not in ["append", "modify"]:
            raise ValueError("Invalid derive_policy, should be 'append' or 'modify'")

    def search(self):
        """Perform MCTS search for a given number of iterations."""
        for b in tqdm(range(self.budget, 0, -1), desc="MCTS searching"):
            node: MCTSNode = self.select()
            max_a = min(b, self.max_w)
            node = node.expand(self.getAction, max_a, self.step,self.derive_policy)
            result = self.getReward(node.action)
            node.score = result
            if result == 1.0:
                return node.action, 1.0, node.depth, self.budget - b + 1
            if self.method == "max":
                node.bp_max(result)
            elif self.method == "accumulate":
                node.bp_acc(result)
            else:
                raise ValueError("Invalid method")
            
            # self.print_tree()
            
        code, score, depth = self.final_select()

        return code, score, depth, self.budget

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
        return best_node.action, best_node.score, best_node.depth
