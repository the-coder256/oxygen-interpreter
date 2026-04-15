define hello() {
    print("Hello, world!")
    x = 25             // Only available here
    return x
}

x = "Hello, world!"    // Sets variable 'x' to Hello, world!
print(x)               // Prints value of 'x'

if true {
    print(hello())
    print(x)
} else if false {
    print("Else if 1")
} else if true {
    print("Else if 2")
} else {
    print("Goodbye")
}

/* print(
    "Goodbye, world!"
) */