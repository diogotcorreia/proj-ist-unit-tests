use std::{thread, time::Duration};

use common::utils::open_client;

mod common;

#[test]
fn test_sample() {
    let mut client = open_client();
    client.write_stdin(b"start 99211\n");
    thread::sleep(Duration::from_secs(2));
    //client.write_stdin(b"play a\n");
    client.write_stdin(b"exit\n");
    thread::sleep(Duration::from_secs(50));
    client.close();
}
