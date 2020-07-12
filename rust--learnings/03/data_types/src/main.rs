fn main() {
    // declare a variable with type and use parse() to convert
    let x: u32 = "123".parse().expect("Not a number");
    println!("Value of u32 variable x: {}", x);

    // declare a 32-bit float
    let y: f32 = 256.24;
    println!("Value of f32 variable y: {}", y);

    // declare a boolean
    let z: bool = true;
    println!("Value of bool variable z: {}", z);

    // declare a character
    let a = 'z';
    println!("Value of char variable a: {}", a);

    // declare a tuple, and assign variables with un-used/un-referenced
    // variables preceded with an underscore `_` to avoid compiler warnings
    // assigning to 3 variables is known as "destructuring"
    // printing shows two ways to access tuple values
    let b: (i32, f64, u8) = (500, 6.4, 1);
    let (_c, d, _e) = b;
    println!("Value of f64 variable using destructuring: {}", d);
    println!("Value of f64 variable via direct reference: {}", b.1);

    // declare an array of i32 elements
    // fixed size of 5 elements
    // data allocated to stack (not heap)
    let f: [i32; 5] = [1, 2, 3, 4, 5];
    println!("Value of array position 1: {}", f[1]);

    // declare an array
    // fixed size of 6 elements
    // all having value 3
    let g = [3; 6];
    println!("Value of initialized array position 3: {}", g[3]);
}
