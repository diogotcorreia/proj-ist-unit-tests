#[macro_export]
macro_rules! run_test {
    // Run a function and catch if it panics
    ($name:literal, $func:expr) => {
        use colored::Colorize;
        match std::panic::catch_unwind(|| $func) {
            Ok(()) => println!("Test '{}': {}", $name, "OK".green().bold()),
            Err(_) => println!("Test '{}': {}", $name, "FAILED".red().bold()),
        }
    };
}
