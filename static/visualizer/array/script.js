let array = [];

function createArray() {
  const size = parseInt(document.getElementById('array-size').value);
  array = new Array(size).fill(null);
  renderArray();
  const code = `<span class="keyword">int</span> <span class="variable">arr</span>[${size}]; <span class="comment">// Declared array with size ${size}</span>`;
  document.getElementById('code-output').innerHTML = code;
}

function renderArray(highlightIndex = null, operation = null) {
  const container = document.getElementById('array-box');
  container.innerHTML = '';

  array.forEach((value, index) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'array-wrapper';

    const element = document.createElement('div');
    element.className = 'array-element';
    element.textContent = value !== null ? value : '';

    // Add animation class if needed
    if (index === highlightIndex && operation) {
      element.classList.add(`highlight-${operation}`);
      setTimeout(() => element.classList.remove(`highlight-${operation}`), 1000); // Remove after 1s
    }

    const label = document.createElement('div');
    label.className = 'array-index';
    label.textContent = index;

    wrapper.appendChild(element);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
  });
}



function performOperation() {
  const op = document.getElementById('operation').value;
  const index = parseInt(document.getElementById('op-index').value);
  const value = document.getElementById('op-value').value;

  if (isNaN(index) || index < 0 || index >= array.length) {
    // Removed alert
    return;
  }

  let code = '';

  switch (op) {
    case 'insert':
      array[index] = value;
      code = `<span class="variable">arr</span>[<span class="number">${index}</span>] = <span class="number">${value}</span>; <span class="comment">// Inserted value</span>`;
      renderArray(index, 'insert');
      break;

    case 'delete':
      array[index] = null;
      code = `<span class="variable">arr</span>[<span class="number">${index}</span>] = <span class="keyword">NULL</span>; <span class="comment">// Deleted value</span>`;
      renderArray(index, 'delete');
      break;

    case 'update':
      array[index] = value;
      code = `<span class="variable">arr</span>[<span class="number">${index}</span>] = <span class="number">${value}</span>; <span class="comment">// Updated value</span>`;
      renderArray(index, 'update');
      break;

    case 'search':
      const found = array.includes(value);
      const searchIndex = array.indexOf(value);
      code = `
<span class="comment">// Searching value</span><br>
<span class="keyword">bool</span> <span class="variable">found</span> = <span class="keyword">false</span>;<br>
<span class="keyword">for</span>(<span class="keyword">int</span> <span class="variable">i</span> = 0; <span class="variable">i</span> < ${array.length}; <span class="variable">i</span>++) {<br>
&nbsp;&nbsp;<span class="keyword">if</span>(<span class="variable">arr</span>[<span class="variable">i</span>] == <span class="number">${value}</span>) {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="variable">found</span> = <span class="keyword">true</span>;<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword">break</span>;<br>
&nbsp;&nbsp;}<br>
}`;
      renderArray(searchIndex, found ? 'search' : null);
      break;
  }

  //  Display colored code
  document.getElementById('code-output').innerHTML = code;
}


