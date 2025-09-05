export const idlFactory = ({ IDL }) => {
  const file_box = IDL.Record({
    'fd' : IDL.Opt(IDL.Vec(IDL.Nat8)),
    'ft' : IDL.Opt(IDL.Text),
  });
  const Conn = IDL.Record({
    'title' : IDL.Text,
    'conn' : IDL.Text,
    'conector' : IDL.Vec(IDL.Text),
  });
  return IDL.Service({
    'file_add' : IDL.Func([file_box], [IDL.Nat], []),
    'file_moderator' : IDL.Func([IDL.Nat], [IDL.Text], []),
    'file_one' : IDL.Func([IDL.Nat], [file_box], ['query']),
    'glue_get' : IDL.Func([IDL.Vec(IDL.Text)], [IDL.Text], ['query']),
    'help' : IDL.Func([IDL.Nat], [IDL.Text], ['query']),
    'hwoisme' : IDL.Func([], [Conn], ['query']),
    'tracker_file' : IDL.Func(
        [IDL.Text, IDL.Nat],
        [IDL.Vec(IDL.Nat)],
        ['query'],
      ),
  });
};
export const init = ({ IDL }) => { return []; };
