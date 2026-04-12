define hello() {
    print("Hello, world!")
    x = 25             // Only available here
}

x = "Hello, world!"    // Sets variable 'x' to Hello, world!
print(x)               // Prints value of 'x'

if 1 {
    print("Hello")
    hello()
    print(x)
}

/* print(
    "Goodbye, world!"
) */