<template>
  <form
    ref="form"
    action="/donate"
    method="post"
    class="form"
    @submit="$event.preventDefault()"
  >
    <div v-show="showServerErrorMessage" class="grid_row grid_separator">
      <div class="col">
        <p class="form__error form__error--prominent">
          {{ serverErrorMessage }}
        </p>
      </div>
    </div>

    <div class="grid_row">
      <div class="col">
        <radios
          :options="frequencyOptions"
          :store-module="storeModule"
          base-classes="form__radios form__radios--stack-at-medium"
          name="installment_period"
          @updateCallback="onFrequencyUpdate"
        />
      </div>
    </div>

    <div class="grid_row grid_separator--xs">
      <div class="col">
        <text-input
          :store-module="storeModule"
          :show-error="showManualErrors || showNativeErrors"
          label-text="amount ($)"
          base-classes="form__text form__text--heavy"
          name="amount"
        />
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <p class="subtext">
          For three-year commitments of $1,000 or more, join our
          <a href="/circle">Circle Membership program</a>.
        </p>
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <text-input
          :store-module="storeModule"
          :show-error="showManualErrors || showNativeErrors"
          label-text="email address"
          type="email"
          base-classes="form__text form__text--standard"
          name="stripeEmail"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :show-error="showManualErrors || showNativeErrors"
          label-text="first name"
          base-classes="form__text form__text--standard"
          name="first_name"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :show-error="showManualErrors || showNativeErrors"
          label-text="last name"
          base-classes="form__text form__text--standard"
          name="last_name"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :required="false"
          :show-error="showManualErrors || showNativeErrors"
          label-text="encouraged to give by"
          base-classes="form__text form__text--standard"
          name="reason"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :required="false"
          :show-error="showManualErrors || showNativeErrors"
          label-text="zip code"
          base-classes="form__text form__text--standard"
          name="zipcode"
        />
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <pay-fees :store-module="storeModule" base-classes="form__fees" />
      </div>
    </div>

    <div class="grid_row">
      <div class="col">
        <native-pay
          :store-module="storeModule"
          :form-is-valid="nativeIsValid"
          :supported="nativeIsSupported"
          base-classes="form__native"
          @setValue="setValue"
          @onSubmit="onSubmit"
        />
      </div>
    </div>

    <div
      v-if="nativeIsSupported && showManualPay"
      class="grid_separator--l"
      aria-hidden="true"
    />

    <div :aria-live="nativeIsSupported ? 'polite' : false">
      <div v-if="showManualPay">
        <div class="grid_row">
          <div class="col">
            <manual-pay
              :show-error="showManualErrors"
              :validation="validation.card"
              base-classes="form__manual"
            />
          </div>
        </div>

        <div class="grid_row">
          <div class="col">
            <manual-submit
              :form-is-valid="manualIsValid"
              :is-fetching-token="isFetchingToken"
              base-classes="form__submit button button--yellow button--l"
              value="Donate"
              @onSubmit="onSubmit"
              @setValue="setValue"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-if="showErrorClue" class="grid_separator--l" aria-hidden="true" />

    <div v-if="showErrorClue" class="grid_row" aria-hidden="true">
      <div class="col">
        <p class="form__error form__error--normal form__error--centered">
          Please correct errors above
        </p>
      </div>
    </div>

    <local-hidden :value="stripeToken" name="stripeToken" />
    <hidden name="installments" :store-module="storeModule" />
    <hidden name="description" :store-module="storeModule" />
    <hidden name="campaign_id" :store-module="storeModule" />
    <hidden name="referral_id" :store-module="storeModule" />
    <hidden name="openended_status" :store-module="storeModule" />
    <hidden name="pay_fees_value" :store-module="storeModule" />
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import LocalHidden from '../../elements/LocalHidden.vue';
import Radios from '../../elements/Radios.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import updateValue from '../../elements/mixins/updateValue';
import formStarter from '../../mixins/form/starter';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    Radios,
    PayFees,
    ManualPay,
    ManualSubmit,
    NativePay,
  },

  mixins: [formStarter, updateValue],

  data() {
    return {
      storeModule: 'baseForm',
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      frequencyOptions: [
        { id: 0, text: 'One-time donation', value: 'None' },
        { id: 1, text: 'Monthly donation', value: 'monthly' },
        { id: 2, text: 'Yearly donation', value: 'yearly' },
      ],
    };
  },

  methods: {
    onFrequencyUpdate(newValue) {
      let openEndedVal = '';

      if (newValue === 'yearly' || newValue === 'monthly') {
        openEndedVal = 'Open';
      } else if (newValue === 'None') {
        openEndedVal = 'None';
      }

      this.updateValue({
        storeModule: 'baseForm',
        key: 'openended_status',
        value: openEndedVal,
      });
    },
  },
};
</script>
