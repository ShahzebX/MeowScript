# MeowScript Compiler - Project Report

## Executive Summary

This document provides a comprehensive report on the design and implementation of **MeowScript**, a cat-themed imperative programming language compiler. The project successfully implements all four core phases of compilation: lexical analysis, syntax analysis, semantic analysis, and intermediate code generation.

---

## 1. Language Design

### 1.1 Language Purpose

MeowScript is designed as an educational programming language that:
- Demonstrates all phases of compiler construction
- Provides a memorable, unique syntax through cat-themed keywords
- Supports essential programming constructs (variables, functions, control flow)
- Implements automatic type inference for simplified syntax

### 1.2 Language Features

**Keywords and Syntax:**
- `Wake` / `Sleep` - Program boundaries (cats wake up and sleep)
- `Hunt` - Function definition (cats hunt with purpose)
- `Box` - Variable declaration (cats love boxes for storage)
- `paws` - Assignment operator (cats paw at things to claim them)
- `Purr` / `Hiss` - If/Else conditions (natural cat opposites)
- `Chase` - While loop (cats chase repetitively)
- `Bring` - Return statement (cats bring gifts)
- `Meow` - Print/output (cats meow to communicate)

**Data Types:**
- **Treats** (Integer) - Whole numbers
- **Whiskers** (Float) - Decimal numbers  
- **Yarn** (String) - Text values

**Type Inference:**
Variables automatically get their type from the first assigned value, simplifying syntax while maintaining type safety.

### 1.3 Design Rationale

The cat theme was chosen for:
1. **Uniqueness** - Stands out from typical mini-languages
2. **Memorability** - Easy to remember and explain
3. **Semantic Fit** - Keywords naturally map to programming concepts
4. **Engagement** - Makes learning compiler concepts more enjoyable

---

## 2. Context-Free Grammar

### 2.1 Original Grammar

The initial grammar was designed to capture all language constructs:

```
<program> ::= 'Wake' <statement_list> 'Sleep'
<statement_list> ::= <statement> <statement_list> | ε
<statement> ::= <var_declaration> | <assignment> | <function_def> 
              | <function_call> | <if_statement> | <while_loop>
              | <return_statement> | <print_statement>
<expression> ::= <expression> '+' <term> | <expression> '-' <term> | <term>
<term> ::= <term> '*' <factor> | <term> '/' <factor> | <factor>
...
```

### 2.2 Grammar Issues Identified

1. **Left Recursion** in expression rules
2. **Ambiguity** in expression parsing (precedence unclear)
3. **Left Factoring** needed for if-else statements
4. **Non-determinism** in parameter/argument lists

### 2.3 Grammar Transformations

#### 2.3.1 Ambiguity Removal

**Problem:** Expression `2 + 3 * 4` could be parsed as `(2 + 3) * 4` or `2 + (3 * 4)`

**Solution:** Structured grammar with precedence levels:
```
<expression> ::= <logical_or>
<logical_or> ::= <logical_and> <logical_or_tail>
<logical_and> ::= <equality> <logical_and_tail>
<equality> ::= <comparison> <equality_tail>
<comparison> ::= <addition> <comparison_tail>
<addition> ::= <multiplication> <addition_tail>
<multiplication> ::= <unary> <multiplication_tail>
<unary> ::= '!' <unary> | '-' <unary> | <primary>
```

**Justification:** Each precedence level is a separate non-terminal, ensuring correct parse tree structure.

#### 2.3.2 Left Recursion Elimination

**Original (Left Recursive):**
```
<expression> ::= <expression> '+' <term> | <term>
```

**Transformed (Right Recursive):**
```
<addition> ::= <multiplication> <addition_tail>
<addition_tail> ::= '+' <multiplication> <addition_tail>
                  | '-' <multiplication> <addition_tail>
                  | ε
```

**Justification:** Eliminates left recursion while preserving left-to-right associativity through iterative processing in the parser.

#### 2.3.3 Left Factoring

**Original:**
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}'
                 | 'Purr' '(' <expression> ')' '{' <statement_list> '}' 
                   'Hiss' '{' <statement_list> '}'
```

**Transformed:**
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}' <else_part>
<else_part> ::= 'Hiss' '{' <statement_list> '}' | ε
```

**Justification:** Removes common prefix, making parser decision clear with one-token lookahead.

#### 2.3.4 Non-determinism Removal

**Original:**
```
<param_list> ::= IDENTIFIER ',' <param_list> | IDENTIFIER | ε
```

**Transformed:**
```
<param_list> ::= IDENTIFIER <param_list_tail> | ε
<param_list_tail> ::= ',' IDENTIFIER <param_list_tail> | ε
```

**Justification:** Parser can decide after seeing IDENTIFIER whether to continue, making the grammar LL(1).

### 2.4 Final Grammar Properties

- **Grammar Class:** LL(1)
- **Lookahead:** 1 token
- **Conflicts:** None
- **Parser Type:** Recursive Descent

---

## 3. Lexical Analysis

### 3.1 Implementation Details

**File:** `src/lexer.py`

**Token Categories:**
1. Keywords (10): Wake, Sleep, Hunt, Box, paws, Purr, Hiss, Chase, Bring, Meow
2. Literals: INTEGER, FLOAT, STRING
3. Identifiers: User-defined names
4. Operators (20): Arithmetic, comparison, logical
5. Delimiters (6): Parentheses, braces, comma, semicolon

### 3.2 Key Features

**Regular Expressions:**
- Identifiers: `[a-zA-Z_][a-zA-Z0-9_]*`
- Integers: `[0-9]+`
- Floats: `[0-9]+\.[0-9]+`
- Strings: `"([^"\\]|\\.)*"`

**Error Handling:**
- Line and column tracking for precise error reporting
- Meaningful error messages (e.g., "Unterminated string at line 5, column 12")
- Recovery strategies for continued parsing

**Comment Support:**
- Single-line: `// comment`
- Multi-line: `/* comment */`

### 3.3 Test Results

Successfully tokenizes:
- All keywords and operators
- Integer and float literals (including edge cases)
- String literals with escape sequences
- Comments (single and multi-line)
- Detects lexical errors (invalid characters, unterminated strings)

---

## 4. Parser Implementation

### 4.1 Parser Selection and Justification

**Chosen Parser:** Recursive Descent (LL)

**Justification:**
1. **Grammar Compatibility:** After transformations, grammar is LL(1)
2. **Implementation Simplicity:** Direct mapping from grammar to code
3. **Maintainability:** Easy to understand and debug
4. **Error Recovery:** Custom error messages and panic-mode recovery
5. **Educational Value:** Clear demonstration of parsing concepts
6. **No Tool Dependency:** Hand-written, no external parser generators needed

**Alternatives Considered:**
- Operator Precedence: Insufficient for full language constructs
- LR/LALR: Overkill for this grammar, requires tools
- Table-driven LL: More complex implementation without significant benefit

### 4.2 Implementation Details

**File:** `src/parser.py`

**Parsing Functions:** One function per non-terminal
```python
def parse_expression(self) -> ExpressionNode
def parse_statement(self) -> StatementNode
def parse_if_statement(self) -> IfStatementNode
...
```

**AST Node Types:**
- ProgramNode
- StatementNodes (VarDeclaration, Assignment, FunctionDef, etc.)
- ExpressionNodes (BinaryOp, UnaryOp, Literal, Identifier, etc.)

**Error Recovery:**
- Panic-mode recovery to synchronization tokens
- Continue parsing after errors to find multiple issues
- Clear error messages with line/column information

### 4.3 Test Results

Successfully parses:
- Variable declarations and assignments
- Function definitions with parameters
- If-else statements (including nested)
- While loops
- Complex expressions with correct precedence
- Function calls with multiple arguments
- Detects syntax errors with helpful messages

---

## 5. Semantic Analysis

### 5.1 Symbol Table Design

**File:** `src/semantic.py`

**Structure:**
- Stack of scopes (list of dictionaries)
- Symbol entries contain:
  - Name
  - Data type
  - Scope level
  - Function flag
  - Parameters (for functions)
  - Line/column (for error reporting)

**Operations:**
- `declare()` - Add symbol to current scope
- `lookup()` - Search current and enclosing scopes
- `enter_scope()` / `exit_scope()` - Manage scope stack

### 5.2 Type System

**Type Inference:**
Variables get their type from first assignment:
```meowscript
Box x paws 42        // x is Treats (int)
Box y paws 3.14      // y is Whiskers (float)
Box s paws "cat"     // s is Yarn (string)
```

**Type Rules:**
- Arithmetic: Treats op Treats → Treats, Whiskers op Whiskers → Whiskers
- Mixed numeric: Treats op Whiskers → Whiskers (promotion)
- String concatenation: Yarn + (Treats|Whiskers|Yarn) → Yarn
- Comparison: Same types → Boolean (represented as Treats)
- Logical: Any type → Boolean

### 5.3 Semantic Checks

**Implemented Checks:**
1. Variable declaration before use
2. No redeclaration in same scope
3. Type compatibility in operations
4. Type consistency in assignments
5. Function existence before call
6. Argument count matches parameters
7. Return statements only in functions
8. Cannot assign to functions

### 5.4 Test Results

Successfully detects:
- Undeclared variables
- Variable redeclarations
- Type mismatches
- Wrong argument counts
- Invalid operations
- All test cases pass semantic validation

---

## 6. Intermediate Code Generation

### 6.1 Three-Address Code Design

**File:** `src/codegen.py`

**TAC Instruction Format:**
```
result = arg1 op arg2
```

**Instruction Types:**
- Assignment: `x = y`
- Binary operation: `t1 = x + y`
- Unary operation: `t2 = -x`
- Label: `L0:`
- Conditional jump: `if_false t1 goto L1`
- Unconditional jump: `goto L2`
- Function call: `t3 = call func, 2`
- Parameter passing: `param x`
- Return: `return t4`
- Print: `print x`

### 6.2 Translation Schemes

**Expressions:**
```
E → E1 + E2
    code(E1)
    code(E2)
    t = newtemp()
    emit(t = E1.addr + E2.addr)
    E.addr = t
```

**If Statement:**
```
S → if (B) S1 else S2
    L_else = newlabel()
    L_end = newlabel()
    code(B)
    emit(if_false B.addr goto L_else)
    code(S1)
    emit(goto L_end)
    emit(L_else:)
    code(S2)
    emit(L_end:)
```

**While Loop:**
```
S → while (B) S1
    L_start = newlabel()
    L_end = newlabel()
    emit(L_start:)
    code(B)
    emit(if_false B.addr goto L_end)
    code(S1)
    emit(goto L_start)
    emit(L_end:)
```

### 6.3 Example Transformations

**Input:**
```meowscript
Box x paws 5 + 3 * 2
```

**Generated TAC:**
```
t0 = 3 * 2
t1 = 5 + t0
x = t1
```

**Input:**
```meowscript
Purr (age < 5) {
    Meow("Young")
} Hiss {
    Meow("Old")
}
```

**Generated TAC:**
```
t0 = age < 5
if_false t0 goto L0
print "Young"
goto L1
L0:
print "Old"
L1:
```

### 6.4 Test Results

Successfully generates TAC for:
- Simple and complex expressions
- If-else statements
- While loops
- Function definitions and calls
- Recursive functions
- Proper temporary and label management

---

## 7. Testing and Validation

### 7.1 Test Suite

**File:** `tests/test_compiler.py`

**Test Coverage:**
- Lexical Analysis: 7 tests
- Syntax Analysis: 7 tests
- Semantic Analysis: 5 tests
- Code Generation: 4 tests
- Integration: 4 complete programs

**Total:** 27 tests covering all compiler phases

### 7.2 Test Results

```
OVERALL TEST SUMMARY
==================================================================
Total Tests: 27
Passed: 27 (100%)
Failed: 0
==================================================================

✓ ALL TESTS PASSED! 🐱
```

### 7.3 Example Programs

Seven complete example programs demonstrate:
1. Arithmetic operations
2. Function definitions and calls
3. Conditional statements
4. Loop constructs
5. Complete integrated program (cat health tracker)
6. Recursive functions (factorial, fibonacci)
7. Complex expressions and string operations

---

## 8. Project Statistics

**Lines of Code:**
- Lexer: ~400 lines
- Parser: ~650 lines
- Semantic Analyzer: ~500 lines
- Code Generator: ~400 lines
- Total Core: ~1,950 lines

**Documentation:**
- Language Specification: ~500 lines
- Grammar Documentation: ~400 lines
- README: ~850 lines
- Total Docs: ~1,750 lines

**Test Code:**
- Comprehensive test suite: ~500 lines
- Example programs: ~250 lines

**Files:**
- Source files: 5
- Documentation files: 4
- Example programs: 7
- Test files: 1

---

## 9. Challenges and Solutions

### 9.1 Challenge: Left Recursion in Expression Grammar

**Problem:** Direct left recursion incompatible with recursive descent parsing

**Solution:** Applied standard left recursion elimination algorithm, creating tail non-terminals for iterative processing

### 9.2 Challenge: Operator Precedence

**Problem:** Ensuring correct precedence without ambiguity

**Solution:** Layered expression grammar with separate non-terminals for each precedence level

### 9.3 Challenge: Type Inference

**Problem:** Determining types without explicit declarations

**Solution:** First-use type assignment with subsequent consistency checking

### 9.4 Challenge: Error Recovery

**Problem:** Stopping at first error vs. finding multiple errors

**Solution:** Implemented panic-mode recovery with synchronization tokens

---

## 10. Conclusions

### 10.1 Project Success

The MeowScript compiler successfully demonstrates all required compiler phases:
- ✅ Complete lexical analyzer with error handling
- ✅ Recursive descent parser with LL(1) grammar
- ✅ Semantic analyzer with symbol table and type checking
- ✅ Three-address code generator with proper TAC
- ✅ Comprehensive test suite (100% pass rate)
- ✅ Extensive documentation and examples

### 10.2 Learning Outcomes

Key concepts mastered:
1. Grammar design and transformation
2. Tokenization and lexical analysis
3. Recursive descent parsing
4. Symbol table management
5. Type inference and checking
6. Intermediate code generation
7. Error handling and recovery

### 10.3 Unique Contributions

- Novel cat-themed language design
- Complete working implementation
- Extensive documentation
- 27 comprehensive tests
- 7 example programs
- Clear code structure for educational use

### 10.4 Future Enhancements

Potential extensions:
- Arrays/collections (Basket type)
- For loops (Prowl keyword)
- Classes/objects (Cat definitions)
- Optimization passes on TAC
- Target code generation (x86, LLVM, etc.)
- Runtime interpreter

---

## 11. References

### 11.1 Textbook References

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.

### 11.2 Grammar Transformation Techniques

- Left recursion elimination (Section 4.3)
- Left factoring (Section 4.3.2)
- First and Follow sets (Section 4.4)

### 11.3 Code Generation

- Three-address code format (Section 6.2)
- Syntax-directed translation (Chapter 5)
- Control flow translation (Section 6.6)

---

## 12. Appendices

### Appendix A: Complete Token List

See `src/lexer.py` - TokenType enum (34 token types)

### Appendix B: Complete Grammar

See `docs/grammar.md` - Full transformed grammar

### Appendix C: AST Node Definitions

See `src/parser.py` - 16 AST node classes

### Appendix D: Example Programs

See `examples/` directory - 7 complete programs

### Appendix E: Test Suite

See `tests/test_compiler.py` - 27 comprehensive tests

---

## Report Metadata

**Project Title:** MeowScript Compiler
**Language:** Python 3.7+
**Total Development Time:** ~2 days
**Lines of Code:** ~2,000 (core) + ~2,250 (docs/tests)
**Test Coverage:** 100% (27/27 tests passed)
**Documentation:** Complete

---

**End of Report**
