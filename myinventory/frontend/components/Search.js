import React, { useState } from 'react'
import {getItem, searchItems, updateItem, createItem} from '../ItemsApi'
import '../styles/Search.css'

function Search() {
  // searchVal always associated w/ name
  const [searchVal, setSearchVal] = useState("");
  const [upc, setUpc] = useState("");
  const [result, setResult] = useState([]);
  // Item is only considered in the inventory if it is an exact match.
  const [matchExact, setMatchExact] = useState(false);
  // Used for displaying the AddItem component. Enabled as soon as non-empty item is searched.
  const [canAdd, setCanAdd] = useState(false);

  const handleItemLoadSuccess = (result) => {
    console.log(result);
    setResult(result);

    // Checks for exact match
    let match = result.some((e) => e.name === searchVal);
    setMatchExact(match);

    // Updates upc if it exists.
    // Would be best to find match and upc at same time.
    if (matchExact) {
      setUpc(result.find((e) => e.name === searchVal).upc)
    }
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."})
  }

  const handleSubmit = (e) => {
    if (searchVal === "") return;  // Empty searchVal probably an accident.
    e.preventDefault();  // Necessary for logging to persist
    setCanAdd(true);

    // Get all items that match search params (name or upc)
    searchItems(searchVal)
      .then(
        (result) => {
          handleItemLoadSuccess(result);
        },
        (error) => {
          handleItemLoadFail(error);
        }
      );
  }

  return (
    <div>
      <form>
        <div className="input-group mb-3">
          <input 
            className="form-control"
            type="text" 
            placeholder="Search" 
            value={searchVal} 
            onChange={(e) => setSearchVal(e.target.value)}
          />
          <div className="input-group-append">
            <input
              className="btn btn-outline-secondary"
              type="submit" 
              value="Submit" 
              onClick={(e) => handleSubmit(e)}
            />
          </div>
        </div>
      </form>
      {matchExact && "yep its there"}
      {result.length > 0 && <ResultsDisplay result={result}/>}
      {canAdd && <AddItem name={searchVal} upc={upc} />}
    </div>
  )
}

function ResultsDisplay(props) {
  const result = props.result;
  const resultItems = result.map((item) =>
    <li key={item.name}>{item.name} - {item.upc}</li>
  )
  return (
    <div>
      <p>Found: </p>
      <ul>{resultItems}</ul>
    </div>
  )
}

function AddItem(props) {
  const [name, setName] = useState(props.name);
  const [upc, setUpc] = useState(props.upc);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Adding item to database.");

    // Get item with the specific name
    getItem(name)
      .then(result => {
        if (!result.detail) {  // result.detail only appears if 404
          // item already exists, update
          let updatedItem = {quantity: result.quantity + 1, upc: upc};
          console.log(updatedItem)
          updateItem(updatedItem);
        } else {
          // item does not exist, create
          let newItem = {name: name, upc: upc};
          console.log(newItem);
          createItem(newItem);
        }
      });
  }

  return (
    <div>
      <p>Would you like to add this item?</p>
      <form>
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)}
        />
        <input 
          type="text" 
          value={upc} 
          onChange={(e) => setUpc(e.target.value)}
        />
        <input type="submit" value="Submit" onClick={(e) => handleSubmit(e)}/>
      </form>
    </div>
  )
}

export default Search;