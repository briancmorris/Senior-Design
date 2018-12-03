// App.jsx
import axios from 'axios'
import React from 'react'
import RadioBox from './RadioBox'
import Checkbox from './Checkbox'
import {featureExtractions, getDataFile} from './serverUtility'
import styles from '../css/styles.css'
export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      features : [] ,
      featuresSelected: [],
      models: [],
      modelSelected:'',
      selectedFile: null,
      loaded: 0,
      output: ''
    };
    this.changeFeature = this.changeFeature.bind(this)
    this.changeModel = this.changeModel.bind(this)
    this.handleFile = this.handleFile.bind(this)
    this.handleUpload = this.handleUpload.bind(this)
    this.downloadcsv = this.downloadcsv.bind(this)
  }
  async downloadcsv(){
    await getDataFile()
  }
  changeFeature(features){
    this.setState({featuresSelected : features})
  }
  changeModel(model){
    this.setState({modelSelected: model})
  }
  handleFile(event){
    this.setState({
      selectedFile: event.target.files[0],
      loaded: 0,
    })
  }

  async handleUpload(){
    const data = new FormData()
    data.append('file', this.state.selectedFile, this.state.selectedFile.name)
    console.log(this.state.modelSelected)
    data.append('model', this.state.modelSelected)
    data.append('features', this.state.featuresSelected)

    axios.post('/results', data, {
      onUploadProgress: ProgressEvent => {
        this.setState({
          loaded: (ProgressEvent.loaded / ProgressEvent.total*100),
        })
      },
    })
    .then(async res => {
      console.log(res)
      const formattedOutput = res.data.map(element =>{
        return <div>
          <p>{element[0] + ': ' + element[1]}</p>
        </div>
      })
      
      console.log(formattedOutput)

      this.setState({output: formattedOutput})
      console.log(res.statusText)
    })

  }

  async componentDidMount(){
    try {
      const data = await featureExtractions()
      const features = data['setup']['features']
      this.setState({ features});
      const models = data['setup']['models']
      this.setState({models})
    } catch (error) {
      console.log(error);
    }
  }

  render () {
    const fileUpload =(
      <div>
        <input type="file" name="" id="" onChange={this.handleFile} />
      </div>
    )
    const modelRadiobox = <RadioBox title='Pick Model:' type='feature' elements={this.state.models} onChange={this.changeModel}/>
    const featureCheckbox = <Checkbox title='Pick Features:' type='model' elements={this.state.features} onChange={this.changeFeature}/>
    return(
    <div>
      <div className={styles.header} > Littlefoot</div>
      <button className={styles.dbutton} onClick={this.downloadcsv}>Create a random csv data file</button>
      <div className={styles.container}>
        <div className={styles.item}>{fileUpload}</div>
        <div className={styles.item}> {modelRadiobox}</div>
        <div className={styles.item}> {featureCheckbox}</div>
        <button onClick={this.handleUpload}>Upload</button>
        <div>
          <div> File Upload: {Math.round(this.state.loaded,2) }%</div>
          <div> {this.state.output}</div>
        </div>
      </div>
    </div>
    )
  }
}