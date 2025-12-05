"""
Test Suite for MeowScript Compiler

Run with: python test_compiler.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from codegen import CodeGenerator


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"  ✓ {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ✗ {test_name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        print("=" * 70)
        if self.errors:
            print("\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")


def test_lexer():
    """Test lexical analyzer"""
    print("\n" + "=" * 70)
    print("TESTING LEXICAL ANALYZER")
    print("=" * 70)
    
    result = TestResult()
    
    # Test 1: Basic tokens
    try:
        code = "Wake Box x paws 10 Sleep"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len(tokens) == 7  # Including EOF
        result.add_pass("Basic tokens")
    except Exception as e:
        result.add_fail("Basic tokens", str(e))
    
    # Test 2: Keywords
    try:
        code = "Wake Hunt Purr Hiss Chase Bring Meow Sleep"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        result.add_pass("All keywords")
    except Exception as e:
        result.add_fail("All keywords", str(e))
    
    # Test 3: Numbers
    try:
        code = "42 3.14 0 100.5"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].value == 42
        assert tokens[1].value == 3.14
        result.add_pass("Integer and float literals")
    except Exception as e:
        result.add_fail("Integer and float literals", str(e))
    
    # Test 4: Strings
    try:
        code = '"Hello" "World" "Cat says: Meow!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].value == "Hello"
        assert tokens[1].value == "World"
        result.add_pass("String literals")
    except Exception as e:
        result.add_fail("String literals", str(e))
    
    # Test 5: Operators
    try:
        code = "+ - * / % == != < > <= >= && || !"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len(tokens) == 15  # 14 operators + EOF
        result.add_pass("All operators")
    except Exception as e:
        result.add_fail("All operators", str(e))
    
    # Test 6: Comments
    try:
        code = """
        // Single line comment
        Box x paws 10
        /* Multi-line
           comment */
        Box y paws 20
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        result.add_pass("Comments (single and multi-line)")
    except Exception as e:
        result.add_fail("Comments", str(e))
    
    # Test 7: Error - unterminated string
    try:
        code = '"Hello'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        result.add_fail("Unterminated string detection", "Should have raised LexerError")
    except LexerError:
        result.add_pass("Unterminated string detection")
    except Exception as e:
        result.add_fail("Unterminated string detection", str(e))
    
    result.summary()
    return result


def test_parser():
    """Test parser"""
    print("\n" + "=" * 70)
    print("TESTING PARSER")
    print("=" * 70)
    
    result = TestResult()
    
    # Test 1: Variable declaration
    try:
        code = "Wake Box x paws 10 Sleep"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("Variable declaration")
    except Exception as e:
        result.add_fail("Variable declaration", str(e))
    
    # Test 2: Function definition
    try:
        code = """
        Wake
        Hunt add(x, y) {
            Bring x + y
        }
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("Function definition")
    except Exception as e:
        result.add_fail("Function definition", str(e))
    
    # Test 3: If statement
    try:
        code = """
        Wake
        Purr (x < 5) {
            Meow("Small")
        } Hiss {
            Meow("Large")
        }
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("If-else statement")
    except Exception as e:
        result.add_fail("If-else statement", str(e))
    
    # Test 4: While loop
    try:
        code = """
        Wake
        Chase (x < 10) {
            x paws x + 1
        }
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("While loop")
    except Exception as e:
        result.add_fail("While loop", str(e))
    
    # Test 5: Complex expressions
    try:
        code = """
        Wake
        Box result paws (x + y) * z - w / 2
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("Complex expressions")
    except Exception as e:
        result.add_fail("Complex expressions", str(e))
    
    # Test 6: Function calls
    try:
        code = """
        Wake
        Box result paws add(10, 20)
        greet("Fluffy")
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_pass("Function calls")
    except Exception as e:
        result.add_fail("Function calls", str(e))
    
    # Test 7: Error - missing Sleep
    try:
        code = "Wake Box x paws 10"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result.add_fail("Missing Sleep detection", "Should have raised ParserError")
    except ParserError:
        result.add_pass("Missing Sleep detection")
    except Exception as e:
        result.add_fail("Missing Sleep detection", str(e))
    
    result.summary()
    return result


def test_semantic():
    """Test semantic analyzer"""
    print("\n" + "=" * 70)
    print("TESTING SEMANTIC ANALYZER")
    print("=" * 70)
    
    result = TestResult()
    
    # Test 1: Valid program
    try:
        code = """
        Wake
        Box x paws 10
        Box y paws 20
        Box sum paws x + y
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result.add_pass("Valid program")
    except Exception as e:
        result.add_fail("Valid program", str(e))
    
    # Test 2: Function with return
    try:
        code = """
        Wake
        Hunt add(x, y) {
            Bring x + y
        }
        Box result paws add(5, 3)
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result.add_pass("Function with return")
    except Exception as e:
        result.add_fail("Function with return", str(e))
    
    # Test 3: Type inference
    try:
        code = """
        Wake
        Box x paws 42
        Box y paws 3.14
        Box s paws "Hello"
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result.add_pass("Type inference")
    except Exception as e:
        result.add_fail("Type inference", str(e))
    
    # Test 4: Error - undeclared variable
    try:
        code = """
        Wake
        Box x paws undefined_var + 10
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result.add_fail("Undeclared variable detection", "Should have raised SemanticError")
    except SemanticError:
        result.add_pass("Undeclared variable detection")
    except Exception as e:
        result.add_fail("Undeclared variable detection", str(e))
    
    # Test 5: Error - redeclaration
    try:
        code = """
        Wake
        Box x paws 10
        Box x paws 20
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result.add_fail("Redeclaration detection", "Should have raised SemanticError")
    except SemanticError:
        result.add_pass("Redeclaration detection")
    except Exception as e:
        result.add_fail("Redeclaration detection", str(e))
    
    result.summary()
    return result


def test_codegen():
    """Test code generator"""
    print("\n" + "=" * 70)
    print("TESTING CODE GENERATOR")
    print("=" * 70)
    
    result = TestResult()
    
    # Test 1: Simple expression
    try:
        code = """
        Wake
        Box x paws 10 + 20
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        generator = CodeGenerator()
        tac = generator.generate(ast)
        assert len(tac) > 0
        result.add_pass("Simple expression TAC")
    except Exception as e:
        result.add_fail("Simple expression TAC", str(e))
    
    # Test 2: If statement
    try:
        code = """
        Wake
        Purr (x < 5) {
            Meow("Small")
        }
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CodeGenerator()
        tac = generator.generate(ast)
        # Check for if_false and label instructions
        ops = [instr.operation for instr in tac]
        assert 'if_false' in ops and 'label' in ops
        result.add_pass("If statement TAC")
    except Exception as e:
        result.add_fail("If statement TAC", str(e))
    
    # Test 3: While loop
    try:
        code = """
        Wake
        Chase (x < 10) {
            x paws x + 1
        }
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CodeGenerator()
        tac = generator.generate(ast)
        # Check for goto and label instructions
        ops = [instr.operation for instr in tac]
        assert 'goto' in ops and 'label' in ops
        result.add_pass("While loop TAC")
    except Exception as e:
        result.add_fail("While loop TAC", str(e))
    
    # Test 4: Function definition and call
    try:
        code = """
        Wake
        Hunt add(x, y) {
            Bring x + y
        }
        Box result paws add(5, 3)
        Sleep
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        generator = CodeGenerator()
        tac = generator.generate(ast)
        ops = [instr.operation for instr in tac]
        assert 'begin_func' in ops and 'call' in ops and 'param' in ops
        result.add_pass("Function TAC")
    except Exception as e:
        result.add_fail("Function TAC", str(e))
    
    result.summary()
    return result


def test_integration():
    """Integration tests - full compilation pipeline"""
    print("\n" + "=" * 70)
    print("INTEGRATION TESTS - FULL PIPELINE")
    print("=" * 70)
    
    result = TestResult()
    
    # Test complete programs from examples
    test_files = [
        ("Arithmetic", """
        Wake
        Box x paws 10
        Box y paws 20
        Box sum paws x + y
        Meow(sum)
        Sleep
        """),
        
        ("Functions", """
        Wake
        Hunt add(a, b) {
            Bring a + b
        }
        Box result paws add(5, 3)
        Meow(result)
        Sleep
        """),
        
        ("Conditionals", """
        Wake
        Box age paws 3
        Purr (age < 5) {
            Meow("Young")
        } Hiss {
            Meow("Old")
        }
        Sleep
        """),
        
        ("Loops", """
        Wake
        Box i paws 0
        Chase (i < 5) {
            Meow(i)
            i paws i + 1
        }
        Sleep
        """),
    ]
    
    for name, code in test_files:
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            generator = CodeGenerator()
            tac = generator.generate(ast)
            assert len(tac) > 0
            result.add_pass(f"Complete: {name}")
        except Exception as e:
            result.add_fail(f"Complete: {name}", str(e))
    
    result.summary()
    return result


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 20 + "MEOWSCRIPT COMPILER TEST SUITE")
    print("=" * 70)
    
    results = []
    results.append(test_lexer())
    results.append(test_parser())
    results.append(test_semantic())
    results.append(test_codegen())
    results.append(test_integration())
    
    # Overall summary
    total_passed = sum(r.passed for r in results)
    total_failed = sum(r.failed for r in results)
    total_tests = total_passed + total_failed
    
    print("\n" + "=" * 70)
    print("OVERALL TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed} ({100*total_passed//total_tests if total_tests > 0 else 0}%)")
    print(f"Failed: {total_failed}")
    print("=" * 70)
    
    if total_failed == 0:
        print("\n✓ ALL TESTS PASSED! 🐱")
    else:
        print(f"\n✗ {total_failed} test(s) failed")
    
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
