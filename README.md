[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/bPoO8GTw)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19526577&assignment_repo_type=AssignmentRepo)

MiniLang Compiler Project
-------------------------

Description:
This project is a custom compiler for a mini programming language called MiniLang. It allows basic variable assignments, conditional statements (if-else), loops (while), and arithmetic operations. The project consists of two versions:
1. A manually implemented interpreter in Python that simulates assembly-like instructions.
2. A proper compiler built using Flex (scanner) and Bison (parser) to generate assembly code from MiniLang source code.

Name: Pearl Agnihotri 
Roll Number: 22000405

Instructions to Run:

Manual Simulator (Python-based)For Versio-1:
--------------------------------
1. Place your MiniLang assembly code in a file named output.asm.
2. Run the simulator using:
   > python simulator.py

Flex & Bison Version (For Version-2):
---------------------
1. Ensure Flex and Bison are installed on your system.
2. Use the following commands to build and run:

   > flex scanner.l  
   > bison -d parser.y  
   > gcc lex.yy.c parser.tab.c -o compiler  
   > ./compiler < input.minilang > output.asm  

3. Then run the Python simulator to execute the generated output.asm:
   > python simulator.py
