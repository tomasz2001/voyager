import Region "mo:base/Region";
import Text "mo:base/Text";
import Option "mo:base/Option";
import Nat "mo:base/Nat";
import HashMap "mo:base/HashMap";
import Principal "mo:base/Principal";

actor {

  var vmesage = HashMap.HashMap<Principal, Vmail>(10, Principal.equal, Principal.hash);

  type Vmail = {
    input: Principal;
    mesage: Text;
  };

  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
    
  };

  public query func hwoisme() : async Conn{
       return {
        conn = "bkxiq-haaaa-aaaad-abo5q-cai";
        title = "this si V-MESSAGE welcome to first messenger on the Voyager system";
        conector = ["glue", "chip", "help"];
       };
  };



  // glue interface func 

  public shared query (msg) func glue_get(get : [Text]) : async Text{
  let caller = msg.caller;
  switch(get[0]){
    
    case("watch"){
     if(vmesage.get(caller) == null){ return "you mail box is empty";};
     return "PUSH";

    };
    case("say"){
      if(get.size() <= 2){return "plesse add all input";};
      return "PUSH";
    };
    case(_){
     return "NULL";

    }
  };
  };
  
  public shared (msg) func glue_push(push : [Text]) : async Text {
  let caller = msg.caller;
  switch(push[0]){
    case("say"){
    if(push.size() <= 2){return "plesse add all input";};
      let principalText = push[1];
      let principal_get : Principal = Principal.fromText(principalText);
      
      if(vmesage.get(principal_get) != null){
        return "boxmails is not empty plesse try later";

      }else{
        let get : Vmail = {
          input = caller;
          mesage = push[2];
        };
        vmesage.put(Principal.fromText(push[1]), get);
        return "ok";

      };
    };
    case("watch"){
      let info = vmesage.get(caller);
        switch (info) {
          case (?info) {
            vmesage.delete(caller);
            return "--from-- \n \n" # Principal.toText(info.input) # "\n" # "--mesage-- \n \n" # info.mesage;
          };
          case null {
            return "you mail box is empty";
          };
        };
    };
  };
    
    
    
  };
   // chip interface func 
  public shared query (msg) func chip(get : Text) : async Text{
    let caller = msg.caller;
    if(get == "query"){
      let info = vmesage.get(caller);
      switch (info) {
          case (?info) {
            return "mail_get";
          };
          case null {
            return "mail_empty";
          };
        };
    };
    return "NULL";
  };
  public shared (msg) func chip_up(get : Text) : async Text{
    let caller = msg.caller;
    if(get == "mail"){
       let info = vmesage.get(caller);
        switch (info) {
          case (?info) {
            vmesage.delete(caller);
            return "from: " # Principal.toText(info.input) # "mesage: " # info.mesage;
          };
          case null {
            return "mail_empty";
          };
        };
    };  
    return "NULL";

  };
  // help interface func 
  public query func help(line : Nat) : async Text{
    
    switch(line){
     case(0){return "this is Vmesage \n help:1 help for glue interface \n help:2 help for chip interface";};
     case(1){return "  glue help \n [watch] check and clear your mail box \n [say] [pripical target] [text mesage] sey masage ";};
     case(2){return "  chip help \n [?query] [^mail] chceck and clear-watch your mail box perfect to make virtual mail-box for arduino or pi-zero";};
    

     case(_){return "NULL";};

    };
    
  };

};