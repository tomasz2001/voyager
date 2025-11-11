import Buffer "mo:base/Buffer";
import Region "mo:base/Region";
import Option "mo:base/Option";
import Text "mo:base/Text";
import Blob "mo:base/Blob";
import Error "mo:base/Error";
import ExperimentalCycles "mo:base/ExperimentalCycles";
import Time "mo:base/Time";
import Principal "mo:base/Principal";
import Nat64 "mo:base/Nat64";

persistent actor {

transient var data_clasters_A = Buffer.Buffer<Blob>(5);
transient var pin_clasters_A = Buffer.Buffer<File_pin>(5);

transient var wallet_one : wallet = {
  payer = Principal.fromText("aaaaa-aa");
  trap_time = 0;
  address = "";
  margin = 0;
};

 type wallet = {
  payer: Principal;
  trap_time: Int;
  address: BitcoinAddress;
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
        title = "free-file run on voyager power by freedom \n plesse use vBp pay by donate voyager project";
        conector = ["vBp", "help", "file"];
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

    private func btc_get_balance(address : BitcoinAddress) : async Satoshi {
        ExperimentalCycles.add<system>(GET_BALANCE_COST_CYCLES);
        await management_canister_actor.bitcoin_get_balance({
            address = address;
            network = #mainnet;
            min_confirmations = null;
        })
    };
    public func btc_get_balance_debug(address : BitcoinAddress) : async Satoshi {
        ExperimentalCycles.add<system>(GET_BALANCE_COST_CYCLES);
        await management_canister_actor.bitcoin_get_balance({
            address = address;
            network = #mainnet;
            min_confirmations = null;
        })
    };

    public shared (msg) func pay_start() : async Text{

      var now = Time.now();
      var margin = await btc_get_balance(wallet_one.address);

      if(now > wallet_one.trap_time){
          return "pay Bitcoin address is busy, plesse try later";
      };
      wallet_one := {
        payer = msg.caller;
        trap_time = now + 600_000_000_000;
        address = wallet_one.address;
        margin = margin;
      };
      return "pay Bitcoin address is ready to pay plesse say here you Bitcoin \n" # wallet_one.address;
    };

    public shared (msg) func pay_end() : async Text{ 
      var now = Time.now();
      var pay = await btc_get_balance(wallet_one.address);
      
      if(wallet_one.payer == msg.caller){
        if(wallet_one.margin == pay){
          
          wallet_one := {
            payer = wallet_one.payer;
            trap_time = now + 600_000_000_000;
            address = wallet_one.address;
            margin = wallet_one.margin;
          };
          return "app wait to pay";
        }else{
          wallet_one := {
            payer = wallet_one.payer;
            trap_time = 0;
            address = wallet_one.address;
            margin = wallet_one.margin;
          };
          var to_pay = pay - wallet_one.margin;
          return "thank you for pay " # Nat64.toText(to_pay) # "  for this app";
        };
      }else{
        return "you are not have active pay";

      };
    };
  
};