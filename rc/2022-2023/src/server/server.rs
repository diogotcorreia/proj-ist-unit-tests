use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};

use crate::common::{
    errors::Error,
    messages::{ClientboundMsg, ServerboundMsg},
};

/// Rogue server implementation to test a well-behaving client
pub struct GameServer {
    pub port: u16,
    udp_socket: UdpSocket,
}

impl GameServer {
    pub fn new() -> GameServer {
        let addr = SocketAddrV4::new(Ipv4Addr::LOCALHOST, 0);
        let udp_socket = UdpSocket::bind(addr).expect("Failed to bind to port.");

        let port = udp_socket.local_addr().unwrap().port();

        GameServer { port, udp_socket }
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
