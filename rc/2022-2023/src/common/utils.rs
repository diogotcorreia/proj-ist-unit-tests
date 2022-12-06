use std::net::{Ipv4Addr, SocketAddrV4, UdpSocket};

pub fn find_free_udp_port() -> Option<u16> {
    let socket = SocketAddrV4::new(Ipv4Addr::LOCALHOST, 0);
    UdpSocket::bind(socket)
        .and_then(|listener| listener.local_addr())
        .and_then(|addr| Ok(addr.port()))
        .ok()
}
