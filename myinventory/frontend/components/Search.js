import React, { useState } from 'react';
import AnimateHeight from 'react-animate-height';
import { getItem, searchItems, updateItem, createItem } from '../ItemsApi';
import '../styles/Search.css';

function Search() {
  // Mount animation setup
  const [height, setHeight] = useState(0);

  // searchVal always associated w/ name
  const [searchVal, setSearchVal] = useState("");
  // upc for now is unsearchable, but planned to implement soon
  const [upc, setUpc] = useState("");
  // tags for searched item
  const [tags, setTags] = useState([]);
  // array of searched item
  const [result, setResult] = useState([]);
  // Item is only considered in the inventory if it is an exact match.
  const [matchExact, setMatchExact] = useState(false);
  // Used for displaying additional components after first search
  const [canDisplay, setCanDisplay] = useState(false);

  const handleItemLoadSuccess = (result) => {
    console.log("Results:", result);
    setResult(result);

    // Checks for exact match
    let matchingItem = result.find((e) => e.name === searchVal);
    let match = matchingItem !== undefined;
    setMatchExact(match);

    // Updates upc and tags if it exists.
    if (match) {
      setUpc(matchingItem.upc);
      setTags(matchingItem.tags);
    }
  }

  const handleItemLoadFail = (error) => {
    console.log(error);
    setResult({name: "There was an error."});
  }

  const handleSubmit = (e) => {
    if (searchVal === "") return;  // Empty searchVal probably an accident.
    e.preventDefault();
    setCanDisplay(false);
    setHeight(0);
    // Get all items that match search params (name or upc)
    searchItems(searchVal)
      .then(
        (result) => {
          handleItemLoadSuccess(result);
          setCanDisplay(true);
          setTimeout(() => setHeight('auto'), 100);
        },
        (error) => {
          handleItemLoadFail(error);
        }
      );
  }

  const searchThisItem = (item) => {
    setSearchVal(item.name);
    setUpc(item.upc);
    setTags(item.tags);
  }

  return (
    <div className="mx-auto max-w-large">
      <div className="mx-auto">
        <h1 className="text-center giant pt-5">Do I own</h1>
      </div>
      <form>
        <div className="mx-auto max-w-medium input-group mb-3">
          <input 
            className="form-control underline"
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
      <AnimateHeight 
        height={height} 
        delay={150}
        duration={300}
      >
        {canDisplay && 
          (<div>
            <PresentDisplay 
              present={matchExact} 
              foundSomething={result.length} 
            />
            <Results 
              className="float-end" 
              name={searchVal} 
              result={result} 
              search={searchThisItem}
            />
            <div className="clr"></div>
            <AddItem 
              present={matchExact} 
              name={searchVal} 
              upc={upc} 
              tags={tags} 
              />
          </div>)}
      </AnimateHeight>
    </div>
  )
}

function PresentDisplay(props) {
  const present = props.present;
  const foundSomething = props.foundSomething;
  
  let classModifier = "danger";
  let icon = <i className="far fa-times-circle"></i>;
  let title = "Item is not present!";
  let body = "It doesn't seem like you own this item...";

  if (foundSomething) {
    body += " But, you may own something similar. Check what we found -->";
  }

  if (present) {
    classModifier = "success"; 
    icon = <i className="far fa-check-circle"></i>;
    title = "Item is present!";
    body = "You already own this!";
  }

  return (
    <div className={"max-h-large left float-start mb-3 card border-" + classModifier}>
      <div className={"card-body text-" + classModifier}>
        <div className="giant">{icon}</div>
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{body}</p>
      </div>
    </div>
  )
}

function Results(props) {
  const result = props.result;

  const resultItems = result.map((item) =>
    <a 
      href="#"
      onClick={() => props.search(item)}
      className={"list-group-item list-group-item-action" 
        + (item.name === props.name ? " active" : "")}
      key={item.name}
      >
      {item.name} - Qty: {item.quantity}
    </a>
  )

  return (
    <div className="right mb-3 float-end">
      <div className="list-group">
        <a href="#" className="list-group-item disabled">
          This is what we found:
        </a>
        <div className="scrollable max-h-medium">
          {resultItems}
        </div>
      </div>
    </div>
  )
}

function AddItem(props) {
  const [name, setName] = useState(props.name);
  // const [upc, setUpc] = useState(props.upc);
  const [tags, setTags] = useState(props.tags);

  let heading = "Would you like to add this item?"
  if (props.present) {
    heading = "This item seems to already be present. Add another one?"
  }

  const showToast = (status) => {
    const toastr = window.toastr;
    if (status) {
      const successMessage = "Added item to inventory!" 
      toastr["success"](successMessage);
    } else {
      const failureMessage = "Failed to add item to inventory."
      toastr["error"](failureMessage);
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    // Get item with the specific name
    // Necessary b/c matchExact can be incorrect if user changes name in add field!
    getItem(name)
      .then(result => {
        if (result !== null) {  // result.detail only appears if not found (404)
          // item already exists, update
          console.log("Item found in database.");
          console.log("Updating existing item.");
          let updatedItem = {
            name: name, 
            quantity: result.quantity + 1, 
            upc: props.upc,
            tags: tags
          };
          console.log(updatedItem);
          updateItem(updatedItem)
            .then(status => showToast(status));
        } else {
          // item does not exist, create
          console.log("Creating new item.");
          let newItem = {name: name, upc: props.upc};
          console.log(newItem);
          createItem(newItem);
        }
      });
  }

  return (
    <div className="card float-none" key={props.name}>
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
              defaultValue={props.name} 
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="input-group input-group-sm mb-3">
            <div className="input-group-prepend">
              <span className="input-group-text" id="basic-addon1">Tags</span>
            </div>
            <input 
              className="form-control"
              type="text" 
              placeholder="(Optional) Enter comma-separated tags for the item you are adding."
              defaultValue={props.tags.join(", ")}
              onChange={e => {
                let newTags = e.target.value.split(",");
                newTags = newTags.map(e => e.trim());
                setTags(newTags);
              }}
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