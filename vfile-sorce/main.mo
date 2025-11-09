import Buffer "mo:base/Buffer";
import Blob "mo:base/Blob";
import Error "mo:base/Error";
import ExperimentalCycles "mo:base/ExperimentalCycles";
import Time "mo:base/Time";

persistent actor {

transient var data_clasters_A = Buffer.Buffer<Blob>(5);
transient var pin_clasters_A = Buffer.Buffer<File_pin>(5);
transient var wallet_one : wallet = {
  trap_time = 0;
  adress = "";
  margin = 0;
};
 type wallet = {
  trap_time: Int;
  adress: BitcoinAddress;
  margin: Satoshi;
 };
 type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  type File_pin = {
    name: Text; // np video.mp4
    file_note: Text; // np "this is video fish dance"
    file_line: [Nat]; // id file bit data claster`s
  };

  transient let management_canister_actor : ManagementCanisterActor = actor("aaaaa-aa");
  transient let GET_BALANCE_COST_CYCLES : Nat = 100_000_000;

  type Network = { #mainnet; #testnet; #regtest };
    type BitcoinAddress = Text;
    type Satoshi = Nat64;

    
    type GetBalanceRequest = {
        address : BitcoinAddress;
        network : Network;
        min_confirmations : ?Nat32;
    };

    type ManagementCanisterActor = actor {
        bitcoin_get_balance : GetBalanceRequest -> async Satoshi;
    };

    

  
  public query func hwoisme() : async Conn{
       return {
        conn = "";
        title = "free-file run on voyager power by freedom";
        conector = ["glue", "help", "file", "help"];
       };
  };

  public query func query_pin(target : Nat) : async File_pin{
   if(target <= pin_clasters_A.size() - 1){
      return pin_clasters_A.get(target)
   }else{
    return {
    name = "ERROR"; 
    file_note = "ERROR"; 
    file_line = [];
    };
   };
    
  };
  public query func query_file(target : Nat) : async Blob{
   if (target <= data_clasters_A.size() - 1) {
      return data_clasters_A.get(target);
   } else {
      throw Error.reject("bruh");
   };

  };
public func add_pin(target : File_pin) : async Nat {
  pin_clasters_A.add(target);
  return pin_clasters_A.size() - 1;
};

public func add_file(target : Blob) : async Nat {
  data_clasters_A.add(target);
  return data_clasters_A.size() - 1;
};

// BTC funk

    private func btc_get_balance(network : Network, address : BitcoinAddress) : async Satoshi {
        ExperimentalCycles.add<system>(GET_BALANCE_COST_CYCLES);
        await management_canister_actor.bitcoin_get_balance({
            address = address;
            network = network;
            min_confirmations = null;
        })
    };

  
};