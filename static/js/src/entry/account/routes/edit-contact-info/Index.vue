<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your contact information
    </template>
  </route-loader>

  <div v-else>
    <h1
      class="has-ump-side-padding has-ump-top-padding has-l-btm-marg t-size-xl"
    >
      Your Profile Settings
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <div class="c-detail-box c-detail-box--from-l">
        <div class="has-xxl-btm-marg">
          <edit-form @setShowModal="setShowModal" />
        </div>
        <links />
      </div>
    </div>

    <help edit />

    <confirm-modal :resolve="checkModalResolve" />
  </div>
</template>

<script>
import routeMixin from '../mixin';
import Help from '../home/components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import Links from './containers/LinksContainer.vue';
import EditForm from './containers/EditFormContainer.vue';
import ConfirmModal from './components/ConfirmModal.vue';

export default {
  name: 'EditContactInfoRoute',

  components: {
    RouteLoader,
    Links,
    EditForm,
    ConfirmModal,
    Help,
  },

  mixins: [routeMixin],

  data() {
    return {
      title: 'Your Profile Settings',
      showModal: false,
      checkModalResolve: () => {},
    };
  },

  methods: {
    setShowModal(shouldShow) {
      this.showModal = shouldShow;
    },

    checkModalAction() {
      return new Promise(resolve => {
        this.checkModalResolve = resolve;
      });
    },
  },

  async beforeRouteLeave(to, from, next) {
    if (this.showModal) {
      this.$modal.show('modal');

      const shouldNav = await this.checkModalAction();

      this.$modal.hide('modal');

      if (shouldNav) {
        next();
      } else {
        next(false);
      }
    } else {
      next();
    }
  },
};
</script>
