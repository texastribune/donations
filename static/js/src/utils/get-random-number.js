export default function getRandomNumber(min = 0, max = 1000000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
