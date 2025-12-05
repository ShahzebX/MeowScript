"""
MeowScript Lexical Analyzer (Lexer)

This module implements the lexical analysis phase of the MeowScript compiler.
It converts source code into a stream of tokens for the parser.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Enumeration of all token types in MeowScript"""
    
    # Keywords
    WAKE = auto()
    SLEEP = auto()
    HUNT = auto()
    BOX = auto()
    PAWS = auto()
    PURR = auto()
    HISS = auto()
    CHASE = auto()
    BRING = auto()
    MEOW = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS = auto()           # <
    GREATER = auto()        # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    
    AND = auto()            # &&
    OR = auto()             # ||
    NOT = auto()            # !
    
    # Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a single token from the source code"""
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"


class LexerError(Exception):
    """Exception raised for lexical errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexical Error at line {line}, column {column}: {message}")


class Lexer:
    """Lexical analyzer for MeowScript"""
    
    # Keywords mapping
    KEYWORDS = {
        'Wake': TokenType.WAKE,
        'Sleep': TokenType.SLEEP,
        'Hunt': TokenType.HUNT,
        'Box': TokenType.BOX,
        'paws': TokenType.PAWS,
        'Purr': TokenType.PURR,
        'Hiss': TokenType.HISS,
        'Chase': TokenType.CHASE,
        'Bring': TokenType.BRING,
        'Meow': TokenType.MEOW,
    }
    
    def __init__(self, source_code: str):
        """
        Initialize the lexer with source code
        
        Args:
            source_code: The MeowScript source code to tokenize
        """
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def current_char(self) -> Optional[str]:
        """Get the current character without advancing"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at a character ahead without advancing"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Advance to the next character and return current"""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters (except newlines in some contexts)"""
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()
    
    def skip_single_line_comment(self):
        """Skip single-line comment starting with //"""
        # Skip the //
        self.advance()
        self.advance()
        
        # Skip until end of line
        while self.current_char() and self.current_char() != '\n':
            self.advance()
    
    def skip_multi_line_comment(self):
        """Skip multi-line comment /* ... */"""
        # Skip the /*
        self.advance()
        self.advance()
        
        # Skip until */
        while self.current_char():
            if self.current_char() == '*' and self.peek_char() == '/':
                self.advance()  # Skip *
                self.advance()  # Skip /
                return
            self.advance()
        
        raise LexerError("Unterminated multi-line comment", self.line, self.column)
    
    def read_number(self) -> Token:
        """Read an integer or float literal"""
        start_line = self.line
        start_column = self.column
        num_str = ''
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    raise LexerError("Invalid number format: multiple decimal points", self.line, self.column)
                is_float = True
            num_str += self.current_char()
            self.advance()
        
        # Check for invalid format like "123."
        if is_float and num_str.endswith('.'):
            # Look ahead to see if there's a digit
            if not (self.current_char() and self.current_char().isdigit()):
                raise LexerError("Invalid number format: decimal point must be followed by digits", start_line, start_column)
        
        if is_float:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_column)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_column)
    
    def read_string(self) -> Token:
        """Read a string literal"""
        start_line = self.line
        start_column = self.column
        
        # Skip opening quote
        self.advance()
        
        string_value = ''
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                # Handle escape sequences
                self.advance()
                next_char = self.current_char()
                
                if next_char == 'n':
                    string_value += '\n'
                elif next_char == 't':
                    string_value += '\t'
                elif next_char == '"':
                    string_value += '"'
                elif next_char == '\\':
                    string_value += '\\'
                elif next_char is None:
                    raise LexerError("Unterminated string literal", start_line, start_column)
                else:
                    # Unknown escape sequence, include as-is
                    string_value += next_char
                
                self.advance()
            elif self.current_char() == '\n':
                raise LexerError("Unterminated string literal (newline in string)", start_line, start_column)
            else:
                string_value += self.current_char()
                self.advance()
        
        if self.current_char() != '"':
            raise LexerError("Unterminated string literal", start_line, start_column)
        
        # Skip closing quote
        self.advance()
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_identifier_or_keyword(self) -> Token:
        """Read an identifier or keyword"""
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        
        return Token(token_type, identifier, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code
        
        Returns:
            List of tokens
            
        Raises:
            LexerError: If a lexical error is encountered
        """
        self.tokens = []
        
        while self.current_char():
            # Skip whitespace
            if self.current_char() in ' \t\n\r':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_single_line_comment()
                continue
            
            if self.current_char() == '/' and self.peek_char() == '*':
                self.skip_multi_line_comment()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier_or_keyword())
                continue
            
            # Operators and delimiters
            start_line = self.line
            start_column = self.column
            char = self.current_char()
            
            # Two-character operators
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_column))
                continue
            
            if char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_column))
                continue
            
            if char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_column))
                continue
            
            if char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_column))
                continue
            
            if char == '&' and self.peek_char() == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', start_line, start_column))
                continue
            
            if char == '|' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', start_line, start_column))
                continue
            
            # Single-character operators and delimiters
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '!': TokenType.NOT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
            }
            
            if char in single_char_tokens:
                self.advance()
                self.tokens.append(Token(single_char_tokens[char], char, start_line, start_column))
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: '{char}'", self.line, self.column)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens
    
    def print_tokens(self):
        """Print all tokens (for debugging)"""
        for token in self.tokens:
            print(token)


def main():
    """Test the lexer with a sample program"""
    sample_code = """
    Wake
    
    // This is a comment
    Hunt add(x, y) {
        Bring x + y
    }
    
    Box age paws 3
    Box weight paws 4.5
    Box name paws "Fluffy"
    
    /* Multi-line
       comment test */
    
    Purr (age < 5) {
        Meow("Kitten")
    } Hiss {
        Meow("Adult")
    }
    
    Box counter paws 0
    Chase (counter < 5) {
        Meow(counter)
        counter paws counter + 1
    }
    
    Sleep
    """
    
    try:
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        
        print("=" * 60)
        print("LEXICAL ANALYSIS - TOKEN STREAM")
        print("=" * 60)
        lexer.print_tokens()
        print("=" * 60)
        print(f"Total tokens: {len(tokens)}")
        
    except LexerError as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
