# BroThatsjs.js
If V8 is a Ferrari, this is a shopping cart with a jet engine.  
A JavaScript interpreter written in Python, powered entirely by questionable decisions.

If you want to test this in a browser like a madman, here’s a Python REPL running inside WebAssembly:  
https://pyodide.org/en/stable/console.html  

Huge thanks to the Pyodide devs for making this chaos possible.

if the snake wanted to be JS, here is the formula 
ok, this is in super early development PLEASE stay patient so we can add more JS commands and parser features.  
# Tests
interpret('console.log(10)')
interpret('console.log(3.14)')

interpret('console.log(10 + 5)')
interpret('console.log(10 - 5)')
interpret('console.log(10 * 5)')
interpret('console.log(10 / 5)')
interpret('console.log(10 % 3)')

interpret('console.log(2 + 3 * 4)')
interpret('console.log((2 + 3) * 4)')
interpret('console.log(2 * (3 + 4))')

interpret('console.log(-10)')
interpret('console.log(+10)')
interpret('console.log(-5 + 10)')

interpret('console.log("Hello")')
interpret('console.log("Hello " + "world")')

interpret('console.log(true)')
interpret('console.log(false)')

interpret('console.log("Hello", "world")')
interpret('console.log(10, 20, 30)')
interpret('console.log("Answer:", 2 + 3 * 4)')
interpret('console.log("A:", 10, "B:", 20)')

interpret('console.log("Hello\\nWorld")')
interpret('console.log("Hello\\tWorld")')
interpret('console.log("He said \\"hi\\"")')
interpret('console.log("C:\\\\test")')
# Appreciated stuff
anyone, and I mean anyone, who bases their project off this, is the ABSOLUTE goat, maybe add a UI or package manager, and if they are good enough, they will be added to this project, well at least I will try.
