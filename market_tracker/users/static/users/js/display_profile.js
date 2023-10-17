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
    const passed_user = JSON.parse(document.getElementById('user_id').textContent);
    if (passed_user) {
        articlesResp = await fetch(`/subscriptions/${'all'}/${passed_user}/`);
    }
    else{
        articlesResp = await fetch(`/subscriptions/${'all'}/`);
    }

    let data = await articlesResp.json();
    sampleData3 = [];
    data.forEach((company, index) => {
        if ('subscription_date' in company){
          sampleData3.push({
            company: company.Name,
            stockSymbol: company.Symbol
          })}
        });
}

async function initialize() {
    await getArticles();
    table = $('#example').on('draw.dt', function () {
        $("#containerexample").attr("id", "container");
        $("#loadercontainer").css("display", "none");
    }).DataTable({
        columns: [
          {title: 'Cop. name', data: 'company'},
          {title: 'Stock symbol', data: 'stockSymbol'},
        ],
        data: sampleData3,
        lengthChange: false,
        "scrollX": false,
        "paging": false,
        "responsive": true,
        "order": [[1, "desc"]]
    });
    table.buttons().container()
        .appendTo('#example_wrapper .col-md-6:eq(0)');
}

document.addEventListener('DOMContentLoaded', function () {
    initialize();
});