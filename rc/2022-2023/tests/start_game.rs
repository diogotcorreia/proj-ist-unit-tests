use rc2223_tests::common::{
    errors::Error,
    messages::{ClientboundMsg, ServerboundMsg, StartStatus},
};
use rstest::*;
use std::{thread, time::Duration};

use common::utils::{setup_client_test, PlayerCommand};

mod common;

#[test]
fn starts_game_correctly() -> Result<(), Error> {
    let (mut client, server) = setup_client_test();

    client.run_command(PlayerCommand::Start("000123".to_string()));
    let addr = server.wait_for_message(ServerboundMsg::Start {
        player_id: *b"000123",
    })?;
    server.send_message(
        &addr,
        ClientboundMsg::Start(StartStatus::Ok {
            word_length: 6,
            max_errors: 8,
        }),
    )?;

    thread::sleep(Duration::from_secs(1));

    client.assert_alive()?;

    client.kill()
}

#[rstest]
#[case("RSG AAAAA\n")]
#[case("")]
#[case("RSG OK 5 8")] // missing \n
fn does_not_crash_with_incorrect_response(#[case] response: String) -> Result<(), Error> {
    let (mut client, server) = setup_client_test();

    client.run_command(PlayerCommand::Start("000123".to_string()));
    let addr = server.wait_for_message(ServerboundMsg::Start {
        player_id: *b"000123",
    })?;
    server.send_message(&addr, ClientboundMsg::Custom(response))?;
    client.assert_alive()?;

    client.run_command(PlayerCommand::Exit);
    thread::sleep(Duration::from_millis(500));
    // Game should not have started, therefore it should immediately exit

    client.assert_exited_cleanly()
}
