import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface Con_url { 'title' : string, 'conn' : string }
export interface Voyager { 'conn' : string, 'mode' : string }
export interface _SERVICE {
  'frend_add' : ActorMethod<[string, string], string>,
  'frend_one' : ActorMethod<[bigint], Voyager>,
  'info' : ActorMethod<[string], string>,
  'moderator' : ActorMethod<[string, bigint], string>,
  'url_add' : ActorMethod<[string, string], string>,
  'url_one' : ActorMethod<[bigint], Con_url>,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
