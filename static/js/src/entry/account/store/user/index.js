/* eslint-disable no-param-reassign */

import axios from 'axios';
import parse from 'date-fns/parse';
import isPast from 'date-fns/is_past';

import formatTransaction from './utils/format-transaction';
import { PORTAL_API_URL } from '../../constants';

const SET_RAW_DATA = 'SET_RAW_DATA';

const initialState = { data: {} };

const mutations = {
  [SET_RAW_DATA](currentState, data) {
    currentState.data = data;
  },
};

const actions = {
  getOtherUser: async ({ commit, rootState }, email) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data[0]);
  },

  getUser: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(SET_RAW_DATA, data);
  },

  updateUser: async ({ getters, rootState }, updates) => {
    const { accessToken } = rootState.tokenUser;
    const { userId } = getters;

    await axios.patch(`${PORTAL_API_URL}persons/${userId}/`, updates, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
  },

  updateIdentity: async ({ getters, rootState }, updates) => {
    const { accessToken } = rootState.tokenUser;
    const { userId, identityId } = getters;

    await axios.patch(
      `${PORTAL_API_URL}persons/${userId}/identities/${identityId}/`,
      updates,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  linkIdentity: async ({ getters, rootState }, identity) => {
    const { accessToken } = rootState.tokenUser;
    const { userId, email } = getters;

    await axios.put(
      `${PORTAL_API_URL}persons/${userId}/identities/${email}/`,
      identity,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },

  confirmLinkedIdentity: async ({ getters, rootState }, ticket) => {
    const { accessToken } = rootState.tokenUser;
    const { userId, email } = getters;

    await axios.put(
      `${PORTAL_API_URL}persons/${userId}/identities/${email}/?ticket=${ticket}`,
      {},
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
  },
};

const getters = {
  email: (
    _,
    __,
    {
      tokenUser: {
        idTokenPayload: { email },
      },
    }
  ) => email,

  identity: ({ data: { identities = [] } }, { email }) => {
    if (!identities.length) return {};

    const [goodIdentity] = identities.filter(
      ({ email: identityEmail }) => identityEmail === email
    );

    return goodIdentity;
  },

  userId: ({ data: { id } }) => id,

  identityId: (_, { identity: { id } }) => id,

  firstName: ({ data: { first_name: firstName } }) => firstName || '',

  lastName: ({ data: { last_name: lastName } }) => lastName || '',

  greeting: ({ data: { greeting } }) => greeting || '',

  zip: ({ data: { postal_code: zip } }) => zip || '',

  lastYearAmount: ({ data: { total_gifts_last_year: lastYearAmount } }) =>
    lastYearAmount,

  didConsent: (_, { identity: { tribune_offers_consent: didConsent } }) =>
    didConsent,

  linkedEmails: ({ data: { identities = [] } }) =>
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

  allTransactions: ({ data: { transactions = [] } }) => {
    const nonBlastTransactions = transactions.filter(
      ({ type }) => type.toLowerCase() !== 'the blast'
    );

    return nonBlastTransactions.map(transaction =>
      formatTransaction(transaction)
    );
  },

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

  allBlastTransactions: ({ data: { transactions = [] } }) => {
    const blastTransactions = transactions.filter(
      ({ type }) => type.toLowerCase() === 'the blast'
    );

    return blastTransactions.map(transaction => formatTransaction(transaction));
  },

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
  state: initialState,
  mutations,
  actions,
  getters,
};
