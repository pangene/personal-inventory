/* ----- Utils ----- */
// Q: Why is this not it's own file?
// A: It's one function. Not worth it. But, I'm also unfamiliar with JS, so
//    maybe this is really bad.

/** Gets a cookie from the document. */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].toString().replace(/^([\s]*)|([\s]*)$/g, "");
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* ----- THE API ----- */

/**
 * Returns a Promise that returns an Item object if it exists.
 * If it doesn't exist, returns: {"detail": "Not found."}
 * 
 * @param  {name: String}
 * @return {Promise} Promise that returns item object, or returns null if DNE.
 */
export const getItem = (name) => {
  return fetch('/api/items/' + name)
      .then(res => res.json())
      .then(res => {
        if (!res.detail) return res;
        else return null;
      });
}

/**
 * Returns a Promise that returns an Array of item objects that have their 
 * names or upcs include the searchParam.
 * 
 * @param  {searchParam: String} either name or upc.
 * @return {Promise} Promise that returns Array of item objects.
 */
export const searchItems = (searchParam) => {
  return fetch('/api/items/?search=' + searchParam)
    .then(res => res.json());
}

/**
 * Updates item with any values given in the updatedItem object.
 * 
 * @param  {name: String, quantity: int, user: int, upc: String}
 */
export const updateItem = (updatedItem) => {
  // Patches item with new quantity
  fetch('/api/items/' + name + '/', {
    method: 'PATCH',
    credentials: "same-origin",
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedItem)
  })
    .then(res => res.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

/**
 * Creates a Promise that returns a new item with given name and upc.
 * Quantity defaults to 1, user defaults to currently logged in.
 * 
 * @param  {name: String, upc: String}
 */
export const createItem = (newItem) => {
  fetch('/api/items/', {
    method: 'POST',
    credentials: "same-origin",
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newItem)
  })
    .then(res => res.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
