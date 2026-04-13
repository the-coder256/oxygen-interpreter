define hello() {
    print("Hello, world!")
    x = 25             // Only available here
}

x = "Hello, world!"    // Sets variable 'x' to Hello, world!
print(x)               // Prints value of 'x'

if true {
    print("Hello", "Hello again")
    hello()
    print(x)
} else {
    print("Goodbye")
}

/* print(
    "Goodbye, world!"
) */