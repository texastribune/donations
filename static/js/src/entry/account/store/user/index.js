/* eslint-disable no-param-reassign */

import axios from 'axios';
import parse from 'date-fns/parse';
import isPast from 'date-fns/is_past';

import formatTransaction from './utils/format-transaction';
import { USER_TYPES } from '../types';
import getTokenIdentity from '../../utils/get-token-identity';
import { PORTAL_API_URL } from '../../constants';

const SET_RAW_DATA = 'SET_RAW_DATA';

const state = { data: {} };

const mutations = {
  [SET_RAW_DATA](currentState, data) {
    currentState.data = data;
  },
};

const actions = {
  [USER_TYPES.getOtherUser]: async ({ commit, rootState }, email) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data[0]);
  },

  [USER_TYPES.getUser]: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data);
  },

  [USER_TYPES.updateUser]: async (
    { state: moduleState, rootState },
    updates
  ) => {
    const { accessToken } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.patch(`${PORTAL_API_URL}persons/${personId}/`, updates, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
  },

  [USER_TYPES.updateIdentity]: async (
    { state: moduleState, rootState },
    updates
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId, identities } = moduleState.data;
    const { id: identityId } = getTokenIdentity(identities, tokenEmail);

    await axios.patch(
      `${PORTAL_API_URL}persons/${personId}/identities/${identityId}/`,
      updates,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  [USER_TYPES.linkIdentity]: async (
    { state: moduleState, rootState },
    identity
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.put(
      `${PORTAL_API_URL}persons/${personId}/identities/${tokenEmail}/`,
      identity,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  [USER_TYPES.confirmLinkedIdentity]: async (
    { state: moduleState, rootState },
    ticket
  ) => {
    const {
      accessToken,
      details: { email: tokenEmail },
    } = rootState.tokenUser;
    const { id: personId } = moduleState.data;

    await axios.put(
      `${PORTAL_API_URL}persons/${personId}/identities/${tokenEmail}/?ticket=${ticket}`,
      {},
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },
};

const getters = {
  userId: ({ data: { id } }) => id,

  firstName: ({ data: { first_name: firstName } }) => firstName,

  lastName: ({ data: { last_name: lastName } }) => lastName,

  zip: ({ data: { postal_code: zip } }) => zip,

  didOfferConsent: () => {},

  linkedEmails: ({ data: { identities } }) =>
    identities.map(({ email }) => email),

  twitterUrl: ({ data: { twitter_share_url: twitterUrl } }) => twitterUrl,

  facebookUrl: ({ data: { facebook_share_url: facebookUrl } }) => facebookUrl,

  emailUrl: ({ data: { email_share_url: emailUrl } }) => emailUrl,

  ambassadorUrl: ({ data: { ambassador_url: ambassadorUrl } }) => ambassadorUrl,

  membershipExpirationDate: ({
    data: { membership_expiration_date: membershipExpirationDate },
  }) => membershipExpirationDate,

  membershipLevel: ({ data: { membership_level: membershipLevel } }) =>
    membershipLevel,

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
    { isNeverGiven, membershipExpirationDate }
  ) =>
    !isNeverGiven && !isRecurringDonor && !!membershipExpirationDate && !isMDev,

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

  allTransactions: ({ data }) => {
    const nonBlastTransactions = data.transactions.filter(
      ({ type }) => type.toLowerCase() !== 'the blast'
    );

    return nonBlastTransactions.map(transaction =>
      formatTransaction(transaction)
    );
  },

  nextTransaction: ({ data }) => {
    const { next_transaction: nextTransaction } = data;

    if (nextTransaction) {
      return formatTransaction(nextTransaction);
    }
    return null;
  },

  lastTransaction: ({ data }) => {
    const { last_transaction: lastTransaction } = data;

    if (lastTransaction) {
      return formatTransaction(lastTransaction);
    }
    return null;
  },

  pastTransactions: (_, { allTransactions }) => {
    const pastTransactions = allTransactions.filter(({ date }) => isPast(date));

    return pastTransactions.sort(
      ({ date: firstDate }, { date: secondDate }) => {
        if (parse(firstDate) > parse(secondDate)) return -1;
        if (parse(firstDate) < parse(secondDate)) return 1;
        return 0;
      }
    );
  },

  allBlastTransactions: ({ data }) => {
    const blastTransactions = data.transactions.filter(
      ({ type }) => type.toLowerCase() === 'the blast'
    );

    return blastTransactions.map(transaction => formatTransaction(transaction));
  },

  nextBlastTransaction: ({ data }) => {
    const { next_blast_transaction: nextBlastTransaction } = data;

    if (nextBlastTransaction) {
      return formatTransaction(nextBlastTransaction);
    }
    return null;
  },

  lastBlastTransaction: ({ data }) => {
    const { last_blast_transaction: lastBlastTransaction } = data;

    if (lastBlastTransaction) {
      return formatTransaction(lastBlastTransaction);
    }
    return null;
  },

  pastBlastTransactions: (_, { allBlastTransactions }) => {
    const pastBlastTransactions = allBlastTransactions.filter(({ date }) =>
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
  state,
  mutations,
  actions,
  getters,
};
