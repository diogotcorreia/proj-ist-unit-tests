use std::{thread, time::Duration};

use common::utils::{open_client, PlayerCommand};

mod common;

#[test]
fn test_sample() {
    let mut client = open_client();
    client.run_command(PlayerCommand::Start("099211".to_string()));
    thread::sleep(Duration::from_secs(2));
    client.run_command(PlayerCommand::Play('a'));
    client.run_command(PlayerCommand::Exit);
    thread::sleep(Duration::from_secs(5));
    client.assert_exited_cleanly();
}
