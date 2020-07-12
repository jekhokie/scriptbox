use std::collections::HashMap;

fn main() {
    // create new hash map, load it with values,
    // and get a value
    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
    let lookup = String::from("Blue");
    let _blue_score = scores.get(&lookup);

    // iterate over key/value pairs
    for (key, value) in &scores {
        println!("{} - {}", key, value);
    }

    // create a HashMap from a list of teams and scores
    let teams = vec![String::from("Blue"), String::from("Yellow")];
    let initial_scores = vec![10, 50];
    let mut _other_scores: HashMap<_, _> =
        teams.into_iter().zip(initial_scores.into_iter()).collect();
    println!("{:?}", _other_scores);

    // inserting Strings into a HashMap changes ownership,
    // making them invalid
    let field_name = String::from("Favorite color");
    let field_value = String::from("Blue");
    let mut map = HashMap::new();
    map.insert(field_name, field_value);
    println!("{:?}", map);

    // overwriting a value
    scores.insert(String::from("Blue"), 25);
    println!("{:?}", scores);

    // only insert a value if one does not yet exist
    scores.entry(String::from("Blue")).or_insert(30);
    println!("{:?}", scores);

    // update value based on old value (count number of words)
    let text = "hello world wonderful world";
    let mut map = HashMap::new();
    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;
    }
    println!("{:?}", map);
}
