# Go Language Analyzer (Subset Compiler Pipeline)

A command-line static analyzer for a defined subset of the Go programming language. This project implements a simplified compiler pipeline including lexical analysis, parsing, Abstract Syntax Tree (AST) construction, and semantic/type checking.

---

## 📌 Overview

This project demonstrates how a compiler pipeline works by processing Go-like source code through multiple stages:

1. **Lexical Analysis (Tokenization)**
2. **Parsing (LALR Grammar using PLY)**
3. **AST Construction**
4. **Semantic Analysis (Scope Resolution + Type Checking)**

The analyzer detects both syntax and semantic errors and can optionally display the generated AST.

---

## 🚀 Features

### Supported Language Constructs

- Variable declarations and assignments
- Arithmetic and comparison expressions
- Control flow:
  - `if` / `else`
  - `for` loops
  - `switch-case-default`
- `return` statements

### Static Analysis Capabilities

- Detection of undeclared variables
- Detection of variable redeclaration within the same scope
- Type checking for expressions and assignments
- Scope-aware symbol resolution (supports nested blocks)

---

## 🏗️ Project Structure

```
.
├── samples/
│   └── sample.go
├── src/
│   ├── ast_nodes.py
│   ├── lexer.py
│   ├── main.py
│   ├── parser.py
│   ├── semantic.py
│   ├── parser.out
│   └── parsetab.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Architecture

### 1. Lexer
- Implemented using **PLY (Lex)**
- Converts source code into tokens (identifiers, keywords, operators, etc.)

### 2. Parser
- Built using **LALR parsing (PLY Yacc)**
- Defines grammar rules for a subset of Go
- Generates an Abstract Syntax Tree (AST)

### 3. AST Representation
- Tree-based structure representing program hierarchy
- Each node contains:
  - `type` (e.g., `VarDecl`, `BinaryOp`)
  - `value`
  - child nodes
- Includes a recursive pretty-printer for visualization

### 4. Semantic Analysis
- Stack-based symbol table for scope management
- Handles:
  - Variable declaration and lookup
  - Nested scope resolution
  - Type validation

---

## 🧪 Example

### Input

```go
var x = 10
if x > 5 {
    var y = x + 2
}
```

### Output

```
✅ Syntax + Semantic + Type Checking Passed

🌳 AST:

Program
  VarDecl: x
    Literal: 10
  If
    BinaryOp: >
      Literal: x
      Literal: 5
    Block
      VarDecl: y
        BinaryOp: +
          Literal: x
          Literal: 2
```

---

## ▶️ How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with AST Output

```bash
python src/main.py samples/sample.go --ast
```

### 3. Run for Validation Only

```bash
python src/main.py samples/sample.go --check
```

---

## 🧠 Design Decisions

- **PLY (Lex/Yacc)** was chosen to explicitly implement grammar rules and understand parsing mechanics instead of relying on abstracted parsers
- **AST-first design** separates parsing from semantic analysis
- **Scoped symbol table** (stack-based) ensures correct handling of nested blocks and variable shadowing

---

## ⚠️ Limitations

- Supports only a subset of Go (no functions, structs, or concurrency primitives)
- Minimal type system (primarily integer-based)
- No error recovery — stops at first error
- No optimization or code generation phase

---

## 🔮 Future Improvements

- Extend type system (strings, booleans, composite types)
- Add function definitions and calls
- Improve error reporting and recovery
- Introduce intermediate representation (IR) or code generation

---

## 🛠️ Tech Stack

- **Python**
- **PLY** (Lex/Yacc)
