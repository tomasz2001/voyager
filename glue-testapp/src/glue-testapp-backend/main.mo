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

  public query func hwoisme() : async Conn{
       return {
        conn = "iruwa-4iaaa-aaaam-aemaq-cai";
        title = "Hello to voyager chat /-/ this is ascii art chan on voyager technology";
        conector = ["glue", "help"];
       }
       ;
  };

  // glue interface func 
  public query func glue_get(get : [Text]) : async Text{
  switch(get[0]){
    case("watch"){
      if (get.size() < 1){
        return "plese ad nuber post value";
      };
      let target = Nat.fromText(get[1]); 
      var targett : Nat = Option.get(target, 0);
      if (targett < table.size()){   
        targett := table.size() - targett - 1;
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
  public func glue_push(push : [Text]) : async Text {
    switch (push[0]) {
        case ("post") {
            var aart_lines : Text = "";
            var i = 3;
            while (i < push.size()) {
                aart_lines := aart_lines # push[i] # "\n";
                i += 1;
            };
            let post_push: Post = {
                nick = push[1];
                post = push[2];
                aart = aart_lines;
            };
            table.add(post_push);
            return "post added";
        };
        case (_) {
            return "NULL";
        };
    };
};
  // help interface func 
  public query func help(line : Nat) : async Text{
    
    switch(line){
     case(0){return "Hello to voyager-chan /-/ this is ascii art chan on voyager technology";};
     case(1){return "intervace glue help 
     /watch] [nuber] watch post
     /post] [nick] [text] [ascii-art] add new post";};
     case(_){return "NULL";}

    };
    
  };



};