// generic struct - both x and y must be same type
struct SomePoint<T> {
    x: T,
    y: T,
}

// generic implementation on a generic struct
impl<T> SomePoint<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

// implementation only on f32 types
#[allow(dead_code)]
impl SomePoint<f32> {
    fn add_one(&self) -> f32 {
        self.x + 1.0
    }
}

// generic struct - x and y can be different
struct OtherPoint<T, U> {
    x: T,
    y: U,
}

// mix things up
impl<T, U> OtherPoint<T, U> {
    fn mixup<V, W>(self, other: OtherPoint<V, W>) -> OtherPoint<T, W> {
    OtherPoint {
        x: self.x,
        y: other.y,
    }
  }
}

// generic enum
#[allow(dead_code)]
enum Option<T> {
    Some(T),
    None,
}

fn main() {
    // use a generic struct
    let u = SomePoint { x: 1, y: 2 };
    println!("Value of u.x: {}", u.x);
    println!("Value of u.y: {}", u.y);

    // use generic implementation on struct
    println!("Generic implementation: {}", u.x());

    // use a multiple-type generic struct
    let v = OtherPoint { x: 1, y: 4.5 };
    println!("Integer X: {}", v.x);
    println!("Float Y: {}", v.y);

    // mix things up
    let w = OtherPoint { x: "Hello", y: 'c' };
    let z = v.mixup(w);
    println!("z.x = {}, z.y = {}", z.x, z.y);

}
