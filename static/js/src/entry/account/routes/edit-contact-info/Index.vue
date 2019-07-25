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
        <div class="has-xxl-btm-marg"><contact-info-form-container /></div>
        <edit-contact-info-links />
      </div>
    </div>

    <help basic :display="{ hasTopPadding: true }" />
  </div>
</template>

<script>
import routeMixin from '../../mixins/route';
import Help from '../../components/Help.vue';
import RouteLoader from '../home/components/RouteLoader.vue';
import EditContactInfoLinks from './containers/EditContactInfoLinksContainer.vue';
import ContactInfoFormContainer from './containers/ContactInfoFormContainer.vue';

export default {
  name: 'EditContactInfoRoute',

  components: {
    RouteLoader,
    EditContactInfoLinks,
    ContactInfoFormContainer,
    Help,
  },

  mixins: [routeMixin],

  data() {
    return { title: 'Edit Contact Info' };
  },
};
</script>
