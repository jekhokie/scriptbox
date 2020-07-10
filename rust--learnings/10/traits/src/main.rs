// define a trait - any type implementing this trait must set up
// its own implementation of the `summarize` function
pub trait Summary {
    fn summarize(&self) -> String;
}

pub trait Display {
	fn show(&self) -> String;
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

// a trait that doesn't require implementation
pub trait Defaulted {
	fn do_something(&self) -> String {
		String::from("Default behavior")
	}
}

pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

// implement a trait that doesn't require self-implementation
impl Defaulted for NewsArticle {}

// trait that calls itself
pub trait NewSummary {
	fn summarize_author(&self) -> String;

	fn summarize(&self) -> String {
		format!("Read more from: {}", self.summarize_author())
	}
}

impl NewSummary for NewsArticle {
	fn summarize_author(&self) -> String {
		format!("@author: {}", self.author)
	}
}

// function using a trait as a parameter
pub fn notify(item: &impl NewSummary) {
    println!("Breaking news! {}", item.summarize());
}

// same as `notify` but allows multiple parameters and
// forces them to implement the same Summary trait
#[allow(dead_code)]
pub fn new_notify<T: Summary>(item1: &T, item2: &T) {
	println!("Item 1: {}, Item 2: {}", item1.summarize(), item2.summarize());
}

// same as new_notify, but requires that the item being passed
// implements both Summary and Display
pub fn expanded_notify<T: Summary + Display>(item: &T) {
	println!("Item: {}", item.summarize());
}

// alternative way to specify trait bounds from expanded_notify
pub fn cleaner_notify<T, U>(_t: &T, _u: &U) -> i32
	where T: Summary + Display,
		  U: Summary
{
	15
}

// define returning something that implements a trait
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    }
}

fn main() {
	// type that implements a trait
    let tweet = Tweet {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        retweet: false,
    };

    println!("1 new tweet: {}", tweet.summarize());

	// type that implements a trait but doesn't require method definition
	let article = NewsArticle {
        headline: String::from("Penguins win the Stanley Cup Championship!"),
        location: String::from("Pittsburgh, PA, USA"),
        author: String::from("Iceburgh"),
        content: String::from(
            "The Pittsburgh Penguins once again are the best \
             hockey team in the NHL.",
        ),
    };
	println!("Default trait implementation: {}", article.do_something());
	println!("Trait self-reference: {}", article.summarize());

	// use a function that leverages a trait
	notify(&article);

	// call a function that returns something that implements a trait
	let t = returns_summarizable();
	println!("Summary: {}", t.summarize());
}
