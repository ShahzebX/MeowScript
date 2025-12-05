# MeowScript Quick Start Guide 🐱

## Installation

No installation needed! Just Python 3.7+

## First Program

Create a file `hello.meow`:

```meowscript
Wake

Box name paws "Fluffy"
Meow("Hello, ")
Meow(name)
Meow("!")

Sleep
```

## Run It

```bash
python src/main.py hello.meow -v
```

## What You'll See

```
======================================================================
                        MEOWSCRIPT COMPILER
======================================================================

[Phase 1] Lexical Analysis
----------------------------------------------------------------------
✓ Successfully tokenized: 15 tokens

[Phase 2] Syntax Analysis
----------------------------------------------------------------------
✓ Successfully parsed: AST constructed

[Phase 3] Semantic Analysis
----------------------------------------------------------------------
✓ Semantic analysis passed

[Phase 4] Code Generation
----------------------------------------------------------------------
✓ Generated 5 TAC instructions

============================================================
THREE-ADDRESS CODE (INTERMEDIATE REPRESENTATION)
============================================================
    t0 = "Fluffy"
    name = t0
    print "Hello, "
    print name
    print "!"
============================================================

======================================================================
                     ✓ COMPILATION SUCCESSFUL!
======================================================================
```

## Try More Examples

```bash
# Arithmetic
python src/main.py examples/01_arithmetic.meow -v

# Functions
python src/main.py examples/02_functions.meow -v

# Conditionals
python src/main.py examples/03_conditionals.meow -v

# Loops
python src/main.py examples/04_loops.meow -v

# Complete Program
python src/main.py examples/05_complete_program.meow -v

# Recursion
python src/main.py examples/06_recursion.meow -v
```

## Run Tests

```bash
python tests/test_compiler.py
```

## Common Commands

```bash
# Compile with verbose output
python src/main.py program.meow -v

# Save intermediate code
python src/main.py program.meow -o output.tac

# Show only TAC
python src/main.py program.meow --tac-only

# Show AST
python src/main.py program.meow --ast
```

## Language Cheat Sheet

### Basic Syntax
```meowscript
Wake
    // Your code here
Sleep
```

### Variables
```meowscript
Box age paws 3
Box weight paws 4.5
Box name paws "Fluffy"
```

### Functions
```meowscript
Hunt add(x, y) {
    Bring x + y
}

Box result paws add(5, 3)
```

### Conditionals
```meowscript
Purr (age < 5) {
    Meow("Young")
} Hiss {
    Meow("Old")
}
```

### Loops
```meowscript
Box i paws 0
Chase (i < 5) {
    Meow(i)
    i paws i + 1
}
```

### Print
```meowscript
Meow("Hello")
Meow(42)
Meow(variable)
```

### Comments
```meowscript
// Single line comment

/*
   Multi-line
   comment
*/
```

## Need Help?

- See `README.md` for complete documentation
- Check `docs/language_specification.md` for detailed syntax
- Look at `examples/` for sample programs
- Read `docs/grammar.md` for grammar details

## Tips

1. Always start with `Wake` and end with `Sleep`
2. Use `Box` to declare variables
3. Use `paws` for assignment
4. `Hunt` defines functions
5. `Purr`/`Hiss` for if/else
6. `Chase` for loops
7. `Meow` to print output

Happy MeowScripting! 🐱
