
from sys import argv
from graphviz import Digraph

class Node:
    label = ""
    children = []
    id = ""

    def __init__(self, label):
        self.label = label
        self.children = []


    def toString(self):
        output = self.label
        for i in range(0, len(self.children)):
            if i==0:
                output += "("
            else:
                output += ", "
            output += self.children[i].toString()
            if i==len(self.children)-1:
                output+=")"
        return output


class Scanner:
    data = []
    idx = 0

    def __init__(self, stringData):
        self.data = separate(stringData)


    def next(self):
        output = self.data[self.idx]
        self.idx += 1
        return output


    def hasNext(self):
        return self.idx < len(self.data)


    def hasNext(self, test):
        return self.data[self.idx] in test


    def hasFunctionNext(self):
        if self.idx >= len(self.data)-1:
            return False

        stopTokens = ["(", ")", ","]
        return (self.data[self.idx] not in stopTokens) and (self.data[self.idx+1] in "(")


    def hasTerminalNext(self):
        if self.idx >= len(self.data) - 1:
            return False

        stopTokens = ["(", ")", ","]
        return (self.data[self.idx] not in stopTokens) and (self.data[self.idx + 1] not in "(")


def separate(data):
    data = data.replace(" ", "")
    output = []
    temp = ""
    for c in data:
        if c in ["(", ")", ","]:
            if len(temp) > 0:
                output.append(temp)
                temp = ""
            output.append(c)
        else:
            temp += c
    if len(temp) > 0:
        output.append(temp)
    return output


def build_tree(scanner):
    if scanner.hasFunctionNext():
        return parseFunctionNode(scanner)
    elif scanner.hasTerminalNext():
        return parseTerminalNode(scanner)


def parseFunctionNode(scanner):
    f_node = Node(scanner.next())

    while not scanner.hasNext(")"):
        scanner.next()  # Remove '(' and ','
        f_node.children.append(build_tree(scanner))

    scanner.next()
    return f_node


def parseTerminalNode(scanner):
    t_node = Node(scanner.next())
    return t_node


def generate_dot(root):
    dot  = Digraph(comment='Graph', format='png')
    generate_node_rec(dot, root, "0")
    generate_connections_rec(dot, root)
    return dot

def generate_node_rec(dot, node, id):
    node.id = id
    dot.node(id, node.label)
    for i in range(0, len(node.children)):
        generate_node_rec(dot, node.children[i], "{}{}".format(id, i))

def generate_connections_rec(dot, node):
    for child in node.children:
        dot.edge(node.id, child.id)
    for child in node.children:
        generate_connections_rec(dot, child)


if __name__ == '__main__':

    OUTPUT_DIR = './treeviz'
    TREE_STR = ''

    for i in range(1, len(argv)):
        if argv[i] == '-o':
            keep_concatinating = False
            OUTPUT_DIR = argv[i+1]
        else:
            TREE_STR = argv[i]

    if TREE_STR in '':
        TREE_STR = input("Tree: ")

    scanner = Scanner(TREE_STR)
    root = build_tree(scanner)
    dot = generate_dot(root)
    dot.render('{}/tree.gv'.format(OUTPUT_DIR), view=True)




