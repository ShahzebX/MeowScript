# MeowScript Compiler 🐱

A cat-themed imperative programming language compiler implementation for the Compiler Construction course project.

## Table of Contents
- [Overview](#overview)
- [Language Features](#language-features)
- [Installation](#installation)
- [Usage](#usage)
- [Language Syntax](#language-syntax)
- [Project Structure](#project-structure)
- [Compiler Phases](#compiler-phases)
- [Examples](#examples)
- [Testing](#testing)
- [Documentation](#documentation)

## Overview

**MeowScript** is a unique, cat-themed programming language designed to demonstrate all phases of compiler construction:
- Lexical Analysis (Tokenization)
- Syntax Analysis (Parsing with Recursive Descent)
- Semantic Analysis (Type Checking, Symbol Tables)
- Intermediate Code Generation (Three-Address Code)

### Why MeowScript?

- **Unique & Memorable**: Cat-themed keywords make the language stand out
- **Educational**: Demonstrates all core compiler concepts
- **Complete**: Supports functions, control flow, expressions, and type inference
- **Well-Documented**: Extensive documentation of grammar transformations and design decisions

## Language Features

### Keywords
- `Wake` / `Sleep` - Program start and end markers
- `Hunt` - Function definition
- `Box` - Variable declaration
- `paws` - Assignment operator
- `Purr` / `Hiss` - If / Else conditional
- `Chase` - While loop
- `Bring` - Return statement
- `Meow` - Print/output function

### Data Types (with automatic inference)
- **Treats** - Integers (e.g., `42`, `-10`)
- **Whiskers** - Floats (e.g., `3.14`, `2.5`)
- **Yarn** - Strings (e.g., `"Hello"`, `"Fluffy"`)

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`

### Sample Program

```meowscript
Wake

Hunt greet(name) {
    Meow("Hello, ")
    Meow(name)
    Bring "Done"
}

Box age paws 3
Box name paws "Fluffy"

Purr (age < 5) {
    Meow("Kitten!")
} Hiss {
    Meow("Adult cat")
}

Box counter paws 0
Chase (counter < 5) {
    Meow(counter)
    counter paws counter + 1
}

greet(name)

Sleep
```

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup
```bash
# Clone or download the project
cd "Compiler Construction/Project"

# No additional dependencies required!
# The compiler is written in pure Python
```

## Usage

### Basic Compilation

```bash
# Compile a MeowScript file
python src/main.py examples/01_arithmetic.meow

# Verbose output (shows all compilation phases)
python src/main.py examples/01_arithmetic.meow -v

# Save intermediate code to file
python src/main.py examples/02_functions.meow -o output.tac

# Show only TAC output
python src/main.py examples/03_conditionals.meow --tac-only

# Show Abstract Syntax Tree
python src/main.py examples/04_loops.meow --ast
```

### Running Tests

```bash
# Run the complete test suite
python tests/test_compiler.py
```

### Example Output

```
==================================================================
                  MEOWSCRIPT COMPILER
==================================================================

[Phase 1] Lexical Analysis
----------------------------------------------------------------------
✓ Successfully tokenized: 45 tokens

[Phase 2] Syntax Analysis
----------------------------------------------------------------------
✓ Successfully parsed: AST constructed

[Phase 3] Semantic Analysis
----------------------------------------------------------------------
✓ Semantic analysis passed

[Phase 4] Code Generation
----------------------------------------------------------------------
✓ Generated 28 TAC instructions

============================================================
THREE-ADDRESS CODE (INTERMEDIATE REPRESENTATION)
============================================================
    t0 = 10
    x = t0
    t1 = 20
    y = t1
    t2 = x + y
    sum = t2
    print sum
============================================================

==================================================================
                     ✓ COMPILATION SUCCESSFUL!
==================================================================
```

## Language Syntax

### Variable Declaration
```meowscript
Box variable_name paws value
```

### Assignment
```meowscript
variable_name paws new_value
```

### Function Definition
```meowscript
Hunt function_name(param1, param2) {
    // Function body
    Bring return_value
}
```

### Function Call
```meowscript
function_name(arg1, arg2)
Box result paws function_name(arg1, arg2)
```

### Conditional Statement
```meowscript
Purr (condition) {
    // If block
} Hiss {
    // Else block (optional)
}
```

### While Loop
```meowscript
Chase (condition) {
    // Loop body
}
```

### Print Statement
```meowscript
Meow(expression)
```

### Comments
```meowscript
// Single-line comment

/*
   Multi-line
   comment
*/
```

## Project Structure

```
Project/
├── src/
│   ├── lexer.py          # Lexical analyzer
│   ├── parser.py         # Syntax analyzer (Recursive Descent)
│   ├── semantic.py       # Semantic analyzer & symbol table
│   ├── codegen.py        # Intermediate code generator (TAC)
│   └── main.py           # Main compiler driver
├── docs/
│   ├── language_specification.md   # Complete language spec
│   └── grammar.md                  # CFG with transformations
├── examples/
│   ├── 01_arithmetic.meow
│   ├── 02_functions.meow
│   ├── 03_conditionals.meow
│   ├── 04_loops.meow
│   ├── 05_complete_program.meow
│   ├── 06_recursion.meow
│   └── 07_expressions.meow
├── tests/
│   └── test_compiler.py  # Comprehensive test suite
└── README.md
```

## Compiler Phases

### 1. Lexical Analysis (`lexer.py`)

**Purpose**: Convert source code into tokens

**Features**:
- Token identification (keywords, identifiers, literals, operators)
- Comment removal (single-line `//` and multi-line `/* */`)
- String escape sequence handling (`\n`, `\t`, `\"`, `\\`)
- Line and column tracking for error reporting
- Comprehensive error messages

**Token Types**:
- Keywords: WAKE, SLEEP, HUNT, BOX, PAWS, PURR, HISS, CHASE, BRING, MEOW
- Literals: INTEGER, FLOAT, STRING
- Identifiers: IDENTIFIER
- Operators: PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, EQUAL, NOT_EQUAL, etc.
- Delimiters: LPAREN, RPAREN, LBRACE, RBRACE, COMMA, SEMICOLON

### 2. Syntax Analysis (`parser.py`)

**Purpose**: Build Abstract Syntax Tree (AST) from token stream

**Parser Type**: Recursive Descent (LL(1))

**Features**:
- Grammar-driven parsing with one-token lookahead
- AST construction for all language constructs
- Syntax error detection and reporting
- Panic-mode error recovery
- Support for:
  - Variable declarations and assignments
  - Function definitions and calls
  - Control structures (if-else, while)
  - Complex expressions with correct precedence

**Operator Precedence** (Highest to Lowest):
1. Parentheses `( )`
2. Unary operators: `!`, `-`
3. Multiplicative: `*`, `/`, `%`
4. Additive: `+`, `-`
5. Comparison: `<`, `>`, `<=`, `>=`
6. Equality: `==`, `!=`
7. Logical AND: `&&`
8. Logical OR: `||`

### 3. Semantic Analysis (`semantic.py`)

**Purpose**: Check program semantics and build symbol table

**Features**:
- **Symbol Table Management**:
  - Scope tracking (global and local)
  - Variable and function declarations
  - Symbol lookup with scope resolution
  
- **Type System**:
  - Automatic type inference from assignments
  - Type checking for operations
  - Type compatibility verification
  - Support for numeric type promotion (Treats ↔ Whiskers)
  - String concatenation with `+` operator

- **Semantic Error Detection**:
  - Undeclared variables
  - Variable redeclaration in same scope
  - Type mismatches
  - Function argument count validation
  - Return statement validation
  - Invalid operations on types

### 4. Code Generation (`codegen.py`)

**Purpose**: Generate Three-Address Code (TAC) intermediate representation

**Features**:
- **TAC Instructions**:
  - Assignments: `x = y`
  - Binary operations: `t1 = x + y`
  - Unary operations: `t2 = -x`
  - Labels: `L0:`
  - Conditional jumps: `if_false t1 goto L1`
  - Unconditional jumps: `goto L2`
  - Function calls: `t3 = call func, 2`
  - Parameters: `param x`
  - Return: `return t4`
  - Print: `print x`

- **Optimizations Ready**:
  - Temporaries for subexpressions
  - Structured control flow with labels
  - Function calling conventions

**Translation Schemes**:
- Expressions → Temporary variables with operations
- If-Else → Conditional jumps with labels
- While loops → Label-based loop structure
- Functions → Function prologue/epilogue with parameters

## Examples

### Example 1: Arithmetic Operations
```meowscript
Wake
Box x paws 10
Box y paws 20
Box sum paws x + y
Meow(sum)
Sleep
```

**Generated TAC**:
```
    t0 = 10
    x = t0
    t1 = 20
    y = t1
    t2 = x + y
    sum = t2
    print sum
```

### Example 2: Functions
```meowscript
Wake

Hunt add(a, b) {
    Bring a + b
}

Box result paws add(5, 3)
Meow(result)

Sleep
```

**Generated TAC**:
```
add:
    t0 = a + b
    return t0
    end_func add
    param 5
    param 3
    t1 = call add, 2
    result = t1
    print result
```

### Example 3: Conditionals
```meowscript
Wake

Box age paws 3

Purr (age < 5) {
    Meow("Kitten")
} Hiss {
    Meow("Adult")
}

Sleep
```

**Generated TAC**:
```
    t0 = 3
    age = t0
    t1 = age < 5
    if_false t1 goto L0
    print "Kitten"
    goto L1
L0:
    print "Adult"
L1:
```

### Example 4: Loops
```meowscript
Wake

Box counter paws 0
Chase (counter < 5) {
    Meow(counter)
    counter paws counter + 1
}

Sleep
```

**Generated TAC**:
```
    t0 = 0
    counter = t0
L0:
    t1 = counter < 5
    if_false t1 goto L1
    print counter
    t2 = counter + 1
    counter = t2
    goto L0
L1:
```

## Testing

The test suite (`tests/test_compiler.py`) includes:

### Test Categories

1. **Lexer Tests**:
   - Basic token recognition
   - Keywords and operators
   - Literals (integers, floats, strings)
   - Comments (single and multi-line)
   - Error detection (unterminated strings, invalid characters)

2. **Parser Tests**:
   - Variable declarations
   - Function definitions
   - Control structures (if-else, while)
   - Complex expressions
   - Error detection (syntax errors)

3. **Semantic Tests**:
   - Type inference
   - Symbol table operations
   - Scope handling
   - Error detection (undeclared variables, redeclarations, type mismatches)

4. **Code Generator Tests**:
   - Expression TAC generation
   - Control flow TAC (if, while)
   - Function TAC (definition, calls)
   - Temporary and label management

5. **Integration Tests**:
   - Complete compilation pipeline
   - Real-world program examples

### Running Tests

```bash
python tests/test_compiler.py
```

**Expected Output**:
```
==================================================================
              MEOWSCRIPT COMPILER TEST SUITE
==================================================================

==================================================================
TESTING LEXICAL ANALYZER
==================================================================
  ✓ Basic tokens
  ✓ All keywords
  ✓ Integer and float literals
  ✓ String literals
  ✓ All operators
  ✓ Comments (single and multi-line)
  ✓ Unterminated string detection

==================================================================
TEST SUMMARY: 7/7 passed
==================================================================

[... more test results ...]

==================================================================
OVERALL TEST SUMMARY
==================================================================
Total Tests: 35
Passed: 35 (100%)
Failed: 0
==================================================================

✓ ALL TESTS PASSED! 🐱
```

## Documentation

### Complete Documentation Files

1. **`docs/language_specification.md`**:
   - Complete language specification
   - Lexical elements (keywords, operators, literals)
   - Syntax and grammar rules
   - Type system and inference rules
   - Scoping rules
   - Complete examples

2. **`docs/grammar.md`**:
   - Original context-free grammar
   - Grammar transformations:
     - Ambiguity removal
     - Left recursion elimination
     - Left factoring
     - Non-determinism removal
   - Final transformed grammar (LL(1))
   - Parser selection justification
   - FIRST and FOLLOW sets
   - Example parse trees

### Grammar Transformations

The grammar underwent these mandatory transformations:

1. **Ambiguity Removal**: Expression grammar structured with precedence levels
2. **Left Recursion Elimination**: Converted left-recursive rules to right-recursive
3. **Left Factoring**: Factored common prefixes (e.g., if-else statements)
4. **Non-determinism Removal**: Restructured parameter/argument lists for LL(1) parsing

### Parser Justification

**Chosen Parser**: Recursive Descent (LL(1))

**Justification**:
- Grammar is LL(1) compatible after transformations
- One-token lookahead sufficient for all parsing decisions
- Easy to implement and maintain
- Direct mapping from grammar to code
- Excellent for educational purposes
- Good error recovery capabilities
- No tool dependencies

## Error Handling

### Lexical Errors
- Invalid characters
- Unterminated strings
- Malformed numbers
- Unterminated multi-line comments

**Example**:
```
Lexical Error at line 5, column 12: Unexpected character: '@'
```

### Syntax Errors
- Missing `Wake` or `Sleep`
- Mismatched parentheses/braces
- Invalid statement structure
- Unexpected tokens

**Example**:
```
Syntax Error at line 8, column 5: Expected RPAREN, got RBRACE
```

### Semantic Errors
- Undeclared variables
- Variable redeclaration
- Type mismatches
- Wrong argument count in function calls
- Return outside function

**Example**:
```
Semantic Error at line 10, column 8: Undeclared variable 'undefined_var'
```

## Design Rationale

### Why Cat Theme?

1. **Memorability**: Unique theme makes the language unforgettable
2. **Engagement**: Fun keywords make programming enjoyable
3. **Semantic Fit**: Keywords naturally map to concepts:
   - `Hunt` = Functions hunt for results
   - `Chase` = Loops chase/repeat
   - `Box` = Variables stored in boxes (cats love boxes!)
   - `paws` = Cats paw at things to claim them
   - `Purr`/`Hiss` = Natural opposites for if/else

### Type Inference Benefits

- Simplified syntax (no explicit type declarations)
- Maintained type safety through inference
- Natural feel similar to modern languages (Python, JavaScript)
- Educational value in implementing inference algorithms

## Future Enhancements (Out of Scope)

Possible extensions for future versions:
- **Arrays/Lists**: `Basket` type for collections
- **For loops**: `Prowl` keyword
- **Switch statements**: `Sniff` for multi-way branching
- **Error handling**: `Scratch`/`Lick` for try/catch
- **Classes/Objects**: `Cat` definitions for OOP
- **Import/Modules**: `Invite` for code organization
- **Optimization**: TAC optimization passes
- **Target Code Generation**: Generate actual executable code

## Contributors

Created by: [Your Name]
Course: Compiler Construction - Semester VII
Institution: SIBAU
Date: December 2025

## License

This project is created for educational purposes as part of the Compiler Construction course.

---

## Quick Reference Card

### Keywords
```
Wake    Sleep    Hunt     Box      paws
Purr    Hiss     Chase    Bring    Meow
```

### Types
```
Treats (int)    Whiskers (float)    Yarn (string)
```

### Operators
```
Arithmetic:  + - * / %
Comparison:  == != < > <= >=
Logical:     && || !
```

### Structure
```meowscript
Wake
    // Program code
Sleep
```

---

**Happy Coding! 🐱💻**
#   M e o w S c r i p t  
 