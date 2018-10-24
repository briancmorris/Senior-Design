import axios from 'axios'

const featureExtractions = () => {
  axios.get('/hello', {
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
}

module.exports = {featureExtractions}