# Go Language Analyzer (Compiler + Static Analysis Engine)

A command-line static analysis tool for a subset of the Go programming language.
This project implements a **compiler front-end pipeline** extended with **control-flow modeling, program analysis, and visualization**.

---

## 📌 Overview

This project goes beyond a traditional compiler assignment by combining:

* Compiler construction (lexing → parsing → AST)
* Semantic analysis (type + scope checking)
* **Control Flow Graph (CFG) generation**
* **Static analysis on program structure**
* **Graph-based visualization of programs**

The system processes Go-like source code through multiple stages and enables both **structural and analytical understanding of programs**.

---

## 🚀 Features

### 🔧 Compiler Pipeline

* Lexical Analysis (Tokenization using PLY)
* LALR Parsing (PLY Yacc)
* Abstract Syntax Tree (AST) construction
* Semantic analysis:

  * Scope resolution
  * Type checking

---

### 🔀 Control Flow Graph (CFG)

* Builds CFG from AST
* Supports:

  * Sequential flow
  * Conditional branching (`if / else`)
  * Loops (`for`)
  * Multi-branch control (`switch-case-default`)
* Explicit representation of:

  * Entry and exit nodes
  * Loop back edges
  * Merge points

---

### 🔍 Static Analysis

* Detection of:

  * Undeclared variables
  * Redeclaration errors
  * Type mismatches
  * **Dead/unreachable code**
  * **Unused variables**
* Scope-aware analysis using symbol tables

---

### 📊 Visualization

* **AST Visualization**

  * Tree representation of program structure
* **CFG Visualization**

  * Graph representation of execution flow
  * Color-coded nodes:

    * 🟢 Entry/Exit
    * 🟠 Conditions
    * 🟣 Switch
    * ⚪ Merge points
    * 🔵 Statements

---

## 🏗️ Project Structure

```
.
├── samples/
│   └── sample.go
├── src/
│   ├── ast_nodes.py
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic.py
│   ├── cfg.py
│   ├── analysis.py
│   ├── visualize.py
│   ├── main.py
│   └── parsetab.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Architecture

### 1. Lexer

* Implemented using **PLY (Lex)**
* Converts source code into tokens

---

### 2. Parser

* Built using **LALR parsing (PLY Yacc)**
* Generates AST from grammar rules

---

### 3. AST (Abstract Syntax Tree)

* Hierarchical program representation
* Node types include:

  * `VarDecl`, `Assign`, `BinaryOp`, `If`, `ForLoop`, `Switch`
* Used as input for semantic and CFG stages

---

### 4. Semantic Analysis

* Stack-based symbol table
* Handles:

  * Variable declaration and lookup
  * Nested scopes
  * Type validation

---

### 5. CFG Generation

* Transforms AST → Control Flow Graph
* Each node = **Basic Block**
* Captures:

  * Execution paths
  * Branching
  * Loop cycles

---

### 6. Static Analysis Engine

* Runs analyses on AST + CFG
* Enables program-level reasoning:

  * Reachability
  * Usage tracking

---

## 🧪 Example

### Input

```go
var x = 2

for x < 5 {
    x = x + 1
}

switch x {
    case 5:
        x = x + 2
    default:
        x = x + 3
}
```

---

### CFG Output (conceptual)

```
ENTRY → VarDecl → LOOP_COND
           ↓        ↘
         BODY ←─────┘
           ↓
       AFTER_LOOP → SWITCH
                    ↙   ↘
                 CASE  DEFAULT
                    ↓      ↓
                   MERGE → EXIT
```

---

## ▶️ How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Run AST view

```bash
python src/main.py samples/sample.go --ast
```

---

### Run CFG view

```bash
python src/main.py samples/sample.go --cfg
```

---

### Visualize CFG

```bash
python src/main.py samples/sample.go --viz-cfg
```

---

### Run Static Analysis

```bash
python src/main.py samples/sample.go --analyze
```

---

## 🧠 Design Decisions

* **PLY (Lex/Yacc)** for explicit grammar control and learning parsing internals
* **AST-first architecture** for separation of concerns
* **CFG-based analysis** to enable graph-level reasoning
* **Modular design** (lexer, parser, semantic, cfg, analysis, visualize)

---

## ⚠️ Limitations

* Supports only a subset of Go
* No functions, structs, or advanced types
* Basic type system (primarily integers)
* No optimization or code generation
* Visualization uses force-directed layout (not hierarchical)

---

## 🔮 Future Improvements

* Data-flow analysis (live variable analysis)
* Intermediate Representation (IR)
* SSA form
* Optimization passes
* Function support
* Better CFG layout (Graphviz-based)
* IDE / VS Code extension

---

## 🛠️ Tech Stack

* **Python**
* **PLY (Lex/Yacc)**
* **NetworkX** (graph modeling)
* **Matplotlib** (visualization)

---

## 🏆 Summary

This project evolves a traditional compiler pipeline into a **graph-based static analysis system**, combining:

* Compiler fundamentals
* Graph theory
* Program analysis

👉 Suitable for systems, compilers, and program analysis exploration.
