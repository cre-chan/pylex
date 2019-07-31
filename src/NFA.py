# -*-coding:utf-8 -*-

from typing import List, Set, Dict

# 特殊常量epsilon
epsilon='ε'


class NFA:
    """
    NFA为多图，各节点包含字典，记录由指定的输入可以到达的节点的合集。
    记录对象id与实际对象的对应关系以便于用id访问结点。
    记录终止状态节点，便于进行操作，任何操作均会产生新的NFA，不会有任何NFA的终态同时包含两种token类型
    """

    State: type=Dict[str, Set[int]]

    # basic constructor, separated for convenience's sake
    def __init__(self, states: List[State], terms: Set):
        self.states=states
        self.id_look_up=dict(
            map(lambda a: (id(a), a), states)
        )
        self.terms=terms  # 终结状态合集

    # 从字符串创建NFA
    @staticmethod
    def from_str(str_literal: str):
        # 创建str.length+1个状态
        states: List[Dict[str, Set[int]]]=list(
            map(lambda i: {}, range(len(str_literal) + 1))
        )

        # 连接各状态
        for (i, c) in enumerate(str_literal):
            states[i][c]={id(states[i + 1])}

        return NFA(states, {id(states[-1])})

    def get_state_by_id(self, state_id: int) -> State:
        return self.id_look_up[state_id]

    def get_start_id(self) -> int:
        return id(self.states[0])

    # self other TODO:此处拼接操作会对self中的状态产生影响，需要消除该处副作用
    def concat(self, other):
        states=self.states + other.states
        self_term_states=map(lambda i: self.get_state_by_id(i), self.terms)

        # 为self的所有终态，增加无条件转换到other的初始状态的边
        for state in self_term_states:
            try:
                epsilon_set=state[epsilon]  # 考虑本身存在边的情况
                state[epsilon]=epsilon_set | {other.get_start_id()}
            except KeyError:
                state[epsilon]={other.get_start_id()}

        return NFA(states, other.terms)

    def union(self, other):
        self_start_id=self.get_start_id()
        other_start_id=other.get_start_id()

        states: List=self.states + other.states
        states.insert(0, {epsilon: {self_start_id, other_start_id}})

        return NFA(states, self.terms | other.terms)





class Token:
    """
    包装一个NFA，将NFA与相应的Token类型关联在一起，
    提供
    """
    pass


if __name__ == "__main__":
    pass
