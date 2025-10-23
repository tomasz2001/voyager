import Buffer "mo:base/Buffer";
import Blob "mo:base/Blob";


persistent actor {

  stable var data_clasters_A : [Blob] = [];
  stable var pin_clasters_A : [File_pin] = [];

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


  
  public query func hwoisme() : async Conn{
       return {
        conn = "";
        title = "this si V-MESSAGE welcome to first messenger on the Voyager system";
        conector = ["glue", "help", "file"];
       };
  };

  public query func query_pin(target : Nat) : async File_pin{
    try{

    }
    
  };
  public query func query_file(target : Nat) : async Blob{
    try{

    }
    
  };
  public func add_pin(target : File_pin) : async Nat{
    try{

    }
    
  };
  public func add_file(target : Blob) : async Nat{
    try{

    }
    
  };
};

