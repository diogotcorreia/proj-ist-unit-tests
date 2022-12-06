use std::fmt::Display;

pub enum ServerboundMsg {
    Start { player_id: [u8; 6] },
    Custom(String),
}

pub enum ClientboundMsg {
    Start(StartStatus),
    Custom(String),
}

pub enum StartStatus {
    Ok { word_length: u8, max_errors: u8 },
    NotOk,
}

impl ToString for ServerboundMsg {
    fn to_string(&self) -> String {
        match self {
            Self::Start { player_id } => format!("SNG {}\n", String::from_utf8_lossy(player_id)),
            Self::Custom(content) => content.clone(),
        }
    }
}

impl ToString for ClientboundMsg {
    fn to_string(&self) -> String {
        match self {
            Self::Start(status) => format!("RSG {}\n", status),
            Self::Custom(content) => content.clone(),
        }
    }
}

impl Display for StartStatus {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Ok {
                word_length,
                max_errors,
            } => write!(f, "OK {} {}", word_length, max_errors),
            Self::NotOk => write!(f, "NOK"),
        }
    }
}
