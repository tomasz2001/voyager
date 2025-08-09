import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface Conn {
  'title' : string,
  'conn' : string,
  'conector' : Array<string>,
}
export interface file_box {
  'fd' : [] | [Uint8Array | number[]],
  'ft' : [] | [string],
}
export interface _SERVICE {
  'file_add' : ActorMethod<[file_box], bigint>,
  'file_moderator' : ActorMethod<[bigint], string>,
  'file_one' : ActorMethod<[bigint], file_box>,
  'glue_get' : ActorMethod<[Array<string>], string>,
  'help' : ActorMethod<[bigint], string>,
  'hwoisme' : ActorMethod<[], Conn>,
  'tracker_file' : ActorMethod<[string, bigint], Array<bigint>>,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
