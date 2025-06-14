import Buffer "mo:base/Buffer";
import Text "mo:base/Text";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";
import Option "mo:base/Option";

// every one here is chaos plesse dont reat wait to new update 

actor {

  var table = Buffer.Buffer<Post>(15);

  type Post = {
   nick: Text;
   post: Text;
   aart: Text;

  };

  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  public query func hwoisme() : async [Conn]{
       return [ {
        conn = "adress aplication";
        title = "Hello to voyager chat /-/ this is ascii art chan on voyager technology";
        conector = ["glue", "help"];
       }
       ];
  };

  // glue interface func 
  public query func glue_get(get : [Text]) : async Text{
  switch(get[0]){
    case("watch"){
      if (get.size() <  1){
        return "plesse ad nuber post value";
      };
      let target = Nat.fromText(get[1]); 
      var targett : Nat = Option.get(target, 0);
      if (targett < table.size()){   
        targett := table.size() - targett;
        let point = table.get(targett);
        return point.nick # "\n" # point.post # "\n" # point.aart;

      }else{
       return"post not exist";
 
      };
    };
    case("post"){
     return "PUSH";

    };
    case(_){
     return "NULL";

    }
  };

   
  };
  // glue interface func 
  public func glue_push(push : [Text]) : async Text{
  return "Hello";

  };

  // help interface func 
  public query func help(line : Int) : async Text{
    
    switch(line){
     case(0){return "Hello to voyager-chan /-/ this is ascii art chan on voyager technology";};
     case(1){return "intervace glue help 
     /[watch] [nuber] watch post
     /[post] [nick] [text] [ascii-art] add new post";};
     case(2){return "";};
     case(_){return "NONE";}

    };
    
  };
};