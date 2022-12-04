use std::path::PathBuf;

use pretty_assertions::assert_eq;

use crate::server::server::start_client;

pub fn test(client_executable: PathBuf) {
    start_client(client_executable);
    assert_eq!(1 + 1, 3);
}
