from NFA import Token, NFA
import NFA as NFA_m
from typing import List, Dict
import itertools
import functools as fnt


class DFA:
    # TODO:状态转换图简化
    def __init__(self, tokens: List[Token]):
        # 将各nfa合并起来，将id与状态的对应关系合并起来
        nfa=map(lambda tk: tk.nfa, tokens)
        nfa=fnt.reduce(lambda sum, i: NFA_m.concat(sum, i), nfa)

        print("nfa:" + str(nfa))

        id_to_term=map(lambda tk: tk.state_lookup.items(), tokens)
        id_to_term=dict(fnt.reduce(lambda sum, i: itertools.chain(sum, i), id_to_term))  # 保存id与终态的对应状态

        # 初始化
        start_set={nfa.get_start_id()}
        all_states=[start_set]
        dfa: List[Dict[str, int]]=[]

        ascii_charset=list(map(lambda i: chr(i), range(256)))  # 0-255ascii字符集

        for state in all_states:
            tbl_entry={}
            for c in ascii_charset:
                state_new=nfa.closure(state, c)  # 求state的闭包
                if state_new != set():
                    # 若state对于c的闭包存在，则
                    try:
                        i=all_states.index(state_new)
                        tbl_entry[c]=i
                    except ValueError:
                        all_states.append(state_new)
                        i=len(all_states)-1
                        tbl_entry[c]=i

            dfa.append(tbl_entry)

        print(all_states)

        self.edge_tbl=dfa

    def __str__(self):
        display=[]
        for i, state in enumerate(self.edge_tbl):
            for c, end in state.items():
                display.append(str(i) + '-' + c + '->' + str(end))
        return str(display)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    let=NFA.from_str("let")
    let_token=Token(let, 0)
    let_dfa=DFA([let_token])
    print("let dfa:"+str(let_dfa))
