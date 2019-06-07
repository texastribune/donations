<template>
  <section class="c-detail-box">
    <div class="has-xxl-btm-marg">
      <info-list :items="data">
        <template v-slot="slotProps">
          <span
            :class="
              slotProps.item.text === 'Your membership expired.'
                ? 'has-text-error'
                : 'has-text-gray-dark'
            "
          >
            {{ slotProps.item.text }}
          </span>
        </template>
      </info-list>
    </div>

    <ul class="c-link-list t-linkstyle--underlined">
      <li v-if="isExpired && !isOneTime" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="#">Renew your membership</a>
        </span>
      </li>
      <li v-if="isOneTime" class="has-xs-btm-marg">
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <span class="has-text-gray-dark">
          <a href="#">Become a sustaining member</a>
        </span>
      </li>
      <li>
        <span class="c-link-list__arrow has-text-teal">
          <strong>&rarr;</strong>
        </span>
        <router-link :to="{ name: 'payments' }"
          >See your donation history</router-link
        >
      </li>
    </ul>
  </section>
</template>

<script>
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'Membership',

  components: { InfoList },

  props: {
    data: {
      type: Array,
      required: true,
    },

    isExpired: {
      type: Boolean,
      required: true,
    },

    isOneTime: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
