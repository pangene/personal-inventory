import React, { useState } from 'react';
import { getItem, updateItem, createItem } from '../ItemsApi';

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

export default AddItem;