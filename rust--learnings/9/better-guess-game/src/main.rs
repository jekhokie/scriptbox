// bring libraries and traits into scope
use rand::Rng;
use std::cmp::Ordering;
use std::io;

// used to define a Guess
pub struct Guess {
    value: i32,
}

// implement Guess functionality, checking if guess falls within a range
impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {}.", value);
        }

        Guess { value }
    }

    pub fn value(&self) -> i32 {
        self.value
    }
}

fn main() {
    println!("Guess the number!");

    // `rand::thread_rng` function gives a random number generator local to thread
    // being executed, and `gen_range` to generate number between 1 and 101,
    // inclusive of 1 but excluding 101 (inclusive lower bound, exclusive upper bound)
    let secret_number = rand::thread_rng().gen_range(1, 101);

    loop {
        println!("Please input your guess.");

        // let is used to create a variable
        let mut guess = String::new();

        // takes input from terminal and places it into a mutable string
        // that is made mutable via a reference notation `&mut`
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");
        // `.expect` accepts a Result that is either an `Ok` value, or
        // an `Err` - in the case of an `Ok`, the value that `Ok` is holding
        // is returned, else the value placed in the `expect` function (this
        // error message) is returned

        // "shadow" the original `guess` variable
        // `trim` to eliminate whitespace (newline character from pressing Enter)
        // `parse` converts to number (in this case, u32), and returns a Result type
        let guess: i32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        // create a new Guess enum instance, validating guess range
        let g: Guess = Guess::new(guess);

        // variable is injected into `{}`
        println!("You guessed: {}", g.value());

        // `cmp` compares two values
        // `match` expression is made up of "arms", each consisting of a "pattern"
        // when the correct number is guessed, break out of loop (terminate program)
        match g.value().cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
