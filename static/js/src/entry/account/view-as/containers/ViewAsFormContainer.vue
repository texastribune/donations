<template>
  <view-as-form
    v-if="context.canViewAs"
    @doViewAs="doViewAs"
    @undoViewAs="undoViewAs"
  />
</template>

<script>
import ViewAsForm from '../components/ViewAsForm.vue';
import userMixin from '../../store/user/mixin';
import tokenUserMixin from '../../store/token-user/mixin';
import contextMixin from '../../store/context/mixin';

export default {
  name: 'ViewAsFormContainer',

  components: { ViewAsForm },

  mixins: [contextMixin, userMixin, tokenUserMixin],

  methods: {
    async doViewAs(email) {
      this.context.setAppIsFetching(true);

      await this.getOtherUser(email);

      this.context.setIsViewingAs(true);
      this.context.setAppIsFetching(false);
    },

    async undoViewAs() {
      this.context.setAppIsFetching(true);

      await this.getUser();

      this.context.setIsViewingAs(false);
      this.context.setAppIsFetching(false);
    },
  },
};
</script>
