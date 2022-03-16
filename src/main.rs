
use base64;
use spl_token;
use num_enum::TryFromPrimitive;

fn main() {
    let data = base64::decode(include_str!("../FvPuwBfjpjxzELaWgNVs5Gegh5rqt4V8DRPBCjbYjMkC_base64.txt")).unwrap();
    let parsed = solana_account_decoder::parse_token::parse_token(&data, Some(0)).unwrap();
    let state0 = spl_token::state::AccountState::try_from_primitive(0).unwrap();
    let state1 = spl_token::state::AccountState::try_from_primitive(1).unwrap();
    let state2 = spl_token::state::AccountState::try_from_primitive(2).unwrap();
    println!("state0: {:?}, state1: {:?}, state2: {:?}", state0, state1, state2);
    println!("{:?}", parsed);
}

