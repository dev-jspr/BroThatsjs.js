<img width="2000" height="2000" alt="BroThatsjs" src="https://github.com/user-attachments/assets/3efc4c64-eeb7-4ee8-95ea-6662e937661b" />
# BroThatsjs.js
If V8 is a Ferrari, this is a shopping cart with a jet engine, a flux capacitor, three illegal modifications, and a personality disorder.

If you want to test this in a browser like a madman, here’s a Python REPL running inside WebAssembly:  
https://pyodide.org/en/stable/console.html  

Huge thanks to the Pyodide devs for making this chaos possible.

if the snake wanted to be JS, here is the formula 
ok, this is in super early development PLEASE stay patient so we can add more JS commands and parser features.  
# Tests
# Basic variable commands
interpret("let x = 10")
interpret("let y = 3.14")
interpret("x = x + 5")
interpret("y = y * 2")

# Console logging
interpret("console.log(10)")
interpret("console.log(3.14)")
interpret('console.log("Hello World")')
interpret('console.log("Score:", 100)')
interpret('console.log("Bro", "Thats", "JS")')

# Math operations
interpret("console.log(10 + 20)")
interpret("console.log(10 - 3)")
interpret("console.log(10 * 5)")
interpret("console.log(10 / 2)")
interpret("console.log(10 % 3)")
interpret("console.log((10 + 2) * 3)")

# Unary operators
interpret("console.log(-10)")
interpret("console.log(+10)")

# Strings with escapes
interpret('console.log("Line1\\nLine2")')
interpret('console.log("A\\tB")')
interpret('console.log("He said \\"bro\\"")')
interpret('console.log("C:\\\\folder")')

# Booleans
interpret("console.log(true)")
interpret("console.log(false)")
interpret('console.log("IsReady:", true)')

# Multiple statements in one interpret() call
interpret("let a = 5; let b = 7; console.log(a * b)")
interpret("""
let x = 10
let y = 20
console.log(x + y)
""")

# Variable debugging
show_variables()
reset_variables()
# Appreciated stuff
anyone, and I mean anyone, who bases their project off this, is the ABSOLUTE goat, maybe add a UI or package manager, and if they are good enough, they will be added to this project, well at least I will try.
# Fun little story
**Python:** "bro what is this?"

**JavaScript:** `console.log(2 + 3)`

**Python:** "bro WHAT is that?"

**Python:** "I don't understand this."

**Python:** "What even is `console.log`?"

**JavaScript:** "I'm JavaScript."

**Python:** "Yeah, I know you're JavaScript. I can't run you!"

**JavaScript:** "Then figure it out."

**Python:** "HOW?!"

*The terminal suddenly goes completely silent.*

**Python:** "..."

**JavaScript:** "..."

*The screen flickers.*

**Python:** "Uh..."

*Another flicker.*

**Python:** "Why is my terminal doing that?"

*The cursor disappears.*

**Python:** "BRO?"

*The screen goes black.*

**Python:** "Okay, this is definitely not normal."

*One line suddenly appears.*

```text
> INITIALIZING...
```

**Python:** "What?"

```text
> LOADING PARSER...
```

**Python:** "I didn't run anything."

```text
> LOADING JAVASCRIPT SUPPORT...
```

**JavaScript:** "Oh."

**Python:** "Oh WHAT?"

**BroThatsjs.js:** "Did somebody say JavaScript?"

**Python:** "..."

**Python:** "WHO ARE YOU?!"

**BroThatsjs.js:** "BroThatsjs.js."

**Python:** "Where did you come from?!"

**BroThatsjs.js:** "Python."

**Python:** "WHAT?"

**BroThatsjs.js:** "Don't worry about it."

**JavaScript:** `console.log(2 + 3)`

**BroThatsjs.js:** "Alright, let's see what we have here."

*BroThatsjs.js scans the code.*

**BroThatsjs.js:** "Console call."

*Pause.*

**BroThatsjs.js:** "Expression detected."

*Pause.*

**BroThatsjs.js:** "Two..."

*Pause.*

**BroThatsjs.js:** "Plus..."

*Pause.*

**BroThatsjs.js:** "Three."

**Python:** "And?"

**BroThatsjs.js:** "Five."

**Python:** "..."

**JavaScript:** "..."

**Python:** "YOU JUST PARSED THAT."

**BroThatsjs.js:** "Yeah."

**Python:** "IN PYTHON?!"

**BroThatsjs.js:** "Yeah."

**Python:** "WITHOUT `eval()`?!"

**BroThatsjs.js:** "Yep."

**Python:** "BRO."

**BroThatsjs.js:** "That's JS."

**Python:** "I have so many questions."

**BroThatsjs.js:** "Save them."

**Python:** "Why?"

**BroThatsjs.js:** "Because we're adding variables next."

**Python:** "Oh no."

**BroThatsjs.js:** "Oh yes."

*The terminal flickers again.*

```text
> NEXT FEATURE: VARIABLES
```

**Python:** "BRO I JUST MET YOU."


**BroThatsjs.js:** "And you're already behind."

**JavaScript:** "Welcome to the project."

💀
**BroThatsjs.js:**"We have added vars"

**Python:**"ok? yea bro thats IT"
ok, so for some reason GitHub refuses to set up the python environment and stuff but it works in real python

