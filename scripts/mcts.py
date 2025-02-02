import math
from tqdm import tqdm
from tree import Tree, TreeNode

class MCTSNode(TreeNode):
    def __init__(self, state = None, action = None, parent = None, score = 0, length_exceeded = False):
        super().__init__(state, action, parent, score)
        self.length_exceeded = length_exceeded

    def is_fully_expanded(self):
        """Check if all possible children have been expanded."""
        return self.actions is not None and len(self.actions) == 0

    def expand(self, getAction, getReward, max_a, step, policy = "append"):
        """Expand the node by creating a new child node for an unexplored action."""
        if self.actions is None:
            self.actions = set(getAction(max_a, self.state, policy))
        
        action = self.actions.pop()
        reward = getReward(action)
        if policy == "append":
            split_action = action.split("\n")
            if len(split_action) <= step * (self.depth + 1):
                child_state = action
                length_exceeded = True
            else:
                child_state = "\n".join(split_action[:step * (self.depth + 1)])
                length_exceeded = False
        elif policy == "modify":
            child_state = action
            length_exceeded = False
        child_node = MCTSNode(child_state, action, self, reward, length_exceeded)
        self.children.append(child_node)
        
        return child_node, reward

    def best_child(self, exploration_weight=1.0):
        """Select the best child node using the UCB formula."""
        return max(
            [child for child in self.children if not child.length_exceeded],
            key=lambda child: child.value / (child.visit + 1e-6) +
                exploration_weight * math.sqrt(math.log(self.visit + 1) / (child.visit + 1e-6))
        )
        
    def bp(self, reward, policy):
        """Propagate the reward of a simulation up the tree."""
        self.visit += 1
        if policy == "max":
            self.value = max(reward, self.value)
        elif policy == "accumulate":
            self.value += reward
        else:
            raise ValueError("Invalid BP policy, should be 'max' or 'accumulate'")
        
        if self.is_fully_expanded():
            length_exceeded = True
            for child in self.children:
                if not child.length_exceeded:
                    length_exceeded = False
                    break
            self.length_exceeded = length_exceeded
        
        if self.parent:
            self.parent.bp(reward, policy)


class MCTSTree(Tree):
    def __init__(self, getAction, getReward, max_w = 3, step = 5, budget = 50, bp_policy="max", derive_policy = "append"):
        super().__init__(getAction, getReward, None, max_w, step, budget)
        self.root = MCTSNode()
        self.bp_policy = bp_policy
        self.derive_policy = derive_policy
        if self.bp_policy not in ["max", "accumulate"]:
            raise ValueError("Invalid BP policy, should be 'max' or 'accumulate'")
        if self.derive_policy not in ["append", "modify"]:
            raise ValueError("Invalid derive_policy, should be 'append' or 'modify'")
    def search(self):
        """Perform MCTS search for a given number of iterations."""
        for b in tqdm(range(self.budget, 0, -1), desc="MCTS searching"):
            node: MCTSNode = self.select()
            max_a = min(b, self.max_w)
            node, reward = node.expand(self.getAction, self.getReward, max_a, self.step, self.derive_policy)
            if reward == 1.0:
                # self.print_tree()
                return node.action, 1.0, node.depth - 1, self.budget - b + 1
            node.bp(reward, self.bp_policy)
            if self.root.length_exceeded:
                code, score, revision = self.final_select()
                # self.print_tree()
                return code, score, revision, self.budget - b + 1
            
        # self.print_tree()
            
        code, score, revision = self.final_select()

        return code, score, revision, self.budget

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
                candidate: MCTSNode = traverse(child)
                if candidate.score > best_node.score:
                    best_node = candidate
                elif candidate.score == best_node.score and candidate.depth > best_node.score:
                    best_node = candidate
            return best_node

        # Start traversal from the root and return the action of the best node
        best_node = traverse(self.root)
        return best_node.action, best_node.score, best_node.depth - 1
