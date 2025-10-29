import Buffer "mo:base/Buffer";
import Blob "mo:base/Blob";
import Error "mo:base/Error";

persistent actor {

transient var data_clasters_A = Buffer.Buffer<Blob>(0);
transient var pin_clasters_A = Buffer.Buffer<File_pin>(5);


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
        title = "freedom file";
        conector = ["glue", "help", "file"];
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
};