import Text "mo:base/Text";
import Nat "mo:base/Nat";
persistent actor core {

  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };
  
  public query func hwoisme() : async Conn{
       return {
        conn = "-----";
        title = "this is simple v_medium canister";
        conector = ["chip"];
       };
  };
  stable var artykul_history = "";
  stable var artykul_0 = "";
  stable var artykul_1 = "";
  stable var artykul_2 = "";
  stable var artykul_3 = "";
  stable var artykul_4 = "";
  stable var artykul_5 = "";
  stable var artykul_6 = "";
  stable var artykul_7 = "";

  stable var margin = 0;

  public func chip_up(input : Text) : async Text {
  let size = Text.size(input);
  
  if (size < 250) {
    return "Błąd: Tekst musi miec co najmniej 250 znakow";
  };
  
  if (size > 1500) {
    return "Błąd: Tekst nie może miec wiecej niż 1500 znakow";
  };
  if (input == artykul_history){
    return "spokojnie twój artykuł jest już w bazie";
  };
  switch (margin) {
  case (7) {  artykul_7 := input;  margin := 0;};
  case (6) {  artykul_6 := input;  margin := 7};
  case (5) {  artykul_5 := input;  margin := 6};
  case (4) {  artykul_4 := input;  margin := 5};
  case (3) {  artykul_3 := input;  margin := 4};
  case (2) {  artykul_2 := input;  margin := 3};
  case (1) {  artykul_1 := input;  margin := 2};
  case (0) {  artykul_0 := input;  margin := 1};
  case (_) { /* obsługa innych wartości */ };
};
  artykul_history := input;
  return "Tekst został zapisany pomyślnie";
  };

  public query func chip(input : Text) : async Text {
    if(input == "0"){
      return artykul_0;
    };
    if(input == "1"){
      return artykul_1;
    };
    if(input == "2"){
      return artykul_2;
    };
    if(input == "3"){
      return artykul_3;
    };
    if(input == "4"){
      return artykul_4;
    };
    if(input == "5"){
      return artykul_5;
    };
    if(input == "6"){
      return artykul_6;
    };
    if(input == "7"){
      return artykul_7;
    };
    if(input == "margin"){
      return Nat.toText(margin);
    };
     return"not suport command plesse take 0/7 medium box or take margin now command margin";
  };
};