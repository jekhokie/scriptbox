struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Counter {
        Counter { count: 0 }
    }
}

// define the iterator functionality
impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < 5 {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

fn main() {
    let v1 = vec![1, 2, 3];
    let v1_iter = v1.iter();

    // use an iterator - this consumes the iterator
    // v1_iter so v1_iter cannot be used again
    for val in v1_iter {
        println!("Value is: {}", val);
    }

    // after the sum() call, you can no longer use v2_iter
    // because sum() consumes the iterator
    let v2_iter = v1.iter();
    let total: i32 = v2_iter.sum();
    if total == 6 {
        println!("Found total!");
    } else {
        println!("Something went wrong!");
    }

    // map() is lazy evaluated and doesn't do anything on its own
    // we call collect() to evaluate the map() functionality/closure
    let x1: Vec<i32> = vec![4, 5, 6];
    let x2: Vec<_> = x1.iter().map(|z| z + 1).collect();
    if x2 == vec![5, 6, 7] {
        println!("collect() worked as expected!");
    } else {
        println!("Something went wrong with collect()!");
    }

    let mut counter = Counter::new();
    println!("Value 1: {:?}", counter.next());
    println!("Value 2: {:?}", counter.next());
    println!("Value 3: {:?}", counter.next());
    println!("Value 4: {:?}", counter.next());
    println!("Value 5: {:?}", counter.next());
}
