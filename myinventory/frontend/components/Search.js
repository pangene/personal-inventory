import React, { useState } from 'react';
import {getItem, searchItems, updateItem, createItem} from '../ItemsApi';
import '../styles/Search.css';

function Search() {
  // searchVal always associated w/ name
  const [searchVal, setSearchVal] = useState("");
  const [upc, setUpc] = useState("");
  const [result, setResult] = useState([]);
  // Item is only considered in the inventory if it is an exact match.
  const [matchExact, setMatchExact] = useState(false);
  // Used for displaying additional components after first search
  const [canDisplay, setCanDisplay] = useState(false);

  const handleItemLoadSuccess = (result) => {
    console.log(result);
    setResult(result);

    // Checks for exact match
    let match = result.some((e) => e.name === searchVal);
    setMatchExact(match);

    // Updates upc if it exists.
    // Would be best to find match and upc at same time.
    if (match) {
      setUpc(result.find((e) => e.name === searchVal).upc)
    }
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."})
  }

  const handleSubmit = (e) => {
    if (searchVal === "") return;  // Empty searchVal probably an accident.
    e.preventDefault();
    setCanDisplay(true);
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
      <div className="mx-auto" id="centerpiece">
        <h1 className="text-center">Do I own</h1>
      </div>
      <form>
        <div className="input-group mb-3">
          <input 
            className="form-control"
            type="text" 
            placeholder="Enter the name of an item to see if you own it" 
            value={searchVal} 
            onChange={(e) => setSearchVal(e.target.value)}
          />
          <div className="input-group-append">
            <input
              className="btn btn-primary px-3"
              type="submit" 
              value="?" 
              onClick={(e) => handleSubmit(e)}
            />
          </div>
        </div>
      </form>
      {canDisplay && <Results present={matchExact} result={result}/>}
      {canDisplay && <AddItem present={matchExact} name={searchVal} upc={upc} />}
    </div>
  )
}

function Results(props) {
  const present = props.present;
  const result = props.result;

  // Defaults to item not being present.
  let foundSomething = false;
  // Item may be there if search query does return some results.
  if (result.length) foundSomething = true;

  const resultItems = result.map((item) =>
    <a 
      href="#"
      className="list-group-item list-group-item-action"
      key={item.name}
      >
      {item.name} - {item.upc}
    </a>
  )

  return (
    <div className="mb-3">
      <PresentDisplay present={present} foundSomething={foundSomething}/>
      <div className="list-group">
        <a href="#" className="list-group-item disabled">
          This is what we found:
        </a>
        {resultItems}
      </div>
    </div>
  )
}

function PresentDisplay(props) {
  const present = props.present;
  const foundSomething = props.foundSomething;
  
  let classModifier = "danger";
  let title = "Item is not present!";
  let body = "It doesn't seem like you own this item...";

  if (foundSomething) {
    body += " But, you may own something similar.";
  }

  if (present) {
    classModifier = "success"; 
    title = "Item is present!";
    body = "You already own this!";
  }

  return (
    <div className={"mb-3 card border-" + classModifier}>
      <div className={"card-body text-" + classModifier}>
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{body}</p>
      </div>
    </div>
  )
}

function AddItem(props) {
  const [name, setName] = useState(props.name);
  const [upc, setUpc] = useState(props.upc);

  let heading = "Would you like to add this item?"
  if (props.present) {
    heading = "This item seems to already be present. Add it anyways?"
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    // Get item with the specific name
    // Necessary b/c matchExact can be incorrect if user changes name in add field!
    getItem(name)
      .then(result => {
        if (result !== null) {  // result.detail only appears if not found (404)
          // item already exists, update
          console.log("Item found in database.")
          console.log("Updating existing item.")
          let updatedItem = {quantity: result.quantity + 1, upc: upc};
          console.log(updatedItem)
          updateItem(updatedItem);
        } else {
          // item does not exist, create
          console.log("Creating new item.")
          let newItem = {name: name, upc: upc};
          console.log(newItem);
          createItem(newItem);
        }
      });
  }

  return (
    <div className="card">
      <div className="card-header">
        {heading}
      </div>
      <div className="card-body">
        <form>
          <div className="input-group mb-3">
            <div className="input-group-prepend">
              <span className="input-group-text" id="basic-addon1">Name</span>
            </div>
            <input 
              className="form-control"
              type="text" 
              placeholder="Enter a name for the item you are adding"
              value={name} 
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="input-group input-group-sm mb-3">
            <div className="input-group-prepend">
              <span className="input-group-text" id="basic-addon1">UPC</span>
            </div>
            <input 
              className="form-control"
              type="text" 
              placeholder="(Optional) Enter a upc for the item you are adding."
              value={upc} 
              onChange={(e) => setUpc(e.target.value)}
            />
          </div>
          <input 
            className="btn btn-primary"
            type="submit" 
            value="Add Item" 
            onClick={(e) => handleSubmit(e)}
          />
        </form>
      </div>
    </div>
  )
}

export default Search;