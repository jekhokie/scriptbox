fn main() {
    // unrecoverable error
    //   panic!("Crash and burn");

    // unrecoverable error caused by someone else's code
    let v = vec![1, 2, 3];
    v[99];
}
