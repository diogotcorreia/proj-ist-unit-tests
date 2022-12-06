use std::{
    env,
    io::Write,
    path::PathBuf,
    process::{Child, Command, Stdio},
    str::FromStr,
};

pub struct PlayerWrapper(Child);

impl PlayerWrapper {
    pub fn write_stdin(&self, message: &[u8]) {
        self.0
            .stdin
            .as_ref()
            .expect("process has already exited")
            .write_all(message)
            .expect("I/O error interacting with client process");
    }

    pub fn run_command(&self, command: PlayerCommand) {
        self.write_stdin(command.to_string().as_bytes());
    }

    pub fn assert_exited_cleanly(&mut self) {
        match self.0.try_wait() {
            Ok(Some(code)) => {
                if !code.success() {
                    panic!(
                        "Player process has exited with non-zero code: {}",
                        code.code().unwrap_or(-1)
                    );
                }
            }
            Ok(None) => panic!("Player process has not exited like intended"),
            Err(e) => panic!(
                "Error while checking if player process exited cleanly: {}",
                e
            ),
        }
    }
}

impl Drop for PlayerWrapper {
    fn drop(&mut self) {
        match self.0.kill() {
            Ok(..) => println!("Player process was still running, but it was killed"),
            _ => {}
        };
    }
}

pub enum PlayerCommand {
    Start(String),
    Play(char),
    Guess(String),
    Scoreboard,
    Hint,
    Quit,
    Exit,
    Reveal,
}

impl ToString for PlayerCommand {
    fn to_string(&self) -> String {
        match self {
            Self::Start(player_id) => format!("start {}\n", player_id),
            Self::Play(letter) => format!("play {}\n", letter),
            Self::Guess(word) => format!("guess {}\n", word),
            Self::Scoreboard => "scoreboard\n".to_string(),
            Self::Hint => "hint\n".to_string(),
            Self::Quit => "quit\n".to_string(),
            Self::Exit => "exit\n".to_string(),
            Self::Reveal => "reveal\n".to_string(),
        }
    }
}

pub fn open_client() -> PlayerWrapper {
    let client_executable = env::var("CLIENT_EXECUTABLE")
        .expect("You should pass a 'CLIENT_EXECUTABLE' environment variable");
    let client_executable =
        PathBuf::from_str(&client_executable).expect("CLIENT_EXECUTABLE is not a valid path");

    let client = Command::new(client_executable)
        .args(["-n", "localhost", "-p", "58000"])
        .stdout(Stdio::null())
        .stdin(Stdio::piped())
        .spawn()
        .expect("cannot run client executable");

    PlayerWrapper(client)
}
