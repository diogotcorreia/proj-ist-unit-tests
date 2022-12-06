use std::net::{SocketAddr, UdpSocket};

use crate::common::{
    errors::Error,
    messages::{ClientboundMsg, ServerboundMsg},
};

/// Rogue server implementation to test a well-behaving client
pub struct GameServer {
    udp_socket: UdpSocket,
}

impl GameServer {
    pub fn new() -> GameServer {
        let udp_socket = UdpSocket::bind("127.0.0.1:58000")
            .expect("Failed to bind to port 58000 (is it already in use?).");

        GameServer { udp_socket }
    }

    pub fn wait_for_message(&self, message: ServerboundMsg) -> Result<SocketAddr, Error> {
        let mut buf = [0u8; 256];
        let (bytes_read, addr) = self.udp_socket.recv_from(&mut buf)?;
        let buf = Vec::from(&buf[0..bytes_read]);

        let message = message.to_string().into_bytes();

        if buf != message {
            Err(Error::MessageMismatch {
                expected: message,
                actual: buf,
            })
        } else {
            Ok(addr)
        }
    }

    pub fn send_message(&self, to: &SocketAddr, message: ClientboundMsg) -> Result<(), Error> {
        let buf = message.to_string();
        let bytes_written = self.udp_socket.send_to(buf.as_bytes(), to)?;

        if bytes_written != buf.len() {
            Err(Error::Other(
                "Written bytes to UDP socket don't match total bytes",
            ))
        } else {
            Ok(())
        }
    }
}
