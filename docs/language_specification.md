# MeowScript Language Specification

## 1. Language Overview

**MeowScript** is a cat-themed imperative programming language designed to demonstrate compiler construction principles while making programming delightful and accessible. It features cat-inspired keywords while maintaining full programming capabilities including functions, control structures, type inference, and operators.

### Language Purpose
MeowScript is designed for:
- Educational purposes in compiler construction
- Demonstrating lexical analysis, parsing, semantic analysis, and code generation
- Creating a memorable and unique programming experience

## 2. Lexical Elements

### 2.1 Keywords
MeowScript has the following reserved keywords:

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Wake` | Program start marker | `Wake` |
| `Sleep` | Program end marker | `Sleep` |
| `Hunt` | Function definition | `Hunt add(x, y) { ... }` |
| `Box` | Variable declaration | `Box x paws 10` |
| `paws` | Assignment operator | `x paws 5` |
| `Purr` | Conditional (if) | `Purr (x > 5) { ... }` |
| `Hiss` | Else clause | `Hiss { ... }` |
| `Chase` | While loop | `Chase (x < 10) { ... }` |
| `Bring` | Return statement | `Bring x + y` |
| `Meow` | Print/output function | `Meow("Hello")` |

### 2.2 Data Types
MeowScript supports three data types with automatic type inference:
- **Treats** (Integer): Whole numbers (e.g., `0`, `42`, `-10`)
- **Whiskers** (Float): Decimal numbers (e.g., `3.14`, `-0.5`, `2.0`)
- **Yarn** (String): Text in double quotes (e.g., `"Hello"`, `"MeowScript"`)

Type is inferred from the first assignment:
```
Box age paws 3           // Treats (integer)
Box weight paws 4.5      // Whiskers (float)
Box name paws "Fluffy"   // Yarn (string)
```

### 2.3 Operators

**Arithmetic Operators:**
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `%` : Modulo

**Comparison Operators:**
- `==` : Equal to
- `!=` : Not equal to
- `<` : Less than
- `>` : Greater than
- `<=` : Less than or equal
- `>=` : Greater than or equal

**Logical Operators:**
- `&&` : Logical AND
- `||` : Logical OR
- `!` : Logical NOT

**Assignment Operator:**
- `paws` : Assignment

### 2.4 Identifiers
- Must start with a letter (a-z, A-Z) or underscore (_)
- Can contain letters, digits, and underscores
- Case-sensitive
- Cannot be a keyword
- Examples: `age`, `cat_count`, `totalFood`, `_temp`

### 2.5 Literals

**Integer Literals:** Sequences of digits, optionally prefixed with `-` for negative values
- Examples: `0`, `42`, `-10`, `1234`

**Float Literals:** Digits with decimal point
- Examples: `3.14`, `-0.5`, `2.0`, `0.001`

**String Literals:** Characters enclosed in double quotes
- Examples: `"Hello"`, `"MeowScript"`, `"Cat says: Meow!"`
- Escape sequences supported: `\n` (newline), `\t` (tab), `\"` (quote), `\\` (backslash)

### 2.6 Delimiters and Separators
- `(` `)` : Parentheses (grouping, function calls/definitions)
- `{` `}` : Braces (code blocks)
- `,` : Comma (parameter separator)
- `;` : Semicolon (optional statement terminator)

### 2.7 Comments
- Single-line comments: `// This is a comment`
- Multi-line comments: `/* This is a multi-line comment */`

### 2.8 Whitespace
Whitespace (spaces, tabs, newlines) is ignored except:
- Inside string literals
- To separate tokens

## 3. Syntax and Grammar

### 3.1 Program Structure
Every MeowScript program must start with `Wake` and end with `Sleep`:

```
Wake

// Program code here

Sleep
```

### 3.2 Variable Declaration and Assignment
Variables are declared with `Box` and assigned with `paws`:

```
Box variable_name paws value
```

Subsequent assignments (without Box):
```
variable_name paws new_value
```

Examples:
```
Box age paws 5
Box name paws "Fluffy"
age paws 6
```

### 3.3 Function Definition
Functions are defined using `Hunt`:

```
Hunt function_name(parameter1, parameter2, ...) {
    // Function body
    Bring return_value
}
```

Examples:
```
Hunt add(x, y) {
    Bring x + y
}

Hunt greet(name) {
    Meow("Hello " + name)
    Bring "Done"
}
```

### 3.4 Function Calls
Functions are called using their name with arguments:

```
function_name(arg1, arg2, ...)
```

Examples:
```
Box result paws add(5, 3)
greet("Fluffy")
```

### 3.5 Conditional Statements
Conditional execution uses `Purr` (if) and `Hiss` (else):

```
Purr (condition) {
    // Code if condition is true
}

Purr (condition) {
    // Code if condition is true
} Hiss {
    // Code if condition is false
}
```

Examples:
```
Purr (age > 5) {
    Meow("Old cat")
}

Purr (weight < 5.0) {
    Meow("Light cat")
} Hiss {
    Meow("Heavy cat")
}
```

### 3.6 Loops
While loops use `Chase`:

```
Chase (condition) {
    // Loop body
}
```

Example:
```
Box counter paws 0
Chase (counter < 5) {
    Meow(counter)
    counter paws counter + 1
}
```

### 3.7 Print Statement
Output is produced using `Meow`:

```
Meow(expression)
```

Examples:
```
Meow("Hello World")
Meow(42)
Meow(age + 5)
```

### 3.8 Return Statement
Functions return values using `Bring`:

```
Bring expression
```

Example:
```
Hunt multiply(a, b) {
    Bring a * b
}
```

## 4. Type System

### 4.1 Type Inference
MeowScript uses automatic type inference. The type of a variable is determined by its first assignment:

```
Box x paws 10        // x is Treats (integer)
Box y paws 3.14      // y is Whiskers (float)
Box s paws "cat"     // s is Yarn (string)
```

### 4.2 Type Rules

**Arithmetic Operations:**
- `Treats op Treats → Treats` (e.g., `5 + 3` = `8`)
- `Whiskers op Whiskers → Whiskers` (e.g., `5.5 + 3.2` = `8.7`)
- `Treats op Whiskers → Whiskers` (e.g., `5 + 3.2` = `8.2`)
- Division always returns Whiskers: `10 / 3` = `3.333...`

**String Operations:**
- `Yarn + Yarn → Yarn` (concatenation: `"Hello" + " World"` = `"Hello World"`)
- `Yarn + Treats → Yarn` (e.g., `"Age: " + 5` = `"Age: 5"`)
- `Yarn + Whiskers → Yarn` (e.g., `"Pi: " + 3.14` = `"Pi: 3.14"`)

**Comparison Operations:**
- Same types can be compared with `==`, `!=`, `<`, `>`, `<=`, `>=`
- Result is boolean (internally represented as Treats: 0 or 1)

**Logical Operations:**
- Operate on boolean values (0 = false, non-zero = true)
- Result is Treats (0 or 1)

### 4.3 Type Errors
The following are type errors:
- Using non-numeric types in arithmetic (except +): `"hello" * 5`
- Comparing incompatible types: `"cat" > 5`
- Using undefined variables
- Type mismatch in assignments after initialization

## 5. Scoping Rules

### 5.1 Global Scope
- Variables and functions defined outside any function have global scope
- Accessible throughout the program after declaration

### 5.2 Local Scope
- Variables defined inside a function are local to that function
- Function parameters are local variables
- Local variables shadow global variables with the same name

### 5.3 Block Scope
- Variables declared in `Purr`, `Hiss`, or `Chase` blocks are local to that block
- Variables persist in nested blocks

## 6. Complete Example Program

```
Wake

// Function to calculate cat age in human years
Hunt cat_to_human_years(cat_age) {
    Box human_age paws cat_age * 7
    Bring human_age
}

// Function to check if cat needs more food
Hunt needs_food(weight, age) {
    Box min_weight paws age * 1.5
    Purr (weight < min_weight) {
        Bring 1
    } Hiss {
        Bring 0
    }
}

// Main program
Box cat_name paws "Fluffy"
Box age paws 3
Box weight paws 4.2

Meow("Cat name: " + cat_name)
Meow("Age: " + age)
Meow("Weight: " + weight)

Box human_years paws cat_to_human_years(age)
Meow("Age in human years: " + human_years)

Box food_needed paws needs_food(weight, age)
Purr (food_needed == 1) {
    Meow("Cat needs more food!")
} Hiss {
    Meow("Cat is well fed")
}

// Count to 5
Box counter paws 1
Chase (counter <= 5) {
    Meow("Meow number " + counter)
    counter paws counter + 1
}

Sleep
```

## 7. Error Handling

### 7.1 Lexical Errors
- Invalid characters
- Unterminated strings
- Malformed numbers

### 7.2 Syntax Errors
- Missing `Wake` or `Sleep`
- Mismatched braces or parentheses
- Invalid statement structure

### 7.3 Semantic Errors
- Undeclared variables
- Type mismatches
- Redeclaration of variables
- Missing return in function
- Wrong number of arguments in function call

## 8. Language Design Rationale

### 8.1 Why Cat Theme?
- **Memorability**: Unique theme makes the language stand out
- **Engagement**: Fun keywords make programming more enjoyable
- **Semantic Fit**: Keywords map naturally to concepts (Hunt = function, Chase = loop, Box = storage)

### 8.2 Design Decisions
- **`paws` for assignment**: Cats paw at things - natural action metaphor
- **Type inference**: Simplifies syntax while maintaining type safety
- **`Wake`/`Sleep` markers**: Clear program boundaries, fits cat behavior
- **`Purr`/`Hiss`**: Natural opposites in cat behavior for if/else
- **`Hunt` for functions**: Cats hunt with purpose - functions perform tasks
- **`Chase` for loops**: Cats chase repetitively - loops repeat actions

## 9. Future Extensions (Out of Scope)
Possible future enhancements:
- Arrays/Lists: `Basket` type
- For loops: `Prowl`
- Switch statements: `Sniff`
- Error handling: `Scratch`/`Lick`
- Classes/Objects: `Cat` definitions
- Import/modules: `Invite`
