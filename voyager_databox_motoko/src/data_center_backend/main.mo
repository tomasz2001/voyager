import Buffer "mo:base/Buffer";
import Principal "mo:base/Principal";
import Text "mo:base/Text";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";
import Blob "mo:base/Blob";

actor {

  // Główny administrator systemu / Root admin of the system
  let root : Principal = Principal.fromText("ilqyx-par5p-y6cnk-rufql-xqhgw-tzpw4-bsbih-knin6-ui74t-aji5h-oqe");
 
  // Bufor przechowujący inne Voyagery / Buffer for other Voyager data boxes
  let frend = Buffer.Buffer<Voyager>(15);

  // Bufor przechowujący testowe URL-e / Buffer for storing test URLs
  var url = Buffer.Buffer<Con_url>(50);

  // Struktura pojedynczego Voyagera / Data structure for a Voyager node
  type Voyager = { 
    mode: Text;
    conn: Text; 
  };

  // Struktura pojedynczego URL-a / Data structure for a single URL
  type Con_url = {
    conn: Text;
    title: Text;
  };

  // Prosta informacja o systemie / Basic system info
  public query func info() : async Text {
    return "HELLO WORLD";
  };

  // Funkcja zapytania o konkretnego Voyagera / Query a specific Voyager
  public query func frend_one(target: Nat): async Voyager {
    return frend.get(target);
  };

  // Funkcja zapytania o konkretny URL / Query a specific URL
  public query func url_one(target: Nat): async Con_url {
    return url.get(target);
  };

  // Publiczna funkcja dodająca Voyagera / Public function to add a Voyager
  public func frend_add(modee: Text, connn: Text): async Text {
    let make: Voyager = {
      mode = modee;
      conn = connn;
    };
    ignore frend.add(make);
    return "Dodano VOYAGER DATA BOX / Voyager data box added";
  };

  // Publiczna funkcja dodająca URL / Public function to add a URL
  public func url_add(connn: Text, titlee: Text): async Text {
    let make: Con_url = {
      conn = connn;
      title = titlee;
    };
    ignore url.add(make);
    return "Dodano URL / URL added";
  };

  // Funkcja administracyjna do zarządzania danymi / Admin function for managing data
  public shared (msg) func moderator(line: Text, target: Nat): async Text {

    let caller_principal = msg.caller;

    if (caller_principal == root) {

      if (line == "url") {
        ignore url.remove(target);
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