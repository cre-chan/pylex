# -*-coding:utf-8 -*-

from typing import List, Set, Dict
from copy import copy
import functools as funct

# 特殊常量epsilon
epsilon='ε'


class NFA:
    """
    NFA为多图，各节点包含字典，记录由指定的输入可以到达的节点的合集。
    记录对象id与实际对象的对应关系以便于用id访问结点。
    记录终止状态节点，便于进行操作，任何操作均会产生新的NFA，不会有任何NFA的终态同时包含两种token类型
    """

    State: type=Dict[str, Set[int]]
    Id: type=int

    # basic constructor, separated for convenience's sake
    def __init__(self, states: List[State], terms: Set[Id]):
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

    # 返回一个由终结状态组成的迭代器
    def get_terminators(self):
        return map(lambda term_id: self.get_state_by_id(term_id), self.terms)

    def get_state_by_id(self, state_id: int) -> State:
        return self.id_look_up[state_id]

    def get_start_id(self) -> Id:
        return id(self.states[0])

    def kleen_closure(self, states_set: Set[Id]) -> Set[Id]:
        states=map(lambda i: self.id_look_up[i][epsilon] if epsilon in self.id_look_up[i] else set(), states_set)
        new_sets=funct.reduce(lambda accum, entry: accum | entry, states, set())  # 新加入的顶点的集合
        return states_set if new_sets == set() else self.kleen_closure(new_sets | states_set)

    def closure(self, states_set: Set[Id], char: str) -> Set[Id]:
        states=map(lambda i: self.id_look_up[i][char] if char in self.id_look_up[i] else set(), states_set)
        result_set=funct.reduce(lambda accum, entry: accum | entry, states, set())
        return self.kleen_closure(result_set)

    # 输出形式为记录各边的顺序表
    def __str__(self):
        return str(NFASerialized(self))

    # 用于表示对象
    def __repr__(self):
        return str(self)


# self other TODO:此处拼接操作会对self中的状态产生影响，需要消除该处副作用
def concat(first: NFA, second: NFA) -> NFA:
    states=first.states + second.states
    self_term_states=first.get_terminators()

    # 为self的所有终态，增加无条件转换到other的初始状态的边
    for state in self_term_states:
        try:
            epsilon_set=state[epsilon]  # 考虑本身存在边的情况
            state[epsilon]=epsilon_set | {second.get_start_id()}
        except KeyError:
            state[epsilon]={second.get_start_id()}

    return NFA(states, second.terms)


# self | other
def union(first: NFA, other: NFA) -> NFA:
    self_start_id=first.get_start_id()
    other_start_id=other.get_start_id()

    states: List=first.states + other.states
    states.insert(0, {epsilon: {self_start_id, other_start_id}})

    return NFA(states, first.terms | other.terms)


# op* TODO:该操作会对op中states产生更改，需要消除副作用
def kleen(op: NFA) -> NFA:
    term_set=set(map(lambda term_state: id(term_state), op.get_terminators()))
    try:
        start_epsilon=op.states[0][epsilon]
        op.states[0][epsilon]=start_epsilon | term_set
    except KeyError:
        op.states[0][epsilon]=term_set

    return NFA(op.states, op.terms)


class NFASerialized:
    """
    将一个NFA化为序列化形式，用于生成易于阅读的形式
    """

    def __init__(self, src: NFA):
        stateid_index_lookup=dict(map(lambda t: (id(t[1]), t[0]), enumerate(src.states)))
        states=[
            copy(dic) for dic in src.states
        ]
        # 将src中各行复制到states中

        stateid_to_index=lambda id: stateid_index_lookup[id]

        for state in states:
            for key, value in state.items():
                state[key]=set(map(stateid_to_index, value))

            terms=set(map(stateid_to_index, src.terms))

            self.states=states
            self.terms=terms

    def __str__(self):
        states=[]

        for index, state in enumerate(self.states):
            for key, value in state.items():
                for end in value:
                    states.append(str(index) + '-' + key + '->' + str(end))

        return "states:" + str(states) + "\t terms:" + str(self.terms)

    def __repr__(self):
        return str(self)


class Token:
    """
    包装一个NFA，将NFA与相应的Token类型关联在一起，
    提供
    """
    pass


if __name__ == "__main__":
    pass
