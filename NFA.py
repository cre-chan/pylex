class NFA:
    # basic constructor, seperated for convinience's sake
    def __init__(self, states=[{}], terms=set()):
        self.states=states
        self.terms=terms

    # the function accepts a string to create an NFA
    @staticmethod
    def from_str(string: str):
        return NFA(
            list(
                map(lambda ic: {ic[1]: {ic[0] + 1}}, enumerate(string))
            ) + [{}],
            {len(string)}
        )

    # shifts the index
    def shift(self, i: int):
        terms=set(map(lambda x: i + x, self.terms))
        # shift indices in the NFA
        states=list(
            map(
                lambda edges: dict(
                    map(
                        lambda kv: (
                            kv[0],
                            set(
                                map(lambda x: x + i, kv[1])
                            )
                        ),
                        edges.items()
                    )
                ),
                self.states
            )
        )
        return NFA(states, terms)

    @staticmethod
    def union(lop, rop):
        pass


# mainly the test functions
def null_string_creation():
    '''test if the NFA with only one state will be created'''
    assert len(
        NFA.from_str("").states
    ) == 1


def copy_test():
    pass


if __name__ == "__main__":
    null_string_creation()
