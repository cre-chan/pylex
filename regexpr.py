'''Definition for AST of regular expression'''



class A_Concat:
    '''lop rop'''
    def __init__(self,lop,rop):
        self.lop=lop
        self.rop=rop



class A_Union:
    '''lop|rop'''
    def __init__(self,lop,rop):
        self.lop=lop
        self.rop=rop


class A_Kleen:
    '''str*'''
    def __init__(self,string):
        self.op=A_String(string)


class A_String:
    '''str'''
    def __init__(self,string):
        self.content=string
