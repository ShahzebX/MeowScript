"""
MeowScript Intermediate Code Generator

This module generates three-address code (TAC) from the AST.
TAC is a linear representation suitable for optimization and target code generation.
"""

from typing import List, Optional
from dataclasses import dataclass
from parser import *
from semantic import SemanticAnalyzer, DataType


@dataclass
class TACInstruction:
    """Represents a three-address code instruction"""
    operation: str
    arg1: Optional[str]
    arg2: Optional[str]
    result: Optional[str]
    
    def __str__(self):
        if self.operation == 'label':
            return f"{self.result}:"
        elif self.operation == 'goto':
            return f"    goto {self.result}"
        elif self.operation == 'if_false':
            return f"    if_false {self.arg1} goto {self.result}"
        elif self.operation == 'if_true':
            return f"    if_true {self.arg1} goto {self.result}"
        elif self.operation == 'param':
            return f"    param {self.arg1}"
        elif self.operation == 'call':
            if self.result:
                return f"    {self.result} = call {self.arg1}, {self.arg2}"
            else:
                return f"    call {self.arg1}, {self.arg2}"
        elif self.operation == 'return':
            return f"    return {self.arg1}"
        elif self.operation == 'print':
            return f"    print {self.arg1}"
        elif self.operation == 'begin_func':
            return f"\n{self.arg1}:"
        elif self.operation == 'end_func':
            return f"    end_func {self.arg1}"
        elif self.operation == '=':
            return f"    {self.result} = {self.arg1}"
        elif self.arg2:
            return f"    {self.result} = {self.arg1} {self.operation} {self.arg2}"
        else:
            return f"    {self.result} = {self.operation} {self.arg1}"


class CodeGenerator:
    """Three-address code generator for MeowScript"""
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_function = None
        
    def new_temp(self) -> str:
        """Generate a new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, operation: str, arg1: Optional[str] = None, 
             arg2: Optional[str] = None, result: Optional[str] = None):
        """Emit a three-address code instruction"""
        instruction = TACInstruction(operation, arg1, arg2, result)
        self.instructions.append(instruction)
    
    def generate(self, ast: ProgramNode) -> List[TACInstruction]:
        """
        Generate three-address code from AST
        
        Args:
            ast: Abstract syntax tree root node
            
        Returns:
            List of TAC instructions
        """
        self.visit_program(ast)
        return self.instructions
    
    def visit_program(self, node: ProgramNode):
        """Visit program node"""
        # Generate code for all statements
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
        # Generate code for the value expression
        value_temp = self.visit_expression(node.value)
        
        # Assignment to the variable
        self.emit('=', value_temp, None, node.identifier)
    
    def visit_assignment(self, node: AssignmentNode):
        """Visit assignment"""
        # Generate code for the value expression
        value_temp = self.visit_expression(node.value)
        
        # Assignment to the variable
        self.emit('=', value_temp, None, node.identifier)
    
    def visit_function_def(self, node: FunctionDefNode):
        """Visit function definition"""
        old_function = self.current_function
        self.current_function = node.name
        
        # Function label
        self.emit('begin_func', node.name, None, None)
        
        # Generate code for function body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # End function marker
        self.emit('end_func', node.name, None, None)
        
        self.current_function = old_function
    
    def visit_if_statement(self, node: IfStatementNode):
        """
        Visit if statement
        
        Generated code pattern:
            <condition_code>
            if_false <condition_temp> goto L_else (or L_end if no else)
            <then_block_code>
            goto L_end
        L_else:
            <else_block_code>
        L_end:
        """
        # Generate condition code
        condition_temp = self.visit_expression(node.condition)
        
        # Create labels
        if node.else_block:
            else_label = self.new_label()
            end_label = self.new_label()
            
            # If condition is false, jump to else
            self.emit('if_false', condition_temp, None, else_label)
            
            # Then block
            for stmt in node.then_block:
                self.visit_statement(stmt)
            
            # Jump over else block
            self.emit('goto', None, None, end_label)
            
            # Else block
            self.emit('label', None, None, else_label)
            for stmt in node.else_block:
                self.visit_statement(stmt)
            
            # End label
            self.emit('label', None, None, end_label)
        else:
            end_label = self.new_label()
            
            # If condition is false, jump to end
            self.emit('if_false', condition_temp, None, end_label)
            
            # Then block
            for stmt in node.then_block:
                self.visit_statement(stmt)
            
            # End label
            self.emit('label', None, None, end_label)
    
    def visit_while_loop(self, node: WhileLoopNode):
        """
        Visit while loop
        
        Generated code pattern:
        L_start:
            <condition_code>
            if_false <condition_temp> goto L_end
            <body_code>
            goto L_start
        L_end:
        """
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start label
        self.emit('label', None, None, start_label)
        
        # Generate condition code
        condition_temp = self.visit_expression(node.condition)
        
        # If condition is false, jump to end
        self.emit('if_false', condition_temp, None, end_label)
        
        # Loop body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # Jump back to start
        self.emit('goto', None, None, start_label)
        
        # End label
        self.emit('label', None, None, end_label)
    
    def visit_return_statement(self, node: ReturnStatementNode):
        """Visit return statement"""
        # Generate code for return value
        value_temp = self.visit_expression(node.value)
        
        # Return instruction
        self.emit('return', value_temp, None, None)
    
    def visit_print_statement(self, node: PrintStatementNode):
        """Visit print statement"""
        # Generate code for the value to print
        value_temp = self.visit_expression(node.value)
        
        # Print instruction
        self.emit('print', value_temp, None, None)
    
    def visit_function_call_statement(self, node: FunctionCallStatementNode):
        """Visit function call statement"""
        # Generate code for function call (ignore return value)
        self.visit_function_call(node.call)
    
    def visit_expression(self, node: ExpressionNode) -> str:
        """
        Visit expression and return the temporary holding its value
        
        Returns:
            Name of temporary variable holding the result
        """
        if isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.visit_unary_op(node)
        elif isinstance(node, IntegerNode):
            return str(node.value)
        elif isinstance(node, FloatNode):
            return str(node.value)
        elif isinstance(node, StringNode):
            # Escape quotes in string
            return f'"{node.value}"'
        elif isinstance(node, IdentifierNode):
            return node.name
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        else:
            # Unknown expression type
            temp = self.new_temp()
            self.emit('=', '0', None, temp)
            return temp
    
    def visit_binary_op(self, node: BinaryOpNode) -> str:
        """Visit binary operation"""
        # Generate code for left operand
        left_temp = self.visit_expression(node.left)
        
        # Generate code for right operand
        right_temp = self.visit_expression(node.right)
        
        # Generate code for the operation
        result_temp = self.new_temp()
        self.emit(node.operator, left_temp, right_temp, result_temp)
        
        return result_temp
    
    def visit_unary_op(self, node: UnaryOpNode) -> str:
        """Visit unary operation"""
        # Generate code for operand
        operand_temp = self.visit_expression(node.operand)
        
        # Generate code for the operation
        result_temp = self.new_temp()
        self.emit(node.operator, operand_temp, None, result_temp)
        
        return result_temp
    
    def visit_function_call(self, node: FunctionCallNode) -> str:
        """Visit function call"""
        # Generate code for arguments (right to left or left to right)
        for arg in node.arguments:
            arg_temp = self.visit_expression(arg)
            self.emit('param', arg_temp, None, None)
        
        # Generate call instruction
        result_temp = self.new_temp()
        num_args = str(len(node.arguments))
        self.emit('call', node.name, num_args, result_temp)
        
        return result_temp
    
    def print_code(self):
        """Print the generated three-address code"""
        print("\n" + "=" * 60)
        print("THREE-ADDRESS CODE (INTERMEDIATE REPRESENTATION)")
        print("=" * 60)
        for instruction in self.instructions:
            print(instruction)
        print("=" * 60 + "\n")
    
    def get_code_string(self) -> str:
        """Get the generated code as a string"""
        return '\n'.join(str(instr) for instr in self.instructions)


def main():
    """Test the code generator"""
    from lexer import Lexer
    from parser import Parser
    from semantic import SemanticAnalyzer
    
    sample_code = """
    Wake
    
    Hunt add(x, y) {
        Bring x + y
    }
    
    Hunt factorial(n) {
        Purr (n <= 1) {
            Bring 1
        } Hiss {
            Box temp paws n - 1
            Box result paws factorial(temp)
            Bring n * result
        }
    }
    
    Box age paws 5
    Box weight paws 4.5
    Box name paws "Fluffy"
    
    Meow(name)
    
    Purr (age < 10) {
        Meow("Young cat")
        Box sum paws add(age, 3)
        Meow(sum)
    } Hiss {
        Meow("Old cat")
    }
    
    Box counter paws 0
    Chase (counter < 3) {
        Meow(counter)
        counter paws counter + 1
    }
    
    Box fact paws factorial(4)
    Meow(fact)
    
    Sleep
    """
    
    try:
        print("=" * 60)
        print("MEOWSCRIPT COMPILER - COMPLETE PIPELINE")
        print("=" * 60)
        
        # Lexical analysis
        print("\n[1] Lexical Analysis...")
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        print(f"✓ Generated {len(tokens)} tokens")
        
        # Syntax analysis
        print("\n[2] Syntax Analysis...")
        parser = Parser(tokens)
        ast = parser.parse()
        print("✓ AST constructed successfully")
        
        # Semantic analysis
        print("\n[3] Semantic Analysis...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("✓ Semantic checks passed")
        
        # Code generation
        print("\n[4] Code Generation...")
        generator = CodeGenerator()
        tac = generator.generate(ast)
        print(f"✓ Generated {len(tac)} TAC instructions")
        
        # Print results
        generator.print_code()
        
        print("\n" + "=" * 60)
        print("COMPILATION SUCCESSFUL!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nCOMPILATION FAILED:")
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
