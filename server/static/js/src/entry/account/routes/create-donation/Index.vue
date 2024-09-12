<template>
  <div>
    <h1
      class="has-ump-side-padding has-ump-top-padding has-l-btm-marg t-size-xl"
    >
      Create Donation
    </h1>

    <div class="has-ump-side-padding has-xxl-btm-marg">
      <div class="c-detail-box c-detail-box--from-l">
        <div class="has-xxl-btm-marg">
          <donate-form />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import routeMixin from '../mixin';

import DonateForm from './containers/DonateFormContainer.vue';

export default {
  name: 'DonateRoute',

  components: {
    DonateForm,
  },

  mixins: [routeMixin],
};
</script>
