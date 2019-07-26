<template>
  <route-loader v-if="routeIsFetching">
    <template v-slot:text>
      Grabbing your contact information
    </template>
  </route-loader>

  <div v-else class="has-ump-top-padding">
    <h1 class="has-l-btm-marg has-ump-side-padding t-size-xl">
      Your Contact Info
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <div class="c-detail-box">
        <div class="has-xxl-btm-marg">
          <edit-contact-info-form @setShowModal="setShowModal" />
        </div>
        <edit-contact-info-links />
      </div>
    </div>

    <help basic :display="{ hasTopPadding: true }" />

    <edit-contact-info-modal @onLeave="onLeave" @onReturn="onReturn" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import EditContactInfoLinks from './containers/EditContactInfoLinksContainer.vue';
import EditContactInfoForm from './containers/EditContactInfoFormContainer.vue';
import EditContactInfoModal from './components/EditContactInfoModal.vue';

export default {
  name: 'EditContactInfoRoute',

  components: {
    RouteLoader,
    EditContactInfoLinks,
    EditContactInfoForm,
    EditContactInfoModal,
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

  async beforeRouteLeave(to, from, next) {
    if (this.showModal) {
      this.$modal.show('modal');
      this.next = next;
    } else {
      next();
    }
  },
};
</script>
