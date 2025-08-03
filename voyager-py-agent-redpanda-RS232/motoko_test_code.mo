import Buffer "mo:base/Buffer";
import Text "mo:base/Text";
import Option "mo:base/Option";
import Nat "mo:base/Nat";

// every one here is chaos plesse dont reat wait to new update 

actor {

  var temp : Text = "0";
  var led : Text = "on";

  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
    
  };

  public query func hwoisme() : async Conn{
       return {
        conn = "iruwa-4iaaa-aaaam-aemaq-cai";
        title = "test voyager core app";
        conector = ["chip", "help"];
       }
       ;
  };

  // glue interface func 
  public query func chip(get : Text) : async Text{
    if(get == "led"){
      return led;
    };
    if(get == "temp"){
      return temp;
    };
    return "none";
  };
  public func chip_up(get : Text) : async Text{
    if(get == "led"){
      if(led == "on"){
        led := "off";
      }else{
        led := "on";
      };
      return "led =" # led;
    };

    temp := get;
    return "new temp is now";

  };
  // help interface func 
  public query func help(line : Nat) : async Text{
    
    switch(line){
     case(0){return "this is a test core voyager/app";};
     case(_){return "NULL";}

    };
    
  };

};