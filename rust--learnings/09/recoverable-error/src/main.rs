use std::fs::File;
use std::io::ErrorKind;
use std::io;
use std::io::Read;

// function signature that can return a Result where the
// success condition is a String and a failure returns the
// io::Error result
fn function_returns_error() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;
    let mut s = String::new();
    // '?' returns value inside `Ok` if successful, or entire Err if failed
    f.read_to_string(&mut s)?;
    Ok(s)

    // shorter form of the above:
    //   let mut s = String::new();
    //   File::open("doesnotexist")?.read_to_string(&mut s)?;
    //   Ok(s)
}

fn main() {
    // catch a Result<T, E> condition by attempting to
    // open a file that does not exist or a file that can't be accessed
    let f = File::open("doesnotexist");
    let _f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("doesnotexist") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {:?}", e),
            },
            other_error => {
                panic!("Problem opening the file: {:?}", other_error)
            }
        },
    };

    // another panic option - unwrap returns the result inside `Ok` if
    // successful, otherwise calls the `panic!` macro
    //   let f = File::open("doesnotexist").unwrap();

    // alternative to the `unwrap()` option, affords providing a user-defined
    // error message
    //   let f = File::open("doesnotexist").expect("File does not exist");
}
