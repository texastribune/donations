<template>
  <modal
    :max-width="450"
    name="messageModal"
    width="80%"
    height="auto"
    adaptive
  >
    <div class="c-modal">
      <div class="c-modal__heading l-align-center-children has-padding">
        <h2 class="t-size-b t-align-center t-lh-b has-text-gray-dark">
          <span class="c-icon c-icon--baseline t-size-b">
            <svg aria-hidden="true">
              <use class="has-text-success" v-if="messageType == 'success'" href="#check"></use>
              <use class="has-text-error" v-if="messageType == 'failure'" href="#close"></use>
            </svg>
          </span>
          {{ heading }}
        </h2>
      </div>
      <div class="t-align-center">
        <div class="c-modal__body" v-if="messageBody">
          <div v-html="messageBody"></div>
          <base-button
            v-if="link"
            :text="linkText"
            :display="{ isFullWidth: false, size: 's' }"
            @onClick="onClick(link)"
          />
        </div>
      </div>
    </div>
    <button
      class="c-modal__close has-bg-white has-text-gray"
      aria-label="close modal"
      @click="$emit('onClose')"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
    </button>
  </modal>
</template>

<script>
export default {
  name: 'MessageModal',

  props: {
    heading: {
      type: String,
      required: true,
    },

    messageType: {
      type: String,
      required: true,
    },

    messageBody: {
      type: String,
      required: true,
    },

    link: {
      type: String,
      required: false,
    },

    linkText: {
      type: String,
      required: false,
    },
  },

  methods: {
    onClick(link) {
      window.open(link);
    }
  }
};
</script>
