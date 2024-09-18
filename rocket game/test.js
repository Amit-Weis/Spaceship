function findKeyWithMaxArrayLength(object) {
    // Get an array of all the object's keys.
    const keys = Object.keys(object);
  
    // Iterate over the array of keys and get the length of each array value.
    const arrayLengths = keys.map(key => object[key].length);
  
    // Find the maximum length of all the array values.
    const maxArrayLength = Math.max(...arrayLengths);
  
    // Return the key whose array value has the maximum length.
    return keys.find(key => object[key].length === maxArrayLength);
  }
  
  // Example usage:
  const object = {
    key1: [1, 2, 3],
    key2: [4, 5, 6, 7],
    key3: [8, 9, 10],
  };
  
  const keyWithMaxArrayLength = findKeyWithMaxArrayLength(object);
  
  console.log(keyWithMaxArrayLength)