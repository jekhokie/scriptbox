// enable debugging using this annotation
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    // first implementation by defining separate variables
    let width1 = 30;
    let height1 = 50;

    println!(
        "The area of the rectangle is {} square pixels.",
        area(width1, height1)
    );

    // better implementation by using a tuple
    let rect1 = (30, 50);

    println!(
        "The better area of the rectangle is {} square pixels.",
        better_area(rect1)
    );

    // best implementation using struct
    let rect2 = Rectangle {
        width: 30,
        height: 50,
    };

    // print the struct using debug mode in both simple
    // and more readable formats
    println!("The rect2 struct looks like this (simple): {:?}", rect2);
    println!("The rect2 struct looks like this (readable): {:#?}", rect2);

    println!(
        "The best area of the rectangle is {} square pixels.",
        best_area(&rect2)
    );
}

fn area(width: u32, height: u32) -> u32 {
    width * height
}

fn better_area(dimensions: (u32, u32)) -> u32 {
    dimensions.0 * dimensions.1
}

// use borrow (&) so the main function can continue using
// the original object and we only get an immutable reference
// pointer to it
fn best_area(r: &Rectangle) -> u32 {
    r.width * r.height
}
