import React from 'react'
import styles from '../css/styles.css'

export default class Checkbox extends React.Component {
  constructor(props) {
    super(props)
    this.state = {selectedElements: []}

    this.getElements = this.getElements.bind(this)
    this.handleInputChange = this.handleInputChange.bind(this)
  }
  
  async handleInputChange(event){
    const target = event.target
    await this.setState((state)=>{
      if(target.checked){
        return {selectedElements: state.selectedElements.concat(target.value)};
      }
      else{
        const elementList = [...this.state.selectedElements]
        const index = elementList.indexOf(target.value)
        elementList.splice(index, 1)
        return {selectedElements: elementList};
      }
    })
    const stuff = this.state.selectedElements
    this.props.onChange(stuff)
  }

  getElements(){
    let elementArray
    if(this.props.elements){
      elementArray = this.props.elements.map(element => 
        <div>
          <input type="checkbox" name={this.props.type} value={`${element}`} onChange={this.handleInputChange}/> {`${element}`}
        </div>
      )
    }
    return elementArray
  }

  render(){
    console.log(this.props)
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