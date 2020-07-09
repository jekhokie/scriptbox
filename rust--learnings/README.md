# Rust Learnings

Repository containing learnings and experimentation with the Rust programming language. Each directory is
named according to the chapter of the following book, from which the corresponding examples were built:

[The Rust Programming Language](https://doc.rust-lang.org/stable/book/)

## Command Line Notes

- `rustc main.rs`: Compile using Rust directly, generating binary named `main`.
- `cargo check`: Check if build compiles.
- `cargo build`: Create binary `target/debug/main`.
- `cargo run`: Create binary and/or run it, in one command (only build if changes).
- `cargo build --release`: Create binary `target/release/main`.
- `cargo doc --open`: Open documentation for dependencies in `Cargo.yaml`.
- `cargo update`: Update dependencies defined in `Cargo.yaml` to latest available per version spec.

## Semantics

- Cargo: Rust's build system and package manager.
- Crate: Libraries (to be used) and binaries built with Cargo.
- [https://crates.io](https://cates.io): Location where crates (dependencies) are downloaded from.
- Comments: Using `//`.
- Macro: Uses exclamation (e.g. `println!()`).
- Association Function: Indicated via use of `::` (commonly known as static method).
- Function: No exclamation.
- Match Expression: Conditional made up of arms, each consisting of a pattern and resulting code to run.
- Annotation: For example, add colon `:` after variable declaration, followed by the type the variable should be.
- Variables: Defined with `let`, and immutable by default (or can be mutable using `mut`).
- Constants: Defined with `const`, always immutable, and must define the type of the value (existing within scope of definition).
- `Result` Type: Used with `expect()` function, either `Ok` with value, or `Err` (returns error message in `expect()`).
- Shadow Variable: Re-use of the same variable (immutable) using `let`, creating a new variable with the same name but possibly different type and keeping the result immutable.
- Scalar Type: Single value (can be integers, floats, bools, and chars).
- Integer Types: Unsigned (`u`) and Signed (`i`), with 8-bit through 128-bit, or `arch` according to computer architecture where program is running (e.g. 32-bit or 64-bit).
- Float Types: 32-bit or 64-bit (`f32` and `f64`, respectively).
- Charater Types: 4 bytes in size, representing Unicode Scalar Value.
- Compount Type: Group multiple values into one type (can be tuples or arrays).
- Tuple Type: Fixed length, comma-separated list of values inside parenthesis.
- Unused Variables: Variables that are assigned but not used should be preceded with an underscore `_`.
- Array Type: All elements must have same type, fixed length, comma-separated list inside square brackets - allocates data to Stack instead of Heap.
- Statement: Instruction that performs some action and does not return a value (e.g. `let`), and therefore cannot be assigned to other variables.
- Expression: Evaluates to a resulting value.
- Conditionals: Use same concept of "arms" as match conditions.
- Stack: All data put on stack (LIFO) must have fixed, known size, otherwise put in heap (slower).
- Heap: Place for dynamically sized data, typically slower, and requires memory pointers for retrieval.
- Borrowing: Using reference pointers that point to the original reference pointer of a variable, thus allowing modification but never taking ownership - does not allow modifications to the borrowed value (read-only).
- Slice: Contiguous sequence of elements in a collection (instead of whole collection) - no ownership.
- Struct: Custom data type to name and package torgether related values (like object data attributes), having fields - use dot `.` notation with field name to access fields.
- Struct Tuple: Same as structs, but fields don't have names (have types in fields instead) - use dot `.` notation with numeric indexes to access fields.
- Unit-Like Structs: Struct that doesn't have any fields.
- Method: Similar to a function, but defined within a Struct (or enum, or trait).
- Implementation (`impl`): Used to define methods on Structs (or enums, or traits).
- Associated Function: Define a function within a Struct, usually used to initialize a struct with a default value (constructor) - uses `::` syntax.
- Enumeration (Enum): Define a type by enumerating its possible variants.
- Pattern Matching: `match` where the first hit applies.
- Package: Cargo feature that lets you build, test, and share crates.
- Crate: Tree of modules that produce a library or executable.
- Module and use: Control organization, scope, and privacy of paths.
- Path: Way of naming an item such as a struct, function, or module.
- `src/main.rs`: Convention for crate root of a binary crate.
- `src/lib.rs`: Convention for crate root of a library crate.
- Vector: Stores multiple values next to each other in memory, each of the same type - to store different types, use an enum to wrap the types, and then create a vector of that enum..

## Starter Syntax

- `println!(... {}, x)`: Prints text to the console, interpolating `x`.
- `println!(... {:?}, Struct)`: Prints to the console, printing debug to support printing the Struct fields (requires annotation `#[derive(Debug)]`).
- `println!(... {:#?}, Struct)`: Prettier debug information (easier for larger Structs).
- `let ...`: Defines a variable, immutable by default.
- `let mut ...`: Defines a mutable variable.
- `let guess: u32 ...`: Defines immutable variable of type u32.
- `... = String::new()`: Creates a new string instance.
- `Result`: Type that contains `Ok` and `Err` variants, used for testing and error handling.
- `Err(_)`: Catch-all (match all `Err` values, no matter what information they have inside them).
- `....expect("this is an error");`: Takes `Result` of `Ok` and returns value, or `Err` and returns message.
- `loop {...}`: Loops.
- `match ... {...}`: Match expression and resulting "arms" to evaluate.
- `x.clone()`: Deep copy a variable (not needed with fixed-length vars, which sit on the Stack).
- `x.len()`: Calculate length of variable.
- `... = String::from("some string")`: Construct `String` variable, stored in heap with pointer in stack.
- `... = "x"`: Construct literal, stored in stack (faster), and immutable as it is technically a slice.
- `x.as_bytes()`: Convert `String` to array of bytes.
- `x.iter()`: Returns each element in a collection.
- `x.iter().enumerate()`: Wraps result of `iter` and returns each element as part of a tuple.
- `b' '`: Byte-literal syntax for a space character (char).
- `x.clear()`: Empties a String, making it equal to "".
- `struct Something...`: Define a struct.
- `..x`: When used in struct instantiation, assigns all unassigned values from `x` to the new instance.
- `enum Something...`: Define an enum.
- `Option<T>`: Special enum type that can be something or nothing.
- `None`: Failure or lack of value in `Option<T>`.
- `Some(value)`: Tuple struct that wraps a `value` with type `T` in `Option<T>`.
- `match x {...}`: Pattern match operation with many "arms" (similar to a case operation, or switch).
- `()`: Unit value (nothing).
- `mod ...`: Define a module.
- `pub ...`: Define a public item.
- `use ...`: Bring a module path into scope to shorthand the calling of the functionality.
- `... as ...`: Provide new name/alias for a type being imported with `use`.
- `pub use ...`: Making/re-exporting code to bring an item into scope and make it available to others in their scope.
- `data.to_string()`: Load data into a String.
- `data.push_str('test')`: Append a string slice to a String.
- `data.push('a')`: Append a character to a String.
- `format!("{}-{}-{}", x, y, z)`: Concatenate a string/interpolate variables.
- `data.chars()`: Iterate over each character in a String.
- `data.bytes()`: Iterate over each byte in a String.
- `HashMap::new()`: Create a new HashMap.
- `data.insert(x, 10)`: Insert key/value into a HashMap.
- `data.get("KeyA")`: Get a value out of a HashMap based on the key name.
- `data.entry(String::from("KeyA")).or_insert(30)`: Only insert value at key if it doesn't already exist.
- `panic = 'abort'`: Used for aborting (instead of unwinding call stack) in a terminal failure - can help with making smaller binaries.
- `RUST_BACKTRACE=1`: Added to command line `cargo run`, will add backtrace information (e.g. call stack) if a `panic!` is encountered to help troubleshoot.
- `...unwrap()`: Returns the value inside the `Ok` if successful, otherwise calls the `panic!` macro.
- `...expect("Does not exist")`: Alternative to `unwrap()` allowing for custom error message during `panic!`.
- `...?`: Using `?` will return result inside `Ok` if successful or return the entire `Err` if unsuccessful. If `Err` is returned, the error type returned is converted into the return `Err` type defined by the function (consistent error types for all failures within the function). Can only be used in a function returning a `Result<T, E>` type (never in `main()` unless the `main()` function signature is updated to return `Result<(), Box<dyn Error>>`).

## Other Notes

- Indent with 4x spaces (no tabs).
- Name files with underscores separating words.
- Name functions using snake case (lowercase with underscore separators)..
- You must declare parameter types in function parameter definitions.
- End lines with semicolons.
- `Cargo.lock` is similar to freezing requirements (Python) or Ruby `Gemfile.lock` files.
- Underscores can be inserted in numeric literals to improve readability (e.g. `100_000` is 100,000).
- Shadow variables are useful for changing immutable variable types (whereas mutable variables cannot do this unless you start with a mutable and convert to immutable and use the `let` directive).
- Rust is statically typed (must know types of all variables at compile time).
- Integer overflow for releases (production) result in complement wrapping, not errors (e.g. it will assign 256 to 0, 257 to 1, 258 to 2 in an 8-bit integer that overflows).
- Some types require heap (undefined size), and these types result in stack pointers/data. Copying (re-assigning) these variables results in a "move", where the previous variable is invalidated in the stack (data is not necessarily copied) to avoid double-free memory operations (where both variables on the stack result in attempting to free the same segment in memory on a free operation).
- To do a deep copy operation, use `clone`.
- Fixed-length types can be re-assigned because the copy is implicit, super-fast, and only exists on the Stack.
- Can only have 1 mutable reference to a particular piece of data within a scope, unless the second reference is after the last occurrence/use by the first reference..
- Rule: At any given time, you can have either one mutable reference or any number of immutable references.
- Implementations (`impl`) always have `self` as the first paramter and can be either reference/immutable using `&self` or mutable using `&mut self`.
- There is no null feature in Rust - only `Option<T>`. When using `None`, you must tell Rust what type the `Option` should be (e.g. `Option<i32>`)..
- You have to convert an `Option<T>` to a `T` before performing operations on `T`.
- Common Rust pattern: `match` against an enum, bind a variable to the data inside, and execute code based on it.
- Pattern matching *must* include an exhausive list of option, including `None` (can use `_` as a fallback and assign it to `()` (unit value, meaning nothing)..
- Can use a nested path to bring items into scope using `use std::{cmp::Ordering, io};`.
- Writing `use std::io; \n use std::io::Write;` is the same as `use std::io{self, Write};`.
- All items in Rust are private by default.
- Strings are UTF-8 encoded.
- For a HashMap, data is stored in Heap, and all keys must have the same type/all values must have the same type.
- 2 types of errors - one that returns a `Result<T, E>` (recoverable) and one that triggers `panic!` (unrecoverable).
- Good to use `unwrap` and `expect` in example/prototype code to indicate where actual error handling might need to be matured before production use.
