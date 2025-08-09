export const idlFactory = ({ IDL }) => {
  const Conn = IDL.Record({
    'title' : IDL.Text,
    'conn' : IDL.Text,
    'conector' : IDL.Vec(IDL.Text),
  });
  const Voyager = IDL.Record({
    'title' : IDL.Text,
    'conn' : IDL.Text,
    'conector' : IDL.Vec(IDL.Text),
  });
  return IDL.Service({
    'conn_add' : IDL.Func(
        [IDL.Text, IDL.Text, IDL.Vec(IDL.Text)],
        [IDL.Text],
        [],
      ),
    'conn_one' : IDL.Func([IDL.Nat], [Conn], ['query']),
    'frend_add' : IDL.Func(
        [IDL.Text, IDL.Text, IDL.Vec(IDL.Text)],
        [IDL.Text],
        [],
      ),
    'frend_one' : IDL.Func([IDL.Nat], [Voyager], ['query']),
    'help' : IDL.Func([IDL.Nat], [IDL.Text], ['query']),
    'hwoisme' : IDL.Func([], [Conn], ['query']),
    'moderator' : IDL.Func([IDL.Text, IDL.Nat], [IDL.Text], []),
  });
};
export const init = ({ IDL }) => { return []; };
