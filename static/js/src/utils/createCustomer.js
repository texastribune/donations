import axios from 'axios';

export default function createCustomer({ token, email }) {
  return axios.post('/create-customer', {
    stripeToken: token,
    stripeEmail: email,
  });
}
