function yearSelectOptions(data) {
  var selectYear = document.getElementById('selectYear');

  // Create an array to store unique option values
  var uniqueYear = [];

  // Loop through the data and add unique option values to the array
  data.forEach(function (item) {
      let yearSelected = item.Year;
      if (!uniqueYear.includes(yearSelected)) {
          uniqueYear.push(yearSelected);
      }
  });

  // Add the unique option values to the select element
  uniqueYear.forEach(function (yearSelected) {
      var optionYear = document.createElement('option');
      optionYear.textContent = yearSelected;
      selectYear.appendChild(optionYear);
  });


}

// Fetch the JSON data from the separate file
fetch('./nakamura_1979_sm_locations.json')
  .then(function (response) {
      return response.json();
  })
  .then(function (jsonNakData) {
      yearSelectOptions(jsonNakData);
      daySelectOptions(jsonNakData);
  })
  .catch(function (error) {
      console.error('Error fetching data:', error);
  });

 
// this is for date
function daySelectOptions(data, yearSelected) {
    let selectDay = document.getElementById('selectDay');
    var yearSelected = "1971";

     // Filter data based on the selected year
     var filteredData = data.filter(function (item) {
        return item.Year === yearSelected;
    });

    
    var uniqueDay = [];
    // Loop through the data and add unique option values to the array
    data.forEach(function (item) {
        var daySelected = item.Day;
        if (!uniqueDay.includes(daySelected)) {
            uniqueDay.push(daySelected);
        }
    });
   
    // Add the unique option values to the select element
    uniqueDay.forEach(function (daySelected) {
        let optionDay = document.createElement('option');
        optionDay.textContent = daySelected;
        selectDay.appendChild(optionDay);
    });
  }
  



