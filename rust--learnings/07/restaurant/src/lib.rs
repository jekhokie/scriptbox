mod front_of_house;

pub use crate::front_of_house::hosting;

pub fn eat_at_restaurant() {
    // absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // relative path
    front_of_house::hosting::add_to_waitlist();

    // local path as a result of `use` operation prior
    // to this function definition
    hosting::add_to_waitlist();
}
