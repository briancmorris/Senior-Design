import axios from 'axios'

const featureExtractions = async () => {
  try {
    let res = await axios.get('/setUp')
     if(res.status == 200){
         // test for status you want, etc
         console.log(res.status)
     }    
     // Don't forget to return something   
     return res.data
    }
    catch (err) {
        console.error(err);
    }
}
const getDataFile = async () => {
    try {
        axios({
            url: '/downloadDataFile',
            method: 'GET',
            responseType: 'blob', 
          }).then(async (response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            var now = await Date.now()
            link.setAttribute('download', 'test_' + now + '.csv');
            document.body.appendChild(link);
            link.click();
          });
      }
      catch (err) {
          console.error(err);
      }
  }

module.exports = {featureExtractions, getDataFile}