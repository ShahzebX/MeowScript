"""
MeowScript Semantic Analyzer

This module implements semantic analysis including:
- Symbol table management
- Type inference and checking
- Scope handling
- Semantic error detection
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from parser import *


class DataType(Enum):
    """Data types in MeowScript"""
    TREATS = auto()      # Integer
    WHISKERS = auto()    # Float
    YARN = auto()        # String
    VOID = auto()        # No return value
    UNKNOWN = auto()     # Type not yet determined


@dataclass
class Symbol:
    """Symbol table entry"""
    name: str
    data_type: DataType
    scope_level: int
    is_function: bool = False
    parameters: Optional[List[str]] = None
    line: int = 0
    column: int = 0


class SymbolTable:
    """Symbol table for tracking variables and functions"""
    
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Stack of scopes
        self.current_scope = 0
        
    def enter_scope(self):
        """Enter a new scope"""
        self.scopes.append({})
        self.current_scope += 1
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def declare(self, symbol: Symbol):
        """
        Declare a new symbol in current scope
        
        Raises:
            SemanticError: If symbol already declared in current scope
        """
        if symbol.name in self.scopes[self.current_scope]:
            existing = self.scopes[self.current_scope][symbol.name]
            raise SemanticError(
                f"Variable '{symbol.name}' already declared in current scope at line {existing.line}",
                symbol.line,
                symbol.column
            )
        
        self.scopes[self.current_scope][symbol.name] = symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in current and enclosing scopes
        
        Returns:
            Symbol if found, None otherwise
        """
        # Search from current scope backwards
        for scope_level in range(self.current_scope, -1, -1):
            if name in self.scopes[scope_level]:
                return self.scopes[scope_level][name]
        return None
    
    def update_type(self, name: str, data_type: DataType):
        """Update the type of an existing symbol"""
        symbol = self.lookup(name)
        if symbol:
            symbol.data_type = data_type
    
    def print_table(self):
        """Print symbol table (for debugging)"""
        print("\n" + "=" * 60)
        print("SYMBOL TABLE")
        print("=" * 60)
        for level, scope in enumerate(self.scopes):
            print(f"\nScope Level {level}:")
            for name, symbol in scope.items():
                type_info = f"{symbol.data_type.name}"
                if symbol.is_function:
                    params = ', '.join(symbol.parameters) if symbol.parameters else ''
                    print(f"  {name}: Function({params}) -> {type_info}")
                else:
                    print(f"  {name}: {type_info}")
        print("=" * 60 + "\n")


class SemanticError(Exception):
    """Exception raised for semantic errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Semantic Error at line {line}, column {column}: {message}")


class SemanticAnalyzer:
    """Semantic analyzer for MeowScript"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.current_function: Optional[str] = None
        self.in_function = False
    
    def analyze(self, ast: ProgramNode):
        """
        Perform semantic analysis on the AST
        
        Args:
            ast: Abstract syntax tree root node
            
        Raises:
            SemanticError: If semantic errors are found
        """
        try:
            self.visit_program(ast)
            
            # Print symbol table for debugging
            self.symbol_table.print_table()
            
            if self.errors:
                print(f"\n{'='*60}")
                print(f"SEMANTIC ERRORS FOUND: {len(self.errors)}")
                print(f"{'='*60}")
                for error in self.errors:
                    print(f"  {error}")
                print(f"{'='*60}\n")
                raise self.errors[0]  # Raise first error
            
        except SemanticError:
            raise
    
    def add_error(self, message: str, line: int, column: int):
        """Add a semantic error"""
        error = SemanticError(message, line, column)
        self.errors.append(error)
    
    def visit_program(self, node: ProgramNode):
        """Visit program node"""
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: StatementNode):
        """Visit a statement node"""
        if isinstance(node, VarDeclarationNode):
            self.visit_var_declaration(node)
        elif isinstance(node, AssignmentNode):
            self.visit_assignment(node)
        elif isinstance(node, FunctionDefNode):
            self.visit_function_def(node)
        elif isinstance(node, IfStatementNode):
            self.visit_if_statement(node)
        elif isinstance(node, WhileLoopNode):
            self.visit_while_loop(node)
        elif isinstance(node, ReturnStatementNode):
            self.visit_return_statement(node)
        elif isinstance(node, PrintStatementNode):
            self.visit_print_statement(node)
        elif isinstance(node, FunctionCallStatementNode):
            self.visit_function_call_statement(node)
    
    def visit_var_declaration(self, node: VarDeclarationNode):
        """Visit variable declaration"""
        # Get the type from the initial value
        value_type = self.visit_expression(node.value)
        
        # Declare the variable
        symbol = Symbol(
            name=node.identifier,
            data_type=value_type,
            scope_level=self.symbol_table.current_scope,
            is_function=False,
            line=node.line,
            column=node.column
        )
        
        try:
            self.symbol_table.declare(symbol)
        except SemanticError as e:
            self.add_error(e.message, e.line, e.column)
    
    def visit_assignment(self, node: AssignmentNode):
        """Visit assignment"""
        # Check if variable is declared
        symbol = self.symbol_table.lookup(node.identifier)
        if not symbol:
            self.add_error(
                f"Undeclared variable '{node.identifier}'",
                node.line,
                node.column
            )
            return
        
        # Check if trying to assign to a function
        if symbol.is_function:
            self.add_error(
                f"Cannot assign to function '{node.identifier}'",
                node.line,
                node.column
            )
            return
        
        # Get the type of the value being assigned
        value_type = self.visit_expression(node.value)
        
        # Type checking: ensure compatible types
        if symbol.data_type != DataType.UNKNOWN and value_type != DataType.UNKNOWN:
            if not self.are_types_compatible(symbol.data_type, value_type):
                self.add_error(
                    f"Type mismatch: cannot assign {value_type.name} to {symbol.data_type.name}",
                    node.line,
                    node.column
                )
    
    def visit_function_def(self, node: FunctionDefNode):
        """Visit function definition"""
        # Declare the function in current scope
        symbol = Symbol(
            name=node.name,
            data_type=DataType.UNKNOWN,  # Return type will be inferred
            scope_level=self.symbol_table.current_scope,
            is_function=True,
            parameters=node.parameters,
            line=node.line,
            column=node.column
        )
        
        try:
            self.symbol_table.declare(symbol)
        except SemanticError as e:
            self.add_error(e.message, e.line, e.column)
            return
        
        # Enter function scope
        self.symbol_table.enter_scope()
        old_function = self.current_function
        old_in_function = self.in_function
        self.current_function = node.name
        self.in_function = True
        
        # Declare parameters as local variables with unknown type initially
        for param in node.parameters:
            param_symbol = Symbol(
                name=param,
                data_type=DataType.UNKNOWN,
                scope_level=self.symbol_table.current_scope,
                is_function=False,
                line=node.line,
                column=node.column
            )
            try:
                self.symbol_table.declare(param_symbol)
            except SemanticError as e:
                self.add_error(e.message, e.line, e.column)
        
        # Visit function body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_function = old_function
        self.in_function = old_in_function
    
    def visit_if_statement(self, node: IfStatementNode):
        """Visit if statement"""
        # Check condition type
        condition_type = self.visit_expression(node.condition)
        
        # Enter then block scope
        self.symbol_table.enter_scope()
        for stmt in node.then_block:
            self.visit_statement(stmt)
        self.symbol_table.exit_scope()
        
        # Enter else block scope if it exists
        if node.else_block:
            self.symbol_table.enter_scope()
            for stmt in node.else_block:
                self.visit_statement(stmt)
            self.symbol_table.exit_scope()
    
    def visit_while_loop(self, node: WhileLoopNode):
        """Visit while loop"""
        # Check condition type
        condition_type = self.visit_expression(node.condition)
        
        # Enter loop body scope
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit_statement(stmt)
        self.symbol_table.exit_scope()
    
    def visit_return_statement(self, node: ReturnStatementNode):
        """Visit return statement"""
        if not self.in_function:
            self.add_error(
                "Return statement outside of function",
                node.line,
                node.column
            )
            return
        
        # Get return value type
        return_type = self.visit_expression(node.value)
        
        # Update function's return type
        if self.current_function:
            symbol = self.symbol_table.lookup(self.current_function)
            if symbol and symbol.data_type == DataType.UNKNOWN:
                symbol.data_type = return_type
            elif symbol and symbol.data_type != return_type:
                # Check for type consistency in multiple returns
                if not self.are_types_compatible(symbol.data_type, return_type):
                    self.add_error(
                        f"Inconsistent return type: expected {symbol.data_type.name}, got {return_type.name}",
                        node.line,
                        node.column
                    )
    
    def visit_print_statement(self, node: PrintStatementNode):
        """Visit print statement"""
        # Expressions of any type can be printed
        self.visit_expression(node.value)
    
    def visit_function_call_statement(self, node: FunctionCallStatementNode):
        """Visit function call statement"""
        self.visit_function_call(node.call)
    
    def visit_expression(self, node: ExpressionNode) -> DataType:
        """
        Visit expression and return its type
        
        Returns:
            DataType of the expression
        """
        if isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.visit_unary_op(node)
        elif isinstance(node, IntegerNode):
            return DataType.TREATS
        elif isinstance(node, FloatNode):
            return DataType.WHISKERS
        elif isinstance(node, StringNode):
            return DataType.YARN
        elif isinstance(node, IdentifierNode):
            return self.visit_identifier(node)
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        else:
            return DataType.UNKNOWN
    
    def visit_binary_op(self, node: BinaryOpNode) -> DataType:
        """Visit binary operation and return result type"""
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)
        
        # Arithmetic operators: +, -, *, /, %
        if node.operator in ['+', '-', '*', '/', '%']:
            # String concatenation with +
            if node.operator == '+' and (left_type == DataType.YARN or right_type == DataType.YARN):
                return DataType.YARN
            
            # Numeric operations
            if left_type in [DataType.TREATS, DataType.WHISKERS] and right_type in [DataType.TREATS, DataType.WHISKERS]:
                # Division always returns float
                if node.operator == '/':
                    return DataType.WHISKERS
                # Float if either operand is float
                if left_type == DataType.WHISKERS or right_type == DataType.WHISKERS:
                    return DataType.WHISKERS
                return DataType.TREATS
            
            # Type error
            if left_type != DataType.UNKNOWN and right_type != DataType.UNKNOWN:
                self.add_error(
                    f"Type error: cannot apply operator '{node.operator}' to {left_type.name} and {right_type.name}",
                    node.line,
                    node.column
                )
            return DataType.UNKNOWN
        
        # Comparison operators: ==, !=, <, >, <=, >=
        elif node.operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Can compare same types
            if left_type == right_type:
                return DataType.TREATS  # Boolean result (0 or 1)
            
            # Can compare numeric types
            if left_type in [DataType.TREATS, DataType.WHISKERS] and right_type in [DataType.TREATS, DataType.WHISKERS]:
                return DataType.TREATS
            
            if left_type != DataType.UNKNOWN and right_type != DataType.UNKNOWN:
                self.add_error(
                    f"Type error: cannot compare {left_type.name} and {right_type.name}",
                    node.line,
                    node.column
                )
            return DataType.TREATS
        
        # Logical operators: &&, ||
        elif node.operator in ['&&', '||']:
            # Logical operations work on any type (0/empty is false, rest is true)
            return DataType.TREATS  # Boolean result
        
        return DataType.UNKNOWN
    
    def visit_unary_op(self, node: UnaryOpNode) -> DataType:
        """Visit unary operation and return result type"""
        operand_type = self.visit_expression(node.operand)
        
        # Logical NOT
        if node.operator == '!':
            return DataType.TREATS  # Boolean result
        
        # Unary minus
        elif node.operator == '-':
            if operand_type in [DataType.TREATS, DataType.WHISKERS]:
                return operand_type
            
            if operand_type != DataType.UNKNOWN:
                self.add_error(
                    f"Type error: cannot apply unary '-' to {operand_type.name}",
                    node.line,
                    node.column
                )
            return DataType.UNKNOWN
        
        return DataType.UNKNOWN
    
    def visit_identifier(self, node: IdentifierNode) -> DataType:
        """Visit identifier and return its type"""
        symbol = self.symbol_table.lookup(node.name)
        
        if not symbol:
            self.add_error(
                f"Undeclared variable '{node.name}'",
                node.line,
                node.column
            )
            return DataType.UNKNOWN
        
        if symbol.is_function:
            self.add_error(
                f"Cannot use function '{node.name}' as a variable",
                node.line,
                node.column
            )
            return DataType.UNKNOWN
        
        return symbol.data_type
    
    def visit_function_call(self, node: FunctionCallNode) -> DataType:
        """Visit function call and return return type"""
        # Check if function is declared
        symbol = self.symbol_table.lookup(node.name)
        
        if not symbol:
            self.add_error(
                f"Undeclared function '{node.name}'",
                node.line,
                node.column
            )
            return DataType.UNKNOWN
        
        if not symbol.is_function:
            self.add_error(
                f"'{node.name}' is not a function",
                node.line,
                node.column
            )
            return DataType.UNKNOWN
        
        # Check argument count
        expected_params = len(symbol.parameters) if symbol.parameters else 0
        actual_args = len(node.arguments)
        
        if expected_params != actual_args:
            self.add_error(
                f"Function '{node.name}' expects {expected_params} arguments, got {actual_args}",
                node.line,
                node.column
            )
        
        # Type check arguments (visit them to catch errors)
        for arg in node.arguments:
            self.visit_expression(arg)
        
        return symbol.data_type
    
    def are_types_compatible(self, type1: DataType, type2: DataType) -> bool:
        """
        Check if two types are compatible for assignment/comparison
        
        Returns:
            True if compatible, False otherwise
        """
        if type1 == type2:
            return True
        
        # Numeric types are somewhat compatible
        if type1 in [DataType.TREATS, DataType.WHISKERS] and type2 in [DataType.TREATS, DataType.WHISKERS]:
            return True
        
        return False


def main():
    """Test the semantic analyzer"""
    from lexer import Lexer
    from parser import Parser
    
    sample_code = """
    Wake
    
    Hunt add(x, y) {
        Bring x + y
    }
    
    Box age paws 3
    Box weight paws 4.5
    Box name paws "Fluffy"
    
    Purr (age < 5) {
        Meow("Kitten")
    } Hiss {
        Meow("Adult")
    }
    
    Box result paws add(age, 2)
    Meow(result)
    
    Box counter paws 0
    Chase (counter < 5) {
        Meow(counter)
        counter paws counter + 1
    }
    
    Sleep
    """
    
    try:
        # Lexical analysis
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        
        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Semantic analysis
        print("=" * 60)
        print("SEMANTIC ANALYSIS")
        print("=" * 60)
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("Semantic analysis completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
