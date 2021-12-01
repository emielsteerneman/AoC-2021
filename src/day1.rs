use std::fs;

fn get_input() -> Vec<i32> {
    /*
    let data: Vec<u32> = contents.split("\n")
    .map(|e| e.parse())
    .map(|e| e.unwrap())
    .collect();
    */

    let contents: String =
        fs::read_to_string("src/input1.txt").expect("Something went wrong reading the file.");
    let contents: &str = contents.trim();
    let numbers_as_strings: Vec<&str> = contents.split("\n").collect();

    let mut numbers: Vec<i32> = Vec::new();

    for number in numbers_as_strings.iter() {
        numbers.push(number.parse::<i32>().unwrap());
    }

    return numbers;
}

pub fn run() {
    println!("Day 1");

    let numbers: Vec<i32> = get_input();
    let mut total_increments = 0;

    for i in 0..numbers.len() - 1 {
        if numbers[i] < numbers[i + 1] {
            total_increments += 1;
        }
    }

    println!("Answer 1 : {}", total_increments);

    let numbers: Vec<i32> = get_input();
    let mut total_increments = 0;

    for i in 0..numbers.len() - 3 {
        if numbers[i] < numbers[i + 3] {
            total_increments += 1;
        }
    }

    println!("Answer 2 : {}", total_increments);
}
