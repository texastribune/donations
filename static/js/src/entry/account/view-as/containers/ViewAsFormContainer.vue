<template>
  <view-as-form
    v-if="tokenUser.canViewAs"
    @doViewAs="doViewAs"
    @undoViewAs="undoViewAs"
  />
</template>

<script>
import userMixin from '../../store/user/mixin';
import tokenUserMixin from '../../store/token-user/mixin';
import contextMixin from '../../store/context/mixin';

import ViewAsForm from '../components/ViewAsForm.vue';

import { CONTEXT_TYPES, USER_TYPES } from '../../store/types';

export default {
  name: 'ViewAsFormContainer',

  components: { ViewAsForm },

  mixins: [contextMixin, userMixin, tokenUserMixin],

  methods: {
    async doViewAs(email) {
      this[CONTEXT_TYPES.setIsFetching](true);
      await this[USER_TYPES.getViewAsUser](email);
      this[CONTEXT_TYPES.setIsFetching](false);
    },

    async undoViewAs() {
      this[CONTEXT_TYPES.setIsFetching](true);
      await this[USER_TYPES.getUser]();
      this[CONTEXT_TYPES.setIsFetching](false);
    },
  },
};
</script>
