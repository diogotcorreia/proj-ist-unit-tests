use colored::Colorize;
use std::{fmt::Debug, io, process::ExitStatus};

pub enum Error {
    IoError(io::Error),
    LengthMismatch { expected: usize, actual: usize },
    MessageMismatch { expected: Vec<u8>, actual: Vec<u8> },
    Exited(ExitStatus),
    Other(&'static str),
}

impl Debug for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::IoError(error) => write!(f, "I/O error: {error:#?}"),
            Self::LengthMismatch { expected, actual } => write!(
                f,
                "Message length ({actual:#?}) does not match expected ({expected:#?})"
            ),
            Self::MessageMismatch { expected, actual } => {
                f.write_str("Message does not match expected content\n")?;
                f.write_fmt(format_args!(
                    "{} {}\n",
                    "Expected:".green(),
                    format!("{:?}", String::from_utf8_lossy(expected)).green()
                ))?;
                f.write_fmt(format_args!(
                    "{} {}",
                    "Actual:  ".red(),
                    format!("{:?}", String::from_utf8_lossy(actual)).red()
                ))
            }
            Self::Exited(status) => {
                write!(f, "Process exited with code: {:?}", status)
            }
            Self::Other(message) => write!(f, "{message}"),
        }
    }
}

impl From<io::Error> for Error {
    fn from(error: io::Error) -> Self {
        Self::IoError(error)
    }
}
