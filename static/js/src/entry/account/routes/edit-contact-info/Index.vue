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
      Your Contact Info
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

    <confirm-modal @onLeave="onLeave" @onReturn="onReturn" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
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
      title: 'Edit Contact Info',
      showModal: false,
      next: null,
    };
  },

  methods: {
    setShowModal(shouldShow) {
      this.showModal = shouldShow;
    },

    onLeave() {
      this.$modal.hide('modal');
      this.next();
      this.clearNext();
    },

    onReturn() {
      this.$modal.hide('modal');
      this.next(false);
      this.clearNext();
    },

    clearNext() {
      this.next = null;
    },
  },

  beforeRouteLeave(to, from, next) {
    if (this.showModal) {
      this.$modal.show('modal');
      this.next = next;
    } else {
      next();
    }
  },
};
</script>
