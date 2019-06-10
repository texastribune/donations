<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg"><info-list :items="data" /></div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <router-link :to="{ name: 'blast-payments' }"
          >See your payment history</router-link
        >
      </li>
    </ul>
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'BlastDetail',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },
  },
};
</script>
