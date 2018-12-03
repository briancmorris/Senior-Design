import React from 'react'
import styles from '../css/styles.css'

export default class Radiobox extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
    this.getElements = this.getElements.bind(this)
    this.handleInputChange = this.handleInputChange.bind(this)
  }

  handleInputChange(event){
    this.props.onChange(event.target.value)
  }

  getElements(){
    let elementsArray
    if(this.props.elements){
      elementsArray = this.props.elements.map(element => 
        <div>
          <input type="radio" name={this.props.type}  value={`${element}`} onChange={this.handleInputChange}/> {`${element}`}
        </div>
      )
    }
    return elementsArray
  }

  render(){
    console.log(this.props)
    this.getElements()
    return(
      <div>
        <form>
          <h1 className={styles.title}>{this.props.title}</h1>
          {this.getElements()}
        </form>
      </div>
    )
  }
}