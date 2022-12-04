use std::path::PathBuf;
use structopt::StructOpt;

#[macro_use]
mod common;
mod server;

/// Test RC's 2022/2023 project with a rogue server and client
#[derive(StructOpt, Debug)]
#[structopt(name = "rc2223-tests")]
#[allow(dead_code)] // TODO remove this
enum Opt {
    /// Run this test server, as a way to test the developed client
    Server {
        #[structopt(name = "CLIENT_PATH", parse(from_os_str))]
        client_executable: PathBuf,
    },
    /// Run this test client, as a way to test the developed server
    Client {
        #[structopt(name = "SERVER_PATH", parse(from_os_str))]
        server_executable: PathBuf,
    },
}

fn main() {
    let opt = Opt::from_args();
    println!("{:#?}", opt);

    match opt {
        Opt::Server { client_executable } => server::init(client_executable),
        _ => unimplemented!("That feature is not implemented yet!"),
    }
}
