class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.left}, {self.data}, {self.right})'

def print_parse_tree(node, cfg_expression):
    if node is None:
        return

    print(f'{cfg_expression}: {node.data}')
    print_parse_tree(node.left, cfg_expression + ' -> term ' + str(node.data))
    print_parse_tree(node.right, cfg_expression + ' -> factor ' + str(node.data))

def parse_expression(expression):
    """Parses the given expression and returns a parse tree."""

    tokens = expression.split()
    root = parse_term(tokens)

    while tokens:
        operator = tokens.pop(0)
        if operator in '+-':
            if operator == '+':
                cfg_expression = 'exp -> exp addop term'
            else:
                cfg_expression = 'exp -> exp addop term'
            right = parse_term(tokens)
            root = Node(operator, root, right)
        else:
            # Assume the operator is a mulop
            cfg_expression = 'term -> term mulop factor'
            right = parse_factor(tokens)
            root = Node(operator, root, right)

    return root

def parse_term(tokens):
    """Parses the next term in the given token list and returns a parse tree node."""

    token = tokens.pop(0)
    if token == '(':
        cfg_expression = 'term -> (exp)'
        node = parse_expression(tokens)
        tokens.pop(0)  # ')'
        return node
    elif token in '0123456789':
        cfg_expression = 'term -> number'
        return Node(int(token))
    else:
        raise Exception('Invalid token: {}'.format(token))

def parse_factor(tokens):
    """Parses the next factor in the given token list and returns a parse tree node."""

    token = tokens.pop(0)
    if token == '(':
        cfg_expression = 'factor -> (exp)'
        node = parse_expression(tokens)
        tokens.pop(0)  # ')'
        return node
    else:
        cfg_expression = 'factor -> number'
        return Node(int(token))

def evaluate_expression(node):
    """Evaluates the given parse tree and returns the result."""

    if node.data == '+':
        return evaluate_expression(node.left) + evaluate_expression(node.right)
    elif node.data == '-':
        return evaluate_expression(node.left) - evaluate_expression(node.right)
    elif node.data == '*':
        return evaluate_expression(node.left) * evaluate_expression(node.right)
    elif node.data == '/':
        return evaluate_expression(node.left) / evaluate_expression(node.right)
    elif node.data == '%':
        return evaluate_expression(node.left) % evaluate_expression(node.right)
    else:
        return node.data

def main():
    expression = input('Enter an expression: ')

    try:
        parse_tree = parse_expression(expression)
        result = evaluate_expression(parse_tree)

        print('Result:', result)

        print_parse_tree(parse_tree, 'exp')
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()
