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

async function getArticles(){
    let articlesResp = await fetch(`/subscriptions/${'all'}`);

    let data = await articlesResp.json();
    sampleData3 = [];
    data.forEach((company, index) => {
        if (company.Default === true){
          sampleData3.push({
            company: company.Name,
            stockSymbol: company.Symbol,
            subscribed: true,
            subscriptionDate: "Default"
          })}
        else if ('subscription_date' in company){
          sampleData3.push({
            company: company.Name,
            stockSymbol: company.Symbol,
            subscribed: true,
            subscriptionDate: company.subscription_date
          })}
        else {
          sampleData3.push({
            company: company.Name,
            stockSymbol: company.Symbol,
            subscribed: false,
            subscriptionDate: ''
          });
        }
        });
}

async function changeSubscription(stockCompanyId, subscribed) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch(`/subscriptions/${'subscribe'}/`, {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': csrfToken
         },
         body: JSON.stringify({ stock_company_id: stockCompanyId }),
    });

    if (response.ok) {
        if (subscribed) {
            console.log('Subscribed successfully');
        } else {
            console.log('Unsubscribed successfully');
        }
        await updateTable();
    } else {
        console.error('Error changing subscription');
    }}


async function updateTable() {
    await getArticles();
    table.clear().rows.add(sampleData3).draw();
}

async function initialize() {
    await getArticles();
    updateTable();
    table = $('#example').on('draw.dt', function () {
        $("#containerexample").attr("id", "container");
        $("#loadercontainer").css("display", "none");
    }).DataTable({
        columns: [
          {title: 'Cop. name', data: 'company'},
          {title: 'Stock symbol', data: 'stockSymbol'},
          {title: 'Subscribed', data: 'subscribed',
        render: function (data, type, row) {
            if (type === 'display') {
              if (row.subscriptionDate === 'Default'){
                return '<input type="checkbox" checked disabled>';
              }
              else {
                return '<input type="checkbox" ' + (data ? 'checked' : '') + '>';
            }}
            return data;
        }
        },
          {title: 'Subscription Date', data: 'subscriptionDate'},
          {title: 'All data', data: 'stockSymbol',
            render: function (data, type, row) {
            if (row.subscriptionDate !== '') {
              return '<form action="/subscriptions/all-data" method="get">' +
                      ' <button type="submit" name="get all data" value="' + data + '">get all data</button>' +
                      ' </form>';
                  }
            else {
              return '<form action="/subscriptions/all-data" method="get">' +
                      ' <button type="submit" name="get all data" value="' + data + '" disabled>get all data</button>' +
                      ' </form>';

            }}

          }
        ],
        data: sampleData3,
        lengthChange: false,
        buttons: ['excel', 'pdf'],
        "scrollX": false,
        "paging": false,
        "responsive": true,
        "order": [[3, "desc"]]
    });
    table.buttons().container()
        .appendTo('#example_wrapper .col-md-6:eq(0)');
}

document.addEventListener('DOMContentLoaded', function () {
    initialize();

    $(document).on('change', 'input[type="checkbox"]', async function () {
        var companyId = $(this).closest('tr').find('td:first').text();
        var subscribed = this.checked;
        await changeSubscription(companyId, subscribed);
    });
});