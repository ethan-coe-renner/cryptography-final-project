mod diffie_hellman {
    use mod_exp::mod_exp;
    use rand::{thread_rng, Rng};

    const P: u64 = 12941;
    const G: u64 = 724;

    pub fn gen_secret() -> u64 {
        let mut rng = thread_rng();
        rng.gen_range(1..P)
    }

    pub fn diffie_hellman_partial(secret: u64) -> u64 {
        mod_exp(G,secret,P)
    }

    pub fn diffie_hellman(partial: u64, secret: u64) -> u64 {
        mod_exp(partial, secret, P)
    }
}

fn text_to_chunks(text: String) -> Vec<u64> {
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

fn chunks_to_text(chunks: Vec<u64>) -> String {
    let mut letters: Vec<u8> = Vec::new();

    for mut chunk in chunks {
        while chunk != 0 {
            letters.push((chunk % (u8::MAX as u64 + 1)) as u8);
            chunk >>= 8;
        }
    }

    println!("{:?}", letters);

    if let Ok(string) = String::from_utf8(letters) {
        string
    }
    else {
        panic!("conversion error")
    }
}

#[cfg(test)]
mod tests {
    use crate::*;
    use crate::diffie_hellman::*;
    #[test]
    fn diffie_hellman_test() {
        let secret_a = gen_secret();
        let secret_b = gen_secret();

        let A = diffie_hellman_partial(secret_a);
        let B = diffie_hellman_partial(secret_b);

        let Ka = diffie_hellman(B, secret_a);
        let Kb = diffie_hellman(A, secret_b);

        assert_eq!(Ka, Kb);
    }

    #[test]
    fn chunk_text_test() {
        let text = String::from("hello world");

        let correct: Vec<u64> = vec![8031924123371070824,6581362];
        assert_eq!(text_to_chunks(text), correct);
    }


    #[test]
    #[should_panic]
    fn chunk_text_fail_test() {
        let text = String::from("hello world");

        let correct: Vec<u64> = vec![803192412337100824,658136];
        assert_eq!(text_to_chunks(text), correct);
    }


    #[test]
    fn chunk_text_and_back_test() {
        let text = String::from("hello world");

        let chunks = text_to_chunks(text.clone());

        assert_eq!(text, chunks_to_text(chunks));
    }
}
