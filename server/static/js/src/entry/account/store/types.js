export const USER_MODULE = 'user';
export const TOKEN_USER_MODULE = 'tokenUser';
export const CONTEXT_MODULE = 'context';

export const USER_TYPES = {
  getUser: `${USER_MODULE}__getUser`,
  getViewAsUser: `${USER_MODULE}__getViewAsUser`,
  updateUser: `${USER_MODULE}__updateUser`,
  updateIdentity: `${USER_MODULE}__updateIdentity`,
  updateCard: `${USER_MODULE}__updateCard`,
  updateRdoCard: `${USER_MODULE}__updateRdoCard`,
  updateOpportunities: `${USER_MODULE}__updateOpportunities`,
  closeRdo: `${USER_MODULE}__closeRdo`,
  linkIdentity: `${USER_MODULE}__linkIdentity`,
  confirmLinkedIdentity: `${USER_MODULE}__confirmLinkedIdentity`,
  createDonation: `${USER_MODULE}__createPayment`,
};

export const TOKEN_USER_TYPES = {
  getTokenUser: `${TOKEN_USER_MODULE}__getTokenUser`,
};

export const CONTEXT_TYPES = {
  setIsFetching: `${CONTEXT_MODULE}__setIsFetching`,
  setError: `${CONTEXT_MODULE}__setError`,
};
