import Buffer "mo:base/Buffer";
import Principal "mo:base/Principal";
import Text "mo:base/Text";
import Option "mo:base/Option";
import Nat "mo:base/Nat";
import Hash "mo:base/Hash";

var file = Buffer.Buffer<file_box>(25);

var news = Buffer.Buffer<post>(25);

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
    maker: Principal;
    title: Text;
    text: Text;
    uf: [Nat];
};


actor {
  public query func glue_get(get : [Text]) : async Text{
  switch(get[0]){
    case("watch"){
      if (get.size() < 1){
        return "plese ad nuber post value";
      };
      let target = Nat.fromText(get[1]); 
      var targett : Nat = Option.get(target, 0);
      if (targett < news.size()){   
        targett := news.size() - targett - 1;
        let point = news.get(targett);
        
        return "_" # Principal.toText(point.maker) # "_" # "\n" # point.title # "\n" # "\n" # point.text;

      }else{
       return"post not exist";
 
      };
    };
    //case("post"){
    // return "PUSH";

    //};
    case(_){
     return "NULL";

    };
  };

   
  };
      // make it
  public query func tracker_file(command : Text, get : Nat) : async [Nat]{
   switch(command){
    case("watch"){
      let target = (get); 
      if (target < news.size()){   
        let targett = news.size() - target;
        let point = news.get(targett);
        
        return point.uf;

      }else{
       return [0];

      };
    };
    case(_){
      return [0];
      
    };
   };
  };
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
