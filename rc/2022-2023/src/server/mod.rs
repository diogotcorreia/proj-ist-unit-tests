use std::path::PathBuf;

mod server;
mod start_cmd;

pub fn init(_client_executable: PathBuf) {
    run_test!("Sample test", start_cmd::test(_client_executable));
}
