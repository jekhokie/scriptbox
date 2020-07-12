#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }

    fn square(size: u32) -> Rectangle {
        Rectangle {
            width: size,
            height: size,
        }
    }
}

fn main() {
    // calculate area using a method
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };

    println!(
        "The area is {} square pixels.",
        rect1.area()
    );

    // figure out if one rectangle can fit inside
    // the other
    let rect2 = Rectangle {
        width: 20,
        height: 10,
    };

    println!(
        "Can rect2 fit inside rect1?: {}",
        rect1.can_hold(&rect2),
    );

    // use an associated function to construct a
    // rectangle that is a square
    let square = Rectangle::square(30);

    println!(
        "Area of the square: {}",
        square.area()
    );
}
