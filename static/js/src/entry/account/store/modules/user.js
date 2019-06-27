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
  } = data;
  let membershipLevel;
  let isExpired;

  const isOneTime = !never_given && !is_recurring_donor;

  // only null if never_given: true
  // or for some special mdevs (i.e. innovation fund)
  if (membership_expiration_date) {
    isExpired = isPast(parse(membership_expiration_date));
  } else {
    isExpired = null;
  }

  // only null if never_given: true
  // or for some special mdevs (i.e. innovation fund)
  if (membership_level) {
    membershipLevel = membership_level.toLowerCase();
  } else {
    membershipLevel = null;
  }

  return {
    ...data,
    is_one_time: isOneTime,
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
