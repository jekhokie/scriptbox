fn main() {
    // use the slice functionality to capture contiguous
    // items in a collection
    let s = String::from("hello world");
    let slice1 = &s[0..2];
    let slice2 = &s[3..5];
    println!("Slice 1: {}", slice1);
    println!("Slice 2: {}", slice2);

    // capture first and last characters
    let len = s.len();
    let slice3 = &s[..5];
    let slice4 = &s[3..len];
    println!("Slice 3: {}", slice3);
    println!("Slice 4: {}", slice4);

    // wrapped as a function to capture the first word
    // in the string
    let fw = first_word(&s);
    println!("First word: {}", fw);

    // can now pass literal strings as well as `String` types
    let fw2 = String::from("test this");
    println!("First word improved with literal: {}", first_word_improved("test this"));
    println!("First word improved with String: {}", first_word_improved(&fw2[..]));

    // can also do slicing on non-strings/other collections
    //  let x = [1, 2, 3, 4, 5];
    //  let slice = &x[0..2];
}

fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}

// accepts both `String` and literal string types
fn first_word_improved(s: &str) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
