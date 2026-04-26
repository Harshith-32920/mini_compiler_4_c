# mini_compiler_4_c
From C to assembly: a mini compiler implementing lexical analysis, parsing, and code generation.
# 🛠️ Mini C Compiler (Lexical Analysis → Assembly)

A **Mini C Compiler** built from scratch that translates a subset of C language into simple assembly-like instructions (`LOAD`, `ADD`, `MUL`, `STORE`).

This project focuses on understanding core compiler design phases including **Lexical Analysis, Parsing, and Code Generation**.

---

## 🚀 Features

* 🔍 Lexical Analyzer (Tokenizer)

  * पहचान (identifies) keywords, identifiers, numbers
  * Handles operators (`+ - * / = == !=`)
  * Supports delimiters (`; , ( ) { }`)
  * Ignores comments (`//`, `/* */`)
  * Tracks line numbers for error reporting

* 🌳 Syntax Analysis (Parser) *(planned / optional depending on your progress)*

  * Recursive Descent Parser
  * Builds Abstract Syntax Tree (AST)

* ⚙️ Intermediate Representation (IR)

  * Converts expressions into 3-address code

* ⚡ Code Generation

  * Outputs simple assembly instructions:

    ```
    LOAD R1, 5
    LOAD R2, 3
    ADD R3, R1, R2
    STORE a, R3
    ```

---

## 🧠 Compiler Architecture

```
C Source Code
     ↓
[ Lexical Analyzer ]
     ↓
Tokens
     ↓
[ Parser ]
     ↓
Abstract Syntax Tree (AST)
     ↓
[ Intermediate Code ]
     ↓
[ Code Generator ]
     ↓
Assembly Code
```

---

## 📂 Project Structure

```
mini-c-compiler/
│
├── lexer.py          # Lexical Analyzer
├── parser.py         # Parser (if implemented)
├── codegen.py        # Assembly Code Generator
├── tokens.py         # Token definitions
├── sample.c          # Sample input program
└── README.md
```

---

## 🧪 Sample Input

```c
int a = 5 + 3;
```

## 🔍 Token Output

```
(KEYWORD, int)
(IDENTIFIER, a)
(OPERATOR, =)
(NUMBER, 5)
(OPERATOR, +)
(NUMBER, 3)
(DELIMITER, ;)
```

## ⚡ Generated Assembly

```
LOAD R1, 5
LOAD R2, 3
ADD R3, R1, R2
STORE a, R3
```

---

## 🛠️ Tech Stack

* Language: **Python**
* Concepts: Compiler Design, Finite State Machines, Parsing, AST

---

## ▶️ How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mini-c-compiler.git
   cd mini-c-compiler
   ```

2. Run the lexer:

   ```bash
   python lexer.py
   ```

3. Modify `sample.c` to test different inputs.

---

## 📌 Supported Grammar (Current Scope)

```
declaration → int identifier = expression ;
expression  → term ((+|-) term)*
term        → factor ((*|/) factor)*
factor      → NUMBER | IDENTIFIER
```

---

## ⚠️ Limitations

* Supports only a subset of C
* No pointers, arrays, or structs
* Limited error recovery
* Basic assembly output (educational purpose)

---

## 🎯 Learning Outcomes

* Understood how compilers tokenize source code
* Implemented a lexer using state-based scanning
* Built foundational knowledge of parsing and AST
* Learned how high-level code translates to low-level instructions

---

## 🔮 Future Improvements

* Add support for:

  * Floating-point numbers
  * Strings
  * Control structures (`if`, `while`)
* Improve error handling
* Optimize generated assembly
* Add symbol table

---

## 👨‍💻 Author

**Medari Harshith**

---

## ⭐ Acknowledgment

This project is inspired by core principles of compiler design and simplified implementations similar to tools like Lex and Yacc.
