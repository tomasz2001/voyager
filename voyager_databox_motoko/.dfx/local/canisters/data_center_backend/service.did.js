export const idlFactory = ({ IDL }) => {
  const Voyager = IDL.Record({ 'conn' : IDL.Text, 'mode' : IDL.Text });
  const Con_url = IDL.Record({ 'title' : IDL.Text, 'conn' : IDL.Text });
  return IDL.Service({
    'frend_add' : IDL.Func([IDL.Text, IDL.Text], [IDL.Text], []),
    'frend_one' : IDL.Func([IDL.Nat], [Voyager], ['query']),
    'info' : IDL.Func([], [IDL.Text], ['query']),
    'moderator' : IDL.Func([IDL.Text, IDL.Nat], [IDL.Text], []),
    'url_add' : IDL.Func([IDL.Text, IDL.Text], [IDL.Text], []),
    'url_one' : IDL.Func([IDL.Nat], [Con_url], ['query']),
  });
};
export const init = ({ IDL }) => { return []; };
