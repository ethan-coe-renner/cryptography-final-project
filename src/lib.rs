pub mod diffie_hellman {
    use mod_exp::mod_exp;
    use rand::{thread_rng, Rng};

    const P: u64 = 12941;
    const G: u64 = 724;

    /// Generate a secret to be used for a diffie hellman key exchange
    pub fn gen_secret() -> u64 {
        let mut rng = thread_rng();
        rng.gen_range(1..P)
    }

    /// Perform the first part of a diffie hellman key exchange, returning a partial key
    pub fn diffie_hellman_partial(secret: u64) -> u64 {
        mod_exp(G, secret, P)
    }

    /// Complete a diffie hellman key exchange using a partial key, return the final key
    pub fn diffie_hellman(partial: u64, secret: u64) -> u64 {
        mod_exp(partial, secret, P)
    }
}

pub mod text_manipulation {
    /// A type to represent a set of chunks
    ///
    /// Each chunk is a 64 bit unsigned value, this is the size of value that DES can encrypt
    pub type Chunks = Vec<u64>;

    /// Convert text into chunks by ascii
    ///
    /// Splits string into character bytes, and batches these into u64 chunks
    pub fn text_to_chunks(text: String) -> Chunks {
        let bytes = text.as_bytes();

        let mut chunks = Vec::new();

        let mut buffer: u64 = 0;
        let mut shift = 0;

        for b in bytes {
            buffer += (*b as u64) << shift;
            shift += 8;
            if shift >= 64 {
                chunks.push(buffer);
                buffer = 0;
                shift = 0;
            }
        }
        if buffer > 0 {
            chunks.push(buffer)
        }

        chunks
    }

    /// Converts chunks into the original text
    ///
    /// Splits each u64 chunk into 8 bytes as characters
    pub fn chunks_to_text(chunks: Chunks) -> String {
        let mut letters: Vec<u8> = Vec::new();

        for mut chunk in chunks {
            while chunk != 0 {
                letters.push((chunk % (u8::MAX as u64 + 1)) as u8);
                chunk >>= 8;
            }
        }

        if let Ok(string) = String::from_utf8(letters) {
            string
        } else {
            panic!("conversion error")
        }
    }
}

pub mod networking {
    use crate::text_manipulation::*;
    use std::{io::prelude::*,io};
    use std::net::{TcpListener, TcpStream};

    /// Send chunks to the given TCPStream.
    fn send_chunks(stream: &mut TcpStream, chunks: Chunks) -> std::io::Result<()> {

	// used to send to python because python sucks
	// let header = chunks.len().to_be_bytes();
	// println!("{:?}", &header[7..]);
	// stream.write(&header[7..])?;
	for chunk in chunks {
	    let chunk_bytes = chunk.to_be_bytes();
	    stream.write_all(&chunk_bytes)?;
	}
	Ok(())
    }

    /// Recieve chunks from a given TCPStream
    fn recv_chunks(stream: &mut TcpStream) -> std::io::Result<Chunks> {
        let mut chunk_buffer: [u8; 8] = [0; 8];
        let mut chunks = Vec::new();



	println!("recieving...");
        loop {
	    if stream.read(&mut chunk_buffer)? == 0 {
                break;
	    }
	    chunks.push(u64::from_be_bytes(chunk_buffer));
        }

        Ok(chunks)
    }

    pub fn host() -> std::io::Result<()> {
        let bind = "0.0.0.0:1812";
        println!("recieving");

        let listener = TcpListener::bind(bind)?;

        for stream in listener.incoming() {
	    println!("connected to client");
	    let mut stream_handle = stream?;
	    send_message(&mut stream_handle)?;
	    recv_message(&mut stream_handle)?;
        }
        Ok(())
    }

    pub fn client(bind: String) -> std::io::Result<()> {
        // let mut stream = TcpStream::connect(bind)?;
        loop {
            let mut stream = TcpStream::connect(&bind)?;
	    recv_message(&mut stream)?;

	    if !send_message(&mut stream)? {
                break;
	    }
        }

        Ok(())
    }

    fn recv_message(stream: &mut TcpStream) -> std::io::Result<()> {
	println!("waiting to recieve chunks");
        let chunks = recv_chunks(stream)?;
	println!("recieved {} chunks", chunks.len());

        println!("recieved: {}", chunks_to_text(chunks));
        Ok(())
    }

    fn send_message(stream: &mut TcpStream) -> std::io::Result<bool> {
	print!("> ");
	io::stdout().flush().ok().expect("Could not flush stdout");
        let mut message = String::new();
        io::stdin()
            .read_line(&mut message)
            .expect("Failed to read input");

        if message == "quit" {
	    return Ok(false);
        }

        send_chunks(stream, text_to_chunks(message))?;
        Ok(true)
    }

}

#[cfg(test)]
mod tests {
    use crate::diffie_hellman::*;
    use crate::text_manipulation::*;
    #[test]
    fn diffie_hellman_test() {
        let secret_a = gen_secret();
        let secret_b = gen_secret();

        let part_key_a = diffie_hellman_partial(secret_a);
        let part_key_b = diffie_hellman_partial(secret_b);

        let key_a = diffie_hellman(part_key_b, secret_a);
        let key_b = diffie_hellman(part_key_a, secret_b);

        assert_eq!(key_a, key_b);
    }

    #[test]
    fn chunk_text_test() {
        let text = String::from("hello world");

        let correct: Vec<u64> = vec![8031924123371070824, 6581362];
        assert_eq!(text_to_chunks(text), correct);
    }

    #[test]
    #[should_panic]
    fn chunk_text_fail_test() {
        let text = String::from("hello world");

        let correct: Vec<u64> = vec![803192412337100824, 658136];
        assert_eq!(text_to_chunks(text), correct);
    }

    #[test]
    fn chunk_text_and_back_test() {
        let text = String::from("hello world");
        let chunks = text_to_chunks(text.clone());
        assert_eq!(text, chunks_to_text(chunks));
    }
}
