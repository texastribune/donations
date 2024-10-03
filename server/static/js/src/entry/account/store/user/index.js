/* eslint-disable no-param-reassign */

import axios from 'axios';
import parse from 'date-fns/parse';
import isPast from 'date-fns/is_past';

import formatTransaction from './utils/format-transaction';

import { USER_TYPES } from '../types';
import { PORTAL_API_URL } from '../../constants';

const SET_ME = 'SET_ME';
const SET_VIEW_AS = 'SET_VIEW_AS';
const SET_UPDATED_CARD = 'SET_UPDATED_CARD';
const SET_UPDATED_RDO_CARD = 'SET_UPDATED_RDO_CARD';
const REMOVE_CLOSED_RDO = 'REMOVE_CLOSED_RDO';

const initialState = {
  data: {},
  viewAsEmail: '',
};

const mutations = {
  [SET_ME](state, data) {
    state.data = data;
    state.viewAsEmail = '';
  },

  [SET_VIEW_AS](state, { data, viewAsEmail }) {
    state.data = data;
    state.viewAsEmail = viewAsEmail;
  },

  [SET_UPDATED_CARD](state, cardUpdates) {
    if (state.data.next_transaction) {
      state.data.next_transaction.credit_card = {
        ...state.data.next_transaction.credit_card,
        last4: cardUpdates.card.last4,
        brand: cardUpdates.card.brand
      }
    }
  },

  [SET_UPDATED_RDO_CARD](state, rdo) {
    state.data.recurring_transactions.forEach(item => {
      if (item.id === rdo.rdoId) {
        item.credit_card = {
          ...item.credit_card,
          last4: rdo.card.last4,
          brand: rdo.card.brand
        }
      }
    })
  },

  [REMOVE_CLOSED_RDO](state, rdo) {
    const recurringTransactions = state.data.recurring_transactions.filter(item =>
      item.id !== rdo.rdoId
    );
    state.data.recurring_transactions = recurringTransactions;
  },
};

const actions = {
  [USER_TYPES.getViewAsUser]: async ({ commit, rootState }, viewAsEmail) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email: viewAsEmail },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_VIEW_AS, { data: data[0], viewAsEmail });
  },

  [USER_TYPES.getUser]: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_ME, data);
  },

  [USER_TYPES.updateUser]: async ({ state, getters, rootState }, updates) => {
    if (!state.viewAsEmail) {
      const { accessToken } = rootState.tokenUser;
      const { userId } = getters;

      await axios.patch(`${PORTAL_API_URL}persons/${userId}/`, updates, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
    }
  },

  [USER_TYPES.updateIdentity]: async (
    { state, getters, rootState },
    updates
  ) => {
    if (!state.viewAsEmail) {
      const { accessToken } = rootState.tokenUser;
      const { userId, identityId } = getters;

      await axios.patch(
        `${PORTAL_API_URL}persons/${userId}/identities/${identityId}/`,
        updates,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
    }
  },

  [USER_TYPES.closeRdo]: async (
    { state, getters, commit, rootState },
    updates
  ) => {
    const { idTokenPayload } = rootState.tokenUser;
    if (!state.viewAsEmail ||
      (state.viewAsEmail && idTokenPayload['https://texastribune.org/is_staff'])) {
      const { accessToken } = rootState.tokenUser;
      const { userId } = getters;
      updates.userInitiated = !state.viewAsEmail

      await axios.patch(
        `${PORTAL_API_URL}persons/${userId}/rdos/close/`,
        updates,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
      commit(REMOVE_CLOSED_RDO, updates);
    }
  },

  [USER_TYPES.updateCard]: async (
    { state, getters, commit, rootState },
    updates
  ) => {
    const { idTokenPayload } = rootState.tokenUser;
    if (!state.viewAsEmail ||
      (state.viewAsEmail && idTokenPayload['https://texastribune.org/is_staff'])) {
      const { accessToken } = rootState.tokenUser;
      const { userId } = getters;

      await axios.patch(
        `${PORTAL_API_URL}persons/${userId}/cards/`,
        updates,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
      commit(SET_UPDATED_CARD, updates);
    }
  },

  [USER_TYPES.updateRdoCard]: async (
    { state, getters, commit, rootState },
    updates
  ) => {
    const { idTokenPayload } = rootState.tokenUser;
    if (!state.viewAsEmail ||
      (state.viewAsEmail && idTokenPayload['https://texastribune.org/is_staff'])) {
      const { accessToken } = rootState.tokenUser;
      const { userId } = getters;

      await axios.patch(
        `${PORTAL_API_URL}persons/${userId}/rdos/card/`,
        updates,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
      commit(SET_UPDATED_RDO_CARD, updates);
    }
  },

  [USER_TYPES.linkIdentity]: async (
    { state, getters, rootState },
    identity
  ) => {
    if (!state.viewAsEmail) {
      const { accessToken } = rootState.tokenUser;
      const { userId, email } = getters;

      await axios.put(
        `${PORTAL_API_URL}persons/${userId}/identities/${email}/`,
        identity,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
    }
  },

  [USER_TYPES.confirmLinkedIdentity]: async (
    { state, getters, rootState },
    ticket
  ) => {
    if (!state.viewAsEmail) {
      const { accessToken } = rootState.tokenUser;
      const { userId, email } = getters;

      await axios.put(
        `${PORTAL_API_URL}persons/${userId}/identities/${email}/?ticket=${ticket}`,
        {},
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
    }
  },
  [USER_TYPES.createDonation]: async (
    { state, rootState },
    donation
  ) => {
    if (!state.viewAsEmail) {
      const { accessToken } = rootState.tokenUser;

      await axios.patch(
        `${PORTAL_API_URL}payments/inperson/`,
        donation,
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );
    }
  },
};

const getters = {
  email: (
    { viewAsEmail },
    _,
    {
      tokenUser: {
        idTokenPayload: { email = '' },
      },
    }
  ) => {
    if (viewAsEmail) {
      return viewAsEmail;
    }
    return email;
  },

  identity: ({ viewAsEmail, data: { identities = [] } }, { email }) => {
    // we're viewing as someone who does not have an Auth0 account
    if (viewAsEmail && !identities.length) {
      return {
        tribune_offers_consent: false,
      };
    }

    // grab the identity associated with a user's Auth0 email address
    const matchingIdentities = identities.filter(
      ({ email: identityEmail }) => identityEmail === email
    );

    return matchingIdentities[0] || {};
  },

  userId: ({ data: { id } }) => id,

  identityId: (_, { identity: { id } }) => id,

  firstName: ({ data: { first_name: firstName = '' } }) => firstName,

  lastName: ({ data: { last_name: lastName = '' } }) => lastName,

  zip: ({ data: { postal_code: zip = '' } }) => zip,

  greeting: ({ data: { greeting } }) => greeting,

  lastYearAmount: ({ data: { total_gifts_last_year: lastYearAmount } }) =>
    lastYearAmount,

  wantsMarketing: (
    _,
    { identity: { tribune_offers_consent: wantsMarketing } }
  ) => wantsMarketing,

  linkedEmails: ({ data: { identities = [] } }) =>
    identities.map(({ email }) => email),

  membershipExpirationDate: ({
    data: { membership_expiration_date: membershipExpirationDate },
  }) => membershipExpirationDate,

  membershipLevel: ({ data: { membership_level: membershipLevel } }) => {
    if (membershipLevel) {
      return membershipLevel.toLowerCase();
    }
    return null;
  },

  isNeverGiven: ({ data: { never_given: isNeverGiven } }) => isNeverGiven,

  isCurrentBlastSubscriber: ({
    data: { is_current_blast_subscriber: isCurrentBlastSubscriber },
  }) => isCurrentBlastSubscriber,

  isFormerBlastSubscriber: ({
    data: { is_former_blast_subscriber: isFormerBlastSubscriber },
  }) => isFormerBlastSubscriber,

  isBlastSubscriber: (
    _,
    { isCurrentBlastSubscriber, isFormerBlastSubscriber }
  ) => isCurrentBlastSubscriber || isFormerBlastSubscriber,

  isCircleDonor: (
    {
      data: {
        is_current_circle: isCurrentCircle,
        is_former_circle: isFormerCircle,
      },
    },
    { membershipExpirationDate }
  ) => (isCurrentCircle || isFormerCircle) && !!membershipExpirationDate,

  isSingleDonor: (
    { data: { is_recurring_donor: isRecurringDonor, is_mdev: isMDev } },
    { isNeverGiven, isCircleDonor, membershipExpirationDate }
  ) =>
    !isNeverGiven &&
    !isRecurringDonor &&
    !!membershipExpirationDate &&
    !isMDev &&
    !isCircleDonor,

  isRecurringDonor: (
    { data: { is_recurring_donor: isRecurringDonor, is_mdev: isMDev } },
    { isCircleDonor, membershipExpirationDate }
  ) =>
    isRecurringDonor && !!membershipExpirationDate && !isMDev && !isCircleDonor,

  isCustomDonor: (
    { data: { is_mdev: isMDev } },
    { isNeverGiven, isCircleDonor, membershipExpirationDate }
  ) =>
    (isMDev && !isCircleDonor) || (!isNeverGiven && !membershipExpirationDate),

  hasGivenNotCustom: (_, { isCircleDonor, isSingleDonor, isRecurringDonor }) =>
    isCircleDonor || isSingleDonor || isRecurringDonor,

  isExpired: (_, { membershipExpirationDate }) => {
    if (membershipExpirationDate) {
      return isPast(parse(membershipExpirationDate));
    }
    return null;
  },

  willExpire: (_, { isExpired, nextTransaction, membershipExpirationDate }) => {
    if (membershipExpirationDate) {
      return !nextTransaction && !isExpired;
    }
    return null;
  },

  transactions: ({ data: { transactions = [] } }) =>
    transactions.map(transaction => formatTransaction(transaction)),

  recurringTransactions: ({ data: { recurring_transactions: recurringTransactions } }) =>
    recurringTransactions,

  nextTransaction: ({ data: { next_transaction: nextTransaction } }) => {
    if (nextTransaction) {
      return formatTransaction(nextTransaction);
    }
    return null;
  },

  lastTransaction: ({ data: { last_transaction: lastTransaction } }) => {
    if (lastTransaction) {
      return formatTransaction(lastTransaction);
    }
    return null;
  },

  pastTransactions: (_, { transactions }) => {
    const pastTransactions = transactions.filter(({ date }) => isPast(date));

    return pastTransactions.sort(
      ({ date: firstDate }, { date: secondDate }) => {
        if (parse(firstDate) > parse(secondDate)) return -1;
        if (parse(firstDate) < parse(secondDate)) return 1;
        return 0;
      }
    );
  },

  blastTransactions: ({
    data: { blast_transactions: blastTransactions = [] },
  }) => blastTransactions.map(transaction => formatTransaction(transaction)),

  nextBlastTransaction: ({
    data: { next_blast_transaction: nextBlastTransaction },
  }) => {
    if (nextBlastTransaction) {
      return formatTransaction(nextBlastTransaction);
    }
    return null;
  },

  lastBlastTransaction: ({
    data: { last_blast_transaction: lastBlastTransaction },
  }) => {
    if (lastBlastTransaction) {
      return formatTransaction(lastBlastTransaction);
    }
    return null;
  },

  pastBlastTransactions: (_, { blastTransactions }) => {
    const pastBlastTransactions = blastTransactions.filter(({ date }) =>
      isPast(date)
    );

    return pastBlastTransactions.sort(
      ({ date: firstDate }, { date: secondDate }) => {
        if (parse(firstDate) > parse(secondDate)) return -1;
        if (parse(firstDate) < parse(secondDate)) return 1;
        return 0;
      }
    );
  },
};

export default {
  namespaced: true,
  state: initialState,
  mutations,
  actions,
  getters,
};
