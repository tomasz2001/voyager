import Buffer "mo:base/Buffer";
import Principal "mo:base/Principal";
import Text "mo:base/Text";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";
import Hash "mo:base/Hash";


//                                   B^                                 
//                                 .J@B~        !^                      
//                                 J@@@&.     ^P!.                      
//                                #@@@@@@:   ~7                         
//                              ~#@@@@@@@&Y.                            
//                          .J?#@@@@@@@@@@@@JJ!                         
//             :::::   ::~&#@@@@@@@@@@@@@@@@@@@#&5::   .::::::::::      
//            .JJJJJ   ?JP@@@@@@@@@@@@@@@@@@@@@@@&?J.  !JJJJJJJJJJ.     
//                        ..7&#@@@@@@@@@@@@@&&G..                       
//                             ^P@@@@@@@@@#7                            
//                           :   .&@@@@@@!                              
//                         7J7    ~B@@@@?                               
//                      .!P^       ^&@&5                                
//                     JJ~           @!                                 
//                  :75:             .                                  
//                .Y?^                                                  
//               !Y.

actor {


    type Cyber_pen = {   // pojedynczy zapis o informacji pisu z hash korzystać z [Buffer]
    vapp: Principal;
    user: Principal;
    hash: Nat32;
    key: Text;

  }; 
  type Cyber_paper = {  // pojedynczy zapis danej aplikacji [hashmap-Pripical voyager-app]
    trust_add: Nat32;
    trust_rem: Nat32;

  };
  type Cyber_book = {  // pojedynczy zapis danej aplikacji [hashmap-Pripical voyager-databox]
    trust: Bool;
    
  };

  // Główny administrator systemu / Root admin of the system
  let root : Principal = Principal.fromText("0000-0000");
 
  // Bufor przechowujący inne Voyagery / Buffer for other Voyager data boxes
  var frend = Buffer.Buffer<Voyager>(15);

  // Bufor przechowujący testowe URL-e / Buffer for storing test URLs
  var app = Buffer.Buffer<Conn>(50);


  // Struktura pojedynczego Voyagera / Data structure for a Voyager node
  type Voyager = { 
    conn: Text;
    title: Text;
    conector: [Text];
  };

  // Struktura pojedynczego URL-a / Data structure for a single URL
  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };
  // Prosta informacja o systemie / Basic system info
  public query func help(line : Nat) : async Text{
    
    switch(line){
     case(0){return "this databox voyager is bulding plesse wait to next update";};
     case(_){return "NULL";}

    };
  };

   public query func hwoisme() : async Conn{
       return {
        conn = "--";
        title = "this is a voyager-databox";
        conector = ["one", "help"];
       }
       ;
  };
  // Funkcja zapytania o konkretnego Voyagera-databox / Query a specific Voyager-databox
  public query func frend_one(target: Nat): async Voyager {
    if ( frend.size() > target ) { 
      return frend.get(target);

    } else {
      return {
        conn = "NULL";
        title = "NULL";
        conector = ["NULL"];
      };
    };
  };

  // Funkcja zapytania o konkretny conn / Query a specific conn
  public query func conn_one(target: Nat): async Conn {
    if ( app.size() > target ) {
      return app.get(target);

    } else {
      return {
        conn = "NULL";
        title = "NULL";
        conector = ["NULL"];
      };
    };
  };

  // Publiczna funkcja dodająca Voyagera / Public function to add a Voyager
  public func frend_add(connn: Text, titlee: Text, conectorr: [Text]): async Text {
    let make: Voyager = {
      conn = connn;
      title = titlee;
      conector = conectorr
    };
    ignore frend.add(make);
    return "Dodano VOYAGER DATA BOX / Voyager data box added";
  };

  // Publiczna funkcja dodająca conn / Public function to add a conn
  public func conn_add(connn: Text, titlee: Text, conectorr: [Text]): async Text {
    let make: Conn = {
      conn = connn;
      title = titlee;
      conector = conectorr;
    };
    ignore app.add(make);
    return "Dodano APP / APP added";
  };

  // Funkcja administracyjna do zarządzania danymi / Admin function for managing data
  public shared (msg) func moderator(line: Text, target: Nat): async Text {

    if(root == Principal.fromText("0000-0000")){
      return("this element is anarhic - not have root principal")
    };

    let caller_principal = msg.caller;

    if (caller_principal == root) {

      if (line == "conn") {
        ignore app.remove(target);
        return "Dostęp przyznany – zadanie wykonane / Access granted – task completed";
      };

      if (line == "frend") {
        ignore frend.remove(target);
        return "Dostęp przyznany – zadanie wykonane / Access granted – task completed";
      };

      return "Dostęp przyznany – nieobsługiwana komenda / Access granted – command not supported";
    } else {
      return "Brak dostępu / Access denied";
    };
  };
};