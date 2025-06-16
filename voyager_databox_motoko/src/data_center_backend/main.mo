import Buffer "mo:base/Buffer";
import Principal "mo:base/Principal";
import Text "mo:base/Text";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";

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

  // Główny administrator systemu / Root admin of the system
  let root : Principal = Principal.fromText("ilqyx-par5p-y6cnk-rufql-xqhgw-tzpw4-bsbih-knin6-ui74t-aji5h-oqe");
 
  // Bufor przechowujący inne Voyagery / Buffer for other Voyager data boxes
  var frend = Buffer.Buffer<Voyager>(15);

  // Bufor przechowujący testowe URL-e / Buffer for storing test URLs
  var app = Buffer.Buffer<Conn>(50);

  // Struktura pojedynczego Voyagera / Data structure for a Voyager node
  type Voyager = { 
    conn: Text;
    mode: Text;
  };

  // Struktura pojedynczego URL-a / Data structure for a single URL
  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  // Prosta informacja o systemie / Basic system info
  public query func info() : async Text {
    return "HELLO WORLD";
  };

  // Funkcja zapytania o konkretnego Voyagera-databox / Query a specific Voyager-databox
  public query func frend_one(target: Nat): async Voyager {
    if ( frend.size() > target ) { 
      return frend.get(target);

    } else {
      return {
        conn = "NULL";
        mode = "NULL";
      };
    };
  };

  // Funkcja zapytania o konkretny voyager-app / Query a specific voyager-app
  public query func conn_one(target: Nat): async Conn {
    if ( app.size() > target ) {
      return app.get(target);

    } else {
      return {
        conn = "NULL";
        title = "NULL";
        conector = ["NULL"]
      };
    };
  };

  // Publiczna funkcja dodająca Voyagera / Public function to add a Voyager
  public func frend_add(connn: Text, modee: Text): async Text {
    let make: Voyager = {
      mode = modee;
      conn = connn;
    };
    ignore frend.add(make);
    return "Dodano VOYAGER DATA BOX / Voyager data box added";
  };

  // Publiczna funkcja dodająca URL / Public function to add a URL
  public func conn_add(connn: Text, titlee: Text, conecto: [Text]): async Text {
    let make: Conn = {
      conn = connn;
      title = titlee;
      conector = conecto;
    };
    ignore app.add(make);
    return "Dodano URL / URL added";
  };

  // Funkcja administracyjna do zarządzania danymi / Admin function for managing data
  public shared (msg) func moderator(line: Text, target: Nat): async Text {

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