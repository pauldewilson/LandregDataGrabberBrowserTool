const formPostcode = document.querySelector('form');

function showLoading(e){
    // create the loading text elements
    const div = document.createElement('div');
    const newTextNode = document.createTextNode('Searching. Estimated 5-10 seconds...');
    div.className = 'row loading_element';
    div.appendChild(newTextNode);
    // append loading element
    document.querySelector('.form_container').appendChild(div);
}




function export2csv() {
    console.log('Trying to export as CSV...');
    let data = "";
    const tableData = [];
    const rows = document.querySelectorAll("table tr");
    for (const row of rows) {
      const rowData = [];
      for (const [index, column] of row.querySelectorAll("th, td").entries()) {
        // To retain the commas in the "Description" column, we can enclose those fields in quotation marks.
        if ((index + 1) % 3 === 0) {
          rowData.push('"' + column.innerText + '"');
        } else {
          rowData.push(column.innerText);
        }
      }
      tableData.push(rowData.join(","));
    }
    data += tableData.join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([data], { type: "text/csv" }));
    a.setAttribute("download", "data.csv");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }






// function copyTableToClipboard(){
//     // function to copy table contents or export as CSV
// }

function initiateEventListeners(){
    switch(window.location.pathname){
        case '/':
        console.log("Index page");
        formPostcode.addEventListener('submit', showLoading);
        break;

        case '/results':
            console.log("Results page");
            let btn = document.querySelector('.btn');
            btn.addEventListener('click', export2csv);
            break;
    }
}

initiateEventListeners();

