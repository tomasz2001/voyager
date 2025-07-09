import Buffer "mo:base/Buffer";
import Principal "mo:base/Principal";
import Text "mo:base/Text";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";
import Hash "mo:base/Hash";

var file = Buffer.Buffer<file_box>(25);



let root : Principal = Principal.fromText("ilqyx-par5p-y6cnk-rufql-xqhgw-tzpw4-bsbih-knin6-ui74t-aji5h-oqe");

type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
};
type file_box = {
    fd: ?Blob;
    ft: ?Text;
};
type post = {
    maker: ?Principal;
    title: Text;
    text: Text;
    uf: [Nat];
};


actor {
  
  //moderate file
  public shared (msg) func file_moderator(target: Nat): async Text{

    let caller_principal = msg.caller;

    if (caller_principal == root) {
      if (target >= file.size()){
        return "size error";
      }else{
        let fr : file_box = { fd = null; ft = null };
        file.put(target, fr);
        return "remove file done";
      };
    }else{
      return "Brak dostępu / Access denied";
    }
  };
  //add file
  public func file_add(add: file_box): async Nat{
    file.add(add);
    return file.size();
    };
  
  //query file 
  public query func file_one(target: Nat): async file_box{
    if ( file.size() > target ) {
      return file.get(target);

    } else {
      return {
        ft = null;
        fd = null;
        
      };
    };
  };

  public query func help(line : Nat) : async Text{
    
    switch(line){
     case(0){return "this realy freedom media [blue-lotos] use [BP]";};
     case(_){return "NULL";}

    };
  };

   public query func hwoisme() : async Conn{
       return {
        conn = "--";
        title = "this realy freedom media [blue-lotos] use [BP]format";
        conector = ["NP", "help", "file", "glue"];
       }
       ;
  };
};
