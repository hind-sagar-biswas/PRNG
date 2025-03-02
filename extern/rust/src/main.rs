use rand::Rng;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} n", args[0]);
        std::process::exit(1);
    }
    let n: usize = args[1].parse().expect("Invalid number");
    let mut rng = rand::thread_rng();
    for _ in 0..n {
        let num: f32 = rng.gen();
        print!("{} ", num);
    }
    println!();
}
