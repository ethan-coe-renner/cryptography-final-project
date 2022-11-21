use std::io;

use final_project::networking::*;

fn main() -> std::io::Result<()> {
    println!("Enter S to be server and C to be client");
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    if input == "S\n" {
        host()?;
    } else if input == "C\n" {
        let mut bind = String::new();

        io::stdin()
            .read_line(&mut bind)
            .expect("Failed to read input");

        // trim trailing newline
        bind.pop();

        client(bind)?;
    } else {
        println!("Unknown input")
    }

    Ok(())
}
