import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface Conn {
  'title' : string,
  'conn' : string,
  'conector' : Array<string>,
}
export interface _SERVICE {
  'glue_get' : ActorMethod<[Array<string>], string>,
  'glue_push' : ActorMethod<[Array<string>], string>,
  'help' : ActorMethod<[bigint], string>,
  'hwoisme' : ActorMethod<[], Conn>,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
