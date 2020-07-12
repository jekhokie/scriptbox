fn main() {
    // loop until condition and return value
    let mut counter = 0;
    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter + 2;
        }
    };
    println!("Result is: {}", result);

    // conditional loop with while
    let mut number = 3;
    while number != 0 {
        println!("{}!", number);

        number -= 1;
    }
    println!("Done with while loop!");

    // for loop to iterate over array
    let a = [10, 20, 30, 40, 50];
    for element in a.iter() {
        println!("Value: {}", element);
    }

    // use for loop to count down
    // instead of while loop used above
    for z in (1..4).rev() {
        println!("{}!", z);
    }
    println!("Done with for loop!");
}
