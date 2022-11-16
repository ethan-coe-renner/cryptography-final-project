use std::io;

use final_project::networking::*;

fn main() -> std::io::Result<()> {
    println!("Enter R to recieve and S to send");
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    if input == "R\n" {
	server()?;
    }
    else if input == "S\n" {
        let mut bind = String::new();

	io::stdin()
            .read_line(&mut bind)
            .expect("Failed to read input");

	// trim trailing newline
	bind.pop(); 

	client(bind)?;
    }
    else {
        println!("Unknown input")
    }

    Ok(())

}
