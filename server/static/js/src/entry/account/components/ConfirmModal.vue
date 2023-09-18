<template>
  <modal
    :max-width="450"
    :click-to-close="false"
    name="confirmModal"
    width="80%"
    height="auto"
    adaptive
  >
    <div class="c-modal">
      <div class="c-modal__heading l-align-center-children has-padding">
        <h2 class="t-size-b t-align-center t-lh-b has-text-gray-dark">{{ heading }}</h2>
      </div>
      <div class="c-modal__body" v-if="message">
        <div class="t-align-center" v-html="message"></div>
      </div>
      <ul class="c-modal__buttons l-width-full">
        <li>
          <base-button
            :text="rejectText"
            :display="{ size: 's' }"
            @onClick="onKeepEditing"
          />
        </li>
        <li>
          <base-button
            :text="acceptText"
            :display="{ size: 's' }"
            @onClick="onAbandon"
          />
        </li>
      </ul>
    </div>
    <button
      class="c-modal__close has-bg-white has-text-gray"
      aria-label="close modal"
      @click="onKeepEditing"
    >
      <icon name="close" :display="{ size: 'xxs', color: 'gray' }" />
    </button>
  </modal>
</template>

<script>
export default {
  name: 'EditContactInfoModal',

  props: {
    resolve: {
      type: Function,
      required: true,
    },
    heading: {
      type: String,
      required: true,
    },
    message: {
      type: String,
      required: false,
    },
    acceptText: {
      type: String,
      required: true,
    },
    rejectText: {
      type: String,
      required: true,
    }
  },

  methods: {
    onAbandon() {
      this.resolve(true);
    },

    onKeepEditing() {
      this.resolve(false);
    },
  },
};
</script>
