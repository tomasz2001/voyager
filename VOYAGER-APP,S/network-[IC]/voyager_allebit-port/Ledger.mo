import Principal "mo:base/Principal";
import Blob "mo:base/Blob";

module {
    public type Account = {
        owner : Principal;
        subaccount : ?Blob;
    };

    public type Ledger = actor {
        icrc1_balance_of : (Account) -> async Nat;
    };
}