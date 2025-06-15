export const idlFactory = ({ IDL }) => {
  const Conn = IDL.Record({
    'title' : IDL.Text,
    'conn' : IDL.Text,
    'conector' : IDL.Vec(IDL.Text),
  });
  return IDL.Service({
    'glue_get' : IDL.Func([IDL.Vec(IDL.Text)], [IDL.Text], ['query']),
    'glue_push' : IDL.Func([IDL.Vec(IDL.Text)], [IDL.Text], []),
    'help' : IDL.Func([IDL.Nat], [IDL.Text], ['query']),
    'hwoisme' : IDL.Func([], [IDL.Vec(Conn)], ['query']),
  });
};
export const init = ({ IDL }) => { return []; };
