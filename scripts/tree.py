from typing import Optional
class TreeNode:
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action
        
        self.children : list[TreeNode] = []
        self.parent : TreeNode = parent

        self.value = 0
        self.visit = 0
        self.depth = parent.depth + 1 if parent else 0

        self.actions:Optional[set[str]] = None
            
    


class Tree:
    def __init__(self,getAction,getReward, max_w = 3, init_state = "", step = 5 , budget = 50):
        self.root = TreeNode(init_state)
        self.root.parent = None

        self.max_w = max_w
        self.init_state = init_state
        self.step = step
        self.budget = budget

        self.getAction = getAction
        self.getReward = getReward
