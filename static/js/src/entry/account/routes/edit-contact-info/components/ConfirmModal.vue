<template>
  <modal
    :max-width="450"
    :click-to-close="false"
    name="modal"
    width="80%"
    height="auto"
    adaptive
  >
    <div class="c-modal">
      <div class="c-modal__top l-align-center-children has-padding">
        <h2 class="t-size-b t-align-center t-lh-b">You have unsaved changes</h2>
      </div>
      <ul class="c-modal__buttons l-width-full">
        <li>
          <base-button
            text="Keep editing"
            :display="{ size: 's' }"
            @onClick="onKeepEditing"
          />
        </li>
        <li>
          <base-button
            text="Don't save"
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
