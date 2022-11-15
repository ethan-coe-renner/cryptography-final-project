use std::io;
use std::net::{TcpStream,TcpListener};

use final_project::networking::*;
use final_project::text_manipulation::*;

fn main() -> std::io::Result<()> {
    let bind = "127.0.0.1:1812";
    println!("Enter R to recieve and S to send");
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    if input == "R\n" {
        println!("recieving");


        let listener = TcpListener::bind(bind)?;
        let mut chunks: Chunks = Vec::new();

        for stream in listener.incoming() {
            println!("connection established");
            chunks = recv_chunks(&mut stream?)?;
            if !chunks.is_empty() {
                break
            }
        }

        let recvd = chunks_to_text(chunks);

        println!("we recieved {recvd}");
    }
    else if input == "S\n" {
        println!("Sending");

        let text_to_send = String::from("Hello World!");
        let chunks_to_send = text_to_chunks(text_to_send);

        let mut stream = TcpStream::connect(bind)?;

        send_chunks(&mut stream, chunks_to_send)?;
        println!("Send complete");
    }
    else {
        println!("Unknown input")
    }

    Ok(())

}
