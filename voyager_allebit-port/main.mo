import Buffer "mo:base/Buffer";
import _Option "mo:base/Option";
import Nat "mo:base/Nat";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Ledger "Ledger";
import Principal "mo:base/Principal";
import Blob "mo:base/Blob";
import File "file";

actor {

  // recovery code
  system func preupgrade() {
    stableOffers := Buffer.toArray(offer);
  };

  system func postupgrade() {
    offer.clear();
    for (o in stableOffers.vals()) {
      offer.add(o);
    };
    stableOffers := [];
  };

  type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  type Ad = {
    text : Text;
    url : Text;
    pay : Nat;
    tim : Int;
  };

  type Freedom = {
    cozaco : Text;
    kontakt : Text;
    oferta : Text;
    kapital : Text;
    cena : Text;
  };

  type Debug = {
    log : Text;
    deb : Text;
  };

  let walletToCheck = Principal.fromText("gpkok-fho47-6eaqa-62sms-fijoq-43rca-7pkil-gmpie-tm6ev-skx5h-cae");
  var ledger : Ledger.Ledger = actor("ryjl3-tyaaa-aaaaa-aaaba-cai"); 

  stable var adnow : Ad = {
    text = "add ad only 0.05 ICP"; 
    url = "https://skontaktuj_sie_na_openchat_raboot24.isnoturl"; 
    pay = 0; 
    tim = 1000;
  };

  stable var adbox : Ad = {
    text = "test2"; 
    url = "test2"; 
    pay = 9999999999999999999999; 
    tim = 1000;
  };

  stable var stableOffers : [Freedom] = [];
  var wallethis : Nat = 0;
  var delay : Int = 420_000_000_000;
  var meit : Int = 1;
  var time = Time.now();
  var offer = Buffer.Buffer<Freedom>(25);

  offer.add({
    cozaco = "Kupie Bitcoina za Ethereum"; 
    kontakt = "niewazne"; 
    oferta = "Witam. Jestem biznesmenem z mysłowic, kupie BTC za ETC. Pozdro."; 
    kapital = "2000000000000000 ETC"; 
    cena = "1BTC ZA 200000000ETC"
  });

  private func checkBalance() : async Nat {
    let account : Ledger.Account = {
      owner = walletToCheck;
      subaccount = null;
    };
    let balance = await ledger.icrc1_balance_of(account);
    return balance;
  };

  // funkcje dodawania postów   
  public query func oferta_cek(marker: Nat) : async Freedom {
    return offer.get(marker);
  };

  public func oferta_add(cozaco: Text, kontakt: Text, oferta: Text, kapital: Text, cena: Text,) : async Debug {
    if (Text.size(cozaco) == 0 or Text.size(kontakt) == 0 or Text.size(oferta) == 0 or Text.size(kapital) == 0 or Text.size(cena) == 0) {
      return { log = "ER"; deb = "przynajmniej jedno pole jest puste" };
    };

    if (Text.size(cozaco) >= 70 or Text.size(kontakt) >= 100 or Text.size(oferta) >= 1000 or Text.size(kapital) >= 100 or Text.size(cena) >= 100) {
      return { log = "ER"; deb = "za dużo znaków w jednym polu : tytuł-max = 70 opis-max = 1000 kapitał/cena/kontakt-max = 100" };
    };

    time := Time.now();
    if (time <= (meit + delay)) {
      return { log = "ER"; deb = "system antyspam nie pozwolił dodać wpisu : spróbuj dodać ofertę później" };
    };

    if (80 <= offer.size()) {
      let x = offer.remove(0);
    };

    offer.add({ cozaco = cozaco; kontakt = kontakt; oferta = oferta; kapital = kapital; cena = cena });
    time := Time.now();
    meit := time;

    return { log = "OK"; deb = "oferta dodana" };
  };

  //
  //
  //
  // kod dodawania i edytowania reklamy

  // publikowanie reklamy
  public func apost() : async Text {
    time := Time.now();
    wallethis := await checkBalance();
    if (adbox.pay <= wallethis) {
      adnow := { text = adbox.text; url = adbox.url; pay = 0; tim = time + 86_400_000_000_000 };
      return "Reklama dodana poprawnie na 1 dzień.";
    } else {
      return "Opłata nie została jeszcze przesłana.";
    };
  };

  // generowanie reklamy
  public func abox(textt: Text, urll: Text) : async Text {
    wallethis := await checkBalance();
    time := Time.now();

    if (adnow.tim >= time) {
      return "Miejsce na reklamę jest zajęte.";
    };

    if (adbox.tim >= time) {
      return "Adbox jest aktualnie zajęty, proszę spróbować później.";
    } else {
      adbox := { text = textt; url = urll; pay = 5_000_000 + wallethis; tim = time + 200_000_000_000 };
      return "Wartości Adbox zostały zaktualizowane. Proszę o wpłatę 0.05 ICP i dokonanie publikacji reklamy. icp pay-here 'gpkok-fho47-6eaqa-62sms-fijoq-43rca-7pkil-gmpie-tm6ev-skx5h-cae'";
    };
  };

  // pokazywanie reklamy
  public query func a_cek() : async Ad {
    time := Time.now();
    if (adnow.tim >= time) {
      return adnow;
    };
    return { text = "add ad only 0.05 ICP"; url = "https://skontaktuj_sie_na_openchat_raboot24.isnoturl"; pay = 0; tim = 0 };
  };

  public query func getFile(phrase : Text) : async Blob {
    switch (phrase) {
      case "file1" { return File.file1() };
      case _ { return File.file1() };
    };
  };

  public query func theFile(phrase : Text) : async Text {
    switch (phrase) {
      case "file1" { return "allebitfont.ttf" };
      case _ { return "null" };
    };
  };

  public query func glue_get(get : [Text]) : async Text {
    switch(get[0]) {
      case("add") {
        if(get.size() <= 6) { return "nie podałeś wszytkich elementów"; };
        return "PUSH";
      };
      case("watch") {
        var target : Nat = 0;
        if (get.size() != 2) {
          target := 0;
        } else {
          switch (Nat.fromText(get[1])) {
            case (?val) { target := val };
            case (null) { target := 0 };
          };
        };
        if (target <= offer.size() and target >= 0) {
          let print = offer.get(target);
          return (print.cozaco # "\n \n" # print.oferta # "\n" # print.kapital # "\n" # print.cena # "\n" # print.kontakt);
        };
        return "takiej ofety nie ma";
      };
      case(_) {
        return "NULL";
      };
    };
  };

  // glue interface func 
  public func glue_push(push : [Text]) : async Text {
    switch (push[0]) {
      case("add") {
        if(push.size() <= 6) { return "nie podałeś wszytkich elementów"; };

        if (Text.size(push[1]) >= 70 or Text.size(push[5]) >= 100 or Text.size(push[2]) >= 1000 or Text.size(push[3]) >= 100 or Text.size(push[4]) >= 100) {
          return "za dużo znaków w jednym polu : tytuł-max = 70 opis-max = 1000 kapitał/cena/kontakt-max = 100";
        };

        time := Time.now();
        if (time <= (meit + delay)) {
          return "system antyspam nie pozwolił dodać wpisu : spróbuj dodać ofertę później";
        };

        if (80 <= offer.size()) {
          let x = offer.remove(0);
        };

        offer.add({ cozaco = push[1]; kontakt = push[5]; oferta = push[2]; kapital = push[3]; cena = push[4] });
        time := Time.now();
        meit := time;

        return "oferta dodana";
      };
      case (_) {
        return "NULL";
      };
    };
  };

  public query func hwoisme() : async Conn {
    return {
      conn = "----";
      title = "ALLEBIT on voyager";
      conector = ["glue", "help"];
    };
  };

  public query func help(line : Nat) : async Text{
    switch (line) {
      case(0) { return "witamy na ALLEBIT w systemie voyager \n help-1  sprawdzanie ofert w glue \n help-2 dodawanie ofert w glue \n zaządzanie reklamami w krutce"; };
      case(1) { return "  sprawdzanie oferty \n  /watch] [adres-numer indexu]"; };
      case(2) { return "  dodawanie oferty \n  /add] [co za co] [opis oferty] [kapitał do obrotu] [cena wymiany] [kontakt]"; };
      case(_) { return "witamy na ALLEBIT w systemie voyager \n help-1  sprawdzanie ofert w glue \n help-2 dodawanie ofert w glue \n zaządzanie reklamami w krutce"; };
    }
  };

};

