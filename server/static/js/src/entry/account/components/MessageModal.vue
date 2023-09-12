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
        <h2 class="t-size-b t-align-center t-lh-b">{{ heading }}</h2>
      </div>
      <div class="t-align-center">
        <span class="c-icon c-icon--teal c-icon--baseline t-size-xl">
          <svg aria-hidden="true">
            <use v-if="messageType == 'success'" href="#check"></use>
            <use v-if="messageType == 'failure'" href="#close"></use>
          </svg>
        </span>
        <div class="c-modal__body" v-if="messageBody">
          <div v-html="messageBody"></div>
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
  },
};
</script>
