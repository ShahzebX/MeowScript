"""
MeowScript Parser (Syntax Analyzer)

This module implements the syntax analysis phase using Recursive Descent parsing.
It builds an Abstract Syntax Tree (AST) from the token stream.
"""

from typing import List, Optional, Union
from dataclasses import dataclass
from lexer import Token, TokenType, Lexer


# ==================== AST Node Definitions ====================

@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int
    column: int


@dataclass
class ProgramNode(ASTNode):
    """Root node representing the entire program"""
    statements: List['StatementNode']


@dataclass
class StatementNode(ASTNode):
    """Base class for all statements"""
    pass


@dataclass
class VarDeclarationNode(StatementNode):
    """Variable declaration: Box x paws value"""
    identifier: str
    value: 'ExpressionNode'


@dataclass
class AssignmentNode(StatementNode):
    """Assignment: x paws value"""
    identifier: str
    value: 'ExpressionNode'


@dataclass
class FunctionDefNode(StatementNode):
    """Function definition: Hunt name(params) { body }"""
    name: str
    parameters: List[str]
    body: List[StatementNode]


@dataclass
class IfStatementNode(StatementNode):
    """If statement: Purr (condition) { then_block } Hiss { else_block }"""
    condition: 'ExpressionNode'
    then_block: List[StatementNode]
    else_block: Optional[List[StatementNode]]


@dataclass
class WhileLoopNode(StatementNode):
    """While loop: Chase (condition) { body }"""
    condition: 'ExpressionNode'
    body: List[StatementNode]


@dataclass
class ReturnStatementNode(StatementNode):
    """Return statement: Bring value"""
    value: 'ExpressionNode'


@dataclass
class PrintStatementNode(StatementNode):
    """Print statement: Meow(value)"""
    value: 'ExpressionNode'


@dataclass
class FunctionCallStatementNode(StatementNode):
    """Function call as a statement"""
    call: 'FunctionCallNode'


@dataclass
class ExpressionNode(ASTNode):
    """Base class for all expressions"""
    pass


@dataclass
class BinaryOpNode(ExpressionNode):
    """Binary operation: left op right"""
    operator: str
    left: ExpressionNode
    right: ExpressionNode


@dataclass
class UnaryOpNode(ExpressionNode):
    """Unary operation: op operand"""
    operator: str
    operand: ExpressionNode


@dataclass
class IntegerNode(ExpressionNode):
    """Integer literal"""
    value: int


@dataclass
class FloatNode(ExpressionNode):
    """Float literal"""
    value: float


@dataclass
class StringNode(ExpressionNode):
    """String literal"""
    value: str


@dataclass
class IdentifierNode(ExpressionNode):
    """Variable identifier"""
    name: str


@dataclass
class FunctionCallNode(ExpressionNode):
    """Function call: name(args)"""
    name: str
    arguments: List[ExpressionNode]


# ==================== Parser ====================

class ParserError(Exception):
    """Exception raised for syntax errors"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Syntax Error at line {token.line}, column {token.column}: {message}")


class Parser:
    """Recursive Descent Parser for MeowScript"""
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with token stream
        
        Args:
            tokens: List of tokens from the lexer
        """
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        
    def advance(self):
        """Move to the next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Peek at a future token without advancing"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """
        Expect a specific token type and advance
        
        Args:
            token_type: Expected token type
            
        Returns:
            The matched token
            
        Raises:
            ParserError: If token type doesn't match
        """
        if self.current_token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {self.current_token.type.name}",
                self.current_token
            )
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        return self.current_token.type in token_types
    
    def parse(self) -> ProgramNode:
        """
        Parse the entire program
        
        Returns:
            AST root node
            
        Raises:
            ParserError: If syntax error encountered
        """
        try:
            return self.parse_program()
        except ParserError as e:
            # Try to provide helpful error messages
            print(f"\n{'='*60}")
            print(f"SYNTAX ERROR")
            print(f"{'='*60}")
            print(f"{e}")
            print(f"{'='*60}\n")
            raise
    
    def parse_program(self) -> ProgramNode:
        """
        Parse program: Wake <statement_list> Sleep
        """
        wake_token = self.expect(TokenType.WAKE)
        statements = self.parse_statement_list()
        self.expect(TokenType.SLEEP)
        self.expect(TokenType.EOF)
        
        return ProgramNode(
            statements=statements,
            line=wake_token.line,
            column=wake_token.column
        )
    
    def parse_statement_list(self) -> List[StatementNode]:
        """
        Parse statement list: <statement>*
        """
        statements = []
        
        while not self.match(TokenType.SLEEP, TokenType.RBRACE, TokenType.EOF):
            try:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            except ParserError as e:
                # Error recovery: skip to next statement
                print(f"Error: {e}")
                print("Attempting to recover...")
                self.recover_from_error()
        
        return statements
    
    def recover_from_error(self):
        """
        Simple panic-mode error recovery
        Skip tokens until we find a statement start or block end
        """
        sync_tokens = {
            TokenType.BOX, TokenType.HUNT, TokenType.PURR, 
            TokenType.CHASE, TokenType.BRING, TokenType.MEOW,
            TokenType.RBRACE, TokenType.SLEEP, TokenType.EOF
        }
        
        while not self.match(*sync_tokens):
            self.advance()
    
    def parse_statement(self) -> Optional[StatementNode]:
        """
        Parse a single statement
        """
        # Variable declaration: Box
        if self.match(TokenType.BOX):
            return self.parse_var_declaration()
        
        # Function definition: Hunt
        if self.match(TokenType.HUNT):
            return self.parse_function_def()
        
        # If statement: Purr
        if self.match(TokenType.PURR):
            return self.parse_if_statement()
        
        # While loop: Chase
        if self.match(TokenType.CHASE):
            return self.parse_while_loop()
        
        # Return statement: Bring
        if self.match(TokenType.BRING):
            return self.parse_return_statement()
        
        # Print statement: Meow
        if self.match(TokenType.MEOW):
            return self.parse_print_statement()
        
        # Assignment or function call: IDENTIFIER
        if self.match(TokenType.IDENTIFIER):
            # Look ahead to determine if it's assignment or function call
            if self.peek() and self.peek().type == TokenType.PAWS:
                return self.parse_assignment()
            elif self.peek() and self.peek().type == TokenType.LPAREN:
                # Function call as statement
                call = self.parse_function_call()
                return FunctionCallStatementNode(
                    call=call,
                    line=call.line,
                    column=call.column
                )
            else:
                raise ParserError(
                    f"Unexpected identifier '{self.current_token.value}'. Expected 'paws' or '('",
                    self.current_token
                )
        
        # Empty statement or error
        if self.match(TokenType.EOF):
            return None
        
        raise ParserError(
            f"Unexpected token: {self.current_token.type.name}",
            self.current_token
        )
    
    def parse_var_declaration(self) -> VarDeclarationNode:
        """
        Parse variable declaration: Box identifier paws expression
        """
        box_token = self.expect(TokenType.BOX)
        identifier_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.PAWS)
        value = self.parse_expression()
        
        return VarDeclarationNode(
            identifier=identifier_token.value,
            value=value,
            line=box_token.line,
            column=box_token.column
        )
    
    def parse_assignment(self) -> AssignmentNode:
        """
        Parse assignment: identifier paws expression
        """
        identifier_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.PAWS)
        value = self.parse_expression()
        
        return AssignmentNode(
            identifier=identifier_token.value,
            value=value,
            line=identifier_token.line,
            column=identifier_token.column
        )
    
    def parse_function_def(self) -> FunctionDefNode:
        """
        Parse function definition: Hunt name(params) { body }
        """
        hunt_token = self.expect(TokenType.HUNT)
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        parameters = self.parse_param_list()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        body = self.parse_statement_list()
        self.expect(TokenType.RBRACE)
        
        return FunctionDefNode(
            name=name_token.value,
            parameters=parameters,
            body=body,
            line=hunt_token.line,
            column=hunt_token.column
        )
    
    def parse_param_list(self) -> List[str]:
        """
        Parse parameter list: identifier (, identifier)*
        """
        params = []
        
        if self.match(TokenType.IDENTIFIER):
            params.append(self.current_token.value)
            self.advance()
            
            while self.match(TokenType.COMMA):
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                params.append(param_token.value)
        
        return params
    
    def parse_if_statement(self) -> IfStatementNode:
        """
        Parse if statement: Purr (condition) { then_block } [Hiss { else_block }]
        """
        purr_token = self.expect(TokenType.PURR)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        then_block = self.parse_statement_list()
        self.expect(TokenType.RBRACE)
        
        else_block = None
        if self.match(TokenType.HISS):
            self.advance()
            self.expect(TokenType.LBRACE)
            else_block = self.parse_statement_list()
            self.expect(TokenType.RBRACE)
        
        return IfStatementNode(
            condition=condition,
            then_block=then_block,
            else_block=else_block,
            line=purr_token.line,
            column=purr_token.column
        )
    
    def parse_while_loop(self) -> WhileLoopNode:
        """
        Parse while loop: Chase (condition) { body }
        """
        chase_token = self.expect(TokenType.CHASE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        body = self.parse_statement_list()
        self.expect(TokenType.RBRACE)
        
        return WhileLoopNode(
            condition=condition,
            body=body,
            line=chase_token.line,
            column=chase_token.column
        )
    
    def parse_return_statement(self) -> ReturnStatementNode:
        """
        Parse return statement: Bring expression
        """
        bring_token = self.expect(TokenType.BRING)
        value = self.parse_expression()
        
        return ReturnStatementNode(
            value=value,
            line=bring_token.line,
            column=bring_token.column
        )
    
    def parse_print_statement(self) -> PrintStatementNode:
        """
        Parse print statement: Meow(expression)
        """
        meow_token = self.expect(TokenType.MEOW)
        self.expect(TokenType.LPAREN)
        value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        return PrintStatementNode(
            value=value,
            line=meow_token.line,
            column=meow_token.column
        )
    
    def parse_expression(self) -> ExpressionNode:
        """
        Parse expression (entry point to expression grammar)
        """
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> ExpressionNode:
        """
        Parse logical OR: <logical_and> (|| <logical_and>)*
        """
        left = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op_token = self.current_token
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOpNode(
                operator='||',
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_logical_and(self) -> ExpressionNode:
        """
        Parse logical AND: <equality> (&& <equality>)*
        """
        left = self.parse_equality()
        
        while self.match(TokenType.AND):
            op_token = self.current_token
            self.advance()
            right = self.parse_equality()
            left = BinaryOpNode(
                operator='&&',
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_equality(self) -> ExpressionNode:
        """
        Parse equality: <comparison> ((== | !=) <comparison>)*
        """
        left = self.parse_comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOpNode(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_comparison(self) -> ExpressionNode:
        """
        Parse comparison: <addition> ((< | > | <= | >=) <addition>)*
        """
        left = self.parse_addition()
        
        while self.match(TokenType.LESS, TokenType.GREATER, 
                         TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.parse_addition()
            left = BinaryOpNode(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_addition(self) -> ExpressionNode:
        """
        Parse addition/subtraction: <multiplication> ((+ | -) <multiplication>)*
        """
        left = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.parse_multiplication()
            left = BinaryOpNode(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_multiplication(self) -> ExpressionNode:
        """
        Parse multiplication/division/modulo: <unary> ((* | / | %) <unary>)*
        """
        left = self.parse_unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op_token = self.current_token
            op = op_token.value
            self.advance()
            right = self.parse_unary()
            left = BinaryOpNode(
                operator=op,
                left=left,
                right=right,
                line=op_token.line,
                column=op_token.column
            )
        
        return left
    
    def parse_unary(self) -> ExpressionNode:
        """
        Parse unary: (! | -) <unary> | <primary>
        """
        if self.match(TokenType.NOT, TokenType.MINUS):
            op_token = self.current_token
            op = op_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(
                operator=op,
                operand=operand,
                line=op_token.line,
                column=op_token.column
            )
        
        return self.parse_primary()
    
    def parse_primary(self) -> ExpressionNode:
        """
        Parse primary: INTEGER | FLOAT | STRING | IDENTIFIER | function_call | ( expression )
        """
        # Integer literal
        if self.match(TokenType.INTEGER):
            token = self.current_token
            self.advance()
            return IntegerNode(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        # Float literal
        if self.match(TokenType.FLOAT):
            token = self.current_token
            self.advance()
            return FloatNode(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        # String literal
        if self.match(TokenType.STRING):
            token = self.current_token
            self.advance()
            return StringNode(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        # Identifier or function call
        if self.match(TokenType.IDENTIFIER):
            # Check if it's a function call
            if self.peek() and self.peek().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                token = self.current_token
                self.advance()
                return IdentifierNode(
                    name=token.value,
                    line=token.line,
                    column=token.column
                )
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise ParserError(
            f"Unexpected token in expression: {self.current_token.type.name}",
            self.current_token
        )
    
    def parse_function_call(self) -> FunctionCallNode:
        """
        Parse function call: identifier(arguments)
        """
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        arguments = self.parse_arg_list()
        self.expect(TokenType.RPAREN)
        
        return FunctionCallNode(
            name=name_token.value,
            arguments=arguments,
            line=name_token.line,
            column=name_token.column
        )
    
    def parse_arg_list(self) -> List[ExpressionNode]:
        """
        Parse argument list: expression (, expression)*
        """
        args = []
        
        # Check for empty argument list
        if self.match(TokenType.RPAREN):
            return args
        
        args.append(self.parse_expression())
        
        while self.match(TokenType.COMMA):
            self.advance()
            args.append(self.parse_expression())
        
        return args


def print_ast(node, indent=0):
    """Pretty print the AST (for debugging)"""
    prefix = "  " * indent
    
    if isinstance(node, ProgramNode):
        print(f"{prefix}Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, VarDeclarationNode):
        print(f"{prefix}VarDecl: {node.identifier}")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, AssignmentNode):
        print(f"{prefix}Assignment: {node.identifier}")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, FunctionDefNode):
        print(f"{prefix}FunctionDef: {node.name}({', '.join(node.parameters)})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, IfStatementNode):
        print(f"{prefix}If:")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Then:")
        for stmt in node.then_block:
            print_ast(stmt, indent + 2)
        if node.else_block:
            print(f"{prefix}  Else:")
            for stmt in node.else_block:
                print_ast(stmt, indent + 2)
    
    elif isinstance(node, WhileLoopNode):
        print(f"{prefix}While:")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    
    elif isinstance(node, ReturnStatementNode):
        print(f"{prefix}Return:")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, PrintStatementNode):
        print(f"{prefix}Print:")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, FunctionCallStatementNode):
        print(f"{prefix}FunctionCallStmt:")
        print_ast(node.call, indent + 1)
    
    elif isinstance(node, BinaryOpNode):
        print(f"{prefix}BinaryOp: {node.operator}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    
    elif isinstance(node, UnaryOpNode):
        print(f"{prefix}UnaryOp: {node.operator}")
        print_ast(node.operand, indent + 1)
    
    elif isinstance(node, IntegerNode):
        print(f"{prefix}Integer: {node.value}")
    
    elif isinstance(node, FloatNode):
        print(f"{prefix}Float: {node.value}")
    
    elif isinstance(node, StringNode):
        print(f"{prefix}String: \"{node.value}\"")
    
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}Identifier: {node.name}")
    
    elif isinstance(node, FunctionCallNode):
        print(f"{prefix}FunctionCall: {node.name}")
        for arg in node.arguments:
            print_ast(arg, indent + 1)


def main():
    """Test the parser with a sample program"""
    sample_code = """
    Wake
    
    Hunt add(x, y) {
        Bring x + y
    }
    
    Box age paws 3
    Box name paws "Fluffy"
    
    Purr (age < 5) {
        Meow("Kitten")
    } Hiss {
        Meow("Adult")
    }
    
    Box result paws add(5, 3)
    Meow(result)
    
    Sleep
    """
    
    try:
        # Lexical analysis
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        
        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        
        print("=" * 60)
        print("SYNTAX ANALYSIS - ABSTRACT SYNTAX TREE")
        print("=" * 60)
        print_ast(ast)
        print("=" * 60)
        print("Parsing completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
