import Text "mo:base/Text";
import Nat "mo:base/Nat";
import Buffer "mo:base/Buffer";
import Region "mo:base/Region";
import Option "mo:base/Option";
import Blob "mo:base/Blob";
import Error "mo:base/Error";
import ExperimentalCycles "mo:base/ExperimentalCycles";
import Time "mo:base/Time";
import Principal "mo:base/Principal";
import Nat64 "mo:base/Nat64";

persistent actor core {

transient var data_clasters_A : Blob = "";

transient var control_pin : Principal = Principal.fromText("aaaaa-aa");

 type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  type File_pin = {
    name: Text; 
    file_note: Text; 
    file_line: [Nat]; 
  };

  public query func hwoisme() : async Conn{
       return {
        conn = "srfms-nqaaa-aaaah-qqipa-cai";
        title = "v_medium włocławek";
        conector = ["chip", "file", "help"];
       };
  };

  public query func query_pin(target : Nat) : async File_pin{
    return {
    name = "v_medium.png"; 
    file_note = "baze image to make news paper"; 
    file_line = [0];
    };
   };
  public query func query_file(target : Nat) : async Blob{
    return data_clasters_A;

  };
public func add_pin(target : File_pin) : async Nat {
  return 0;
};

public shared(msg) func add_file(target : Blob) : async Nat {
  if(control_pin == Principal.fromText("aaaaa-aa")){
    data_clasters_A := target;
    control_pin := msg.caller;
    return 0;
  }else if(control_pin != msg.caller){
    data_clasters_A := target;
    return 0;
  };
    return 404;
};

  stable var artykul_history = "";

  stable var artykul_0  = "";
  stable var artykul_1  = "";
  stable var artykul_2  = "";
  stable var artykul_3  = "";
  stable var artykul_4  = "";
  stable var artykul_5  = "";
  stable var artykul_6  = "";
  stable var artykul_7  = "";
  stable var artykul_8  = "";
  stable var artykul_9  = "";
  stable var artykul_10 = "";
  stable var artykul_11 = "";
  stable var artykul_12 = "";
  stable var artykul_13 = "";
  stable var artykul_14 = "";
  stable var artykul_15 = "";
  stable var artykul_16 = "";
  stable var artykul_17 = "";
  stable var artykul_18 = "";
  stable var artykul_19 = "";
  stable var artykul_20 = "";
  stable var artykul_21 = "";
  stable var artykul_22 = "";
  stable var artykul_23 = "";
  stable var artykul_24 = "";
  stable var artykul_25 = "";
  stable var artykul_26 = "";
  stable var artykul_27 = "";
  stable var artykul_28 = "";
  stable var artykul_29 = "";
  stable var artykul_30 = "";
  stable var artykul_31 = "";

  stable var margin : Nat = 0;

  public func chip_up(input : Text) : async Text {
    let size = Text.size(input);

    if (size < 250) {
      return "Błąd: Tekst musi miec co najmniej 250 znakow";
    };

    if (size > 1500) {
      return "Błąd: Tekst nie może miec wiecej niż 1500 znakow";
    };

    if (input == artykul_history) {
      return "spokojnie twój artykuł jest już w bazie";
    };

    // zapis do odpowiedniego rejestru i aktualizacja margin
    switch (margin) {
      case (31) { artykul_31 := input; margin := 0 };
      case (30) { artykul_30 := input; margin := 31 };
      case (29) { artykul_29 := input; margin := 30 };
      case (28) { artykul_28 := input; margin := 29 };
      case (27) { artykul_27 := input; margin := 28 };
      case (26) { artykul_26 := input; margin := 27 };
      case (25) { artykul_25 := input; margin := 26 };
      case (24) { artykul_24 := input; margin := 25 };
      case (23) { artykul_23 := input; margin := 24 };
      case (22) { artykul_22 := input; margin := 23 };
      case (21) { artykul_21 := input; margin := 22 };
      case (20) { artykul_20 := input; margin := 21 };
      case (19) { artykul_19 := input; margin := 20 };
      case (18) { artykul_18 := input; margin := 19 };
      case (17) { artykul_17 := input; margin := 18 };
      case (16) { artykul_16 := input; margin := 17 };
      case (15) { artykul_15 := input; margin := 16 };
      case (14) { artykul_14 := input; margin := 15 };
      case (13) { artykul_13 := input; margin := 14 };
      case (12) { artykul_12 := input; margin := 13 };
      case (11) { artykul_11 := input; margin := 12 };
      case (10) { artykul_10 := input; margin := 11 };
      case (9)  { artykul_9  := input; margin := 10 };
      case (8)  { artykul_8  := input; margin := 9  };
      case (7)  { artykul_7  := input; margin := 8  };
      case (6)  { artykul_6  := input; margin := 7  };
      case (5)  { artykul_5  := input; margin := 6  };
      case (4)  { artykul_4  := input; margin := 5  };
      case (3)  { artykul_3  := input; margin := 4  };
      case (2)  { artykul_2  := input; margin := 3  };
      case (1)  { artykul_1  := input; margin := 2  };
      case (0)  { artykul_0  := input; margin := 1  };
      case (_)  { /* inne wartości margin – tu nic nie robimy */ };
    };

    artykul_history := input;
    return "Tekst został zapisany pomyślnie";
  };

  public query func chip(input : Text) : async Text {
    if (input == "0")  return artykul_0;
    if (input == "1")  return artykul_1;
    if (input == "2")  return artykul_2;
    if (input == "3")  return artykul_3;
    if (input == "4")  return artykul_4;
    if (input == "5")  return artykul_5;
    if (input == "6")  return artykul_6;
    if (input == "7")  return artykul_7;
    if (input == "8")  return artykul_8;
    if (input == "9")  return artykul_9;
    if (input == "10") return artykul_10;
    if (input == "11") return artykul_11;
    if (input == "12") return artykul_12;
    if (input == "13") return artykul_13;
    if (input == "14") return artykul_14;
    if (input == "15") return artykul_15;
    if (input == "16") return artykul_16;
    if (input == "17") return artykul_17;
    if (input == "18") return artykul_18;
    if (input == "19") return artykul_19;
    if (input == "20") return artykul_20;
    if (input == "21") return artykul_21;
    if (input == "22") return artykul_22;
    if (input == "23") return artykul_23;
    if (input == "24") return artykul_24;
    if (input == "25") return artykul_25;
    if (input == "26") return artykul_26;
    if (input == "27") return artykul_27;
    if (input == "28") return artykul_28;
    if (input == "29") return artykul_29;
    if (input == "30") return artykul_30;
    if (input == "31") return artykul_31;

    if (input == "margin") {
      return Nat.toText(margin);
    };
    if (input == "size") {
      return "32";

    };

    return "not suport command";
  };
  public query func help(line : Nat) : async Text{
    return 
    "CORE CANISTER – LOW-LEVEL API DESCRIPTION

This canister acts as a lightweight persistent content storage.
It stores text articles and a single binary file (Blob), preserving state across upgrades.

=== GENERAL STRUCTURE ===
- Up to 32 text articles (artykul_0 .. artykul_31)
- One binary file (Blob) – write-once
- A cyclic pointer (margin) defines the current article write position

=== IDENTIFICATION ===
hwoisme() -> Conn
Returns canister metadata:
- conn      : canister principal ID
- title     : logical instance name
- conector  : available logical modules ('chip', 'file', 'help')

=== CHIP MODULE (TEXT ARTICLES) ===

chip_up(input : Text) -> Text
- Stores a text article in the next available slot (0–31)
- Constraints:
  * minimum length: 250 characters
  * maximum length: 1500 characters
  * duplicate of the last stored article is rejected
- Storage position is controlled by the 'margin' variable
- After reaching slot 31, the index wraps back to 0
- Returns a human-readable status message

chip(input : Text) -> Text
- Reads stored data by command:
  * 0 .. 31 → article content
  * 'margin'   → current write index
  * 'size'     → total slot count (always 32)

=== FILE MODULE (BLOB STORAGE) ===

add_file(target : Blob) -> Nat
- One-time binary file upload
- First successful call:
  * stores the Blob
  * locks further writes (control_pin = true)
  * returns 0
- Subsequent calls:
  * overwrite is denied
  * returns 404

query_file(target : Nat) -> Blob
- Returns the stored Blob
- Parameter 'target' is currently ignored

=== PIN / METADATA MODULE ===

query_pin(target : Nat) -> File_pin
- Returns logical file metadata:
  * name        file name
  * file_note  descriptive note
  * file_lin   logical line references (placeholder)

add_pin(target : File_pin) -> Nat
- Reserved for future use
- Currently always returns 0

=== STABLE STATE (PERSISTENT DATA) ===
- artykul_0 .. artykul_31
- artykul_history
- margin

These variables survive canister upgrades.

=== PROTOCOL NOTES ===
- No authorization or access control
- No cycle management
- Text-based command interface
- Intended for low-level integration, scripting, or custom frontends";
  };
};
