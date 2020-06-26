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

## Starter Syntax

- `println!(...)`: Prints text to the console.
- `let ...`: Defines a variable, immutable by default.
- `let mut ...`: Defines a mutable variable.
- `let guess: u32 ...`: Defines immutable variable of type u32.
- `... = String::new()`: Creates a new string instance.
- `Result`: Type that contains `Ok` and `Err` variants, used for testing and error handling.
- `Err(_)`: Catch-all (match all `Err` values, no matter what information they have inside them).
- `....expect("this is an error");`: Takes `Result` of `Ok` and returns value, or `Err` and returns message.
- `loop {...}`: Loops.
- `match ... {...}`: Match expression and resulting "arms" to evaluate.

## Random Notes

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
