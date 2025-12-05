# MeowScript Context-Free Grammar

## 1. Original Grammar (Before Transformations)

### 1.1 Grammar Productions

```
<program> ::= 'Wake' <statement_list> 'Sleep'

<statement_list> ::= <statement> <statement_list>
                   | ε

<statement> ::= <var_declaration>
              | <assignment>
              | <function_def>
              | <function_call>
              | <if_statement>
              | <while_loop>
              | <return_statement>
              | <print_statement>

<var_declaration> ::= 'Box' IDENTIFIER 'paws' <expression>

<assignment> ::= IDENTIFIER 'paws' <expression>

<function_def> ::= 'Hunt' IDENTIFIER '(' <param_list> ')' '{' <statement_list> '}'

<param_list> ::= IDENTIFIER ',' <param_list>
               | IDENTIFIER
               | ε

<function_call> ::= IDENTIFIER '(' <arg_list> ')'

<arg_list> ::= <expression> ',' <arg_list>
             | <expression>
             | ε

<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}'
                 | 'Purr' '(' <expression> ')' '{' <statement_list> '}' 'Hiss' '{' <statement_list> '}'

<while_loop> ::= 'Chase' '(' <expression> ')' '{' <statement_list> '}'

<return_statement> ::= 'Bring' <expression>

<print_statement> ::= 'Meow' '(' <expression> ')'

<expression> ::= <expression> '+' <term>
               | <expression> '-' <term>
               | <term>

<term> ::= <term> '*' <factor>
         | <term> '/' <factor>
         | <term> '%' <factor>
         | <factor>

<factor> ::= <unary>
           | <factor> '&&' <unary>
           | <factor> '||' <unary>

<unary> ::= '!' <unary>
          | <comparison>

<comparison> ::= <comparison> '==' <primary>
               | <comparison> '!=' <primary>
               | <comparison> '<' <primary>
               | <comparison> '>' <primary>
               | <comparison> '<=' <primary>
               | <comparison> '>=' <primary>
               | <primary>

<primary> ::= INTEGER
            | FLOAT
            | STRING
            | IDENTIFIER
            | <function_call>
            | '(' <expression> ')'
```

## 2. Grammar Issues and Transformations

### 2.1 Left Recursion

**Problem**: Several productions contain left recursion, which is problematic for top-down parsers (like recursive descent).

**Left-Recursive Productions:**
1. `<statement_list> ::= <statement> <statement_list>`
2. `<expression> ::= <expression> '+' <term>`
3. `<expression> ::= <expression> '-' <term>`
4. `<term> ::= <term> '*' <factor>`
5. `<term> ::= <term> '/' <factor>`
6. `<term> ::= <term> '%' <factor>`
7. `<comparison> ::= <comparison> '==' <primary>`
8. `<comparison> ::= <comparison> '!=' <primary>`
9. `<comparison> ::= <comparison> '<' <primary>`
10. `<comparison> ::= <comparison> '>' <primary>`
11. `<comparison> ::= <comparison> '<=' <primary>`
12. `<comparison> ::= <comparison> '>=' <primary>`

**Transformation**: Convert left recursion to right recursion using the standard algorithm:
- For `A ::= Aα | β`, transform to: `A ::= βA'` and `A' ::= αA' | ε`

### 2.2 Ambiguity

**Problem**: The original expression grammar can have ambiguous parse trees.

**Example Ambiguity:**
- Expression `2 + 3 * 4` could be parsed as `(2 + 3) * 4` or `2 + (3 * 4)`

**Resolution**: Use precedence levels in grammar productions:
- Lowest precedence: Logical operators (`||`, `&&`)
- Next: Comparison operators (`==`, `!=`, `<`, `>`, etc.)
- Next: Addition/Subtraction (`+`, `-`)
- Highest: Multiplication/Division/Modulo (`*`, `/`, `%`)
- Unary operators and primary expressions

This ensures correct operator precedence and associativity.

### 2.3 Left Factoring

**Problem**: Some productions have common prefixes, making it difficult to predict which production to use.

**Example:**
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}'
                 | 'Purr' '(' <expression> ')' '{' <statement_list> '}' 'Hiss' '{' <statement_list> '}'
```

Both alternatives start with `'Purr' '(' <expression> ')' '{' <statement_list> '}'`

**Transformation**: Factor out common prefix:
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}' <else_part>
<else_part> ::= 'Hiss' '{' <statement_list> '}'
              | ε
```

### 2.4 Non-determinism

**Problem**: Rules like `<param_list>` and `<arg_list>` have overlapping productions.

**Original:**
```
<param_list> ::= IDENTIFIER ',' <param_list>
               | IDENTIFIER
               | ε
```

**Issue**: When parser sees `IDENTIFIER`, it cannot determine if more parameters follow without lookahead.

**Resolution**: Restructure to make choice clear:
```
<param_list> ::= IDENTIFIER <param_list_tail>
               | ε
<param_list_tail> ::= ',' IDENTIFIER <param_list_tail>
                    | ε
```

## 3. Transformed Grammar (Final)

### 3.1 Complete Transformed Productions

```
<program> ::= 'Wake' <statement_list> 'Sleep'

<statement_list> ::= <statement> <statement_list>
                   | ε

<statement> ::= <var_declaration>
              | <assignment>
              | <function_def>
              | <function_call>
              | <if_statement>
              | <while_loop>
              | <return_statement>
              | <print_statement>

<var_declaration> ::= 'Box' IDENTIFIER 'paws' <expression>

<assignment> ::= IDENTIFIER 'paws' <expression>

<function_def> ::= 'Hunt' IDENTIFIER '(' <param_list> ')' '{' <statement_list> '}'

<param_list> ::= IDENTIFIER <param_list_tail>
               | ε

<param_list_tail> ::= ',' IDENTIFIER <param_list_tail>
                    | ε

<function_call> ::= IDENTIFIER '(' <arg_list> ')'

<arg_list> ::= <expression> <arg_list_tail>
             | ε

<arg_list_tail> ::= ',' <expression> <arg_list_tail>
                  | ε

<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}' <else_part>

<else_part> ::= 'Hiss' '{' <statement_list> '}'
              | ε

<while_loop> ::= 'Chase' '(' <expression> ')' '{' <statement_list> '}'

<return_statement> ::= 'Bring' <expression>

<print_statement> ::= 'Meow' '(' <expression> ')'

<expression> ::= <logical_or>

<logical_or> ::= <logical_and> <logical_or_tail>

<logical_or_tail> ::= '||' <logical_and> <logical_or_tail>
                    | ε

<logical_and> ::= <equality> <logical_and_tail>

<logical_and_tail> ::= '&&' <equality> <logical_and_tail>
                     | ε

<equality> ::= <comparison> <equality_tail>

<equality_tail> ::= '==' <comparison> <equality_tail>
                  | '!=' <comparison> <equality_tail>
                  | ε

<comparison> ::= <addition> <comparison_tail>

<comparison_tail> ::= '<' <addition> <comparison_tail>
                    | '>' <addition> <comparison_tail>
                    | '<=' <addition> <comparison_tail>
                    | '>=' <addition> <comparison_tail>
                    | ε

<addition> ::= <multiplication> <addition_tail>

<addition_tail> ::= '+' <multiplication> <addition_tail>
                  | '-' <multiplication> <addition_tail>
                  | ε

<multiplication> ::= <unary> <multiplication_tail>

<multiplication_tail> ::= '*' <unary> <multiplication_tail>
                        | '/' <unary> <multiplication_tail>
                        | '%' <unary> <multiplication_tail>
                        | ε

<unary> ::= '!' <unary>
          | '-' <unary>
          | <primary>

<primary> ::= INTEGER
            | FLOAT
            | STRING
            | IDENTIFIER
            | <function_call>
            | '(' <expression> ')'
```

## 4. Transformation Summary

### 4.1 Left Recursion Elimination

**Original (Left Recursive):**
```
<expression> ::= <expression> '+' <term> | <expression> '-' <term> | <term>
<term> ::= <term> '*' <factor> | <term> '/' <factor> | <factor>
```

**Transformed (Right Recursive):**
```
<addition> ::= <multiplication> <addition_tail>
<addition_tail> ::= '+' <multiplication> <addition_tail>
                  | '-' <multiplication> <addition_tail>
                  | ε

<multiplication> ::= <unary> <multiplication_tail>
<multiplication_tail> ::= '*' <unary> <multiplication_tail>
                        | '/' <unary> <multiplication_tail>
                        | '%' <unary> <multiplication_tail>
                        | ε
```

**Justification**: Eliminates left recursion while preserving left-to-right associativity through iterative processing in parser.

### 4.2 Left Factoring

**Original:**
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}'
                 | 'Purr' '(' <expression> ')' '{' <statement_list> '}' 'Hiss' '{' <statement_list> '}'
```

**Transformed:**
```
<if_statement> ::= 'Purr' '(' <expression> ')' '{' <statement_list> '}' <else_part>
<else_part> ::= 'Hiss' '{' <statement_list> '}' | ε
```

**Justification**: Removes common prefix, making parser decision clear after parsing the if body.

### 4.3 Ambiguity Resolution

**Original Issue**: Multiple parse trees possible for expressions like `2 + 3 * 4`

**Solution**: Layered expression grammar with precedence levels:
1. `<logical_or>` (lowest precedence)
2. `<logical_and>`
3. `<equality>`
4. `<comparison>`
5. `<addition>`
6. `<multiplication>` (highest precedence)
7. `<unary>` (unary minus, logical not)
8. `<primary>` (literals, identifiers, grouping)

**Justification**: Each level represents an operator precedence class. Higher-precedence operators appear lower in the grammar tree, ensuring correct parse tree structure.

### 4.4 Non-determinism Removal

**Original:**
```
<param_list> ::= IDENTIFIER ',' <param_list> | IDENTIFIER | ε
```

**Problem**: After seeing IDENTIFIER, parser doesn't know which production without extra lookahead.

**Transformed:**
```
<param_list> ::= IDENTIFIER <param_list_tail> | ε
<param_list_tail> ::= ',' IDENTIFIER <param_list_tail> | ε
```

**Justification**: Parser can decide after seeing IDENTIFIER whether to continue (if comma follows) or stop. Makes LL(1) parsing possible.

## 5. Parser Suitability

### 5.1 Chosen Parser: Recursive Descent (LL)

**Why Recursive Descent?**

1. **Grammar is LL(1) Compatible**: After transformations, each production choice can be made with 1-token lookahead
2. **Easy to Implement**: Direct mapping from grammar rules to parsing functions
3. **Good Error Recovery**: Can implement custom error messages and recovery strategies
4. **Maintainable**: Code is readable and easy to debug
5. **Sufficient for Language**: MeowScript doesn't require more powerful parsing techniques

### 5.2 LL(1) Verification

**FIRST Sets** (sample):
- FIRST(statement) = {Box, IDENTIFIER, Hunt, Purr, Chase, Bring, Meow}
- FIRST(expression) = {INTEGER, FLOAT, STRING, IDENTIFIER, '(', '!', '-'}
- FIRST(param_list) = {IDENTIFIER, ε}

**FOLLOW Sets** (sample):
- FOLLOW(statement_list) = {Sleep, '}'}
- FOLLOW(expression) = {')', ',', '}'}
- FOLLOW(param_list) = {')'}

**No Conflicts**: For each non-terminal, the FIRST sets of alternative productions are disjoint, and FIRST/FOLLOW sets don't overlap when ε-productions exist.

### 5.3 Alternative Parsers Considered

**Operator Precedence Parser:**
- Good for expression-heavy languages
- Not suitable for full statement structures in MeowScript

**LR/LALR Parser:**
- More powerful, handles broader grammar class
- Overkill for MeowScript
- Requires parser generator tools
- Less transparent for educational purposes

**Conclusion**: Recursive descent is optimal for MeowScript given its grammar structure and educational goals.

## 6. Grammar Properties

### 6.1 Operator Precedence (Highest to Lowest)
1. Parentheses: `( )`
2. Unary operators: `!`, `-` (unary)
3. Multiplicative: `*`, `/`, `%`
4. Additive: `+`, `-`
5. Comparison: `<`, `>`, `<=`, `>=`
6. Equality: `==`, `!=`
7. Logical AND: `&&`
8. Logical OR: `||`

### 6.2 Associativity
- All binary operators: **Left associative** (achieved through iterative processing in parser)
- Unary operators: **Right associative** (natural from recursive production)

### 6.3 Grammar Class
- **Type**: LL(1) after transformations
- **Parser**: Recursive Descent
- **Lookahead**: 1 token
- **Conflicts**: None

## 7. Example Parse Tree

### Input Program:
```
Wake
Box x paws 5 + 3 * 2
Sleep
```

### Parse Tree:
```
<program>
├── Wake
├── <statement_list>
│   ├── <statement>
│   │   └── <var_declaration>
│   │       ├── Box
│   │       ├── x
│   │       ├── paws
│   │       └── <expression>
│   │           └── <logical_or>
│   │               └── <logical_and>
│   │                   └── <equality>
│   │                       └── <comparison>
│   │                           └── <addition>
│   │                               ├── <multiplication>
│   │                               │   └── <unary>
│   │                               │       └── <primary>
│   │                               │           └── 5
│   │                               └── <addition_tail>
│   │                                   ├── +
│   │                                   ├── <multiplication>
│   │                                   │   ├── <unary>
│   │                                   │   │   └── <primary>
│   │                                   │   │       └── 3
│   │                                   │   └── <multiplication_tail>
│   │                                   │       ├── *
│   │                                   │       ├── <unary>
│   │                                   │       │   └── <primary>
│   │                                   │       │       └── 2
│   │                                   │       └── <multiplication_tail>
│   │                                   │           └── ε
│   │                                   └── <addition_tail>
│   │                                       └── ε
│   └── <statement_list>
│       └── ε
└── Sleep
```

**Result**: Expression correctly parsed as `5 + (3 * 2)` = `11`, respecting operator precedence.
