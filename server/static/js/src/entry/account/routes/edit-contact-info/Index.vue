<template>
  <div>
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

        <internal-nav />
      </div>
    </div>

    <contact-us :ga-label="ga.userPortal.labels['edit-contact-info']">
      <template #text>
        Have questions about your account? Or feedback about this website? Email
      </template>
    </contact-us>

    <confirm-modal
      :resolve="checkModalResolve"
      :heading="'You have unsaved changes'"
      :reject-text="'Keep editing'" 
      :accept-text="'Do not save'" />
  </div>
</template>

<script>
import routeMixin from '../mixin';

import EditForm from './containers/EditFormContainer.vue';

import ContactUs from '../../components/ContactUs.vue';
import ConfirmModal from '../../components/ConfirmModal.vue';
import InternalNav from './components/InternalNav.vue';

export default {
  name: 'EditContactInfoRoute',

  components: {
    InternalNav,
    EditForm,
    ConfirmModal,
    ContactUs,
  },

  mixins: [routeMixin],

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

  data() {
    return {
      showModal: false,
      checkModalResolve: () => {},
    };
  },

  methods: {
    setShowModal(shouldShow) {
      this.showModal = shouldShow;
    },

    checkModalAction() {
      return new Promise((resolve) => {
        this.checkModalResolve = resolve;
      });
    },
  },
};
</script>
