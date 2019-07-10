/* eslint-disable no-param-reassign, camelcase */

import axios from 'axios';
import parse from 'date-fns/parse';
import isPast from 'date-fns/is_past';

import { MultiplePersonsError, NoPersonsError } from '../../errors';
import { PORTAL_API_URL } from '../../constants';

/*
  Add some convenience fields to our API response to make
  conditionals easier throughout the app.
*/
function addFields(data) {
  const {
    is_recurring_donor,
    membership_expiration_date,
    membership_level,
    never_given,
    is_mdev,
    is_current_circle,
    is_former_circle,
  } = data;

  let membershipLevel;
  let isExpired;

  const isSingleDonor =
    !never_given &&
    !is_recurring_donor &&
    !!membership_expiration_date &&
    !is_mdev;

  const isRecurringDonor =
    is_recurring_donor &&
    !!membership_expiration_date &&
    !is_mdev &&
    !is_current_circle &&
    !is_former_circle;

  const isCircleDonor =
    (is_current_circle || is_former_circle) && !!membership_expiration_date;

  const isCustomDonor =
    (is_mdev && !is_current_circle && !is_former_circle) ||
    (!never_given && !membership_expiration_date);

  if (membership_expiration_date) {
    isExpired = isPast(parse(membership_expiration_date));
  } else {
    isExpired = null;
  }

  if (membership_level) {
    membershipLevel = membership_level.toLowerCase();
  } else {
    membershipLevel = null;
  }

  delete data.is_mdev;
  delete data.is_former_circle;
  delete data.is_current_circle;

  return {
    ...data,
    is_single_donor: isSingleDonor,
    is_recurring_donor: isRecurringDonor,
    is_circle_donor: isCircleDonor,
    is_custom_donor: isCustomDonor,
    is_expired: isExpired,
    membership_level: membershipLevel,
  };
}

function createDefaultState() {
  return { details: {} };
}

const MUTATION_TYPES = {
  setDetails: 'SET_DETAILS',
};

const mutations = {
  [MUTATION_TYPES.setDetails](state, details) {
    state.details = details;
  },
};

const actions = {
  getOtherUser: async ({ commit, rootState }, email) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}persons/`, {
      params: { email },
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    if (!data.length) throw new NoPersonsError();
    if (data.length > 1) throw new MultiplePersonsError();

    commit(MUTATION_TYPES.setDetails, addFields(data[0]));
  },

  getUser: async ({ commit, rootState }) => {
    const { accessToken } = rootState.tokenUser;
    const { data } = await axios.get(`${PORTAL_API_URL}self/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    commit(MUTATION_TYPES.setDetails, addFields(data));
  },
};

export default {
  namespaced: true,
  state: createDefaultState(),
  mutations,
  actions,
  getters: {},
};
