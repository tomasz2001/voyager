import Buffer "mo:base/Buffer";
import Blob "mo:base/Blob";


persistent actor {

  stable var data_claster_stable : [Blob] = [];

 type Conn = {
    conn: Text;
    title: Text;
    conector: [Text];
  };

  type File_pin = {
    name: Text; // np video.mp4
    file_note: Text; // np "this is video fish dance"
    file_line: [Nat]; // id file bit data box`s
  };


  
  public query func hwoisme() : async Conn{
       return {
        conn = "bkxiq-haaaa-aaaad-abo5q-cai";
        title = "this si V-MESSAGE welcome to first messenger on the Voyager system";
        conector = ["glue", "help", "file"];
       };
  };


};
