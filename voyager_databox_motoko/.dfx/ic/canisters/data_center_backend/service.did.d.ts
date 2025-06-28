import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface Conn {
  'title' : string,
  'conn' : string,
  'conector' : Array<string>,
}
export interface Voyager {
  'title' : string,
  'conn' : string,
  'conector' : Array<string>,
}
export interface _SERVICE {
  'conn_add' : ActorMethod<[string, string, Array<string>], string>,
  'conn_one' : ActorMethod<[bigint], Conn>,
  'frend_add' : ActorMethod<[string, string, Array<string>], string>,
  'frend_one' : ActorMethod<[bigint], Voyager>,
  'help' : ActorMethod<[bigint], string>,
  'moderator' : ActorMethod<[string, bigint], string>,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
