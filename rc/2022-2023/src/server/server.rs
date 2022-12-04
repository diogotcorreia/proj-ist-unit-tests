use std::{
    io::Write,
    path::PathBuf,
    process::{Command, Stdio},
};

pub fn start_client(client_executable: PathBuf) {
    let mut client = Command::new(client_executable)
        .args(["-n", "localhost", "-p", "58000"])
        .stdin(Stdio::piped())
        .spawn()
        .expect("cannot run client executable");

    client.stdin.take().unwrap().write_all(b"exit").unwrap();
}
