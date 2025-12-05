"""
MeowScript Compiler - Main Driver

This is the main entry point for the MeowScript compiler.
It orchestrates all compilation phases: lexing, parsing, semantic analysis, and code generation.
"""

import sys
import argparse
from pathlib import Path
from lexer import Lexer, LexerError
from parser import Parser, ParserError, print_ast
from semantic import SemanticAnalyzer, SemanticError
from codegen import CodeGenerator


class MeowScriptCompiler:
    """Main compiler driver for MeowScript"""
    
    def __init__(self, source_code: str, verbose: bool = False):
        """
        Initialize the compiler
        
        Args:
            source_code: MeowScript source code
            verbose: Print detailed information during compilation
        """
        self.source_code = source_code
        self.verbose = verbose
        self.tokens = None
        self.ast = None
        self.tac = None
        
    def compile(self) -> bool:
        """
        Run the complete compilation pipeline
        
        Returns:
            True if compilation succeeded, False otherwise
        """
        try:
            if self.verbose:
                print("\n" + "=" * 70)
                print(" " * 20 + "MEOWSCRIPT COMPILER")
                print("=" * 70)
            
            # Phase 1: Lexical Analysis
            if not self.lexical_analysis():
                return False
            
            # Phase 2: Syntax Analysis
            if not self.syntax_analysis():
                return False
            
            # Phase 3: Semantic Analysis
            if not self.semantic_analysis():
                return False
            
            # Phase 4: Code Generation
            if not self.code_generation():
                return False
            
            if self.verbose:
                print("\n" + "=" * 70)
                print(" " * 25 + "✓ COMPILATION SUCCESSFUL!")
                print("=" * 70 + "\n")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\nCompilation interrupted by user.")
            return False
        except Exception as e:
            print(f"\n\nUNEXPECTED ERROR: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def lexical_analysis(self) -> bool:
        """
        Phase 1: Lexical Analysis
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print("\n[Phase 1] Lexical Analysis")
                print("-" * 70)
            
            lexer = Lexer(self.source_code)
            self.tokens = lexer.tokenize()
            
            if self.verbose:
                print(f"✓ Successfully tokenized: {len(self.tokens)} tokens")
                
                # Print token summary
                token_types = {}
                for token in self.tokens:
                    token_type = token.type.name
                    token_types[token_type] = token_types.get(token_type, 0) + 1
                
                print("\nToken Summary:")
                for token_type, count in sorted(token_types.items()):
                    print(f"  {token_type}: {count}")
            
            return True
            
        except LexerError as e:
            print(f"\n✗ LEXICAL ERROR: {e}")
            return False
    
    def syntax_analysis(self) -> bool:
        """
        Phase 2: Syntax Analysis
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print("\n[Phase 2] Syntax Analysis")
                print("-" * 70)
            
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            if self.verbose:
                print("✓ Successfully parsed: AST constructed")
                print("\nAbstract Syntax Tree:")
                print_ast(self.ast)
            
            return True
            
        except ParserError as e:
            print(f"\n✗ SYNTAX ERROR: {e}")
            return False
    
    def semantic_analysis(self) -> bool:
        """
        Phase 3: Semantic Analysis
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print("\n[Phase 3] Semantic Analysis")
                print("-" * 70)
            
            analyzer = SemanticAnalyzer()
            analyzer.analyze(self.ast)
            
            if self.verbose:
                print("✓ Semantic analysis passed")
            
            return True
            
        except SemanticError as e:
            print(f"\n✗ SEMANTIC ERROR: {e}")
            return False
    
    def code_generation(self) -> bool:
        """
        Phase 4: Code Generation
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.verbose:
                print("\n[Phase 4] Code Generation")
                print("-" * 70)
            
            generator = CodeGenerator()
            self.tac = generator.generate(self.ast)
            
            if self.verbose:
                print(f"✓ Generated {len(self.tac)} TAC instructions")
                generator.print_code()
            
            return True
            
        except Exception as e:
            print(f"\n✗ CODE GENERATION ERROR: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False
    
    def get_intermediate_code(self) -> str:
        """
        Get the generated intermediate code as a string
        
        Returns:
            Three-address code as string
        """
        if self.tac:
            return '\n'.join(str(instr) for instr in self.tac)
        return ""
    
    def save_intermediate_code(self, output_file: str):
        """
        Save intermediate code to a file
        
        Args:
            output_file: Path to output file
        """
        if self.tac:
            with open(output_file, 'w') as f:
                f.write(self.get_intermediate_code())
            print(f"Intermediate code saved to: {output_file}")


def main():
    """Main entry point for the compiler"""
    parser = argparse.ArgumentParser(
        description='MeowScript Compiler - A cat-themed programming language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile a MeowScript file
  python main.py program.meow
  
  # Compile with verbose output
  python main.py program.meow -v
  
  # Save intermediate code to file
  python main.py program.meow -o output.tac
  
  # Show only intermediate code
  python main.py program.meow --tac-only
        """
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help='MeowScript source file (.meow)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output (show all compilation phases)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file for intermediate code (.tac)'
    )
    
    parser.add_argument(
        '--tac-only',
        action='store_true',
        help='Only print the three-address code (no other output)'
    )
    
    parser.add_argument(
        '--ast',
        action='store_true',
        help='Print the Abstract Syntax Tree'
    )
    
    args = parser.parse_args()
    
    # Read input file
    try:
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: File '{args.input_file}' not found.")
            sys.exit(1)
        
        source_code = input_path.read_text()
        
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Compile
    compiler = MeowScriptCompiler(source_code, verbose=args.verbose and not args.tac_only)
    success = compiler.compile()
    
    if not success:
        sys.exit(1)
    
    # Output results
    if args.tac_only:
        print(compiler.get_intermediate_code())
    
    if args.ast and compiler.ast:
        print("\n" + "=" * 70)
        print("ABSTRACT SYNTAX TREE")
        print("=" * 70)
        print_ast(compiler.ast)
        print("=" * 70)
    
    if args.output:
        compiler.save_intermediate_code(args.output)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
