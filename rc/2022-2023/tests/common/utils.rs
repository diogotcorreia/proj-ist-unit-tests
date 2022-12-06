use std::{
    env,
    io::Write,
    path::PathBuf,
    process::{Child, Command, Stdio},
    str::FromStr,
};

pub struct ChildWrapper(Child);

impl ChildWrapper {
    pub fn write_stdin(&mut self, message: &[u8]) {
        self.0
            .stdin
            .as_mut()
            .expect("process has already exited")
            .write_all(message)
            .expect("I/O error interacting with client process");
    }

    pub fn close(&mut self) {
        self.0
            .kill()
            .expect("failed to kill project, it has exited prematurely");
    }
}

pub fn open_client() -> ChildWrapper {
    let client_executable = env::var("CLIENT_EXECUTABLE")
        .expect("You should pass a 'CLIENT_EXECUTABLE' environment variable");
    let client_executable =
        PathBuf::from_str(&client_executable).expect("CLIENT_EXECUTABLE is not a valid path");

    let client = Command::new(client_executable)
        .args(["-n", "localhost", "-p", "58000"])
        //.stdout(Stdio::null())
        .stdin(Stdio::piped())
        .spawn()
        .expect("cannot run client executable");

    ChildWrapper(client)
}
