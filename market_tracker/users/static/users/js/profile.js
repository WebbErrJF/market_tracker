document.addEventListener('DOMContentLoaded', function() {
    var header = document.querySelector('header');
    var background_image = document.querySelector('.landing');
    if (header) {
        header.style.display = 'none';
    }
    if (background_image) {
        background_image.style.backgroundImage = 'none';
    }
    });

async function fetchApiResponse(url) {
      const response = await fetch(url);
      return await response.json();
      }
async function addOptions() {
  var selectElements = [
    document.getElementById("first-chart"),
    document.getElementById("second-chart"),
    document.getElementById("third-chart"),
    document.getElementById("fourth-chart")
  ];

  response = await fetchApiResponse(`/subscriptions/${'subscribed'}`)

  var optionValues = [];
  var optionTexts = [];
  var dashboardNumber = [];
  response.forEach(responseItem => {
    const name = responseItem.stock_company__Name;
    const value = responseItem.stock_company__Symbol;
    const number = responseItem.dashboard_number;
    optionValues.push(value)
    optionTexts.push(name)
    dashboardNumber.push(number)
  })

  for (var i = 0; i < selectElements.length; i++) {
    for (var j = 0; j < optionValues.length; j++) {
      var option = document.createElement("option");
      option.value = optionValues[j];
      option.text = optionTexts[j];
      if (i+1 === dashboardNumber[j]) {
        option.selected = true;
      }
      selectElements[i].add(option);
    }
  }
}

addOptions()
  async function myFunction(dashboard_number, chartId) {
    var stock_symbol = document.getElementById(chartId).value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch(`/subscriptions/${'display'}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({stock_company_symbol: stock_symbol,
                            dashboard_number: dashboard_number
                           }),
    });
    if (response.ok) {
            console.log('Post successfully');
        } else {
            console.error('Error changing subscription');
        }
  }
