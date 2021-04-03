function getTags() {
  let tagsInput = document.getElementById("tags_input");
  let tagsInputVal = tagsInput.value;
  console.log(tagsInputVal);
  // An empty string split would return [""]
  let tags = tagsInputVal !== "" ? tagsInputVal.split(",") : [];
  tags = tags.map(e => e.trim());
  console.log(tags);
  return tags;
}

function addSearchTag(tag) {
  let tags = getTags();
  if (!tags.includes(tag)) {
    tags.push(tag);
  }
  let newTagsInputVal = tags.join(', ');
  let tagsInput = document.getElementById("tags_input");
  tagsInput.value = newTagsInputVal; 
}